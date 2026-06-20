import fitz  # PyMuPDF
import os


def pdf_to_images(pdf_path):
    """
    Convert all pages of a PDF into high-resolution PNG images.

    Args:
        pdf_path (str): Path to PDF file

    Returns:
        list: Paths of generated page images
    """

    pages = []

    # Open PDF
    document = fitz.open(pdf_path)

    # Loop through each page
    for page_number in range(len(document)):

        page = document[page_number]

        # Increase resolution
        zoom = 3
        matrix = fitz.Matrix(zoom, zoom)

        # Render page into a pixel image
        pix = page.get_pixmap(matrix=matrix)

        # Save image
        output_path = f"pages/page_{page_number + 1}.png"

        pix.save(output_path)

        pages.append(output_path)

    document.close()

    return pages