import pandas as pd
import json
import logging
logging.basicConfig(level=logging.INFO)


def csv2json(path: str) -> None:
    """ Converts CSV file into nested Json list which forms a tree structure
    Input to the function will be the path to CSV file including file name

    CSV file needs to be in agreed format, below points are important
    1. Base URL is first column and need not be displayed in the output Json
    2. Each level of data will have 3 columns Name, ID and Link in said order
    3. File can have any number of columns or rows
    4. Duplicate IDs at any level will be ignored
    """
    try:
        file_data, headers = read_edit_data(path)
        no_attr = 3
        no_levels = int(len(headers)/no_attr)
        list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
        all_items = filedata_to_flatlist(file_data, no_levels, list_levels, no_attr)
        final = flatlist_to_tree(all_items, no_levels)
        create_json(final)

    except FileNotFoundError:
        logging.error('The CSV data file is missing.')
    except PermissionError:
        logging.error('The required permissions missing on CSV file.')
    except Exception:
        logging.error('Some other error occurred.', exc_info=True)


def read_edit_data(path: str) -> list:
    """ This function will read the csv data and
    make necessary transformations to the data frame
    """
    file_data = pd.read_csv(path)
    headers = list(file_data.columns)
    headers.pop(0)
    file_data = file_data[headers[:]]
    file_data.dropna(subset=[headers[0]], inplace=True)
    return file_data, headers


def filedata_to_flatlist(file_data: list, no_levels: int, list_levels: list, no_attr: int) -> list:
    """ This function creates a json tree structure
    and returns a list which has the created json tree
    """
    all_items = []
    id_list = []
    curr_id = 0

    for line in file_data.values:
        level_grp = split_line(line, no_levels, no_attr)
        for level in range(0, (no_levels)):
            data = {list_levels[level][i]: level_grp[level][i] for i in range(no_attr)}
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


def split_line(line: list, no_levels: int, no_attr: int) -> list:
    """ This function splits the line into one list per level
    """
    level_grp = []
    for level in range(no_levels):
        level_grp.append(line[level * no_attr:(level + 1) * no_attr])
    return level_grp


def flatlist_to_tree(all_items: list, no_levels: int) -> list:
    """ This function will convert flattened list into
    a tree structure as requested
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


def create_json(final: list) -> None:
    """ This function takes Json list as input
    Creates a json file with Json list string
    at the same path as Csv2Json.py file
    """
    json_dump = json.dumps(final)
    json_str = json.loads(json_dump, parse_int=str)
    final_json = json.dumps(json_str, indent=4)
    with open('data.json', 'w') as outfile:
        outfile.write(final_json)
        logging.info("Json file successfully created.")


if __name__ == "__main__":
    csv2json(r'data_c.csv')
