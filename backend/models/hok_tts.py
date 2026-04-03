from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import numpy as np

class HokTTS:
    def __init__(self):
        self.model = VitsModel.from_pretrained("facebook/mms-tts-nan")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-nan")
        self.output_dir = "audio-clips"

    def generate_tts(self, node_id, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs).waveform
        output = output.detach().cpu().numpy().squeeze()
        output = np.clip(output, -1, 1)
        output = (output * 32767).astype(np.int16)

        scipy.io.wavfile.write(f"{self.output_dir}/{node_id}.wav", rate=self.model.config.sampling_rate, data=output)
        return f"audio-clips/{node_id}.wav"