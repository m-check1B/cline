# Boss Agent API (VS Code Extension)

This VS Code extension serves as an intermediary between the Cline VS Code extension and the Boss Agent. It provides an API layer that allows the Boss Agent to control and interact with the Cline extension, enabling more advanced AI-assisted coding capabilities.

## Features

- Connects to the Boss Agent via WebSocket
- Translates Boss Agent commands into Cline extension actions
- Provides an API for project analysis, code generation, refactoring, and more
- Handles asynchronous communication between the Boss Agent and Cline extension

## Setup

1. Ensure you have the Cline VS Code extension installed.
2. Install this Boss Agent API extension in VS Code.
3. Configure the extension settings:
   - `clineBossAgentApi.serverUrl`: WebSocket URL for connecting to the Boss Agent (default: ws://localhost:8765)

## Usage

This extension works in the background and doesn't require direct user interaction. It automatically connects to the Boss Agent when activated and listens for commands.

## API Endpoints

The Boss Agent API exposes the following endpoints:

- `analyze_project`: Analyze the current project structure and codebase
- `generate_code`: Generate code based on a given prompt
- `refactor_code`: Refactor code in a specified file
- `suggest_improvements`: Suggest improvements for a given file
- `run_tests`: Run tests for the project or a specific module
- `create_file`, `read_file`, `update_file`, `delete_file`: File operations
- `search_and_replace`: Perform project-wide search and replace

## Troubleshooting

If you encounter issues:

1. Check the VS Code output panel for logs (select "Boss Agent API" from the dropdown)
2. Ensure the Boss Agent is running and accessible at the configured WebSocket URL
3. Verify that the Cline extension is properly installed and activated

For more detailed information, refer to the main project README.
