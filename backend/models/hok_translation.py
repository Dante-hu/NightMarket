# Load model directly
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import torch
import accelerate
import re

PROMPT_TEMPLATE = "[TRANS]\n{source_sentence}\n[/TRANS]\n[{target_language}]\n"

class HokTranslation:
    def __init__(self):
        self.model_dir = "Bohanlu/Taigi-Llama-2-Translator-7B" # or "Bohanlu/Taigi-Llama-2-Translator-13B" for the 13B model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir, use_fast=False)

        self.accelerator = accelerate.Accelerator()
        self.pipe = self.get_pipeline(self.model_dir, self.tokenizer, self.accelerator)


    def get_pipeline(self, path:str, tokenizer:AutoTokenizer, accelerator:accelerate.Accelerator) -> TextGenerationPipeline:
        model = AutoModelForCausalLM.from_pretrained(
            path, torch_dtype=torch.float16, device_map='auto', trust_remote_code=True)
        
        terminators = [tokenizer.eos_token_id, tokenizer.pad_token_id]

        pipeline = TextGenerationPipeline(model = model, tokenizer = tokenizer, num_workers=accelerator.state.num_processes*4, pad_token_id=tokenizer.pad_token_id, eos_token_id=terminators)

        return pipeline

    def translate(self, source_sentence:str, target_language:str) -> str:
        print(f"[TRANSLATE] Input: '{source_sentence}' -> target: {target_language}")
        prompt = PROMPT_TEMPLATE.format(source_sentence=source_sentence, target_language=target_language)
        print(f"[TRANSLATE] Prompt: {repr(prompt)}")
        out = self.pipe(prompt, return_full_text=False, max_new_tokens=1024)[0]['generated_text']
        print(f"[TRANSLATE] Raw: {out}")
        text = out[:out.rfind("[ /")].strip()
        text = re.sub(r'\s*\[.*?[A-Z]+.*?\]', '', text).strip()
        text = self.decode(text)
        print(f"[TRANSLATE] Result: {text}")
        return text

    def decode(self, text):
        text = re.sub(r'<0x([0-9A-Fa-f]{2})>', lambda m: chr(int(m.group(1), 16)), text)
        text = text.replace("▁", "")
        text = re.sub(r'\s+', '', text)
        return text.strip()