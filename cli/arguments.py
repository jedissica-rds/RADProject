from pathlib import Path
import argparse

def receive_file():
    parser = argparse.ArgumentParser(
        description="RAD: Resumidor de Arquivos e Documentos"
    )
    parser.add_argument("file", type=str, nargs='?', help="Caminho para o PDF.")

    args = parser.parse_args()

    if args.file is None:
        file_input = input("\nDigite o caminho do arquivo PDF: ").strip()
        file_path = Path(file_input)
    else:
        file_path = Path(args.file)

    return file_path