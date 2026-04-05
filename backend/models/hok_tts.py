from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import numpy as np
import os

class HokTTS:
    def __init__(self):
        self.model = VitsModel.from_pretrained("facebook/mms-tts-nan")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-nan")
        self.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "audio-clips"
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_tts(self, node_id, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs).waveform
        output = output.detach().cpu().numpy().squeeze()
        output = np.clip(output, -1, 1)
        output = (output * 32767).astype(np.int16)
        wav_path = os.path.join(self.output_dir, f"{node_id}.wav")
        scipy.io.wavfile.write(
            wav_path, rate=self.model.config.sampling_rate, data=output
        )
        return f"audio-clips/{node_id}.wav"