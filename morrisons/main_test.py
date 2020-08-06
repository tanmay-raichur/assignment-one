from unittest.mock import patch, mock_open
import csv_converter
import pandas as pd


def test_file_exist(caplog):
    csv_converter.csv_to_json('random.csv','data.json')
    assert 'The CSV data file is missing.' in caplog.text

    
def test_split_line():
    split_line = csv_converter._split_line(line=['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974',
                                                               'FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969',
                                                               'CHEESE',178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975'],
                                                        no_levels=3,
                                                        NO_ATTR=3)
    test1 = (split_line == [['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974'],
                            ['FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969'],
                            ['CHEESE', 178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975']])
    assert test1


def test_read_data_flatlist():
    file_data, headers = csv_converter._read_edit_data(r'test_data_input.csv')
    no_attr = 3
    no_levels = int(len(headers)/no_attr)
    list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
    actual_list = csv_converter._filedata_to_flatlist(file_data, no_levels, list_levels, no_attr)
    expected_list = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': []}, {'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [], 'level': 1, 'parent': 178974.0}, {'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [], 'level': 2, 'parent': 178969.0}]
    assert actual_list == expected_list


def test_flatlist_to_tree():
    all_items = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': []}, {'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [], 'level': 1, 'parent': 178974.0}, {'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [], 'level': 2, 'parent': 178969.0}]
    no_levels = 3
    actual_tree = csv_converter._flatlist_to_tree(all_items, no_levels)
    expected_tree = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [{'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}]}]}]
    assert actual_tree == expected_tree


def test_csv_to_json():
    with open(r'test_data_output.json', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("csv_converter.open", open_mock, create=True):
        csv_converter.csv_to_json('test_data_input.csv','data.json')

    open_mock.assert_called_with("data.json", "w")
    open_mock.return_value.write.assert_called_once_with(output)
