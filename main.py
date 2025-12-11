from pathlib import Path
from cli.arguments import receive_file
from utils.formatter import format_pdf_report, exhibit_section, get_mode, exhibit_header
from utils.reporter import create_markdown_report, save_report
from utils.validators import validate_file
from llm.summarize import Summarizer
from llm.model import ModelLoader
from pdf.extractor import PDFExtractor
from pdf.images import extract_images


def main():
    exhibit_header()

    file_path: Path = receive_file()

    if not validate_file(file_path):
        return

    if not file_path.exists():
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return

    extractor = PDFExtractor(file_path)

    try:
        exhibit_section("MÉTRICAS")
        report = extractor.get_report()
        print(format_pdf_report(report))

        exhibit_section("EXTRAÇÃO DE IMAGENS")
        images_count = extract_images(file_path)

        exhibit_section("RESUMO")

        modo = get_mode()
        report['batch_mode'] = (modo == '2')

        print("\nCarregando modelo de linguagem...")
        loader = ModelLoader()

        with Summarizer(loader, extractor) as summarizer:
            text = extractor.get_text()

            print("📝 Gerando resumo...\n")

            if modo == '2':
                summary = summarizer.summarize_batched_pdfs(text)
            else:
                summary = summarizer.summarize_pdf(text)

        exhibit_section("RESUMO EXECUTIVO FINAL")
        print(summary)
        print()

    except FileNotFoundError as e:
        print(f"Erro: O arquivo não pôde ser aberto.")
        print(f"   Detalhes: {e}")
        return

    except KeyboardInterrupt:
        print("\n\nProcesso interrompido pelo usuário.")
        return

    except Exception as e:
        print(f"Erro inesperado durante o processamento: {e}")
        import traceback
        traceback.print_exc()
        return

    finally:
        extractor.close()

    try:
        exhibit_section("GERAÇÃO DE RELATÓRIO")

        markdown_report = create_markdown_report(
            report=report,
            summary=summary,
            file_path=file_path,
            images_count=images_count
        )

        base_name = f"relatorio_{file_path.stem}"
        save_report(markdown_report, base_name)

        print("\n" + "=" * 70)
        print("Processamento concluído com sucesso!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")
        print("   O processamento foi concluído, mas o relatório não foi salvo.")


if __name__ == "__main__":
    main()