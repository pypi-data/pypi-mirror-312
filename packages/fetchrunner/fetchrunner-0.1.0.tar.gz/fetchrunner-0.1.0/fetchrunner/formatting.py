import re
from datetime import datetime


def format_time_string(time_str):
    """
    Format a time string into a standardized string format 'XXhXXmXXs'.

    Args:
    time_str (str): A string containing time in format like 2h30'5'' or 45'30''

    Returns:
    str: Formatted time string in 'XXhXXmXXs' format
    """
    if 'h' in time_str:
        # Case with hours
        hours_part, rest = time_str.split('h')
        hours = int(hours_part)
    else:
        # Case without hours
        hours = 0
        rest = time_str

    parts = rest.split("'")
    minutes = int(parts[0])
    seconds = int(parts[1].rstrip("'")) if len(parts) > 1 else 0

    # Format the time string
    formatted_time = ""
    if hours > 0:
        formatted_time += f"{hours:02d}h"
    if minutes > 0 or hours > 0:
        formatted_time += f"{minutes:02d}m"
    formatted_time += f"{seconds:02d}s"

    return formatted_time


def format_date(date_string):
    """
    Convert a date string from DD-MM-YYYY format to DD/MM/YYYY format.

    Args:
    date_string (str): A date string in the format DD-MM-YYYY

    Returns:
    str: The date string in DD/MM/YYYY format

    Raises:
    ValueError: If the input string is not in the correct format
    """
    try:
        date_obj = datetime.strptime(date_string, "%d-%m-%Y")
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY.")


def format_distance(distance_str):
    """
    Format a distance string to a dictionary containing the numeric value and unit.

    Args:
    distance_str (str): A string containing a distance value and 'kms' unit

    Returns:
    dict: A dictionary with 'value' (float) and 'unit' (str) keys

    Raises:
    ValueError: If the input string is not in the correct format
    """
    # Use regex to extract the numeric part and the unit
    match = re.match(r'(\d+(?:\.\d+)?)\s*(kms?)', distance_str.strip())
    if match:
        value = float(match.group(1))
        unit = 'km'  # Standardize the unit to 'km'
        return {'value': value, 'unit': unit}
    else:
        raise ValueError(f"Invalid distance format: {distance_str}")


def format_location(location_str):
    """
    Format a location string into a structured dictionary.

    Args:
    location_str (str): A string containing location information

    Returns:
    dict: A dictionary with keys 'city', 'department_code', 'department', and 'region'

    Raises:
    ValueError: If the input string is not in the correct format
    """
    pattern = r"([^(]+)\s*\((\d+)\s*-\s*([^,]+),\s*(.+?)\s*\)"
    match = re.match(pattern, location_str.strip())

    if match:
        return {
            'city': match.group(1).strip(),
            'department_code': match.group(2),
            'department': match.group(3).strip(),
            'region': match.group(4).strip()
        }
    else:
        raise ValueError(f"Invalid location format: {location_str}")
