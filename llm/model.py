import logging
from typing import Tuple
from transformers import AutoTokenizer, Gemma2ForCausalLM
import torch


class ModelLoader:
    def __init__(self, model_id: str = "google/gemma-2-2b-it"):
        self.model_id = model_id

    def load(self) -> Tuple[Gemma2ForCausalLM, AutoTokenizer]:
        logging.info(f"carregando modelo: {self.model_id}")

        device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

        dtype = torch.bfloat16 if device == "mps" else (torch.float16 if device == "cuda" else torch.float32)

        model = Gemma2ForCausalLM.from_pretrained(
            self.model_id,
            device_map="balanced",
            dtype=dtype,
            low_cpu_mem_usage=True
        )
        model.eval()

        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        return model, tokenizer

