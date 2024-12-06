from pathlib import Path

from ..enums import ConfigFileFormat
from ..exceptions import AssonantDataParserError
from ._assonant_data_parser_interface import IAssonantDataParser
from ._csv_data_parser import CSVDataParser


class DataParserFactory:
    """Data Parser Factory.

    Class that implements the factory design pattern
    (https://refactoring.guru/design-patterns/factory-method) to fully abstract
    the procedure of creating Assonant Data Parsers
    """

    def create_data_parser(self, config_file_path: str) -> IAssonantDataParser:
        """Public method that abstracts data parser creation process for the factory user.

        Internally, this method deals with validation and specific Data Parser
        creation

        Args:
            config_file_path (str): Path to configuration file.

        Raises:
            AssonantDataParserError: An error occured during the creation of
            the respective Data Parser.

        Returns:
            IAssonantDataParser: Data Parser instance which implements the
            IAssonantDataParser interface for the given config_file_format.
        """
        file_format = self._get_file_format(config_file_path)

        self._validate_file_format(file_format)

        if file_format == ConfigFileFormat.CSV.value:
            return self._create_csv_data_parser(config_file_path)

        raise AssonantDataParserError(
            f"'{file_format}' file format is set as supported but its creation method is not implemented."
        )

    def _create_csv_data_parser(self, config_file_path: str) -> CSVDataParser:
        return CSVDataParser(config_file_path=config_file_path)

    def _validate_file_format(self, file_format: str):
        """Check if file format is supported

        Args:
            file_format (str): Configuration file format extension.

        Raises:
            AssonantDataParserError: File format is not supported
        """

        if file_format not in ConfigFileFormat._value2member_map_:
            raise AssonantDataParserError(f"'{file_format}' is not supported on Data Parser!")

    def _get_file_format(self, config_file_path: str) -> str:
        """Get file extension from given path

        Args:
            config_file_path (str): Path to configuration file.

        Raises:
            AssonantDataParserError: Erro raised if path passed is not from a file.

        Returns:
            str: File extesion without '.' character.
        """

        with Path(config_file_path) as path:
            if path.is_file():
                # Get file extension and remove the '.' character
                return path.suffix[1:]
            else:
                raise AssonantDataParserError(f"'{config_file_path}' is not a file!")
