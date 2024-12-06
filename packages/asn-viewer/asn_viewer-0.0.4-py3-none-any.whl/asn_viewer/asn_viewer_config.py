from argparse import ArgumentParser, Action
from os import PathLike
from pathlib import Path

from yaml import safe_load


class ASNViewerConfig:
    """
    Configuration container class for the ASN Viewer
    """
    def __init__(self, config_file: PathLike):
        self.__parse_config_file(config_file)


    def __parse_config_file(self, config_file: PathLike):
        """
        Parses configuration file
        :param config_file: Path to config file

        """
        with open(config_file, 'r') as config_file:
            self.raw_yaml_config = safe_load(config_file)
            self.definition = Path(self.raw_yaml_config['definition'])
            self.object_name = self.raw_yaml_config['object-name']

            try:
                self.search = self.raw_yaml_config['search']
            except KeyError:
                self.search = None

            try:
                self.files = tuple(Path(f) for f in self.raw_yaml_config['files'])
            except KeyError:
                self.files = None

            try:
                self.output = self.raw_yaml_config['output']
            except KeyError:
                self.output = '.'

    def __str__(self):
        return (f'asn-schema-file: {self.definition}\n'
                f'output: {self.output}\n'
                f'object-name: {self.object_name}\n'
                f'search {self.search}\n')

class ParseSearchKwargs(Action):
    """
    ASN Viewer Argument parser helper Action for search params

    """
    def __call__(self, parser, namespace, values, option_string=None, ):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = tuple(s.strip() for s in value.replace(';', ',').split(','))


class ASNViewerCmdArguments(ArgumentParser):
    """
    ASN Viewer Argument parser

    """
    def __init__(self):
        super().__init__()

        self.add_argument('-c', '--config', type=Path, help='Config filename')
        self.add_argument('-d', '--definition', type=Path, help='Schema Definition file')
        self.add_argument('-o', '--output', type=Path, help='Output filename')
        self.add_argument('-n', '--object-name', help='ASN Object Name')
        self.add_argument('-f', '--files', nargs='*', help='Filenames to decode')

        self.add_argument('-s', '--search',
                          nargs='*', action=ParseSearchKwargs,
                          help='Search filter: fieldName=value. Multiple values per key should be separated by a comma')