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

    args, file_path = receive_file()

    if not validate_file(file_path):
        return

    extractor = PDFExtractor(file_path)

    try:
        # MÉTRICAS
        if not args.no_metrics:
            exhibit_section("MÉTRICAS")
            report = extractor.get_report()
            print(format_pdf_report(report))
        else:
            report = {"skipped_metrics": True}

        # EXTRAÇÃO DE IMAGENS
        exhibit_section("EXTRAÇÃO DE IMAGENS")
        images_count = extract_images(file_path)

        # RESUMO
        summary = ""
        if not args.no_summary:
            exhibit_section("RESUMO")

            modo = get_mode() if not args.no_ui else "1"
            report["batch_mode"] = (modo == '2')

            print("\nCarregando modelo de linguagem...")
            loader = ModelLoader()

            with Summarizer(loader, extractor) as summarizer:
                text = extractor.get_text()

                print("Gerando resumo...\n")

                if modo == '2':
                    summary = summarizer.summarize_batched_pdfs(text)
                else:
                    summary = summarizer.summarize_pdf(text)

            exhibit_section("RESUMO EXECUTIVO FINAL")
            print(summary)
            print()
        else:
            summary = "**(Resumo não gerado — flag --no-summary)**"

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return

    finally:
        extractor.close()

    #RELATÓRIO
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


if __name__ == "__main__":
    main()