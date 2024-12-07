#!/usr/bin/env python3
"""File Operations Example

This example demonstrates how to work with files using both chatbot and agent services.
It shows how to:
1. Initialize the clients
2. Create instances with file handling capabilities
3. Process file content
4. Handle file-related operations
"""
import traceback

from agentcli.clients import AgentClient
from agentcli.clients.base_client import ApiError, AuthenticationError
from agentcli.core.command_handler import ToolConfigGenerator

class FileTools:
    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        with open(file_path, 'r') as f:
            return f.read()

    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file"""
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"

def main():
    # Initialize clients
    base_url = "http://localhost:8000"
    agent = AgentClient(base_url)

    # Set API key
    api_key = "your-api-key"
    agent.set_api_key(api_key)

    try:
        # Create an agent with file handling tools
        print("=== Creating File Processing Agent ===\n")
        tools = FileTools()
        file_tools = ToolConfigGenerator.extract_command_config(tools)
        
        # Register tools with the interpreter
        agent.interpreter.register_command_instance(tools, file_tools)

        agent_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 4000
        }

        agent_instance = agent.create_agent(
            name="FileAgent",
            agent_type="file_processor",
            behavior="An agent that helps with file operations and content processing.\nHere are your tools: {tools}",
            tools=file_tools,
            config=agent_config
        )
        print(f"Created agent: {agent_instance['id']}\n")

        # Example file operations
        print("=== File Operations ===\n")

        # Create a test file
        test_content = "Hello, this is a test file.\nIt contains multiple lines.\nPlease process this content."
        test_file = "example_files/test.txt"

        print("User: Please create a test file with some content.")
        response = agent.interact(
            agent_instance['id'],
            f"Create a file at {test_file} with this content: {test_content}"
        )
        print(response)

        # Read and analyze the file
        print("User: Please read the file and summarize its content.")
        response = agent.interact(
            agent_instance['id'],
            f"Read the file at {test_file} and give me a summary of its content."
        )
        print(f"Agent: {response['response']}\n")

        # Modify the file
        print("User: Please add a new line to the file.")
        response = agent.interact(
            agent_instance['id'],
            f"Add 'This is a new line.' to the end of {test_file}"
        )
        print(f"Agent: {response['response']}\n")

        # Error handling example
        print("=== Error Handling ===\n")
        try:
            # Try to read non-existent file
            response = agent.interact(
                agent_instance['id'],
                "Read the file at non_existent.txt"
            )
        except ApiError as e:
            print(f"Expected error handled: {str(e)}\n")

    except AuthenticationError as e:
        print(f"Authentication error: {str(traceback.format_exc())}")
    except ApiError as e:
        print(f"API error: {str(traceback.format_exc())}")
    except Exception as e:
        print(f"Unexpected error: {str(traceback.format_exc())}")

if __name__ == "__main__":
    main()
