"""
junit_xml_parser.py - A parser for JUnit XML files.
"""

import pathlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List

from dacite import from_dict

from kakkerlak.kakkerlak import DataEntry, DataGroup


@dataclass
class JunitTestsuite:
    name: str = ""
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    assertions: int = 0
    time: float = 0.0
    timestamp: str = ""


@dataclass
class JunitTestsuites:
    name: str = ""
    tests: int = 0
    failures: int = 0
    errors: int = 0
    skipped: int = 0
    assertions: int = 0
    time: float = 0.0
    timestamp: str = ""  # ISO 8601 format

    testsuites: List[JunitTestsuite] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "JunitTestsuites":
        return from_dict(data_class=cls, data=data)


def parse_junit_xml(file_path: pathlib.Path) -> DataGroup:
    """
    Parse a JUnit XML file and return a DataGroup object.

    :param file_path: Path to the JUnit XML file.
    :return: JunitTestsuites object containing parsed data.
    """
    data_group: DataGroup = DataGroup()

    tree = ET.parse(file_path)
    root = tree.getroot()

    testsuites_data: dict = {
        "name": root.get("name", ""),
        "tests": int(root.get("tests", 0)),
        "failures": int(root.get("failures", 0)),
        "errors": int(root.get("errors", 0)),
        "skipped": int(root.get("skipped", 0)),
        "assertions": int(root.get("assertions", 0)),
        "time": float(root.get("time", 0.0)),
        "timestamp": root.get("timestamp", ""),
        "testsuites": [],
    }

    return data_group
