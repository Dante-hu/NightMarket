# Load model directly
from transformers import AutoModelForCausalLM, AutoTokenizer, TextGenerationPipeline
import torch
import accelerate
import re

def get_pipeline(path:str, tokenizer:AutoTokenizer, accelerator:accelerate.Accelerator) -> TextGenerationPipeline:
    model = AutoModelForCausalLM.from_pretrained(
        path, torch_dtype=torch.float16, device_map='auto', trust_remote_code=True)
    
    terminators = [tokenizer.eos_token_id, tokenizer.pad_token_id]

    pipeline = TextGenerationPipeline(model = model, tokenizer = tokenizer, num_workers=accelerator.state.num_processes*4, pad_token_id=tokenizer.pad_token_id, eos_token_id=terminators)

    return pipeline

model_dir = "Bohanlu/Taigi-Llama-2-Translator-7B" # or "Bohanlu/Taigi-Llama-2-Translator-13B" for the 13B model
tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False)

accelerator = accelerate.Accelerator()
pipe = get_pipeline(model_dir, tokenizer, accelerator)

PROMPT_TEMPLATE = "[TRANS]\n{source_sentence}\n[/TRANS]\n[{target_language}]\n"

def translate(source_sentence:str, target_language:str) -> str:
    prompt = PROMPT_TEMPLATE.format(source_sentence=source_sentence, target_language=target_language)
    out = pipe(prompt, return_full_text=False, repetition_penalty=1.1, do_sample=False)[0]['generated_text']
    text = out[:out.find("[/")].strip()
    return decode(text)


def hex_to_bytes(match):
    return bytes([int(match.group(1), 16)])

def decode(text):
    byte_seq = b"".join(
        hex_to_bytes(m) if m else s.encode("utf-8")
        for s in re.split(r'(<0x[0-9A-Fa-f]{2}>)', text)
        for m in ([re.match(r'<0x([0-9A-Fa-f]{2})>', s)] if s.startswith("<0x") else [None])
    )
    decoded = byte_seq.decode("utf-8", errors="ignore")
    decoded = decoded.replace("▁", " ")
    decoded = re.sub(r'\s+', ' ', decoded)
    return decoded.strip()