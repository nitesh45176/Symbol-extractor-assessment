from processors.metadata_generator import generate_metadata
from processors.symbol_detector import extract_symbols
from processors.vectorizer import convert_all_to_svg


symbols = [
    "symbols/symbol_1.png",
    "symbols/symbol_2.png",
    "symbols/symbol_3.png"
]


result = convert_all_to_svg(symbols)


print(result)