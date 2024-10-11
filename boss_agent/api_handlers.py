import openai
import anthropic
import os
from typing import Dict, Any

class APIHandler:
    def __init__(self, api_configuration: Dict[str, Any]):
        self.api_configuration = api_configuration
        self.setup_api_clients()

    def setup_api_clients(self):
        if self.api_configuration['apiProvider'] == 'openai':
            openai.api_key = self.api_configuration.get('openAiApiKey') or os.getenv("OPENAI_API_KEY")
        elif self.api_configuration['apiProvider'] == 'anthropic':
            self.anthropic_client = anthropic.Anthropic(api_key=self.api_configuration.get('apiKey') or os.getenv("ANTHROPIC_API_KEY"))

    async def process_with_openai(self, messages: list) -> Dict[str, Any]:
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.api_configuration.get('apiModelId', 'gpt-3.5-turbo'),
                messages=messages
            )
            return {
                'content': response.choices[0].message.content,
                'role': response.choices[0].message.role
            }
        except Exception as e:
            print(f"Error in OpenAI API call: {str(e)}")
            return {'content': str(e), 'role': 'error'}

    async def process_with_anthropic(self, messages: list) -> Dict[str, Any]:
        try:
            prompt = "\n\n".join([f"{m['role']}: {m['content']}" for m in messages])
            response = await self.anthropic_client.completions.create(
                model=self.api_configuration.get('apiModelId', 'claude-2'),
                prompt=prompt,
                max_tokens_to_sample=1000
            )
            return {
                'content': response.completion,
                'role': 'assistant'
            }
        except Exception as e:
            print(f"Error in Anthropic API call: {str(e)}")
            return {'content': str(e), 'role': 'error'}

    async def process_request(self, messages: list) -> Dict[str, Any]:
        if self.api_configuration['apiProvider'] == 'openai':
            return await self.process_with_openai(messages)
        elif self.api_configuration['apiProvider'] == 'anthropic':
            return await self.process_with_anthropic(messages)
        else:
            raise ValueError(f"Unsupported API provider: {self.api_configuration['apiProvider']}")
