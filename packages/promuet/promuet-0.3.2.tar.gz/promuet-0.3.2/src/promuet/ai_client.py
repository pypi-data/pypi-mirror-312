from abc import ABC, abstractmethod
from hashlib import md5
import json
from pathlib import Path

from openai import OpenAI


class ChatClientBase(ABC):
    cache_key: str = ''

    @abstractmethod
    def predict(self, messages: list[dict]) -> str:
        pass


class OpenAiChatClient(ChatClientBase):
    def __init__(self, openai: OpenAI = None, completion_kwargs: dict = None):
        self.client = openai or OpenAI()
        self.kwargs = completion_kwargs or {}
        self.kwargs.setdefault('model', 'gpt-3.5-turbo')
        self.cache_key = md5(
            json.dumps(self.kwargs, sort_keys=True).encode()
        ).hexdigest()

    def predict(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(messages=messages, **self.kwargs)
        return response.choices[0].message.content


class CachedChatClient(ChatClientBase):
    def __init__(self, cache_path: Path, client: ChatClientBase):
        self.cache_path = cache_path
        self.cache = json.loads(cache_path.read_text()) if cache_path.is_file() else {}
        self.client = client

    def predict(self, messages: list[dict]) -> str:
        key = md5(
            (self.client.cache_key + json.dumps(messages, sort_keys=True)).encode()
        ).hexdigest()
        if key not in self.cache:
            self.cache[key] = self.client.predict(messages)
        return self.cache[key]
