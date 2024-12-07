import requests
from lxml import html
from enum import Enum

class MappingsType(Enum):
    MOJANG = 'N Q'
    YARN = 'N T'
    INTERMEDIARY = 'N R'
    SEARGE = 'N S'

class InvalidMappingTypeError(Exception):    
    def __init__(self, version, mapping_type):
        message = f'For versions less than 1.15, use only Searge mappings! Version: {version}, Mapping Type: {mapping_type}'
        super().__init__(message)


class Mappings:
    def __init__(self, version, mapping_type=MappingsType.MOJANG):
        if int(version.split('.')[1]) < 15 and mapping_type != MappingsType.SEARGE:
            raise InvalidMappingTypeError(version, mapping_type)

        self.version = version
        self.mapping_type = mapping_type
        self.field_mappings = {}
        self.method_mappings = {}
        self.mapping_class_name = None
        self.obfuscated_class_name = None

    def fetch(self, class_path):
        url = f'https://mappings.dev/{self.version}/{class_path.replace(".", "/")}.html'

        response = requests.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.content)

        find_class = self.mapping_type.value
        mapping_class_element = tree.cssselect(f'[class="{find_class}"]')[0]
        self.mapping_class_name = mapping_class_element.getnext().text_content().strip()
        obfuscated_class_element = tree.cssselect('[class="N O"]')[0]
        self.obfuscated_class_name = obfuscated_class_element.getnext().text_content().strip()

        tables = tree.cssselect('table.W.X')
        if len(tables) < 2:
            raise ValueError("Expected at least two tables for fields and methods.")

        fields_table, methods_table = tables[0], tables[1]
        self._process_table(fields_table, self.field_mappings)
        self._process_table(methods_table, self.method_mappings)
        return self.get()

    def _process_table(self, table, mapping_dict):
        find_class = self.mapping_type.value
        mapping_cells = table.cssselect(f'td[class*="{find_class}"]')
        obfuscated_cells = table.cssselect('td[class*="N O"]')

        for idx, cell in enumerate(mapping_cells):
            mapping_name = cell.getnext().text_content().strip()
            obfuscated_name = obfuscated_cells[idx].getnext().text_content().strip()
            if '(' in mapping_name:
                mapping_name = mapping_name.split('(')[0]
                obfuscated_name = obfuscated_name.split('(')[0]
            mapping_dict[mapping_name] = obfuscated_name

    def get(self):
        return {
            "class_name": self.mapping_class_name,
            "obfuscated_class_name": self.obfuscated_class_name,
            "fields": self.field_mappings,
            "methods": self.method_mappings
        }
