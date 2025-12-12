import torch
import re
from transformers import TextStreamer

from llm.model import ModelLoader
from llm.prompts import create_prompt, create_fast_prompt
from pdf.extractor import PDFExtractor
from typing import List

import logging

from utils.progressBar import ProgressBar


class Summarizer:

    def __init__(self, loader: ModelLoader, pdf_extractor: PDFExtractor):
        self.model, self.tokenizer = loader.load()
        self.extractor = pdf_extractor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return False

    def divide_chunks(self, text: str, chunk_size=400, overlap=1) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        chunks = []
        current_chunk = []
        current_len = 0

        for sentence in sentences:
            sentence_len = len(sentence.split())

            if current_len + sentence_len > chunk_size:
                chunks.append(" ".join(current_chunk))

                if overlap > 0:
                    current_chunk = current_chunk[-overlap:]
                    current_len = sum(len(s.split()) for s in current_chunk)
                else:
                    current_chunk = []
                    current_len = 0

            current_chunk.append(sentence)
            current_len += sentence_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def fast_summarize(self, text_prompt: str, max_tokens=1000, stream: bool = False) -> str:
        messages = [
            {"role": "user", "content": [{"type": "text", "text": text_prompt}]}
        ]

        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        input_len = inputs["input_ids"].shape[-1]

        info = {
            **inputs,
            "max_new_tokens": max_tokens,
            "do_sample": False,
            "use_cache": True,
            "pad_token_id": self.tokenizer.pad_token_id,
        }

        if not stream:
            with torch.inference_mode():
                output = self.model.generate(**info)
        else:
            streamer = TextStreamer(self.tokenizer, skip_prompt=True)
            info["streamer"] = streamer

            with torch.inference_mode():
                output = self.model.generate(**info)

        generated = output[0][input_len:]
        return self.tokenizer.decode(generated, skip_special_tokens=True)

    def process_chunks(self, chunks: List[str], batch_size: int = None) -> List[str]:
        partial_summaries = []

        total = len(chunks)
        bar = ProgressBar(total, prefix="Progresso")

        if batch_size is None:
            for idx, chunk in enumerate(chunks):
                prompt = create_fast_prompt(chunk)
                summary = self.fast_summarize(prompt)
                partial_summaries.append(summary)

                bar.update()

                if (idx + 1) % 5 == 0 and torch.cuda.is_available():
                    torch.cuda.empty_cache()
        else:
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]

                for chunk in batch_chunks:
                    prompt = create_fast_prompt(chunk)
                    summary = self.fast_summarize(prompt)
                    partial_summaries.append(summary)

                    bar.update()

                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

        bar.finish()
        return partial_summaries

    def generate_final_summary(self, partial_summaries: List[str]) -> str:
        compiled = " ".join(partial_summaries)
        final_prompt = create_prompt(compiled)
        return self.fast_summarize(final_prompt, stream=True)

    def summarize_pdf(self, long_text: str) -> str:
        chunks = self.divide_chunks(long_text)
        logging.info(f"Texto dividido em {len(chunks)} chunks.\n")

        partial_summaries = self.process_chunks(chunks)
        return self.generate_final_summary(partial_summaries)

    def summarize_batched_pdfs(self, long_text: str) -> str:
        chunks = self.divide_chunks(long_text)
        logging.info(f"Texto dividido em {len(chunks)} chunks.\n")

        batch_size = 2 if torch.cuda.is_available() else 1
        partial_summaries = self.process_chunks(chunks, batch_size=batch_size)
        return self.generate_final_summary(partial_summaries)