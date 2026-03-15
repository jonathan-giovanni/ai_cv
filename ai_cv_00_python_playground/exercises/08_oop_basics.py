# 08_oop_basics.py

# This file introduces:
# - classes
# - constructors
# - instance methods
# - dataclass
# - inheritance
# - a simple async example

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class ImageSample:
    """A simple class to represent an image sample."""
    sample_id: int
    file_path: Path
    label: Optional[str] = None

    def is_labeled(self) -> bool:
        """Check if the sample has a label."""
        return self.label is not None

class Processor:
    def process(self, sample: ImageSample) -> ImageSample:
        return sample

class DefaultLabelProcessor(Processor):
    def __init__(self, default_label: str):
        self.default_label = default_label

    def process(self, sample: ImageSample) -> ImageSample:
        if not sample.is_labeled():
            sample.label = self.default_label
        return sample

async def load_metadata(sample: ImageSample) -> dict[str, str]:
    """Simulate loading metadata asynchronously."""
    await asyncio.sleep(1)  # Simulate a delay
    return {
        "sample_id": str(sample.sample_id),
        "file_path": str(sample.file_path),
        "label": sample.label or "unlabeled"
    }

def main() -> None:
    sample = ImageSample(sample_id=1, file_path=Path("../samples/sample1.jpg"))
    print("Before processing:", sample)

    processor = DefaultLabelProcessor(default_label="unknown")
    processed_sample = processor.process(sample)
    print("After processing:", processed_sample)

    # Load metadata asynchronously
    metadata = asyncio.run(load_metadata(processed_sample))
    print("Loaded Metadata:", metadata)

if __name__ == "__main__":
    main()