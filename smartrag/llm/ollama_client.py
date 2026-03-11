import requests
from typing import Iterator
from smartrag.config import settings

class OllamaClient:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    def generate(self, prompt: str, stream: bool = False) -> str | Iterator[str]:
        url = f"{self.base_url}/api/generate"
        data = {"model": self.model, "prompt": prompt, "stream": stream}
        
        if stream:
            return self._stream_generate(url, data)
        
        response = requests.post(url, json=data)
        return response.json()["response"]
    
    def _stream_generate(self, url: str, data: dict) -> Iterator[str]:
        with requests.post(url, json=data, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
