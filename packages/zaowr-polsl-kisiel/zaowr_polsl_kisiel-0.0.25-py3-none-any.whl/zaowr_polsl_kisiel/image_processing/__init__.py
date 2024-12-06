"""
The `image_processing` module provides utilities for processing images
after camera calibration.

Functions:

- `remove_distortion`: Removes distortion from a single image using calibration parameters.

- `stereo_rectify`: Rectifies a stereo image pair after stereo calibration.

Usage:
Import this module for image distortion correction and stereo rectification.
"""

__all__ = [
    "remove_distortion",
    "stereo_rectify",
]

from .remove_distortion import remove_distortion # remove distortion from single image
from .stereo_rectify import stereo_rectify # rectify stereo image after stereo calibration