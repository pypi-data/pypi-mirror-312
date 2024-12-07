"""Command handling module for client-side execution."""

import uuid

class CommandExecutionError(Exception):
    """Raised when a command execution fails"""

class ToolConfigGenerator:
    @staticmethod
    def extract_command_config(instance: object) -> dict:
        """Extract command configurations from a class instance.

        Args:
            instance: Object instance containing command-decorated methods

        Returns:
            dict: Tool configuration in the format expected by the agent
        """
        tool_config = {}
        
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            if hasattr(attr, 'command'):
                section = getattr(attr, 'section', 'Default')
                if section not in tool_config:
                    tool_config[section] = {}
                
                # Get the command configuration
                cmd = attr.command
                tool_config[section][cmd.name] = cmd
        
        return tool_config


class CommandExecutor:
    def __init__(self):
        self.instances = {}
        self.configs = {}
    
    def register_instance(self, instance: object, config: dict) -> str:
        """Register an instance for command execution.

        Args:
            instance: Object instance containing the commands
            config: Tool configuration for the instance

        Returns:
            str: Instance ID for future reference
        """
        instance_id = str(uuid.uuid4())
        self.instances[instance_id] = instance
        self.configs[instance_id] = config
        return instance_id
    
    def execute_command(self, command: dict, instance_id: str) -> dict:
        """Execute a command using the registered instance.

        Args:
            command: Command dictionary with name and parameters
            instance_id: ID of the instance to use

        Returns:
            dict: Execution result
        """
        if instance_id not in self.instances:
            return {
                'status': 'error',
                'error': 'Instance not found'
            }

        instance = self.instances[instance_id]

        try:
            # Get command name and args
            cmd_name = next(iter(command))
            cmd_args = command[cmd_name]

            # Find method with matching command name
            for attr_name in dir(instance):
                attr = getattr(instance, attr_name)
                if hasattr(attr, 'command') and attr.command.name == cmd_name:
                    result = attr(**cmd_args)
                    return {
                        'status': 'success',
                        'result': result
                    }

            return {
                'status': 'error',
                'error': f'Command {cmd_name} not found'
            }

        except (AttributeError, TypeError, ValueError, KeyError) as e:
            return {
                'status': 'error',
                'error': f'Command execution failed: {str(e)}'
            }