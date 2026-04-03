from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import numpy as np

model = VitsModel.from_pretrained("facebook/mms-tts-nan")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-nan")
output_dir = "audio-clips"

def generate_tts(node_id, text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    output = output.detach().cpu().numpy().squeeze()
    output = np.clip(output, -1, 1)
    output = (output * 32767).astype(np.int16)

    scipy.io.wavfile.write(f"{output_dir}/{node_id}.wav", rate=model.config.sampling_rate, data=output)
    return f"audio-clips/{node_id}.wav"