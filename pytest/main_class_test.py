from unittest.mock import patch, mock_open
from CsvConverter import CsvConverter
import pandas as pd

c = CsvConverter(r'test_data_input.csv')
c.convert_csv()

def test_split_line():
    actual = c.level_grp[2][1]
    expected = 178975
    assert actual == expected


def test_read_data_flatlist():
    expected_list = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [{'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}]}]}, {'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}], 'level': 1, 'parent': 178974.0}, {'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [], 'level': 2, 'parent': 178969.0}]
    assert c.all_items == expected_list


def test_flatlist_to_tree():
    expected_tree = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [{'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}]}]}]
    assert c.final == expected_tree


def test_csv_to_json():
    with open(r'test_data_output.json', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("CsvConverter.open", open_mock, create=True):
        c = CsvConverter(r'test_data_input.csv', 'j')
        c.convert_csv()

    open_mock.assert_called_with("data.json", "w")
    open_mock.return_value.write.assert_called_once_with(output)


def test_csv_to_xml():
    with open(r'test_data_output.xml', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("CsvConverter.open", open_mock, create=True):
        c = CsvConverter(r'test_data_input.csv', 'x')
        c.convert_csv()

    open_mock.assert_called_with("data.xml", "w")
    open_mock.return_value.write.assert_called_once_with(output)
