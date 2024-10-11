import asyncio
from main import BossAgent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_boss_agent():
    boss_agent = BossAgent()
    await boss_agent.connect_to_boss_agent_api()

    test_goals = [
        "Create a new Python file called 'hello_world.py' and write a simple 'Hello, World!' program.",
        "Analyze the current project structure and suggest improvements.",
        "Refactor the 'process_user_goal' method in the BossAgent class to improve error handling.",
        "Generate unit tests for the APIHandler class.",
        "Search for all TODO comments in the project and list them.",
    ]

    for goal in test_goals:
        logging.info(f"Testing goal: {goal}")
        await boss_agent.process_user_goal(goal)
        logging.info("Goal processing completed.")
        logging.info("---")

    logging.info("All tests completed.")

if __name__ == "__main__":
    asyncio.run(test_boss_agent())
