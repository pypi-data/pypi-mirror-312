import argparse
from typing_test.typing_test import typing_test

def main():
    # Call the typing_test function with default paths for config.json and sentences
    typing_test(
        config_path="typing_test/config.json",  # Default path for config.json
        sentences_file="typing_test/input_sentences.txt",  # Default path for sentences
    )

if __name__ == "__main__":
    main()