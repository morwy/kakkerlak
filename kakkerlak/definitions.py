"""
definitions.py - Definitions for the Kakkerlak application.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


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


@dataclass
class DataEntry:
    """
    A class representing a data entry.
    """

    name: str = ""


@dataclass
class DataGroup:
    """
    A class representing a group of data entries.
    """

    name: str = ""
    properties: dict | None = None
    entries: List[DataEntry] | None = None
