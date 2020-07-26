def csv2json(path: str) -> 'data.json':
    """ Converts CSV file into nested Json file which forms a tree structure
    Input to the function will be the path to CSV file including file name
    
    CSV file needs to be in agreed format, below points are important
    1. Base URL is first column and need not be displayed in the output Json
    2. Each level of data will have 3 columns Name, ID and Link in said order
    3. File can have any number of columns or rows
    4. Duplicate IDs at any level will be ignored
    
    Output will a Json file created in same path as .py file
    """
    import pandas as pd
    import json
    try:
        df = pd.read_csv(path)
        list_heads = []
        for k,v in df.items():
            list_heads.append(k)                                         # Collect header columns
        df = df[list_heads[1:]]                                          # Base URL column removed from dataframe
        df.dropna(subset = [list_heads[1]], inplace=True)                # Remove blank rows         
        list_heads.pop(0)                                                # Remove Base URL
        no_of_levels = int(len(list_heads)/3)                            # Calculate number of levels based on number of columns in CSV and assuming each level has 3 attributes
        n = 3                                                            # Assuming each level has 3 attributes
        list_levels = [list_heads[i * n:(i + 1) * n] for i in range((len(list_heads) + n - 1) // n )] # Create nested lists, one for each level
        for record in list_levels:                                       # Rename Headers. Assumption - Label, Id and Link are the three attributes per level and in given order
            record[0]='label'
            record[1]='id'
            record[2]='link'
        d = {}
        final = []
        index_list = []
        dict_list = {}
        position = int

        for line in df.values:
            data_levels = [line[i * n:(i + 1) * n] for i in range((len(line) + n - 1) // n )]    # Divide data into lists, one for each level
            index_list = [dict_list[data_levels[i][1]] for i in range(len(data_levels)) if data_levels[i][1] == data_levels[i][1] and data_levels[i][1] in dict_list.keys()]  # Store index of each item id in line - Assumption is position of id column in CSV file
            j = 0
            while j <= (no_of_levels-1):
                d = {list_levels[j][i] : data_levels[j][i] for i in range(len(list_levels[j]))}  # Dictionary to map data with headers proposed in Readme.md
                d['children'] = []
                if not d['id'] in dict_list.keys() and d['id'] == d['id']:                       # Check Item Id not already processed and is not null
                    d['id'] = int(d['id'])
                    if j == 0:                                                                   # Top level parent added in final list and positions noted for inserting child, if any
                        final.append(d.copy())
                        position = len(final)
                        dict_list[d['id']] = position-1
                    else:                                                                        # All children added in final list one by one and their positions noted for inserting child, if any
                        indexes = index_list[:j]
                        eval("final["+"]['children'][".join([str(m) for m in indexes])+"]['children'].append(d.copy())")
                        position = eval("len(final["+"]['children'][".join([str(m) for m in indexes])+"]['children'])")
                        dict_list[d['id']] = position-1
                d.clear()
                j += 1
            index_list.clear()

        json_dump = json.dumps(final)
        json_str = json.loads(json_dump, parse_int=str)                                             # Converting id to str as shown in Readme.md
        final_json = json.dumps(json_str, indent = 4)
        with open('data.json', 'w') as outfile:                                                     # Write output to Json file
            outfile.write(final_json)
            print("Json file successfully created.")
    except FileNotFoundError:
        print('The CSV data file is missing.')
    except PermissionError:
        print('The required permissions missing on CSV file.')
    except:
        print('Some other error occurred.')

if __name__ == "__main__":
    import doctest
    doctest.testfile("UnitTest.txt")
