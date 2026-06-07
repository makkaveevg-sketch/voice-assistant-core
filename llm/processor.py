from ollama import chat
import json
import re


class LLMProcessor:

    def __init__(self):

        self.model = "qwen3:8b"

        self.aliases = {
            "дискорд": "discord",
            "дис": "discord",
            "discord": "discord",

            "ютуб": "youtube",
            "youtube": "youtube",
            "yt": "youtube",

            "телеграм": "telegram",
            "телега": "telegram",
            "tg": "telegram",
            
            "стим": "steam",
            "стимчик": "steam",
            
            "хром": "chrome",
            "гугл хром": "chrome",
            "гугл": "chrome",
            
            "яндекс": "yandex",
            
            "вс код": "vscode",
            "визуал студио код": "vscode"
        }

        self.system_prompt = """
Ты модуль определения действий голосового ассистента Windows.

Твоя задача — преобразовывать команды пользователя в JSON.

ОТВЕЧАЙ ТОЛЬКО ВАЛИДНЫМ JSON.

Не добавляй:
- пояснения
- markdown
- комментарии
- текст до JSON
- текст после JSON

Используй только действия:

open_app
close_app
open_url
shutdown_pc
restart_pc
unknown

Формат ответа:

{
  "action": "...",
  "parameters": {}
}

Примеры:

Команда: Открой Discord

Ответ:
{
  "action": "open_app",
  "parameters": {
    "app_name": "discord"
  }
}

Команда: Закрой Discord

Ответ:
{
  "action": "close_app",
  "parameters": {
    "app_name": "discord"
  }
}

Команда: Открой YouTube

Ответ:
{
  "action": "open_url",
  "parameters": {
    "url": "https://youtube.com"
  }
}

Команда: Выключи компьютер

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

Команда: Сделай что-нибудь

Ответ:
{
  "action": "unknown",
  "parameters": {}
}
"""

    def extract_json(self, text):

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return match.group(0)

        return None

    def normalize_text(self, text):

        return text.lower().strip()

    def normalize_app_name(self, app_name):

        if not app_name:
            return app_name

        app_name = app_name.lower().strip()

        if app_name in self.aliases:
            return self.aliases[app_name]

        return app_name

    def process_command(self, text):

        text = self.normalize_text(text)

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        content = response["message"]["content"]

        json_str = self.extract_json(content)

        if not json_str:
            return {
                "action": "unknown",
                "parameters": {}
            }

        try:

            data = json.loads(json_str)

            if "action" not in data:
                return {
                    "action": "unknown",
                    "parameters": {}
                }

            if "parameters" not in data:
                data["parameters"] = {}

            if "app_name" in data["parameters"]:
                data["parameters"]["app_name"] = (
                    self.normalize_app_name(
                        data["parameters"]["app_name"]
                    )
                )

            return data

        except json.JSONDecodeError:

            return {
                "action": "unknown",
                "parameters": {}
            }


if __name__ == "__main__":

    processor = LLMProcessor()

    tests = [
        "открой дискорд",
        "закрой дискорд",
        "открой ютуб",
        "выключи компьютер",
        "перезагрузи компьютер"
    ]

    for command in tests:

        result = processor.process_command(command)

        print(command)
        print(result)
        print("-" * 50)