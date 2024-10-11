import asyncio
import websockets
import json
import unittest
from unittest.mock import MagicMock, patch
from api_layer import BossAgentAPI, BossAgentAPIError
from vscode_bridge import VSCodeBridge, VSCodeBridgeError

# Mock vscode module
mock_vscode = MagicMock()
mock_vscode.window.showErrorMessage = MagicMock()
mock_vscode.window.showInformationMessage = MagicMock()

# Apply the mock
@patch.dict('sys.modules', {'vscode': mock_vscode})
class TestBossAgentAPI(unittest.TestCase):
    def setUp(self):
        self.config = {
            'cline_extension_id': 'test.cline',
            'server_url': 'ws://localhost:8765',
            'log_level': 'INFO'
        }
        self.api = BossAgentAPI(self.config)

    @patch('websockets.connect')
    async def test_connect_to_server(self, mock_connect):
        mock_connect.return_value = MagicMock()
        await self.api.connect_to_server()
        mock_connect.assert_called_once_with(self.config['server_url'])
        mock_vscode.window.showInformationMessage.assert_called_once()

    @patch('websockets.connect')
    async def test_connect_to_server_retry(self, mock_connect):
        mock_connect.side_effect = [
            websockets.exceptions.WebSocketException("Connection failed"),
            websockets.exceptions.WebSocketException("Connection failed"),
            MagicMock()
        ]
        await self.api.connect_to_server()
        self.assertEqual(mock_connect.call_count, 3)
        mock_vscode.window.showInformationMessage.assert_called_once()

    @patch('websockets.connect')
    async def test_connect_to_server_failure_after_retries(self, mock_connect):
        mock_connect.side_effect = websockets.exceptions.WebSocketException("Connection failed")
        with self.assertRaises(BossAgentAPIError):
            await self.api.connect_to_server()
        self.assertEqual(mock_connect.call_count, 3)
        mock_vscode.window.showErrorMessage.assert_called()

    @patch('websockets.connect')
    async def test_process_user_goal(self, mock_connect):
        mock_websocket = MagicMock()
        mock_connect.return_value = mock_websocket
        mock_websocket.recv.side_effect = [
            json.dumps({'type': 'task', 'command': 'analyze_project'}),
            json.dumps({'type': 'task', 'command': 'suggest_improvements', 'args': {'file_path': 'test.py'}}),
            json.dumps({'type': 'complete'})
        ]

        await self.api.connect_to_server()
        result = await self.api.process_user_goal("Improve code quality")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['command'], 'analyze_project')
        self.assertEqual(result[1]['command'], 'suggest_improvements')

    @patch('websockets.connect')
    async def test_process_user_goal_retry(self, mock_connect):
        mock_websocket = MagicMock()
        mock_connect.return_value = mock_websocket
        mock_websocket.send.side_effect = [
            websockets.exceptions.WebSocketException("Send failed"),
            None
        ]
        mock_websocket.recv.side_effect = [
            json.dumps({'type': 'task', 'command': 'analyze_project'}),
            json.dumps({'type': 'complete'})
        ]

        await self.api.connect_to_server()
        result = await self.api.process_user_goal("Improve code quality")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['command'], 'analyze_project')
        self.assertEqual(mock_websocket.send.call_count, 2)

    @patch('websockets.connect')
    async def test_cancel_goal(self, mock_connect):
        mock_websocket = MagicMock()
        mock_connect.return_value = mock_websocket

        await self.api.connect_to_server()
        self.api.current_task = asyncio.create_task(asyncio.sleep(10))  # Simulate a long-running task
        await self.api.cancel_goal()

        self.assertTrue(self.api.current_task.cancelled())
        mock_websocket.send.assert_called_with(json.dumps({'type': 'cancel'}))
        mock_vscode.window.showInformationMessage.assert_called_with("Goal processing cancelled")

    @patch('vscode_bridge.VSCodeBridge.get_cline_context')
    async def test_get_cline_context(self, mock_get_context):
        mock_get_context.return_value = {'context': 'test_context'}
        result = await self.api.handle_server_message({'command': 'get_cline_context'})
        self.assertEqual(result['command'], 'get_cline_context')
        self.assertEqual(result['result'], {'context': 'test_context'})

    @patch('vscode_bridge.VSCodeBridge.get_cline_context')
    async def test_get_cline_context_error(self, mock_get_context):
        mock_get_context.side_effect = VSCodeBridgeError("Failed to get context")
        result = await self.api.handle_server_message({'command': 'get_cline_context'})
        self.assertEqual(result['command'], 'get_cline_context')
        self.assertIn('error', result['result'])

    @patch('vscode_bridge.VSCodeBridge.set_cline_context')
    async def test_set_cline_context(self, mock_set_context):
        mock_set_context.return_value = {'success': True}
        result = await self.api.handle_server_message({'command': 'set_cline_context', 'args': {'context': 'new_context'}})
        self.assertEqual(result['command'], 'set_cline_context')
        self.assertEqual(result['result'], {'success': True})

    @patch('vscode_bridge.VSCodeBridge.set_cline_context')
    async def test_set_cline_context_error(self, mock_set_context):
        mock_set_context.side_effect = VSCodeBridgeError("Failed to set context")
        result = await self.api.handle_server_message({'command': 'set_cline_context', 'args': {'context': 'new_context'}})
        self.assertEqual(result['command'], 'set_cline_context')
        self.assertIn('error', result['result'])

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()
