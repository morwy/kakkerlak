"""
kakkerlak.py - A simple module for demonstration purposes
"""

import os
import pathlib
from enum import Enum
from typing import List

from .logger import logger


class ImportType(str, Enum):
    """
    Enum for import types.
    """

    UNKNOWN = "UNKNOWN"
    JUNIT_XML = "JUNIT_XML"


class ExportType(str, Enum):
    """
    Enum for export types.
    """

    UNKNOWN = "UNKNOWN"
    HTML = "HTML"


class Kakkerlak:
    def __init__(self):
        self.data_paths: List[pathlib.Path] = []
        self.data_entries: list = []

    def __determine_input_type(self, path: pathlib.Path) -> ImportType:
        """
        Determine the type of input based on the file extension.
        :param path: Path to the file.
        :return: Type of input as an ImportType.
        """
        if path.suffix == ".xml":
            return ImportType.JUNIT_XML

        raise ValueError(f"Unsupported file type: {path.suffix}.")

    def __parse_data_entries(self, data_paths: List[pathlib.Path]) -> list:
        """
        Parse the input data entries into a dictionary.
        :return: Parsed data as a dictionary.
        """
        data_entries: list = []

        for data_path in data_paths:
            data = {}
            if data_path.exists():
                input_type = self.__determine_input_type(data_path)
                if input_type == ImportType.JUNIT_XML:
                    # Placeholder for JUnit XML parsing logic
                    data["parsed"] = "Parsed JUnit XML data"
                else:
                    logger.warning("Unsupported file type: %s", data_path)
            else:
                logger.error("File does not exist: %s", data_path)
                raise FileNotFoundError(f"File does not exist: {data_path}.")

            self.data_entries.append(data)

        return data_entries

    def add(self, path: pathlib.Path | os.PathLike | str) -> None:
        """
        Add a file to the list of files to be processed.
        :param path: Path to the file to be added.
        :type path: pathlib.Path | os.PathLike | str
        :raises TypeError: If the path is not a string, pathlib.Path, or os.PathLike object.
        """
        if not isinstance(path, (str, pathlib.Path, os.PathLike)):
            raise TypeError(
                "Path must be a string, pathlib.Path, or os.PathLike object."
            )

        if isinstance(path, (str, os.PathLike)):
            path = pathlib.Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}.")

        if path.is_file() and not path.stat().st_size > 0:
            raise ValueError(f"File is empty: {path}.")

        if not path.is_file() and len(list(path.iterdir())) == 0:
            raise ValueError(f"Directory is empty: {path}.")

        if path in self.data_paths:
            logger.warning("File already added: %s.", path)
            return

        self.data_paths.append(path)

    def export(
        self,
        path: pathlib.Path | os.PathLike | str,
        export_type: ExportType = ExportType.HTML,
    ) -> None:
        """
        Export the data in the specified format.
        :param path: Path to the output file.
        :type path: pathlib.Path | os.PathLike | str
        :raises TypeError: If the path is not a string, pathlib.Path, or os.PathLike object.
        :param export_type: The type of export to perform.
        :type export_type: ExportType
        :raises ValueError: If the export type is not supported.
        """
        if not isinstance(path, (str, pathlib.Path, os.PathLike)):
            raise TypeError(
                "Path must be a string, pathlib.Path, or os.PathLike object."
            )

        if export_type != ExportType.HTML:
            raise ValueError(f"Unsupported export type: {export_type}.")

        if isinstance(path, (str, os.PathLike)):
            path = pathlib.Path(path)

        if not path.parent.exists():
            logger.debug("Creating directory for export path: %s.", path.parent)
            path.parent.mkdir(parents=True, exist_ok=True)

        self.data_entries = self.__parse_data_entries(self.data_paths)
