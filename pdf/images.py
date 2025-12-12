from pymupdf import Document
from pathlib import Path
import pymupdf


def extract_images(file_path: Path):
    document = pymupdf.open(file_path)
    index = 1

    for page_index in range(len(document)):

        page = document.load_page(page_index)
        image_list = page.get_images(full=True)

        if len(image_list) > 0:

            destination: Path = create_pdf_directory(document)

            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]

                base_image = document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                image_name = f"img_{index}.{image_ext}"
                image_path = destination / image_name

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                index += 1

    if (index-1) > 0:
        print(f"{index-1} Imagens salvas!")
    else:
        print(f"Não há imagens no arquivo.")

    document.close()


def create_pdf_directory(document: Document):
    metadata: dict = document.metadata
    pdf_title: str = metadata.get("title") or "unknown"
    output_path: Path = Path("./images") / pdf_title
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path
