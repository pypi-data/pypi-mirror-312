import time
import random
import getpass
import json
from utils import (
    clear_screen,
    calculate_wpm,
    calculate_accuracy,
    colorize_typed,
    display_session_bar_chart,
)

def load_config():
    """Load configuration from the config.json file."""
    try:
        with open("config.json", "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Configuration file 'config.json' not found. Using default values.")
        return {"tests": 3, "sentences_per_test": 2, "blind_mode": False}
    except json.JSONDecodeError:
        print("Error parsing 'config.json'. Please ensure it is valid JSON.")
        exit(1)

def load_sentences(file_path="input_sentences.txt"):
    """Load sentences from a text file."""
    try:
        with open(file_path, "r") as file:
            sentences = [line.strip() for line in file if line.strip()]
            if not sentences:
                raise ValueError("The sentences file is empty.")
            return sentences
    except FileNotFoundError:
        print(f"Sentences file '{file_path}' not found.")
        exit(1)
    except ValueError as e:
        print(e)
        exit(1)

def typing_test():
    """Main typing test function."""
    config = load_config()  # Load configuration
    sentences = load_sentences()  # Load sentences from file

    num_tests = config.get("tests", 3)
    sentences_per_test = config.get("sentences_per_test", 2)
    blind_mode = config.get("blind_mode", False)

    clear_screen()
    print("Typing Speed Test")
    print("-----------------")
    print(f"Number of tests: {num_tests}")
    print(f"Sentences per test: {sentences_per_test}")
    print(f"Blind mode: {'Enabled' if blind_mode else 'Disabled'}")

    session_results = []
    session_accuracies = []
    tests_completed = 0  # Track the number of tests with valid input

    for test_number in range(1, num_tests + 1):
        clear_screen()
        print(f"Typing Speed Test - Test {test_number}/{num_tests}")
        print("-------------------------------")

        # Select random sentences
        selected_sentences = random.sample(sentences, sentences_per_test)
        start_time = time.time()  # Start the timer
        typed_sentences = []
        total_words = 0

        # Display sentences one by one
        valid_input = False  # Track if the user typed valid input
        for i, sentence in enumerate(selected_sentences, start=1):
            clear_screen()
            print(f"Sentence {i}/{sentences_per_test}:")
            print(f"\033[1;33m{sentence}\033[0m")  # Highlight the sentence in yellow

            # Blind mode hides user input
            if blind_mode:
                print("\nType the sentence (input will be hidden):")
                user_input = getpass.getpass("")  # Hidden input
            else:
                user_input = input("\nType the sentence: ").strip()

            # Check if user actually typed something
            if user_input:
                valid_input = True
                typed_sentences.append(user_input)
                total_words += len(sentence.split())
            else:
                typed_sentences.append("")  # To maintain alignment for skipped sentences

        end_time = time.time()  # End the timer

        # Skip results if no valid input was provided
        if not valid_input:
            print("\nNo valid input detected for this test. Test skipped.")
            time.sleep(2)
            continue

        # Calculate results
        wpm = calculate_wpm(start_time, end_time, total_words)
        accuracy = calculate_accuracy(selected_sentences, typed_sentences)
        elapsed_time = round(end_time - start_time, 2)

        # Store the WPM and accuracy for valid tests only
        session_results.append(wpm)
        session_accuracies.append(accuracy)
        tests_completed += 1

        # Display individual test results
        clear_screen()
        print("\nResults")
        print("-------")
        print(f"Test {test_number} - Time: {elapsed_time}s, WPM: {wpm}, Accuracy: {accuracy}%")
        print("\nSentence-by-Sentence Details:")
        for original, typed in zip(selected_sentences, typed_sentences):
            colored_typed = colorize_typed(original, typed)
            max_length = max(len(original), len(typed))
            print(f"{original.ljust(max_length)}")  # Display original sentence
            print(f"{colored_typed.ljust(max_length)}")  # Display typed sentence
            print()

        # Wait briefly before the next test, unless it's the last test
        if test_number < num_tests:
            time.sleep(2)

    # Handle case where no tests are completed
    if tests_completed == 0:
        clear_screen()
        print("\nSession Results")
        print("----------------")
        print("No tests were completed. Final result is FAIL.")
        return  # Exit without displaying the bar chart

    # Calculate final results
    average_accuracy = sum(session_accuracies) / len(session_accuracies) if session_accuracies else 0
    average_wpm = sum(session_results) / len(session_results) if session_results else 0
    final_result = "PASS" if average_accuracy >= 70 else "FAIL"

    # Display Final Results with Proper Alignment
    clear_screen()
    print("\nFinal Results")
    print("-------------")
    print(f"{'Average Accuracy:'.ljust(25)} {average_accuracy:.2f}%")
    print(f"{'Average Typing Speed:'.ljust(25)} {average_wpm:.2f} WPM")
    print(f"{'Result:'.ljust(25)} \033[1;32m{final_result}\033[0m" if final_result == "PASS" else f"{'Result:'.ljust(25)} \033[1;31m{final_result}\033[0m")
    print()

    # Display bar chart only if at least one test was completed
    display_session_bar_chart(session_results)

# if __name__ == "__main__":
#     typing_test()