from ollama import chat
import json
import re


class LLMProcessor:

    ALLOWED_ACTIONS = {
        "open_app",
        "close_app",
        "shutdown_pc",
        "restart_pc",
        "open_url",
        "unknown"
    }

    def __init__(self):
        self.model = "qwen3:8b"

        self.system_prompt = """
Ты модуль голосового ассистента Windows.

Ты ВОЗВРАЩАЕШЬ ТОЛЬКО JSON.

ПРИМЕРЫ КОМАНД И ОТВЕТОВ:

Команда: Открой Telegram
Команда: Запусти Telegram
Команда: Открой мессенджер Telegram
Ответ:
{
  "action": "open_url",
  "parameters": {
    "url": "https://web.telegram.org"
  }
}

Команда: Открой YouTube
Команда: Запусти ютуб
Команда: Включи YouTube
Ответ:
{
  "action": "open_url",
  "parameters": {
    "url": "https://youtube.com"
  }
}

Команда: Открой Google
Команда: Запусти браузер
Ответ:
{
  "action": "open_url",
  "parameters": {
    "url": "https://google.com"
  }
}

Команда: Выключи компьютер
Команда: Заверши работу ПК
Ответ:
{
  "action": "shutdown_pc",
  "parameters": {}
}

Команда: Перезагрузи компьютер
Ответ:
{
  "action": "restart_pc",
  "parameters": {}
}

Команда: Закрой Telegram
Ответ:
{
  "action": "unknown",
  "parameters": {}
}

Команда: Включи музыку
Команда: Сделай что-нибудь
Ответ:
{
  "action": "unknown",
  "parameters": {}
}

Допустимые действия:
open_app, close_app, shutdown_pc, restart_pc, open_url, unknown

Если команда неизвестна → unknown
ПРАВИЛА:

1. Если action = open_app → ОБЯЗАТЕЛЬНО укажи:
   parameters.app_name

2. Если action = close_app → ОБЯЗАТЕЛЬНО укажи:
   parameters.app_name

3. Если action = open_url → ОБЯЗАТЕЛЬНО укажи:
   parameters.url

4. parameters НИКОГДА не должен быть пустым, если action требует данные.

5. Если не можешь определить параметры → возвращай:
{
  "action": "unknown",
  "parameters": {}
}
"""

    # 🔥 1. вытаскиваем JSON даже из текста
    def extract_json(self, text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        return match.group(0)

    # 🔥 2. валидация структуры
    def validate(self, data):
        if not isinstance(data, dict):
            return False

        if "action" not in data:
            return False

        if "parameters" not in data:
            return False

        if data["action"] not in self.ALLOWED_ACTIONS:
            data["action"] = "unknown"
            data["parameters"] = {}

        return True

    # 🔥 3. основной метод
    def process_command(self, text):

        for attempt in range(2):  # retry

            response = chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ]
            )

            content = response["message"]["content"]

            json_str = self.extract_json(content)

            if not json_str:
                continue

            try:
                data = json.loads(json_str)

                if self.validate(data):
                    return data

            except json.JSONDecodeError:
                continue

        # fallback если всё сломалось
        return {
            "action": "error",
            "parameters": {
                "reason": "failed_to_parse_llm_output"
            }
        }
processor = LLMProcessor()

print(processor.process_command("Открой Telegram"))
print(processor.process_command("Выключи компьютер"))
print(processor.process_command("Включи музыку"))
print(processor.process_command("Запусти телеграм"))