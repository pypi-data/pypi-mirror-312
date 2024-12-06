import requests
from bs4 import BeautifulSoup
from loguru import logger

from fetchrunner.formatting import (
    format_date,
    format_distance,
    format_location,
    format_time_string,
)
from fetchrunner.utils import timing_decorator


class RaceFetcher:
    """Class to fetch race information and results from Kikourou website."""

    def __init__(self, base_url):
        self.base_url = base_url

    @staticmethod
    def fetch_html(url):
        """Fetch HTML content from a given URL."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logger.error(f"Failed to retrieve data from {url}: {response.status_code}")
            return None

    def get_race_information(self, url):
        """Parse race information from a given URL."""
        html_content = self.fetch_html(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            target_section = soup.find(class_="deuxcol50")

            if target_section:
                return self._parse_race_info(target_section)
            else:
                logger.error("Target section with class 'deuxcol50' not found.")
        return {}

    def _parse_race_info(self, section):
        """Extract race information from the section."""
        for br in section.find_all('br'):
            br.replace_with('__BR__')

        section_text = section.get_text(strip=True, separator=' ')
        text_list = section_text.split('__BR__')

        info_dict = {}
        for item in text_list:
            if ':' in item:
                key, value = item.split(':', 1)
                key = key.strip()
                value = " ".join(value.strip().split())
                if key == "Distance":
                    value = format_distance(value)
                elif key == "Lieu":
                    value = format_location(value)
                info_dict[key] = value

        return info_dict

    @timing_decorator
    def get_race_results(self, url):
        """Extract race results from the results page."""
        results = {"metadata": {}, "races": []}
        html_content = self.fetch_html(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Fetch all <tr> elements from the table with id 'tableresultats'
            table = soup.find('table', id='tableresultats')
            all_rows = table.find_all('tr') if table else []

            # Iterate over all races and extract the data
            for row in all_rows:
                result_data = self._extract_result_data(row)
                if result_data:
                    results["races"].append(result_data)

        return results

    def fetch(self, url):
        race_results, inference_time = self.get_race_results(url)
        race_results = self.add_metadata(race_results, url, inference_time)
        return race_results

    def add_metadata(self, results, url, inference_time):
        """Add metadata to the results dictionary."""
        name, surname = url.split("/")[-1][:-5].split("+")
        n_races = len(results["races"])
        metadata = {
            "name": name.capitalize(),
            "surname": surname.capitalize(),
            "n_races": n_races,
            "inference_time": inference_time
        }
        results["metadata"] = metadata
        return results

    def _extract_result_data(self, row):
        """Extract data from a single result row."""
        elements = row.find_all('td')

        # Ensure there are enough <td> elements to avoid IndexError
        if len(elements) >= 5:
            date = format_date(elements[0].text.strip())
            course_element = elements[1].find('a')
            course = course_element.text.strip() if course_element else "No course link"
            course_href = course_element['href'] if course_element and 'href' in course_element.attrs else "No href"
            time = format_time_string(elements[2].text.strip())
            name = elements[3].text.strip()
            # club = elements[4].text.strip()

            # Construct the new URL for race information
            new_url = f"{self.base_url}{course_href}"

            # Get race information from the constructed URL
            race_info = self.get_race_information(new_url)

            # Clean up race_info by removing unwanted keys
            for key in ["Temps limite", "Heure départ", "Sport", "Date"]:
                race_info.pop(key, None)

            # Combine results with race information
            return {
                "Date": date,
                "Course": course,
                "Time": time,
                "Name": name,
                **race_info  # Unpack additional race info into the dictionary
            }

        return None
