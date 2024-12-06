
import json

import pyfiglet
from colorama import Fore, Style
from loguru import logger


def save_results_to_file(results, filename):
    """Save race results to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    logger.info(f"Results saved to {filename}")


def display_app_name():
    # Generate and display ASCII art for the CLI name with color
    ascii_art = pyfiglet.figlet_format("FetchRunner", font="slant")

    # Determine the width of the ASCII art for framing
    art_lines = ascii_art.splitlines()
    max_length = max(len(line) for line in art_lines)

    # Print top border with color
    print()
    print(Fore.GREEN + "=" * (max_length + 4))  # Add padding for borders

    # Print ASCII art with side borders in green and reset font color for the art
    for line in art_lines:
        print(Fore.GREEN + "= " + line + Fore.GREEN + " =")

    # Print bottom border with color
    print(Fore.GREEN + "=" * (max_length + 4) + Style.RESET_ALL)
    print()
