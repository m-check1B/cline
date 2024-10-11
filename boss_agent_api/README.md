# Boss Agent API

The Boss Agent API is a VS Code extension that serves as an intermediary between the Cline extension and an AI-powered agent, providing advanced coding assistance.

## Features

- Process coding goals using AI
- Interact with the Cline extension to perform coding tasks
- Display results in a user-friendly webview
- Maintain a history of processed goals
- Cancel ongoing goal processing
- Manage Cline extension context and history

## Installation

1. Install the Cline extension in VS Code.
2. Install this Boss Agent API extension.
3. Configure the extension settings (see Configuration section).

## Usage

1. Open the Boss Agent webview from the VS Code activity bar.
2. Enter your coding goal in the input field.
3. Click "Process Goal" to start processing.
4. View the results in the webview.
5. Use the goal history to revisit previous goals and their results.

## Configuration

Configure the following settings in VS Code:

- `bossClineAgentApi.serverUrl`: WebSocket URL for the agentic framework server (default: ws://localhost:8765)

## Commands

- `Boss Cline Agent API: Connect to Server`: Manually connect to the WebSocket server
- `Boss Agent: Open Webview`: Open the Boss Agent webview
- `Boss Agent: Cancel Current Goal`: Cancel the currently processing goal
- `Boss Agent: Run Tests`: Run the test suite for the Boss Agent API

## Cline Extension Integration

The Boss Agent API now provides deeper integration with the Cline extension:

- Get and set Cline context
- Retrieve and clear Cline history
- Perform Cline-specific actions like code generation, refactoring, and improvement suggestions

For detailed information on these interactions, refer to the `vscode_bridge.py` file.

## Development

To set up the development environment:

1. Clone the repository.
2. Run `npm install` to install dependencies.
3. Open the project in VS Code.
4. Press F5 to start debugging the extension.

## Testing

Refer to the [TESTING.md](./TESTING.md) file for detailed information on running tests, known limitations, and edge cases.

## Error Handling

The Boss Agent API implements error handling at various levels:

- WebSocket connection errors
- Command execution errors
- Cline extension interaction errors

Errors are logged and, where appropriate, displayed to the user via VS Code's information/error messages.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
