"""
logger.py - A simple logger for the Kakkerlak application.
"""

import logging

logger = logging.getLogger("kakkerlak")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
