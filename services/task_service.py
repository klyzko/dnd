from openai import OpenAI
from scripts.regsetup import description

from ..core.config import settings
import json
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from ..model.tasks import Task
from dnd.shemas.taskqwestionai import Mission
from dnd.core.logger_config import logg



async def dndtask(user_prompt:str,max_retries: int = 3):
    """
    создание квеста из задачи, используя промт
    """
    client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    file_path = Path(__file__).parent.parent / 'promt' / 'quest'

    with open(file_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    print(system_prompt)
    print(f"user_prompt: {user_prompt}")
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
            logg.info(f"Попытка {attempt + 1}: Получен ответ от AI")
            logg.info(f"Длина ответа: {len(content)} символов")

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
            if 'Mission' in result:
                logg.info(f"Успешно распарсено! Получено {len(result['Mission'])} подзадач")
                qwest = Mission.model_validate(result.get('Mission'))
                return qwest
            else:
                logg.error(f"⚠Нет ключа 'Mission' в ответе. Получено: {list(result.keys())}")
                if attempt == max_retries - 1:
                    return {"Mission": []}

        except json.JSONDecodeError as e:
            logg.error(f"Ошибка парсинга JSON (попытка {attempt + 1}): {e}")
            logg.error(f"Проблемный контент: {content[:200]}...")
            if attempt == max_retries - 1:
                return {"Mission": []}

        except Exception as e:
            logg.error(f"Ошибка API (попытка {attempt + 1}): {e}")
            if attempt == max_retries - 1:
                return {"Mission": []}

    return {"Mission": []}