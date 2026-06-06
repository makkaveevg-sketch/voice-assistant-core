# Voice Assistant Core

Локальный голосовой ассистент для Windows.

## Архитектура

User → Speech → LLM → Resolver → Windows Executor

## Модули

### llm/
Преобразует текст пользователя в JSON-команду.

### core/
Обрабатывает команды и сопоставляет их с действиями системы.

### contracts/
Контракт данных между всеми модулями (schema).

## Формат команды

```json
{
  "action": "open | close | shutdown_pc | restart_pc | scenario | unknown",
  "parameters": {
    "target": "string",
    "url": "string"
  }
}