import vscode
import json
import os

class BossAgentWebviewProvider(vscode.WebviewViewProvider):
    viewType = "bossAgentWebview"

    def __init__(self, context, api):
        self.context = context
        self.api = api
        self._view = None
        self.history = []

    def resolveWebviewView(self, webviewView, context, token):
        self._view = webviewView

        webviewView.webview.options = {
            "enableScripts": True,
            "localResourceRoots": [self.context.extensionUri]
        }

        webviewView.webview.html = self._get_html_content()

        webviewView.webview.onDidReceiveMessage(self._handle_message)

    def _get_html_content(self):
        html_path = os.path.join(os.path.dirname(__file__), 'webview', 'index.html')
        with open(html_path, 'r') as file:
            html_content = file.read()

        html_content = html_content.replace('${webview.cspSource}', self._view.webview.cspSource)
        return html_content

    async def _handle_message(self, message):
        if message.get('command') == 'processGoal':
            goal = message.get('goal')
            try:
                result = await self.api.process_user_goal(goal)
                self.history.append({'goal': goal, 'result': result})
                await self._view.webview.postMessage({
                    'type': 'result',
                    'content': json.dumps(result)
                })
                await self._update_history()
            except Exception as e:
                await self._view.webview.postMessage({
                    'type': 'error',
                    'content': str(e)
                })
        elif message.get('command') == 'cancelGoal':
            await self.api.cancel_goal()
        elif message.get('command') == 'getHistory':
            await self._update_history()
        elif message.get('command') == 'showError':
            vscode.window.showErrorMessage(message.get('message'))

    async def _update_history(self):
        await self._view.webview.postMessage({
            'type': 'history',
            'content': self.history
        })

    def update_view(self, data):
        if self._view:
            self._view.webview.postMessage(data)
