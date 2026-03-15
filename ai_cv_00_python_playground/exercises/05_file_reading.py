# 05_file_reading.py

# This file introduces:
# - pathlib.Path
# - reading text files
# - writing text files
# - checking if a file exists
# - simple file summary

from pathlib import Path

def read_txt_file(file_path: Path) -> str:
    """Read the contents of a text file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    return file_path.read_text(encoding="utf-8")

def summarize_text(text: str) -> dict[str, int]:
    """Summarize the text by counting lines, words, and characters."""
    lines = text.splitlines()
    words = text.split()
    characters = len(text)
    return {
        "lines": len(lines),
        "words": len(words),
        "characters": characters
    }

# separate properties by semicolons and store in a dictionary
def parse_properties(text: str) -> dict[str, str]:
    """Parse properties from a text string where each line is in the format 'key: value'."""
    properties = {}
    lines = text.splitlines()
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)  # Split only on the first colon
            properties[key.strip()] = value.strip()  # Remove extra whitespace
    return properties

def main() -> None:
    file_path = Path("../samples/samples.txt")
    # Read the text file
    text = read_txt_file(file_path)
    print("File Contents:")
    print(text)
    print()

    # Summarize the text
    summary = summarize_text(text)
    print("Text Summary:")
    print(f"Lines: {summary['lines']}")
    print(f"Words: {summary['words']}")
    print(f"Characters: {summary['characters']}")
    print()

    # Parse properties from the text
    properties = parse_properties(text)
    print("Parsed Properties:")
    for key, value in properties.items():
        print(f"{key}: {value}")
    print()


if __name__ == "__main__":
    main()
