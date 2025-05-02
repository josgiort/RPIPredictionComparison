from pathlib import Path
from pdf2image import convert_from_path

Path("png_figures").mkdir(exist_ok=True)

for pdf_file in Path("Plots").glob("*.pdf"):
    images = convert_from_path(str(pdf_file), dpi=150)
    images[0].save(f"png_figures/{pdf_file.stem}.png", "PNG")
