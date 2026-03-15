# 04_collections_basics.py

# This file introduces:
# - lists
# - tuples
# - sets
# - dictionaries
# - list comprehensions
# - dictionary iteration

def main() -> None:
    # Lists
    filenames = ["image1.jpg", "image2.jpg", "image3.jpg" , "image4.jpg"]
    print("Filenames:", filenames)
    print("First filename:", filenames[0])  # Accessing the first element
    print("Last filename:", filenames[-1])  # Accessing the last element
    print()

    # Tuples
    image_shape = (224, 224, 3)  # height, width, channels
    print("Image Shape:", image_shape)
    height, width, channels = image_shape  # Unpacking a tuple
    print(f"Height: {height}, Width: {width}, Channels: {channels}")
    print()

    # Sets
    unique_labels = {"cat", "dog", "bird" , "cat" , "dog"} # Sets automatically remove duplicates
    print("Unique Labels:", unique_labels)
    print()

    # Dictionaries
    image_info = {
        "filename": "image1.jpg",
        "shape": (224, 224, 3),
        "label": "cat"
    }
    print("Image Info:", image_info)
    print("Filename from dictionary:", image_info["filename"])  # Accessing value by key
    for key, value in image_info.items():  # Iterating over dictionary items
        print(f"{key}: {value}")
    print()

    # List comprehensions
    scores = [0.9, 0.85, 0.8, 0.75]
    high_scores = [score for score in scores if score >= 0.85]  # Filtering high scores using a list comprehension
    print("High Scores:", high_scores)

    # Dictionary comprehension
    dataset_count = {"train": 1000, "validation": 200, "test": 300}
    dataset_percentage = {key: (count / sum(dataset_count.values())) * 100 for key, count in dataset_count.items()}  # Calculating percentage using a dictionary comprehension
    print("Dataset Percentage:", dataset_percentage)
    print()

if __name__ == "__main__":
    main()
