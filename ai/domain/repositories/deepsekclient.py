from ai.ports.ILLMclient import LLMClient
from ai.domain.entities.Message import Message
from openai import OpenAI,APITimeoutError, RateLimitError
from ai.ports.llm_errors import LLMTimeoutError, LLMResponseFormatError, LLMUnavailableError

import httpx
from core.logger_config import logg


class deepseekClient(LLMClient):

    def __init__(self, client: OpenAI, temperature: float = 0.7):
        self.client = client
        self.temperature = temperature



    async def chat(self,message: Message,model:str,**kwargs):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": message.role},
                        {"role": "user", "content": message.content}],
                temperature=self.temperature,
                stream=False,
                timeout=httpx.Timeout(60.0, connect=10.0),
                **kwargs
            )
            content = response.choices[0].message.content
            # Очистка от маркеров кода если есть
            content = self._sanitize(content)
            return content
        except APITimeoutError as e:
            logg.error(f"Timeout: {e}")
            raise LLMTimeoutError(f"Timeout: {e}")
        except LLMResponseFormatError as e:
            logg.error(f"limit Error: {e}")
            raise LLMResponseFormatError(f"limit Error: {e}")
        except RateLimitError as e:
            logg.error(f"Unavailable: {e}")
            raise LLMUnavailableError(f"Unavailable: {e}")
        except Exception as e:
            logg.error(f"Error: {e}")
            raise e

    def _sanitize(self, content: str) -> str:
        if not content:
            raise LLMResponseFormatError("Empty response")

        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        return content.strip()








    async def image(self,message: Message,model:str,**kwargs):
        pass
