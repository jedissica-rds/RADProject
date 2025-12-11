from typing import Tuple
from transformers import AutoProcessor, Gemma2ForCausalLM
import torch

class ModelLoader:
    def __init__(self, model_id: str = "google/gemma-2-2b-it"):
        self.model_id = model_id

    def load(self) -> Tuple[Gemma2ForCausalLM, AutoProcessor]:
        print(f"Carregando modelo...")

        model = Gemma2ForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True
        )
        model.eval()

        if torch.cuda.is_available():
            try:
                model = torch.compile(model, mode="reduce-overhead")
                print("Modelo compilado com torch.compile")
            except Exception as e:
                print(f"⚠ torch.compile não disponível: {e}")

        processor = AutoProcessor.from_pretrained(self.model_id)

        return model, processor