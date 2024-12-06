import argparse
from typing_test.typing_test import typing_test

def main():
    parser = argparse.ArgumentParser(description="Typing Test CLI")
    parser.add_argument(
        "--config", type=str, help="Path to the configuration JSON file", default=None
    )
    parser.add_argument(
        "--sentences", type=str, help="Path to the input sentences file", default=None
    )
    args = parser.parse_args()

    # Pass the arguments to the main typing test
    typing_test(config_path=args.config, sentences_file=args.sentences)

if __name__ == "__main__":
    main()