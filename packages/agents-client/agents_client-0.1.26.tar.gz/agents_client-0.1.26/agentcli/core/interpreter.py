"""Client-side command interpreter for executing agent commands and collecting results."""

import asyncio
from typing import Dict, Any, Optional
from .command_handler import CommandExecutor, CommandExecutionError

class ClientInterpreter:
    """Interprets and executes commands from agent responses."""

    def __init__(self):
        self.command_executor = CommandExecutor()
        self.current_results: Dict[str, Any] = {}
        self._registered_instance_id: Optional[str] = None

    def register_command_instance(self, instance: object, config: dict) -> None:
        """Register a command instance for execution.

        Args:
            instance: Object instance containing the commands
            config: Tool configuration for the instance
        """
        self._registered_instance_id = self.command_executor.register_instance(instance, config)

    async def execute_command(self, cmd_name: str, cmd_args: dict) -> Any:
        """Execute a single command and return its result.

        Args:
            cmd_name: Name of the command to execute
            cmd_args: Arguments for the command

        Returns:
            Any: Result of the command execution

        Raises:
            CommandExecutionError: If command execution fails
        """
        if not self._registered_instance_id:
            raise CommandExecutionError("No command instance registered")

        command = {cmd_name: cmd_args}
        result = self.command_executor.execute_command(command, self._registered_instance_id)

        if result['status'] == 'error':
            raise CommandExecutionError(result['error'])

        return result['result']

    async def interpret_response(self, agent_response: dict) -> Dict[str, Any]:
        """Interpret an agent response and execute any commands.

        Args:
            agent_response: Response from the agent containing commands to execute

        Returns:
            Dict[str, Any]: Dictionary of command results with command names as keys

        Raises:
            CommandExecutionError: If command execution fails
        """
        self.current_results = {}
        commands = agent_response.get('commands_to_execute', {})

        for cmd_name, cmd_args in commands.items():
            try:
                result = await self.execute_command(cmd_name, cmd_args)
                self.current_results[cmd_name] = result
            except CommandExecutionError as e:
                self.current_results[cmd_name] = {
                    'error': str(e),
                    'status': 'error'
                }
            except Exception as e:
                self.current_results[cmd_name] = {
                    'error': f'Unexpected error: {str(e)}',
                    'status': 'error'
                }

        return self.current_results

    def get_current_results(self) -> Dict[str, Any]:
        """Get the results of the most recent command executions.

        Returns:
            Dict[str, Any]: Dictionary of command results
        """
        return self.current_results

    def clear_results(self) -> None:
        """Clear the current results."""
        self.current_results = {}
