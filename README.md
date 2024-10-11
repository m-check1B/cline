# Advanced AI Coding Assistant

This project combines the power of the Cline VS Code extension with an AI-powered Boss Agent to provide advanced coding assistance. It consists of two main components: the Boss Agent API (a VS Code extension) and the Boss Agent (a Python application).

## Overview

- **Cline VS Code Extension**: A powerful coding assistant (not part of this repository)
- **Boss Agent API**: A VS Code extension that acts as an intermediary between Cline and the Boss Agent
- **Boss Agent**: An AI-powered assistant that processes user goals and controls the Cline extension

## How It Works

1. The user provides a high-level coding goal to the Boss Agent.
2. The Boss Agent uses AI to break down the goal into specific tasks.
3. These tasks are sent to the Boss Agent API (VS Code extension).
4. The Boss Agent API translates the tasks into actions for the Cline extension.
5. The Cline extension performs the coding tasks in the VS Code environment.
6. Results are sent back through the chain to the Boss Agent, which updates its understanding of the project.

This workflow allows for more complex and context-aware coding assistance than using the Cline extension alone.

## Setup

1. Install the Cline VS Code extension (refer to Cline's documentation).
2. Set up the Boss Agent API:
   - See [Boss Agent API README](./boss_agent_api/README.md) for instructions.
3. Set up the Boss Agent:
   - See [Boss Agent README](./boss_agent/README.md) for instructions.

## Usage

1. Start VS Code with the Cline extension and Boss Agent API installed.
2. Run the Boss Agent in a terminal.
3. In the Boss Agent terminal, enter your coding goals in natural language.
4. Watch as the system works together to accomplish your coding tasks!

## Project Structure

```
.
├── boss_agent_api/    # VS Code extension acting as API layer
│   ├── README.md
│   └── ...
├── boss_agent/        # AI-powered agent
│   ├── README.md
│   └── ...
└── README.md          # This file
```

## Contributing

Contributions are welcome! Please read our contributing guidelines for details on how to submit pull requests, report issues, or request features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT model used in the Boss Agent
- The Cline extension developers for their powerful coding assistant

For component-specific details, please refer to the README files in each subdirectory.
