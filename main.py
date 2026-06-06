from llm.processor import LLMProcessor
from core.resolver import resolve

processor = LLMProcessor()

while True:
    text = input("Ты: ")

    command = processor.process_command(text)
    print("LLM:", command)

    result = resolve(command)
    print("RESOLVED:", result)
    print("-" * 40)