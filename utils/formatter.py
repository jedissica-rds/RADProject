from typing import List


# TODO: CHECAR FORMA  MAIS MODULARIZADA DE REALIZAR ISSO

def format_pdf_report(report: dict) -> str:
    output: List = [
        "\n",
        "Análise do PDF",
        "=" * 50,
        f"Número de páginas: {report.get('page_count', 0)}",
        f"Total de palavras: {report.get('word_count', 0)}",
        f"Tamanho do vocabulário: {report.get('vocabulary_size', 0)}",
        f"Top 10 palavras: {format_top_ten_words(report.get('top_words'))}",
        "\n"
    ]
    return "\n".join(output)


def format_top_ten_words(top_words: List):
    display: str = ""
    count = 1

    for word, frequency in top_words:
        display += f"\n{count}. {word} - {frequency}"
        count += 1

    return display


def exhibit_header():
    print("\n" + "=" * 70)
    print("RAD: Resumidor de Arquivos e Documentos!")
    print("=" * 70)
    print()


def exhibit_section(title: str):
    print("\n" + "-" * 70)
    print(f"📌 {title}")
    print("-" * 70)

def get_mode() -> str:
    print("\nModo de processamento:")
    print("  1. Normal (lento, porém bom resumo!)")
    print("  2. Batch (rápido, porém menos coerente!)")

    modo = input("Escolha (1 ou 2, padrão=1): ").strip()
    return modo if modo in ['1', '2'] else '1'
