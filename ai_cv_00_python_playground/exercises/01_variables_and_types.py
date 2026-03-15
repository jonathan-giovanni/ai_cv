# 01_variables_and_types.py

# This file introduces the most common Python data types.
# Focus:
# - variables
# - primitive-like values
# - tuples
# - lists
# - dictionaries
# - None
# - type hints

from typing import Optional

def main() -> None:
    # Basic scalar variables
    project_name: str = "ai_cv"
    module_number: int = 0
    confidence: float = 0.95
    is_active: bool = True

    print("Project Name:", project_name)
    print("Module Number:", module_number)
    print("Confidence:", confidence)
    print("Is Active:", is_active)
    print()

    # Optional variable - can be a value or None
    label: Optional[str] = None  # This variable can be a string or None - null in other languages
    print("Label:", label)
    print()

    # Tuples - immutable ordered collections
    image_shape: tuple[int, int, int] = (224, 224, 3)  # height, width, channels
    height, width, channels = image_shape  # Unpacking a tuple

    print("Image Shape:", image_shape)
    print(f"Height: {height}, Width: {width}, Channels: {channels}")
    print()

    # Lists - mutable ordered collections
    scores = [0.9, 0.85, 0.8]
    print("Scores:", scores)
    scores.append(0.75)  # Adding a new score to the list
    print("Updated Scores:", scores)
    print()

    # Dictionaries - mutable key-value pairs
    image_info = {
        "filename": "image1.jpg",
        "shape": (224, 224, 3),
        "label": None
    }
    print("Image Info:", image_info)
    print()

    # Python variables point to objects
    a = 10
    b = a  # b points to the same object as a
    a = 20  # a now points to a new object, b still points to the original object
    print(f"a: {a}, b: {b}")  # a: 20, b: 10
    print()

    # Mutable behavior of lists
    values = [1, 2, 3]
    alias = values  # alias points to the same list object
    values.append(4)  # Modifying the list through values also modifies alias because they reference the same list object
    print("Values:", values)
    print("Alias:", alias)
    same_list = values is alias  # True, both variables point to the same list object
    print("same list:", same_list)
    print()

    # Using copy to create an independent list (changes to the copy don't affect the original)
    values_copy = values.copy()
    values_copy.append(5)
    print("Values:", values)  # Original list remains unchanged
    print("Values Copy:", values_copy)  # New list with the added value
    same_list_copy = values is values_copy  # False, they are different objects
    print("same list copy:", same_list_copy)

if __name__ == "__main__":
    main()