from voice.voice_module import VoiceModule

from llm.processor import LLMProcessor
from executor.main import process_command

import json

processor = LLMProcessor()

def vik_logic(user_text):

    command = processor.process_command(user_text)

    result = process_command(
        json.dumps(command)
)

    return str(result)

voice = VoiceModule()

voice.start_listening(
llm_function=vik_logic
)        