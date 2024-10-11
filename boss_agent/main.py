import asyncio
import websockets
import json
import os
import logging
from dotenv import load_dotenv
from memory import Memory
from api_handlers import APIHandler
from typing import Dict, Any, List

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BossAgent:
    def __init__(self):
        self.boss_agent_api_url = os.getenv("BOSS_AGENT_API_URL")
        self.websocket = None
        self.memory = Memory(os.path.join(os.path.dirname(__file__), 'storage'))
        self.api_configuration: Dict[str, Any] = {}
        self.load_api_configuration()
        self.api_handler = APIHandler(self.api_configuration)

    def load_api_configuration(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.api_configuration = json.load(f)
        else:
            logging.warning("Config file not found. Using default configuration.")
            self.api_configuration = {"apiProvider": "openai", "apiModelId": "gpt-3.5-turbo"}

    async def connect_to_boss_agent_api(self):
        try:
            self.websocket = await websockets.connect(self.boss_agent_api_url)
            logging.info(f"Connected to Boss Agent API at {self.boss_agent_api_url}")
        except Exception as e:
            logging.error(f"Failed to connect to Boss Agent API: {str(e)}")

    async def send_to_boss_agent_api(self, message):
        try:
            await self.websocket.send(json.dumps(message))
        except Exception as e:
            logging.error(f"Error sending message to Boss Agent API: {str(e)}")

    async def receive_from_boss_agent_api(self):
        try:
            return json.loads(await self.websocket.recv())
        except Exception as e:
            logging.error(f"Error receiving message from Boss Agent API: {str(e)}")
            return None

    async def process_user_goal(self, goal: str):
        try:
            messages = [
                {"role": "system", "content": "You are an AI assistant that helps to break down coding goals into specific tasks."},
                {"role": "user", "content": f"Break down this coding goal into specific tasks: {goal}"}
            ]
            response = await self.api_handler.process_request(messages)
            
            if response['role'] == 'error':
                logging.error(f"Error processing user goal: {response['content']}")
                return

            plan = response['content']
            tasks = await self.plan_to_tasks(plan)
            
            for task in tasks:
                await self.send_to_boss_agent_api(task)
                result = await self.receive_from_boss_agent_api()
                if result:
                    logging.info(f"Task result: {result}")
                    self.memory.add_message({"role": "system", "content": f"Task: {task}\nResult: {result}"})
                else:
                    logging.warning(f"No result received for task: {task}")

        except Exception as e:
            logging.error(f"Error in process_user_goal: {str(e)}")

    async def plan_to_tasks(self, plan: str) -> List[Dict[str, Any]]:
        try:
            messages = [
                {"role": "system", "content": "You are an AI assistant that converts high-level coding plans into specific tasks for a coding assistant. Each task should be a dictionary with 'command' and 'args' keys."},
                {"role": "user", "content": f"Convert this plan into a list of tasks:\n\n{plan}"}
            ]
            response = await self.api_handler.process_request(messages)
            
            if response['role'] == 'error':
                logging.error(f"Error converting plan to tasks: {response['content']}")
                return []

            tasks = json.loads(response['content'])
            return tasks
        except json.JSONDecodeError:
            logging.error(f"Error decoding tasks JSON: {response['content']}")
            return []
        except Exception as e:
            logging.error(f"Error in plan_to_tasks: {str(e)}")
            return []

    async def run(self):
        await self.connect_to_boss_agent_api()
        while True:
            try:
                goal = input("Enter your coding goal (or 'quit' to exit): ")
                if goal.lower() == 'quit':
                    break
                await self.process_user_goal(goal)
                self.memory.add_task({"goal": goal, "timestamp": asyncio.get_event_loop().time()})
            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")

if __name__ == "__main__":
    boss_agent = BossAgent()
    asyncio.get_event_loop().run_until_complete(boss_agent.run())
