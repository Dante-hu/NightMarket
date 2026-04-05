# Load model directly
'''
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import torch
import accelerate
import re
'''

PROMPT_TEMPLATE = "[TRANS]\n{source_sentence}\n[/TRANS]\n[{target_language}]\n"
#for now return nothing since deplyoment is a bit tricky with the translation model and it's not essential to the core gameplay loop. Will add back in later when we have a better solution for hosting the model.

class HokTranslation:
    def __init__(self):
        print("[HokTranslation] Running in stub mode — translation model not loaded")


    def get_pipeline(self, path:str, tokenizer:'AutoTokenizer', accelerator:'accelerate.Accelerator') -> 'TextGenerationPipeline':
         return "translation not available"

    def translate(self, source_sentence:str, target_language:str) -> str:
        if not self.pipe:
            return "Translation unavailable in preview mode."
        prompt = PROMPT_TEMPLATE.format(source_sentence=source_sentence, target_language=target_language)
        out = self.pipe(prompt, return_full_text=False, repetition_penalty=1.1, do_sample=False)[0]['generated_text']
        text = out[:out.find("[/")].strip()
        return self.decode(text)

    def hex_to_bytes(self, match):
        return bytes([int(match.group(1), 16)])

    def decode(self, text):
         return text