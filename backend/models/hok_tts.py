'''
from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import numpy as np
'''

class HokTTS:
    def __init__(self):
         print("[HokTTS] TTS model not loaded")

    def generate_tts(self, node_id, text):
        return ""