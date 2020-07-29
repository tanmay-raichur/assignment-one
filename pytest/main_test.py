from unittest.mock import patch, mock_open

import Csv2Json


def test_csv_to_json():
    with open(r'test_data_output.json', 'r') as h:
        output = h.read()
    open_mock = mock_open()
    with patch("Csv2Json.open", open_mock, create=True):
        Csv2Json.csv2json(r'test_data_input.csv')

    open_mock.assert_called_with("data.json", "w")
    open_mock.return_value.write.assert_called_once_with(output)


if __name__ == "__main__":
    test_csv_to_json()
