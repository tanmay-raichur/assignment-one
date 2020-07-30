from unittest.mock import patch, mock_open
import Csv2Json
import pandas as pd

def test_split_line():
    split_line = Csv2Json.split_line(line=['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974',
                                                               'FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969',
                                                               'CHEESE',178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975'],
                                                        no_levels=3,
                                                        no_attr=3)
    test1 = (split_line == [['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974'],
                            ['FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969'],
                            ['CHEESE', 178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975']])
    assert test1


def test_read_data_flatlist():
    file_data, headers = Csv2Json.read_edit_data(r'test_data_input.csv')
    no_attr = 3
    no_levels = int(len(headers)/no_attr)
    list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
    actual_list = Csv2Json.filedata_to_flatlist(file_data, no_levels, list_levels, no_attr)
    expected_list = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': []}, {'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [], 'level': 1, 'parent': 178974.0}, {'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [], 'level': 2, 'parent': 178969.0}]
    assert actual_list == expected_list


def test_flatlist_to_tree():
    all_items = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': []}, {'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [], 'level': 1, 'parent': 178974.0}, {'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': [], 'level': 2, 'parent': 178969.0}]
    no_levels = 3
    actual_tree = Csv2Json.flatlist_to_tree(all_items, no_levels)
    expected_tree = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [{'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}]}]}]
    assert actual_tree == expected_tree


def test_csv2json():
    with open(r'test_data_output.json', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("Csv2Json.open", open_mock, create=True):
        Csv2Json.csv2json(r'test_data_input.csv')

    open_mock.assert_called_with("data.json", "w")
    open_mock.return_value.write.assert_called_once_with(output)
