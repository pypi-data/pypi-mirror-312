import unittest

from fetchrunner.formatting import (
    format_date,
    format_distance,
    format_location,
    format_time_string,
)


class TestFormatDate(unittest.TestCase):

    def test_valid_date(self):
        self.assertEqual(format_date("01-01-2023"), "01/01/2023")
        self.assertEqual(format_date("31-12-2022"), "31/12/2022")
        self.assertEqual(format_date("15-06-1990"), "15/06/1990")
        self.assertEqual(format_date("1-1-2023"), "01/01/2023")

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            format_date("2023-01-01")
        with self.assertRaises(ValueError):
            format_date("01/01/2023")

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            format_date("31-02-2023")  # Invalid day for February
        with self.assertRaises(ValueError):
            format_date("00-01-2023")  # Invalid day

    def test_edge_cases(self):
        self.assertEqual(format_date("29-02-2020"), "29/02/2020")  # Leap year
        with self.assertRaises(ValueError):
            format_date("29-02-2021")  # Not a leap year


class TestFormatDistance(unittest.TestCase):

    def test_valid_distances(self):
        self.assertEqual(format_distance('51.5 kms'), {'value': 51.5, 'unit': 'km'})
        self.assertEqual(format_distance('10 kms'), {'value': 10.0, 'unit': 'km'})
        self.assertEqual(format_distance('5.0 kms'), {'value': 5.0, 'unit': 'km'})
        self.assertEqual(format_distance('100kms'), {'value': 100.0, 'unit': 'km'})

    def test_whitespace_handling(self):
        self.assertEqual(format_distance(' 42.0 kms '), {'value': 42.0, 'unit': 'km'})
        self.assertEqual(format_distance('30.5  kms'), {'value': 30.5, 'unit': 'km'})

    def test_singular_km(self):
        self.assertEqual(format_distance('1 km'), {'value': 1.0, 'unit': 'km'})

    def test_invalid_formats(self):
        with self.assertRaises(ValueError):
            format_distance('abc kms')
        with self.assertRaises(ValueError):
            format_distance('51.5')

    def test_zero_distance(self):
        self.assertEqual(format_distance('0 kms'), {'value': 0.0, 'unit': 'km'})


class TestFormatLocation(unittest.TestCase):

    def test_valid_locations(self):
        test_cases = [
            ('Gerardmer (88 - Vosges, Lorraine)',
             {'city': 'Gerardmer', 'department_code': '88', 'department': 'Vosges', 'region': 'Lorraine'}),
            ('Cannes (06 - Alpes-Maritimes, Provence-Alpes-Côte-d\'Azur)',
             {'city': 'Cannes', 'department_code': '06', 'department': 'Alpes-Maritimes', 'region': 'Provence-Alpes-Côte-d\'Azur'}),
            ('Nice (06 - Alpes-Maritimes, Provence-Alpes-Côte-d\'Azur)',
             {'city': 'Nice', 'department_code': '06', 'department': 'Alpes-Maritimes', 'region': 'Provence-Alpes-Côte-d\'Azur'}),
            ('Ottrott (67 - Bas-Rhin, Alsace)',
             {'city': 'Ottrott', 'department_code': '67', 'department': 'Bas-Rhin', 'region': 'Alsace'}),
            ('Reichsfeld (67 - Bas-Rhin, Alsace)',
             {'city': 'Reichsfeld', 'department_code': '67', 'department': 'Bas-Rhin', 'region': 'Alsace'})
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                self.assertEqual(format_location(input_str), expected)

    def test_extra_whitespace(self):
        result = format_location('  Nice  (06 -  Alpes-Maritimes ,  Provence-Alpes-Côte-d\'Azur  ) ')
        expected = {
            'city': 'Nice',
            'department_code': '06',
            'department': 'Alpes-Maritimes',
            'region': "Provence-Alpes-Côte-d'Azur"
        }
        self.assertEqual(result, expected)

    def test_hyphenated_names(self):
        result = format_location('Saint-Étienne-de-Tinée (06 - Alpes-Maritimes, Provence-Alpes-Côte-d\'Azur)')
        expected = {
            'city': 'Saint-Étienne-de-Tinée',
            'department_code': '06',
            'department': 'Alpes-Maritimes',
            'region': "Provence-Alpes-Côte-d'Azur"
        }
        self.assertEqual(result, expected)

    def test_invalid_format(self):
        invalid_inputs = [
            'Paris 75 - Île-de-France',
            'Marseille (13)',
            "Lyon",
            '(75 - Paris, Île-de-France)'
        ]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValueError):
                    format_location(invalid_input)

    def test_special_characters(self):
        result = format_location('Bagnères-de-Bigorre (65 - Hautes-Pyrénées, Occitanie)')
        expected = {
            'city': "Bagnères-de-Bigorre",
            "department_code": "65",
            "department": "Hautes-Pyrénées",
            "region": "Occitanie"
        }
        self.assertEqual(result, expected)


class TestFormatTimeString(unittest.TestCase):

    def test_with_hours(self):
        self.assertEqual(format_time_string("2h30'5''"), "02h30m05s")
        self.assertEqual(format_time_string("1h0'0''"), "01h00m00s")
        self.assertEqual(format_time_string("10h15'45''"), "10h15m45s")

    def test_without_hours(self):
        self.assertEqual(format_time_string("30'5''"), "30m05s")
        self.assertEqual(format_time_string("0'10''"), "10s")
        self.assertEqual(format_time_string("45'0''"), "45m00s")

    def test_only_minutes(self):
        self.assertEqual(format_time_string("0'5''"), "05s")
        self.assertEqual(format_time_string("5'0''"), "05m00s")

    def test_only_seconds(self):
        self.assertEqual(format_time_string("0'0''"), "00s")  # Edge case for zero time


if __name__ == '__main__':
    unittest.main()
