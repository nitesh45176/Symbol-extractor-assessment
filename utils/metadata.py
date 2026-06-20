import json
import os


METADATA_FILE = "metadata/symbols.json"


def create_metadata(svg_files):
    """
    Create JSON metadata for all SVG symbols.
    """

    symbols = []

    for index, svg_path in enumerate(svg_files, start=1):

        name = os.path.splitext(
            os.path.basename(svg_path)
        )[0]


        symbol = {
            "id": index,
            "name": name,
            "svg_file": svg_path,

            "properties": {
                "color": "black",
                "width": 100,
                "height": 100,
                "rotation": 0,
                "description": ""
            }
        }


        symbols.append(symbol)


    with open(
        METADATA_FILE,
        "w"
    ) as file:
        json.dump(
            symbols,
            file,
            indent=4
        )


    return symbols



def get_all_symbols():
    """
    Read all symbols from JSON.
    """

    if not os.path.exists(METADATA_FILE):
        return []


    with open(METADATA_FILE, "r") as file:
        return json.load(file)



def get_symbol(symbol_id):
    """
    Get one symbol by ID.
    """

    symbols = get_all_symbols()


    for symbol in symbols:

        if symbol["id"] == symbol_id:
            return symbol


    return None



def update_properties(symbol_id, new_properties):
    """
    Update custom properties.
    """

    symbols = get_all_symbols()


    for symbol in symbols:

        if symbol["id"] == symbol_id:

            symbol["properties"].update(
                new_properties
            )

            break


    with open(
        METADATA_FILE,
        "w"
    ) as file:
        json.dump(
            symbols,
            file,
            indent=4
        )


    return get_symbol(symbol_id)