from openai import OpenAI
from ..core.config import settings
import json
import asyncio
from pathlib import Path





async def subtask(user_prompt:str,max_retries: int = 3):
    """
    Декомпозиция задачи на подзадачи
     max_retries - максимальное количество попыток
    """
    client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    file_path = Path(__file__).parent / 'promt' / 'subtask_system_prompt'

    with open(file_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False,
                temperature=0.7  # Добавьте для более предсказуемых результатов
            )

            content = response.choices[0].message.content
            print(f"Попытка {attempt + 1}: Получен ответ от AI")
            print(f"Длина ответа: {len(content)} символов")

            # Очистка от маркеров кода если есть
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()

            # Парсим JSON
            result = json.loads(content)

            # Проверяем структуру
            if 'subtask' in result:
                print(f"Успешно распарсено! Получено {len(result['subtask'])} подзадач")
                return result
            else:
                print(f"⚠Нет ключа 'subtask' в ответе. Получено: {list(result.keys())}")
                if attempt == max_retries - 1:
                    return {"subtask": []}

        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON (попытка {attempt + 1}): {e}")
            print(f"Проблемный контент: {content[:200]}...")
            if attempt == max_retries - 1:
                return {"subtask": []}

        except Exception as e:
            print(f"Ошибка API (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                return {"subtask": []}

    return {"subtask": []}