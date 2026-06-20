from fastapi import FastAPI, UploadFile, File, HTTPException
import os

from processors.pdf_processors import pdf_to_images
from processors.symbol_detector import extract_symbols
from processors.vectorizer import convert_all_to_svg

from utils.metadata import (
    create_metadata,
    get_all_symbols,
    get_symbol,
    update_properties
)


app = FastAPI(
    title="AI Symbol Extraction API",
    description="Extract symbols from PDF and convert them into editable SVG objects",
    version="1.0"
)


# Create required directories
folders = [
    "uploads",
    "pages",
    "symbols",
    "vectors",
    "metadata"
]


for folder in folders:
    os.makedirs(folder, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Symbol Extraction API is running"
    }


# 1. Upload PDF and process complete pipeline

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    # Save uploaded PDF
    pdf_path = f"uploads/{file.filename}"


    with open(pdf_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)


    # Step 1: PDF -> PNG pages
    pages = pdf_to_images(pdf_path)


    # Step 2: PNG pages -> Symbol PNGs
    symbols = extract_symbols(pages)


    # Step 3: Symbol PNG -> SVG
    svg_files = convert_all_to_svg(symbols)


    # Step 4: Create JSON metadata
    data = create_metadata(svg_files)


    return {
        "status": "success",
        "message": "PDF processed successfully",

        "results": {
            "pages_processed": len(pages),
            "symbols_found": len(symbols),
            "svg_created": len(svg_files)
        },

        "symbols": data
    }


# 2. Get all symbols

@app.get("/symbols")
def read_all_symbols():

    symbols = get_all_symbols()


    return {
        "count": len(symbols),
        "symbols": symbols
    }


# 3. Get a single symbol

@app.get("/symbols/{symbol_id}")
def read_symbol(symbol_id: int):

    symbol = get_symbol(symbol_id)


    if not symbol:
        raise HTTPException(
            status_code=404,
            detail="Symbol not found"
        )


    return symbol


# 4. Update properties

@app.put("/symbols/{symbol_id}")
def edit_symbol(
    symbol_id: int,
    properties: dict
):

    symbol = update_properties(
        symbol_id,
        properties
    )


    if not symbol:
        raise HTTPException(
            status_code=404,
            detail="Symbol not found"
        )


    return {
        "message": "Symbol updated successfully",
        "symbol": symbol
    }