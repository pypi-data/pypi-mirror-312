from pprint import pprint

from fetchrunner.config import BASE_URL
from fetchrunner.fetcher import RaceFetcher
from fetchrunner.io import display_app_name, save_results_to_file
from fetchrunner.utils import construct_results_url, parse_arguments, validate_name


def main():
    """Main function to fetch and display race results."""
    # Display the application name with ASCI art
    display_app_name()

    # Parse command-line arguments
    args = parse_arguments()

    # Validate the runner's name format
    validate_name(args.name)

    # Construct the URL for the runner's results on Kikourou
    results_url = construct_results_url(args.name)

    # Initialize the RaceFetcher class
    race_fetcher = RaceFetcher(BASE_URL)

    # Get race results and combine with their corresponding information
    race_results = race_fetcher.fetch(results_url)

    # Save results to JSON file if specified else print results
    if args.save:
        save_results_to_file(race_results, args.save)
    else:
        pprint(race_results)


if __name__ == "__main__":
    main()
