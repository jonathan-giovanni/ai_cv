# 06_json_and_csv.py

# This file introduces:
# - JSON reading and writing
# - CSV reading and writing
# - simple structured data handling

import csv
import json
from pathlib import Path

def read_json_file(file_path: Path) -> list[dict[str, str]]:
    """Read a JSON file and return its contents."""
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    return json.loads(file_path.read_text(encoding="utf-8"))

def pretty_print_json(data: list[dict[str, str]]) -> None:
    """Pretty print JSON data."""
    print(json.dumps(data, indent=4))

def read_csv_file(file_path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return its contents as a list of dictionaries."""
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with file_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def main() -> None:
    # Read JSON file
    json_file_path = Path("../samples/samples.json")
    json_data = read_json_file(json_file_path)
    print("JSON Data:")
    print(json_data)
    print("Pretty Printed JSON Data: ")
    pretty_print_json(json_data)
    print()

    # Read CSV file
    csv_file_path = Path("../samples/samples.csv")
    csv_data = read_csv_file(csv_file_path)
    print("CSV Data:")
    for row in csv_data:
        print(row)
    print()

if __name__ == "__main__":
    main()