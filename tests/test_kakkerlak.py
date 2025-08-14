"""
Tests for the Kakkerlak class.
"""

import os

from kakkerlak import Kakkerlak


def test_initial():
    kakkerlak = Kakkerlak()

    data_folder_path = os.path.join(
        os.path.dirname(__file__), "data", "146-lots-of-fails"
    )

    kakkerlak.add(data_folder_path)

    kakkerlak.export(
        os.path.join(os.path.dirname(__file__), "data", "146-lots-of-fails", "export")
    )

    assert True
