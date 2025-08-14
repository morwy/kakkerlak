"""
kakkerlak.py - A simple module for demonstration purposes
"""

import os
import pathlib
from typing import List

from .definitions import DataEntry, DataGroup, ExportType, ImportType
from .logger import logger
from .parsers.junit_xml_parser import parse_junit_xml


class Kakkerlak:
    def __init__(self):
        self.data_paths: List[pathlib.Path] = []
        self.data_entries: List[DataGroup] = []

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
        data_entries: List[DataGroup] = []

        for data_path in data_paths:
            data: DataGroup = DataGroup()

            if data_path.exists():
                input_type = self.__determine_input_type(data_path)
                if input_type == ImportType.JUNIT_XML:
                    data = parse_junit_xml(data_path)
                else:
                    logger.warning("Unsupported file type: %s", data_path)
                    continue

            else:
                logger.error("File does not exist: %s", data_path)
                raise FileNotFoundError(f"File does not exist: {data_path}.")

            data_entries.append(data)

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

        if path.exists():
            logger.warning("File already exists and will be overwritten: %s.", path)
            os.remove(path)

        self.data_entries = self.__parse_data_entries(self.data_paths)
