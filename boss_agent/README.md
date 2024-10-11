# Boss Agent

The Boss Agent is an AI-powered assistant that works in tandem with the Boss Agent API VS Code extension to provide advanced coding assistance. It uses natural language processing to understand user goals and translates them into specific actions for the Cline VS Code extension.

## Features

- Natural language understanding of coding goals
- Task breakdown and planning
- Interaction with the Cline extension via the Boss Agent API
- Project state management
- Continuous learning and improvement

## Setup

1. Ensure you have Python 3.7+ installed.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with the following variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `BOSS_AGENT_API_URL`: WebSocket URL of the Boss Agent API (default: ws://localhost:8765)
   - `LOG_LEVEL`: Logging level (e.g., INFO, DEBUG)

## Usage

1. Start the Boss Agent:
   ```
   python main.py
   ```
2. Enter your coding goals in natural language when prompted.
3. The Boss Agent will process your goal, break it down into tasks, and interact with the Cline extension via the Boss Agent API to accomplish the goal.

## How it Works

1. The Boss Agent receives a coding goal from the user.
2. It uses OpenAI's GPT model to analyze the goal and create a plan.
3. The plan is converted into specific commands for the Cline extension.
4. These commands are sent to the Boss Agent API, which translates them into actions for the Cline extension.
5. The Boss Agent receives results from each action and updates its project state.
6. This process continues until the entire goal is accomplished.

## Customization

You can extend the Boss Agent's capabilities by:
- Adding new command types in the `plan_to_tasks` method
- Enhancing the project state management in the `update_project_state` method
- Implementing more sophisticated goal processing algorithms

## Troubleshooting

If you encounter issues:

1. Check the log file for error messages
2. Ensure the Boss Agent API extension is running in VS Code
3. Verify that your OpenAI API key is valid and has sufficient credits

For more detailed information, refer to the main project README.
