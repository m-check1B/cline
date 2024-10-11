import vscode
from api_layer import BossAgentAPI
import asyncio
import os
from dotenv import load_dotenv
from webview_provider import BossAgentWebviewProvider
import subprocess

load_dotenv()

def activate(context):
    config = {
        'cline_extension_id': os.getenv('CLINE_EXTENSION_ID'),
        'server_url': os.getenv('SERVER_URL'),
        'log_level': os.getenv('LOG_LEVEL')
    }
    api = BossAgentAPI(config)

    # Start server communication
    asyncio.create_task(api.start_server_communication())

    # Create and register webview provider
    webview_provider = BossAgentWebviewProvider(context, api)
    context.subscriptions.append(
        vscode.window.registerWebviewViewProvider(BossAgentWebviewProvider.viewType, webview_provider)
    )

    # Register commands
    context.subscriptions.append(
        vscode.commands.registerCommand('bossClineAgentApi.connectToServer', api.connect_to_server)
    )
    context.subscriptions.append(
        vscode.commands.registerCommand('bossClineAgentApi.openWebview', lambda: vscode.commands.executeCommand('workbench.view.extension.boss-agent'))
    )
    context.subscriptions.append(
        vscode.commands.registerCommand('bossClineAgentApi.cancelGoal', api.cancel_goal)
    )
    context.subscriptions.append(
        vscode.commands.registerCommand('bossClineAgentApi.runTests', run_tests)
    )

    vscode.window.showInformationMessage("Boss Cline Agent API is now active!")

def deactivate():
    vscode.window.showInformationMessage("Boss Cline Agent API has been deactivated.")

def run_tests():
    test_file = os.path.join(os.path.dirname(__file__), 'test_boss_agent_api.py')
    result = subprocess.run(['python', test_file], capture_output=True, text=True)
    if result.returncode == 0:
        vscode.window.showInformationMessage("All tests passed successfully!")
    else:
        vscode.window.showErrorMessage(f"Tests failed. Error: {result.stderr}")
    vscode.window.showInformationMessage(f"Test output: {result.stdout}")
