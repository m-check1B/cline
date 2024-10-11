import json
from typing import List, Dict, Any
import os

class Memory:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.conversation_history: List[Dict[str, Any]] = []
        self.task_history: List[Dict[str, Any]] = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(os.path.join(self.storage_path, 'conversation_history.json')):
            with open(os.path.join(self.storage_path, 'conversation_history.json'), 'r') as f:
                self.conversation_history = json.load(f)
        if os.path.exists(os.path.join(self.storage_path, 'task_history.json')):
            with open(os.path.join(self.storage_path, 'task_history.json'), 'r') as f:
                self.task_history = json.load(f)

    def save_memory(self):
        with open(os.path.join(self.storage_path, 'conversation_history.json'), 'w') as f:
            json.dump(self.conversation_history, f)
        with open(os.path.join(self.storage_path, 'task_history.json'), 'w') as f:
            json.dump(self.task_history, f)

    def add_message(self, message: Dict[str, Any]):
        self.conversation_history.append(message)
        self.save_memory()

    def add_task(self, task: Dict[str, Any]):
        self.task_history.append(task)
        self.save_memory()

    def get_conversation_history(self) -> List[Dict[str, Any]]:
        return self.conversation_history

    def get_task_history(self) -> List[Dict[str, Any]]:
        return self.task_history

    def clear_conversation_history(self):
        self.conversation_history = []
        self.save_memory()

    def clear_task_history(self):
        self.task_history = []
        self.save_memory()
