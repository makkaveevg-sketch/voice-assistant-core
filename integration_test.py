from llm.processor import LLMProcessor
from executor.main import process_command

import json

processor = LLMProcessor()

while True:

    text = input("Команда: ")

    if text.lower() == "exit":
        break

    command = processor.process_command(text)

    print("\nJSON от LLM:")
    print(command)

    result = process_command(
        json.dumps(command)
    )

    print("\nОтвет Executor:")
    print(result)

    print("\n" + "=" * 50 + "\n")