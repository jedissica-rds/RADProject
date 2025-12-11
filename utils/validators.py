from pathlib import Path


def validate_file(file: Path) -> bool:
    if file.suffix.lower() != '.pdf':
        print("Aviso: O arquivo não possui extensão .pdf")
        print("Uso: suporte apenas para arquivos pdf")
        return False
    return True