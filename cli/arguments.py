from pathlib import Path
import argparse

DEFAULT_TEST_FILE = "./utils/files/teste_pdf.pdf"

def receive_file():
    parser = argparse.ArgumentParser(
        description="RAD: Resumidor de Arquivos e Documentos"
    )

    parser.add_argument("file", type=str, nargs="?", help="Caminho para o PDF.")

    parser.add_argument("--no-metrics", action="store_true",
                        help="Não gerar métricas do PDF.")

    parser.add_argument("--no-summary", action="store_true",
                        help="Não gerar resumo do PDF.")

    parser.add_argument("--no-ui", action="store_true",
                        help="Não exibir interface interativa / Sem input().")

    parser.add_argument("--default-file", action="store_true",
                        help="Usar arquivo de teste caso nenhum arquivo seja fornecido.")

    args = parser.parse_args()

    if args.no_ui:
        if args.file:
            file_path = Path(args.file)
        elif args.default_file:
            file_path = Path(DEFAULT_TEST_FILE)
        else:
            file_path = Path(DEFAULT_TEST_FILE)
        return args, file_path

    if args.file is None:
        file_input = input("\nDigite o caminho do arquivo PDF: ").strip()
        file_path = Path(file_input)
    else:
        file_path = Path(args.file)

    if args.file is None and args.default_file:
        file_path = Path(DEFAULT_TEST_FILE)

    return args, file_path
