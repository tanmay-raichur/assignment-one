import pandas as pd
import json
import logging as log
import argparse

log.basicConfig(level=log.INFO)


def csv_to_json(ip_path: str, op_path: str) -> None:
    """ Converts given csv file into json file.

    Csv file needs to be in agreed format, below points are important
    1. Base URL is first column and need not be displayed in the output Json
    2. Each level of data will have 3 columns Label, ID and Link in said order
    3. File can have any number of columns or rows
    4. Duplicate IDs at any level will be ignored
    5. First row is the header and will be ignored in tree

     :parameter
        ip_path : csv filename or path to the file including filename
        op_path : json filename or path to the file including filename

    """
    try:
        file_data, headers = _read_edit_data(ip_path)
        NO_ATTR = 3
        no_levels = int(len(headers)/NO_ATTR)
        list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
        all_items = _filedata_to_flatlist(file_data, no_levels,
                                          list_levels, NO_ATTR)
        final = _flatlist_to_tree(all_items, no_levels)
        _create_json(final, op_path)

    except FileNotFoundError:
        log.error('The CSV data file is missing.')
    except PermissionError:
        log.error('The required permissions missing on CSV file.')
    except Exception:
        log.error('Some other error occurred.', exc_info=True)


def _read_edit_data(ip_path: str) -> list:
    """ This function will read the csv data and
    make necessary transformations to the data frame
    """
    file_data = pd.read_csv(ip_path)
    headers = list(file_data.columns)
    headers.pop(0)
    file_data = file_data[headers[:]]
    file_data.dropna(subset=[headers[0]], inplace=True)
    return file_data, headers


def _filedata_to_flatlist(file_data: list, no_levels: int,
                          list_levels: list, NO_ATTR: int) -> list:
    """ This function creates a list with flat structure. """
    all_items = []
    id_list = []
    curr_id = 0

    for line in file_data.values:
        level_grp = _split_line(line, no_levels, NO_ATTR)
        for level in range(0, (no_levels)):
            data = {list_levels[level][i]: level_grp[level][i] for i in range(NO_ATTR)}
            data['children'] = []
            prev_id = curr_id
            curr_id = data['id']
            id_isnull = (curr_id != curr_id)
            id_exists = (curr_id in id_list)
            if not id_exists and not id_isnull:
                data['id'] = int(data['id'])
                if level == 0:
                    all_items.append(data.copy())
                else:
                    data['level'] = level
                    data['parent'] = prev_id
                    all_items.append(data.copy())
                id_list.append(curr_id)
            data.clear()
    return all_items


def _split_line(line: list, no_levels: int, NO_ATTR: int) -> list:
    """ This function splits the line into one list per level. """
    level_grp = []
    for level in range(no_levels):
        level_grp.append(line[level * NO_ATTR:(level + 1) * NO_ATTR])
    return level_grp


def _flatlist_to_tree(all_items: list, no_levels: int) -> list:
    """ This function will convert flat list into
    a tree structure as requested.
    """
    pop_list = []
    final = []
    for j in reversed(range(1, no_levels)):
        for i in range(len(all_items)):
            if 'level' in all_items[i].keys() and all_items[i]['level'] == j:
                pop_list.append(i)
                data = all_items[i].copy()
                parent = all_items[i]['parent']
                for k in range(len(all_items)):
                    if all_items[k]['id'] == parent:
                        data.pop('level')
                        data.pop('parent')
                        all_items[k]['children'].append(data.copy())
                        break

    for i in range(len(all_items)):
        if 'level' not in all_items[i].keys():
            final.append(all_items[i])

    return final


def _create_json(final: list, op_path: str) -> None:
    """ Creates a json file at output path. """
    json_dump = json.dumps(final)
    json_str = json.loads(json_dump, parse_int=str)
    final_json = json.dumps(json_str, indent=2)
    with open(op_path, 'w') as outfile:
        outfile.write(final_json)
        log.info("Json file successfully created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_path',
                        help="Enter csv filename or path including filename")
    parser.add_argument('op_path',
                        help="Enter json filename or path including filename")
    args = parser.parse_args()
    csv_to_json(args.ip_path, args.op_path)
