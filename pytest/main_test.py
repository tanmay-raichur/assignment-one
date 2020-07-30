from unittest.mock import patch, mock_open
import Csv2Json
import pandas as pd

def test_splitline_findindex():
    split_line, id_index = Csv2Json.splitLine_findIndex(line=['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974',
                                                               'FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969',
                                                               'CHEESE',178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975'],
                                                        no_levels=3,
                                                        no_attr=3,
                                                        index_list={178974.0: 0, 178969.0: 0})
    test1 = (split_line == [['THE BEST', 178974.0,'https://groceries.morrisons.com/browse/178974'],
                            ['FRESH', 178969.0,'https://groceries.morrisons.com/browse/178974/178969'],
                            ['CHEESE', 178975.0,'https://groceries.morrisons.com/browse/178974/178969/178975']])
    test2 = (id_index == [0, 0])
    assert test1 and test2


def test_create_expr():
    add_child_expr, child_pos_expr = Csv2Json.create_expr([0,0])
    test1 = (add_child_expr == "final[0]['children'][0]['children'].append(data.copy())")
    test2 = (child_pos_expr == "len(final[0]['children'][0]['children'])")
    assert test1 and test2


def test_read_data_form_tree():
    file_data, headers = Csv2Json.read_edit_data(r'test_data_input.csv')
    no_attr = 3
    no_levels = int(len(headers)/no_attr)
    list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
    actual_tree = Csv2Json.form_tree(file_data, no_levels, list_levels, no_attr)
    expected_tree = [{'label': 'THE BEST', 'id': 178974, 'link': 'https://groceries.morrisons.com/browse/178974', 'children': [{'label': 'FRESH', 'id': 178969, 'link': 'https://groceries.morrisons.com/browse/178974/178969', 'children': [{'label': 'CHEESE', 'id': 178975, 'link': 'https://groceries.morrisons.com/browse/178974/178969/178975', 'children': []}]}]}]
    assert actual_tree == expected_tree


def test_csv_to_json():
    with open(r'test_data_output.json', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("Csv2Json.open", open_mock, create=True):
        Csv2Json.csv2json(r'test_data_input.csv')

    open_mock.assert_called_with("data.json", "w")
    open_mock.return_value.write.assert_called_once_with(output)
