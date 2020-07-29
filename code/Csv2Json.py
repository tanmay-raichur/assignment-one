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
        file_data = pd.read_csv(path)
        headers = list(file_data.columns)
        headers.pop(0)
        file_data = file_data[headers[:]]
        file_data.dropna(subset=[headers[0]], inplace=True)
        no_attr = 3
        no_levels = int(len(headers)/no_attr)
        list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
        final = form_tree(file_data, no_levels, list_levels, no_attr)
        create_json(final)

    except FileNotFoundError:
        logging.error('The CSV data file is missing.')
    except PermissionError:
        logging.error('The required permissions missing on CSV file.')
    except Exception:
        logging.error('Some other error occurred.', exc_info=True)


def form_tree(file_data: list, no_levels: int, list_levels: list, no_attr: int) -> list:
    """ This function creates a json tree structure
    and returns a list which has the created json tree
    """
    data = {}
    final = []
    index_list = {}
    pos = int

    for line in file_data.values:
        split_line, id_index = splitLine_findIndex(line, no_levels, no_attr, index_list)
        for level in range(0, (no_levels)):
            data = {list_levels[level][i]: split_line[level][i] for i in range(no_attr)}
            data['children'] = []
            Id = data['id']
            id_isnull = (Id != Id)
            id_exists = (Id in index_list.keys())
            if not id_exists and not id_isnull:
                data['id'] = int(data['id'])
                if level == 0:
                    final.append(data.copy())
                    pos = len(final)
                    index_list[Id] = pos-1
                else:
                    indexes = id_index[:level]
                    add_child_expr, child_pos_expr = create_expr(indexes)
                    eval(add_child_expr)
                    pos = eval(child_pos_expr)
                    index_list[Id] = pos-1
            data.clear()
    return final


def splitLine_findIndex(line: list, no_levels: int, no_attr: int, index_list: list) -> list:
    """ This function splits the line into one list per level
    and finds the index of parent item for child insertion
    """
    split_line = []
    id_index = []
    for level in range(no_levels):
        split_line.append(line[level * no_attr:(level + 1) * no_attr])
        Id = split_line[level][1]
        id_isnull = (Id != Id)
        id_exists = (Id in index_list.keys())
        if not id_isnull and id_exists:
            id_index.append(index_list[Id])
    return split_line, id_index


def create_expr(indexes: list) -> str:
    """ This function creates and returns expressions for child insertion
    as per the level to which child node needs to be inserted.
    After insertion finds and returns the position of inserted child
    """
    join = "]['children'][".join([str(m) for m in indexes])

    start = "final["
    end = "]['children'].append(data.copy())"
    add_child_expr = start+join+end

    start = "len(final["
    end = "]['children'])"
    child_pos_expr = start+join+end

    return add_child_expr, child_pos_expr


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
