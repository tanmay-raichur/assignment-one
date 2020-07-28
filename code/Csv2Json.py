import pandas as pd
import json


def csv2json(path: str) -> None:
    """ Converts CSV file into nested Json list which forms a tree structure
    Input to the function will be the path to CSV file including file name

    CSV file needs to be in agreed format, below points are important
    1. Base URL is first column and need not be displayed in the output Json
    2. Each level of data will have 3 columns Name, ID and Link in said order
    3. File can have any number of columns or rows
    4. Duplicate IDs at any level will be ignored

    This function calls write_json function with Json list as parameter
    """
    try:
        df = pd.read_csv(path)
        headers = list(df.columns)
        headers.pop(0)
        df = df[headers[:]]
        df.dropna(subset=[headers[0]], inplace=True)
        no_attr = 3
        no_levels = int(len(headers)/no_attr)
        list_levels = [['label', 'id', 'link'] for i in range(no_levels)]
        d = {}
        final = []
        index_list = []
        dict_list = {}
        pos = int

        for line in df.values:
            data_levels = [line[i * no_attr:(i + 1) * no_attr] for i in range(no_levels)]
            for i in range(no_levels):
                cond_nan_1 = bool(data_levels[i][1] == data_levels[i][1])
                cond_exists_1 = bool(data_levels[i][1] in dict_list.keys())
                if cond_nan_1 and cond_exists_1:
                    index_list.append(dict_list[data_levels[i][1]])
            j = 0
            while j <= (no_levels-1):
                d = {list_levels[j][i]: data_levels[j][i] for i in range(no_attr)}
                d['children'] = []
                cond_nan_2 = bool(d['id'] == d['id'])
                cond_exists_2 = bool(d['id'] in dict_list.keys())
                if not cond_exists_2 and cond_nan_2:
                    d['id'] = int(d['id'])
                    if j == 0:
                        final.append(d.copy())
                        pos = len(final)
                        dict_list[d['id']] = pos-1
                    else:
                        indexes = index_list[:j]
                        srt_str = "final["
                        join_str = "]['children']["
                        end_str = "]['children'].append(d.copy())"
                        eval(srt_str+join_str.join([str(m) for m in indexes])+end_str)
                        srt_str = "len(final["
                        join_str = "]['children']["
                        end_str = "]['children'])"
                        pos = eval(srt_str+join_str.join([str(m) for m in indexes])+end_str)
                        dict_list[d['id']] = pos-1
                d.clear()
                j += 1
            index_list.clear()
        create_json(final)

    except FileNotFoundError:
        print('The CSV data file is missing.')
    except PermissionError:
        print('The required permissions missing on CSV file.')
    except Exception:
        print('Some other error occurred.')


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
        print("Json file successfully created.")


if __name__ == "__main__":
    import doctest
    doctest.testfile("UnitTest.txt")
