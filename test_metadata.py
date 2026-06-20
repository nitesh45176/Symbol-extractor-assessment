from utils.metadata import (
    get_all_symbols,
    get_symbol,
    update_properties
)


print("All Symbols:")
print(get_all_symbols())


print("\nSingle Symbol:")
print(get_symbol(1))


print("\nUpdating Symbol 1")

updated = update_properties(
    1,
    {
        "color": "red",
        "rotation": 45,
        "tag": "Vehicle"
    }
)

print(updated)