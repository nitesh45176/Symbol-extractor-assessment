import cv2
import json
import os

from models.symbol import Symbol


def generate_metadata(symbol_paths):
    """
    Generate metadata for extracted symbols.
    """

    symbols = []

    for index, path in enumerate(symbol_paths, start=1):

        image = cv2.imread(path)

        height, width = image.shape[:2]

        symbol = Symbol(
            id=f"symbol_{index}",
            filename=path,
            width=width,
            height=height,
            area=width * height
        )

        symbols.append(symbol.__dict__)


    os.makedirs("metadata", exist_ok=True)


    with open(
        "metadata/symbols.json",
        "w"
    ) as file:

        json.dump(
            symbols,
            file,
            indent=4
        )


    print(
        f"Metadata generated for {len(symbols)} symbols"
    )


    return symbols