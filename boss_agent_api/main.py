import vscode
from api_layer import BossAgentAPI
import asyncio
import os
from dotenv import load_dotenv
from webview_provider import BossAgentWebviewProvider

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

    vscode.window.showInformationMessage("Boss Cline Agent API is now active!")

def deactivate():
    vscode.window.showInformationMessage("Boss Cline Agent API has been deactivated.")
