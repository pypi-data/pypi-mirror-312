"""
The `tools` module contains additional utilities for specific tasks.

Functions:

- `find_aruco_dict`: Identifies the ArUco dictionary used in marker detection.

Usage:
Use this module for miscellaneous tools that enhance functionality.
"""

__all__ = [
    "find_aruco_dict",
]

from .find_aruco_dict import find_aruco_dict # find aruco dictionary if we don't know it