import vscode
import logging

class VSCodeBridgeError(Exception):
    pass

class VSCodeBridge:
    def __init__(self, extension_id):
        self.extension_id = extension_id
        logging.basicConfig(filename='vscode_bridge.log', level=logging.INFO)

    async def execute_command(self, command, args=None):
        try:
            if args:
                result = await vscode.commands.executeCommand(command, args)
            else:
                result = await vscode.commands.executeCommand(command)
            logging.info(f"Command executed: {command}")
            return result
        except Exception as e:
            error_msg = f"Error executing command {command}: {e}"
            logging.error(error_msg)
            raise VSCodeBridgeError(error_msg)

    async def send_custom_message(self, message):
        return await self.execute_command(f"{self.extension_id}.sendMessage", {"message": message})

    async def analyze_project(self):
        return await self.execute_command(f"{self.extension_id}.analyzeProject")

    async def suggest_improvements(self, file_path):
        return await self.execute_command(f"{self.extension_id}.suggestImprovements", {"filePath": file_path})

    async def generate_code(self, prompt):
        return await self.execute_command(f"{self.extension_id}.generateCode", {"prompt": prompt})

    async def refactor_code(self, file_path, refactor_type):
        return await self.execute_command(f"{self.extension_id}.refactorCode", {"filePath": file_path, "refactorType": refactor_type})

    async def run_tests(self, test_path):
        return await self.execute_command(f"{self.extension_id}.runTests", {"testPath": test_path})

    async def create_file(self, file_path, content):
        return await self.execute_command(f"{self.extension_id}.createFile", {"filePath": file_path, "content": content})

    async def read_file(self, file_path):
        return await self.execute_command(f"{self.extension_id}.readFile", {"filePath": file_path})

    async def update_file(self, file_path, content):
        return await self.execute_command(f"{self.extension_id}.updateFile", {"filePath": file_path, "content": content})

    async def delete_file(self, file_path):
        return await self.execute_command(f"{self.extension_id}.deleteFile", {"filePath": file_path})

    async def search_and_replace(self, search_pattern, replace_pattern):
        return await self.execute_command(f"{self.extension_id}.searchAndReplace", {"searchPattern": search_pattern, "replacePattern": replace_pattern})

    async def get_cline_context(self):
        try:
            return await self.execute_command(f"{self.extension_id}.getContext")
        except VSCodeBridgeError as e:
            logging.error(f"Failed to get Cline context: {str(e)}")
            raise VSCodeBridgeError(f"Failed to get Cline context: {str(e)}")

    async def set_cline_context(self, context):
        try:
            return await self.execute_command(f"{self.extension_id}.setContext", {"context": context})
        except VSCodeBridgeError as e:
            logging.error(f"Failed to set Cline context: {str(e)}")
            raise VSCodeBridgeError(f"Failed to set Cline context: {str(e)}")

    async def get_cline_history(self):
        try:
            return await self.execute_command(f"{self.extension_id}.getHistory")
        except VSCodeBridgeError as e:
            logging.error(f"Failed to get Cline history: {str(e)}")
            raise VSCodeBridgeError(f"Failed to get Cline history: {str(e)}")

    async def clear_cline_history(self):
        try:
            return await self.execute_command(f"{self.extension_id}.clearHistory")
        except VSCodeBridgeError as e:
            logging.error(f"Failed to clear Cline history: {str(e)}")
            raise VSCodeBridgeError(f"Failed to clear Cline history: {str(e)}")
