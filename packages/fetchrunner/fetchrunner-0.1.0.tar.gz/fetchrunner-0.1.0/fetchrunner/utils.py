
import argparse
import time
import urllib.parse

from colorama import Fore

from fetchrunner.config import BASE_URL


def url_ready_string(input_string):
    """Use urllib's quote function to encode the string"""
    return urllib.parse.quote(input_string)


def is_valid_name(name):
    """Check if the name contains a comma."""
    return ', ' in name


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch race results from Kikourou.")
    parser.add_argument('--name', required=True, help='Name of the runner in the format "Surname, Firstname"')
    parser.add_argument('--save', help='Optional: Save results to a JSON file')
    return parser.parse_args()


def validate_name(name):
    """Validate the runner's name format."""
    if not is_valid_name(name):
        print(Fore.RED + "Error: Please enter a target name in the correct format!")
        print(Fore.YELLOW + "Use for example: fetchrunner --name 'Surname, Firstname'.")
        exit(1)


def construct_results_url(name):
    """Construct the results URL based on the runner's name."""
    surname, firstname = name.split(', ')
    name_slug = url_ready_string(firstname.lower())
    surname_slug = url_ready_string(surname.lower())
    return f"{BASE_URL}/resultats/{name_slug}+{surname_slug}.html"


def timing_decorator(func):
    """Decorator to measure execution time of a function."""
    def wrapper(self, *args, **kwargs):
        start_time = time.time()  # Start timing
        result = func(self, *args, **kwargs)  # Call the original function
        end_time = time.time()  # End timing

        # Calculate elapsed time in seconds
        elapsed_time = end_time - start_time

        # Format time
        formatted_time = f"{elapsed_time:.2f} s"  # Format to two decimal places

        return result, formatted_time  # Return both result and formatted inference time
    return wrapper
