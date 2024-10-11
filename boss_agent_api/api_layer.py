import asyncio
import websockets
import json
import vscode
from vscode_bridge import VSCodeBridge
import logging
from retry import async_retry

class BossAgentAPIError(Exception):
    pass

class BossAgentAPI:
    def __init__(self, config):
        self.config = config
        self.vscode_bridge = VSCodeBridge(self.config.get('cline_extension_id', 'matej.cline'))
        self.websocket = None
        self.request_queue = asyncio.Queue()
        self.current_task = None
        logging.basicConfig(filename='boss_agent_api.log', level=logging.INFO)

    @async_retry(max_retries=3, delay=1, backoff=2, exceptions=(websockets.exceptions.WebSocketException,))
    async def connect_to_server(self):
        server_url = self.config.get('server_url', 'ws://localhost:8765')
        try:
            self.websocket = await websockets.connect(server_url)
            logging.info(f"Connected to server at {server_url}")
            vscode.window.showInformationMessage(f"Connected to server at {server_url}")
        except Exception as e:
            error_msg = f"Failed to connect to server: {str(e)}"
            logging.error(error_msg)
            vscode.window.showErrorMessage(error_msg)
            raise BossAgentAPIError(error_msg)

    @async_retry(max_retries=3, delay=1, backoff=2, exceptions=(websockets.exceptions.WebSocketException,))
    async def send_to_server(self, message):
        if self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
            except Exception as e:
                error_msg = f"Failed to send message to server: {str(e)}"
                logging.error(error_msg)
                vscode.window.showErrorMessage(error_msg)
                raise BossAgentAPIError(error_msg)
        else:
            error_msg = "Not connected to server"
            logging.error(error_msg)
            vscode.window.showErrorMessage(error_msg)
            raise BossAgentAPIError(error_msg)

    @async_retry(max_retries=3, delay=1, backoff=2, exceptions=(websockets.exceptions.WebSocketException, json.JSONDecodeError))
    async def receive_from_server(self):
        if self.websocket:
            try:
                return json.loads(await self.websocket.recv())
            except json.JSONDecodeError as e:
                error_msg = f"Received invalid JSON from server: {str(e)}"
                logging.error(error_msg)
                vscode.window.showErrorMessage(error_msg)
                raise BossAgentAPIError(error_msg)
            except Exception as e:
                error_msg = f"Failed to receive message from server: {str(e)}"
                logging.error(error_msg)
                vscode.window.showErrorMessage(error_msg)
                raise BossAgentAPIError(error_msg)
        else:
            error_msg = "Not connected to server"
            logging.error(error_msg)
            vscode.window.showErrorMessage(error_msg)
            raise BossAgentAPIError(error_msg)

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
            elif command == 'get_cline_context':
                result = await self.vscode_bridge.get_cline_context()
            elif command == 'set_cline_context':
                result = await self.vscode_bridge.set_cline_context(args.get('context'))
            elif command == 'get_cline_history':
                result = await self.vscode_bridge.get_cline_history()
            elif command == 'clear_cline_history':
                result = await self.vscode_bridge.clear_cline_history()
            else:
                logging.warning(f"Unknown command: {command}")
                return {'command': command, 'result': {'error': f"Unknown command: {command}"}}
            
            return {'command': command, 'result': result}
        except Exception as e:
            error_msg = f"Error handling command {command}: {str(e)}"
            logging.error(error_msg)
            return {'command': command, 'result': {'error': error_msg}}

    async def process_queue(self):
        while True:
            message = await self.request_queue.get()
            self.current_task = asyncio.create_task(self.handle_server_message(message))
            try:
                result = await self.current_task
                await self.send_to_server(result)
            except asyncio.CancelledError:
                logging.info("Task was cancelled")
            except BossAgentAPIError as e:
                logging.error(f"BossAgentAPIError: {str(e)}")
                vscode.window.showErrorMessage(f"BossAgentAPIError: {str(e)}")
            finally:
                self.current_task = None
            self.request_queue.task_done()

    async def start_server_communication(self):
        try:
            await self.connect_to_server()
            asyncio.create_task(self.process_queue())
            while True:
                message = await self.receive_from_server()
                if message:
                    await self.request_queue.put(message)
        except BossAgentAPIError as e:
            logging.error(f"BossAgentAPIError in server communication: {str(e)}")
            vscode.window.showErrorMessage(f"BossAgentAPIError in server communication: {str(e)}")

    def run_server_communication(self):
        asyncio.run(self.start_server_communication())

    @async_retry(max_retries=3, delay=1, backoff=2, exceptions=(BossAgentAPIError,))
    async def process_user_goal(self, goal):
        if not self.websocket:
            try:
                await self.connect_to_server()
            except BossAgentAPIError as e:
                logging.error(f"Failed to connect to server while processing user goal: {str(e)}")
                vscode.window.showErrorMessage(f"Failed to connect to server: {str(e)}")
                return []
        
        try:
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
        except BossAgentAPIError as e:
            logging.error(f"Error processing user goal: {str(e)}")
            vscode.window.showErrorMessage(f"Error processing user goal: {str(e)}")
            return []

    async def cancel_goal(self):
        if self.current_task:
            self.current_task.cancel()
            try:
                await self.send_to_server({'type': 'cancel'})
                logging.info("Goal processing cancelled")
                vscode.window.showInformationMessage("Goal processing cancelled")
            except BossAgentAPIError as e:
                logging.error(f"Failed to send cancel message to server: {str(e)}")
                vscode.window.showErrorMessage(f"Failed to cancel goal: {str(e)}")

api = BossAgentAPI(vscode.workspace.getConfiguration('bossClineAgentApi'))
