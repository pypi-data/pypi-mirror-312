import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_wpm(start_time, end_time, total_words):
    """Calculate words per minute (WPM)."""
    if total_words == 0:
        return 0
    elapsed_time = end_time - start_time  # Time in seconds
    wpm = (total_words / elapsed_time) * 60  # Convert to words per minute
    return round(wpm, 2)

def calculate_accuracy(original_sentences, typed_sentences):
    """Calculate typing accuracy as a percentage."""
    total_correct = 0
    total_words = 0

    for original, typed in zip(original_sentences, typed_sentences):
        original_words = original.split()
        typed_words = typed.split()
        total_words += len(original_words)
        total_correct += sum(1 for o, t in zip(original_words, typed_words) if o == t)

    accuracy = (total_correct / total_words) * 100
    return round(accuracy, 2)

def colorize_typed(original, typed):
    """Colorize the typed words based on correctness."""
    original_words = original.split()
    typed_words = typed.split()
    colored_output = []

    for o, t in zip(original_words, typed_words):
        if o == t:
            colored_output.append(f"\033[1;32m{t}\033[0m")  # Green for correct
        else:
            colored_output.append(f"\033[1;31m{t}\033[0m")  # Red for incorrect

    # Add remaining words from the typed sentence (if any)
    if len(typed_words) > len(original_words):
        for t in typed_words[len(original_words):]:
            colored_output.append(f"\033[1;31m{t}\033[0m")  # Extra words in red

    return " ".join(colored_output)

def display_session_bar_chart(results):
    """Display a bar chart showing all test results in the session."""
    print("\nSession Progress Bar Chart")
    bar_width = 8  # Adjust bar width to align bars over labels
    chart_width = len(results) * bar_width + 10  # Total width of the chart
    print("-" * chart_width)  # Top border spanning the chart

    max_wpm = max(results + [65])  # Ensure at least 65 for proper scaling
    max_height = int((max_wpm // 5 + 1) * 5)  # Round up to nearest multiple of 5

    for row in range(max_height, 0, -5):
        # Add row labels and spacing
        line = f"{str(row).rjust(4)} |"

        # Add bars for each result
        for wpm in results:
            if wpm >= row:
                if wpm < 45:
                    color = "\033[1;31m"  # Red for below average
                elif 45 <= wpm < 65:
                    color = "\033[1;33m"  # Yellow for average
                else:
                    color = "\033[1;32m"  # Green for fast
                line += f"   {color}#\033[0m   "
            else:
                line += "       "  # Empty space for unused bar positions

        # Add thresholds for Fast and Average as continuous lines
        if row == 45:
            print("\033[1;34m" + "-" * chart_width + "\033[0m (Average)")  # Blue line
        elif row == 65:
            print("\033[1;36m" + "-" * chart_width + "\033[0m (Fast)")  # Cyan line

        print(line)

    # Bottom horizontal line
    print("-" * chart_width)

    # Add WPM and Test labels aligned on the same line
    wpm_label = "  WPM".ljust(1)  # Align WPM label with vertical numbers
    test_labels = "".join([f"T{i+1}".center(bar_width) for i in range(len(results))])
    print(wpm_label + " " + test_labels)  # Shift test labels one space left