from pathlib import Path
import argparse


def receive_file():
    parser = argparse.ArgumentParser(
        description="RAD: Resumidor de Arquivos e Documentos"
    )
    parser.add_argument("file", type=str, help="Caminho para o PDF.")

    args = parser.parse_args()

    file_path = Path(args.file)
    return file_path
