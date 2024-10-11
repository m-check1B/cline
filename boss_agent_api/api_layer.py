import asyncio
import websockets
import json
import vscode
from vscode_bridge import VSCodeBridge
import logging

class BossAgentAPI:
    def __init__(self, config):
        self.config = config
        self.vscode_bridge = VSCodeBridge(self.config.get('cline_extension_id', 'matej.cline'))
        self.websocket = None
        self.request_queue = asyncio.Queue()
        self.current_task = None
        logging.basicConfig(filename='boss_agent_api.log', level=logging.INFO)

    async def connect_to_server(self):
        server_url = self.config.get('server_url', 'ws://localhost:8765')
        try:
            self.websocket = await websockets.connect(server_url)
            logging.info(f"Connected to server at {server_url}")
            vscode.window.showInformationMessage(f"Connected to server at {server_url}")
        except Exception as e:
            logging.error(f"Failed to connect to server: {str(e)}")
            vscode.window.showErrorMessage(f"Failed to connect to server: {str(e)}")

    async def send_to_server(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))
        else:
            logging.error("Not connected to server")
            vscode.window.showErrorMessage("Not connected to server")

    async def receive_from_server(self):
        if self.websocket:
            return json.loads(await self.websocket.recv())
        else:
            logging.error("Not connected to server")
            vscode.window.showErrorMessage("Not connected to server")
            return None

    async def handle_server_message(self, message):
        try:
            command = message.get('command')
            args = message.get('args', {})
            if command == 'send_message':
                result = await self.vscode_bridge.send_custom_message(args.get('content'))
            elif command == 'analyze_project':
                result = await self.vscode_bridge.analyze_project()
            elif command == 'suggest_improvements':
                result = await self.vscode_bridge.suggest_improvements(args.get('file_path'))
            elif command == 'generate_code':
                result = await self.vscode_bridge.generate_code(args.get('prompt'))
            elif command == 'refactor_code':
                result = await self.vscode_bridge.refactor_code(args.get('file_path'), args.get('refactor_type'))
            elif command == 'run_tests':
                result = await self.vscode_bridge.run_tests(args.get('test_path'))
            elif command == 'create_file':
                result = await self.vscode_bridge.create_file(args.get('file_path'), args.get('content'))
            elif command == 'read_file':
                result = await self.vscode_bridge.read_file(args.get('file_path'))
            elif command == 'update_file':
                result = await self.vscode_bridge.update_file(args.get('file_path'), args.get('content'))
            elif command == 'delete_file':
                result = await self.vscode_bridge.delete_file(args.get('file_path'))
            elif command == 'search_and_replace':
                result = await self.vscode_bridge.search_and_replace(args.get('search_pattern'), args.get('replace_pattern'))
            else:
                logging.warning(f"Unknown command: {command}")
                result = {"error": f"Unknown command: {command}"}
            
            return {'command': command, 'result': result}
        except Exception as e:
            logging.error(f"Error handling command {command}: {str(e)}")
            return {'command': command, 'result': {'error': str(e)}}

    async def process_queue(self):
        while True:
            message = await self.request_queue.get()
            self.current_task = asyncio.create_task(self.handle_server_message(message))
            try:
                result = await self.current_task
                await self.send_to_server(result)
            except asyncio.CancelledError:
                logging.info("Task was cancelled")
            finally:
                self.current_task = None
            self.request_queue.task_done()

    async def start_server_communication(self):
        await self.connect_to_server()
        asyncio.create_task(self.process_queue())
        while True:
            message = await self.receive_from_server()
            if message:
                await self.request_queue.put(message)

    def run_server_communication(self):
        asyncio.run(self.start_server_communication())

    async def process_user_goal(self, goal):
        if not self.websocket:
            await self.connect_to_server()
        
        await self.send_to_server({'type': 'goal', 'content': goal})
        tasks = []
        while True:
            result = await self.receive_from_server()
            if result.get('type') == 'task':
                task_result = await self.handle_server_message(result)
                tasks.append(task_result)
            elif result.get('type') == 'complete':
                break
        return tasks

    async def cancel_goal(self):
        if self.current_task:
            self.current_task.cancel()
            await self.send_to_server({'type': 'cancel'})
            logging.info("Goal processing cancelled")
            vscode.window.showInformationMessage("Goal processing cancelled")

api = BossAgentAPI(vscode.workspace.getConfiguration('bossClineAgentApi'))
