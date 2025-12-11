from pathlib import Path
from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from llm.model import ModelLoader
from llm.prompts import create_prompt, create_fast_prompt
from pdf.extractor import PDFExtractor


class Summarizer:

    def __init__(self, loader: ModelLoader, pdf_extractor: PDFExtractor):
        self.model, self.processor = loader.load()
        self.extractor = pdf_extractor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return False

    def divide_chunks(self, text: str, chunk_size=600, overlap=50) -> List[str]:
        words = text.split()
        chunks = []
        i = 0

        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - overlap

        return [c for c in chunks if c.strip()]

    def fast_summarize(self, text_prompt: str, max_tokens=100) -> str:
        messages = [
            {"role": "user", "content": [{"type": "text", "text": text_prompt}]}
        ]

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        input_len = inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                num_beams=1,
                use_cache=True,
            )

        generated = output[0][input_len:]
        return self.processor.decode(generated, skip_special_tokens=True)

    def process_chunks(self, chunks: List[str], batch_size: int = None) -> List[str]:
        partial_summaries = []

        if batch_size is None:
            for idx, chunk in enumerate(chunks):
                print(f"{idx + 1}/{len(chunks)}...", end=" ")
                prompt = create_fast_prompt(chunk)
                summary = self.fast_summarize(prompt, max_tokens=80)
                partial_summaries.append(summary)
                print("✔")
        else:
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                current_batch = i // batch_size + 1
                total_batch = (len(chunks) - 1) // batch_size + 1

                print(f"Batch {current_batch}/{total_batch}...", end=" ")

                for chunk in batch_chunks:
                    prompt = create_fast_prompt(chunk)
                    summary = self.fast_summarize(prompt, max_tokens=150)
                    partial_summaries.append(summary)

                print("✔")

        return partial_summaries

    def generate_final_summary(self, partial_summaries: List[str]) -> str:
        compiled = " ".join(partial_summaries)
        final_prompt = create_prompt(compiled)
        return self.fast_summarize(final_prompt, max_tokens=800)

    def summarize_pdf(self, long_text: str) -> str:
        chunks = self.divide_chunks(long_text, chunk_size=600, overlap=50)
        print(f"Texto dividido em {len(chunks)} chunks.\n")

        partial_summaries = self.process_chunks(chunks)
        return self.generate_final_summary(partial_summaries)

    def summarize_batched_pdfs(self, long_text: str) -> str:
        chunks = self.divide_chunks(long_text, chunk_size=600, overlap=50)
        print(f"Texto dividido em {len(chunks)} chunks.\n")

        batch_size = 4 if torch.cuda.is_available() else 2
        partial_summaries = self.process_chunks(chunks, batch_size=batch_size)
        return self.generate_final_summary(partial_summaries)