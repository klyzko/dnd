from openai import OpenAI
from core.config import settings

def Openaiclient():
    return OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")