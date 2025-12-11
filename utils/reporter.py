from datetime import datetime
from pathlib import Path


def create_markdown_report(report: dict, summary: str, file_path: Path, images_count: int) -> str:

    markdown = f"""# Relatório de Análise de PDF

---

## Informações do Documento

**Arquivo:** `{file_path.name}`  
**Caminho:** `{file_path.absolute()}`  

---

##Estatísticas do Documento

| Métrica | Valor |
|---------|-------|
| **Número de páginas** | {report.get('page_count', 0)} |
| **Total de palavras** | {report.get('word_count', 0):,} |
| **Tamanho do vocabulário** | {report.get('vocabulary_size', 0):,} palavras únicas |
| **Tamanho do arquivo** | {report.get('file_size', 0):,} bytes ({report.get('file_size', 0) / 1024:.2f} KB) |
| **Imagens extraídas** | {images_count} |

---

##Top 10 Palavras Mais Frequentes

"""
    top_words = report.get('top_words', [])
    for idx, (word, freq) in enumerate(top_words, 1):
        markdown += f"{idx}. **{word}** - {freq} ocorrências\n"

    markdown += f"""
---

##Resumo

{summary}

---

*Relatório gerado automaticamente pelo RAD!*
"""

    return markdown


def save_report(content: str, base_name: str = "relatorio") -> None:
    print("\nDeseja salvar o relatório completo em Markdown?")
    salvar = input("(s/n, padrão=s): ").strip().lower()

    if salvar in ['s', 'sim', 'yes', 'y', '']:
        nome_arquivo = input(f"Nome do arquivo (padrão='{base_name}'): ").strip()
        if not nome_arquivo:
            nome_arquivo = base_name

        if not nome_arquivo.endswith('.md'):
            nome_arquivo += '.md'

        output_path = Path("./reports") / nome_arquivo

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Relatório salvo em: {output_path.absolute()}")
    else:
        print("Erro.")