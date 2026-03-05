# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("Bohanlu/Taigi-Llama-2-Translator-7B")
model = AutoModelForCausalLM.from_pretrained("Bohanlu/Taigi-Llama-2-Translator-7B")


PROMPT_TEMPLATE = "[TRANS]\n{source_sentence}\n[/TRANS]\n[{target_language}]\n"

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def translate(source_sentence:str, target_language:str) -> str:
    prompt = PROMPT_TEMPLATE.format(source_sentence=source_sentence, target_language=target_language)
    out = pipe(prompt, return_full_text=False, repetition_penalty=1.1, do_sample=False)[0]['generated_text']
    return out[:out.find("[/")].strip()

source_sentence = "How are you today？"

print("To Hanzi: " + translate(source_sentence, "HAN"))
# Output: To Hanzi: 你今仔日好無？

print("To POJ: " + translate(source_sentence, "POJ"))
# Output: To POJ: Lí kin-á-ji̍t án-chóaⁿ?

print("To Traditional Chinese: " + translate(source_sentence, "ZH"))
# Output: To Traditional Chinese: 你今天好嗎？

print("To Hanlo: " + translate(source_sentence, "HL"))
# Output: To Hanlo: 你今仔日好無？