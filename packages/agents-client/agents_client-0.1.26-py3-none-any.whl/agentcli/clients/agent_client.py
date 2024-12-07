import json
from typing import Dict, Any, Optional, List
from .base_client import BaseClient, ApiError, AuthenticationError
from agentcli.core.interpreter import ClientInterpreter

class AgentClient(BaseClient):
    """Client for interacting with agent endpoints"""

    def __init__(self):
        super().__init__()
        self.interpreter = ClientInterpreter()

    def create_agent(
        self,
        name: str,
        agent_type: str,
        behavior: str,
        tools: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new agent instance

        Args:
            name (str): Name of the agent
            agent_type (str): Type of agent (e.g., 'general', 'coding', etc.)
            behavior (str): Behavior description
            tools (Dict[str, Any]): Tool configuration
            config (Optional[Dict[str, Any]], optional): Additional configuration. Defaults to None.

        Returns:
            Dict[str, Any]: Created agent instance data
        """
        data = {
            'name': name,
            'agent_type': agent_type,
            'behavior': behavior,
            'tool_config': tools,
            'config': config or {}
        }
        return self.post('/agent/create', data)

    def interact(
        self,
        agent_id: str,
        message: str,
        image: Optional[str] = None,
        command_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a message to the agent

        Args:
            agent_id (str): ID of the agent
            message (str): Message to send
            image (Optional[str], optional): Image input - can be URL, base64 string, or file path. Defaults to None.
            command_results (Optional[Dict[str, Any]], optional): Results from previous commands. Defaults to None.

        Returns:
            Dict[str, Any]: Agent response
        """
        if not self.api_key:
            raise AuthenticationError('API key not set. Call set_api_key() first.')

        data = {
            'message': message,
            'image': self.process_image(image) if image else None,
            'command_results': command_results
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = self.session.post(
            url=f'{self.base_url}/api/{self.api_version}/agent/{agent_id}/interact',
            json=data,
            headers=headers
        )
        print(response.text)
        if response.status_code != 200:
            raise ApiError(f'Request failed with status {response.status_code}: {response.text}')
            
        try:
            response_text = response.text.strip()
            # Handle multi-line SSE response
            if 'event:' in response_text:
                # Split into event blocks
                events = []
                current_event = {'event': None, 'data': None}
                
                for line in response_text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith('event:'):
                        if current_event['event'] and current_event['data']:
                            events.append(current_event.copy())
                        current_event['event'] = line.replace('event:', '').strip()
                    elif line.startswith('data:'):
                        try:
                            data = json.loads(line.replace('data:', '', 1).strip())
                            current_event['data'] = data
                        except json.JSONDecodeError:
                            continue
                            
                if current_event['event'] and current_event['data']:
                    events.append(current_event)
                
                # Process events
                for event in events:
                    if event['event'] == 'function_call':
                        response_data = event['data']
                        if 'commands_to_execute' in response_data:
                            results = self.interpreter.interpret_response(response_data)
                            return self.interact(
                                agent_id=agent_id,
                                message=message,
                                command_results=results
                            )
                    elif event['event'] == 'complete':
                        response_data = event['data']
                        metadata = response_data.get('metadata', {})
                        # Ensure model info is included in metadata
                        if 'model' in metadata:
                            metadata['model_name'] = metadata['model']
                        return {
                            'response': response_data.get('response', response_data),
                            'metadata': metadata,
                            'model_info': {
                                'name': metadata.get('model', 'unknown'),
                                'tokens': metadata.get('tokens', {}),
                                'costs': metadata.get('costs', {})
                            }
                        }
                    elif event['event'] == 'error':
                        raise ApiError(f'Agent error: {event["data"].get("error", "Unknown error")}')
                        
                raise ApiError('No valid events found in SSE response')
            else:
                # Try parsing as regular JSON response
                response_data = json.loads(response_text)
                if isinstance(response_data, dict) and 'response' not in response_data:
                    response_data = {'response': response_data}
                return response_data
        except json.JSONDecodeError as e:
            raise ApiError(f'Failed to parse response: {str(e)}\nResponse text: {response.text}')

    def get_state(
        self,
        agent_id: str
    ) -> Dict[str, Any]:
        """Get current state of an agent

        Args:
            agent_id (str): ID of the agent

        Returns:
            Dict[str, Any]: Agent state data
        """
        return self.get(f'/agent/{agent_id}/state')

    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete an agent instance

        Args:
            agent_id (str): ID of the agent to delete

        Returns:
            Dict[str, Any]: Deletion confirmation
        """
        return self.delete(f'/agent/{agent_id}')

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent instance details

        Args:
            agent_id (str): ID of the agent

        Returns:
            Dict[str, Any]: Agent instance data
        """
        return self.get(f'/agent/{agent_id}')

    def list_agents(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all agent instances

        Args:
            skip (int, optional): Number of instances to skip. Defaults to 0.
            limit (int, optional): Maximum number of instances to return. Defaults to 100.

        Returns:
            List[Dict[str, Any]]: List of agent instances
        """
        params = {
            'skip': skip,
            'limit': limit
        }
        return self.get('/agent/list', params)

    def update_agent(
        self,
        agent_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update agent configuration

        Args:
            agent_id (str): ID of the agent
            updates (Dict[str, Any]): Updated fields

        Returns:
            Dict[str, Any]: Updated agent instance data
        """
        return self.post(f'/agent/{agent_id}/update', updates)
