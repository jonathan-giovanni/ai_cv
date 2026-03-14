# 02_conditionals_and_loops.py
from typing import Tuple


# This file introduces:
# - if / elif / else
# - for loops
# - while loops
# - break / continue
# - enumerate
# - simple filtering

def classify_score(score: float) -> str:
    """Classify a score into categories."""
    if score >= 0.9:
        return "high"
    elif score >= 0.7:
        return "medium"
    elif score >= 0.5:
        return "low"
    else:
        return "reject"

def main() -> None:
    score= 0.85
    classification = classify_score(score)
    print(f"Score: {score}, Classification: {classification}")
    print()

    # Basic loop
    scores = [0.65, 0.85, 0.35,0.95, 0.65, 0.90]
    for score in scores:
        classification = classify_score(score)
        print(f"Score: {score}, Classification: {classification}")
    print()

    # Using enumerate to get index and value
    for index, score in enumerate(scores):
        classification = classify_score(score)
        print(f"Index: {index}, Score: {score}, Classification: {classification}")
    print()

    # Filtering scores using a loop
    high_scores = []
    for index,score in enumerate(scores):
        classification = classify_score(score)
        if classification == "high":
            high_scores.append((index,score,classification))
    print("High Scores:", high_scores)
    print()

    # Break and continue example
    for score in scores:
        classification = classify_score(score)
        if classification == "reject":
            print(f"Score: {score} is rejected, stopping evaluation.")
            break  # Stop the loop if we encounter a reject
        elif classification == "low":
            print(f"Score: {score} is low, skipping.")
            continue
        else:
            print(f"Score: {score} is {classification}.")
        print(f"Only scores above low are processed, current score: {score} classified as {classification}.")
    print()


    # While loop example
    target_classification = "high"
    index = 0
    result: Tuple[int, float, str] | None = None
    while index < len(scores) and result is None:
        score = scores[index]
        classification = classify_score(score)
        if classification == target_classification:
            print(f"Found a {target_classification} score: {score} at index {index}.")
            result = (index, score, classification)
        index += 1
    print(f"Finished searching for {target_classification} scores: result={result}")



if __name__ == "__main__":
    main()