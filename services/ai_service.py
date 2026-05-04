import aiohttp
import asyncio
import json


async def deepseek_request_async(messages, api_key, **kwargs):
    """
    Асинхронный запрос к DeepSeek API

    Args:
        messages: список сообщений [{"role": "user", "content": "..."}]
        api_key: ваш API ключ
        **kwargs: дополнительные параметры (temperature, max_tokens и т.д.)
    """
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "stream": False,
        **kwargs
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"Ошибка {response.status}: {error_text}")


# Пример использования
async def main():
    api_key = "ВАШ_API_КЛЮЧ"

    messages = [
        {"role": "system", "content": "Ты полезный ассистент"},
        {"role": "user", "content": "Расскажи шутку про программистов"}
    ]

    response = await deepseek_request_async(messages, api_key, temperature=0.8)
    print(response)