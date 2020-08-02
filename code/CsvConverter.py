import pandas as pd
import json
import dicttoxml
from xml.dom.minidom import parseString
import logging
logging.basicConfig(level=logging.INFO)


class CsvConverter:
    """ A class to convert CSV to other formats
    with child parent tree representation.

    Attributes
    ----------
    path: str
        Path where Csv file is placed
    target_format: str
        Format to which file needs to be converted
        'x' - XML
        'j' - JSON
        'all' - All available formats (default selection)

    Methods
    -------
    convert_csv():
        Creates requested files in current directory

    """

    def __init__(self, path: str, target_format: str='all') -> None:
        self.path = path
        self.format = target_format

    def convert_csv(self) -> None:
        """ Converts CSV file into nested Json list which forms a tree structure
        Input to the function will be the path to CSV file including file name

        CSV file needs to be in agreed format, below points are important
        1. Base URL is first column and need not be displayed in the output Json
        2. Each level of data will have 3 columns Name, ID and Link in said order
        3. File can have any number of columns or rows
        4. Duplicate IDs at any level will be ignored
        """
        try:
            self.read_edit_data()
            self.no_attr = 3
            self.no_levels = int(len(self.headers)/self.no_attr)
            self.list_levels = [['label', 'id', 'link'] for i in range(self.no_levels)]
            self.filedata_to_flatlist()
            self.flatlist_to_tree()
            if self.format == 'j':
                self.create_json()
            elif self.format == 'x':
                self.create_xml()
            else:
                self.create_json()
                self.create_xml()

        except FileNotFoundError:
            logging.error('The CSV data file is missing.')
        except PermissionError:
            logging.error('The required permissions missing on CSV file.')
        except Exception:
            logging.error('Some other error occurred.', exc_info=True)

    def read_edit_data(self) -> list:
        """ This function will read the csv data and
        make necessary transformations to the data frame
        """
        self.file_data = pd.read_csv(self.path)
        self.headers = list(self.file_data.columns)
        self.headers.pop(0)
        self.file_data = self.file_data[self.headers[:]]
        self.file_data.dropna(subset=[self.headers[0]], inplace=True)

    def filedata_to_flatlist(self) -> list:
        """ This function creates a json tree structure
        and returns a list which has the created json tree
        """
        self.all_items = []
        id_list = []
        curr_id = 0

        for self.line in self.file_data.values:
            self.split_line()
            for level in range(0, (self.no_levels)):
                data = {self.list_levels[level][i]: self.level_grp[level][i] for i in range(self.no_attr)}
                data['children'] = []
                prev_id = curr_id
                curr_id = data['id']
                id_isnull = (curr_id != curr_id)
                id_exists = (curr_id in id_list)
                if not id_exists and not id_isnull:
                    data['id'] = int(data['id'])
                    if level == 0:
                        self.all_items.append(data.copy())
                    else:
                        data['level'] = level
                        data['parent'] = prev_id
                        self.all_items.append(data.copy())
                    id_list.append(curr_id)
                data.clear()

    def split_line(self) -> list:
        """ This function splits the line into one list per level
        """
        self.level_grp = []
        for level in range(self.no_levels):
            self.level_grp.append(self.line[level * self.no_attr:(level + 1) * self.no_attr])

    def flatlist_to_tree(self) -> list:
        """ This function will convert flattened list into
        a tree structure as requested
        """
        pop_list = []
        self.final = []
        for j in reversed(range(1, self.no_levels)):
            for i in range(len(self.all_items)):
                if 'level' in self.all_items[i].keys() and self.all_items[i]['level'] == j:
                    pop_list.append(i)
                    data = self.all_items[i].copy()
                    parent = self.all_items[i]['parent']
                    for k in range(len(self.all_items)):
                        if self.all_items[k]['id'] == parent:
                            data.pop('level')
                            data.pop('parent')
                            self.all_items[k]['children'].append(data.copy())
                            break

        for i in range(len(self.all_items)):
            if 'level' not in self.all_items[i].keys():
                self.final.append(self.all_items[i])

    def create_json(self) -> None:
        """ This function takes Json list as input
        Creates a json file with Json list string
        at the same path as Csv2Json.py file
        """
        json_dump = json.dumps(self.final)
        json_str = json.loads(json_dump, parse_int=str)
        final_json = json.dumps(json_str, indent=4)
        with open('data.json', 'w') as outfile:
            outfile.write(final_json)
            logging.info("Json file successfully created.")

    def create_xml(self) -> None:
        """ This function takes list as input
        Creates a xml file at the same path as Csv2Json.py file
        """
        xml = dicttoxml.dicttoxml(self.final, attr_type=False)
        final_xml = parseString(xml)
        with open('data.xml', 'w') as outfile:
            outfile.write(final_xml.toprettyxml())
            logging.info("XML file successfully created.")
        
