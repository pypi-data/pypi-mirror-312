"""
This package provides tools and utilities for camera calibration, stereo calibration,
image processing, and related operations.

Modules:

- `calibration`: Tools for camera and stereo calibration.

- `content_loaders`: Functions to load and validate calibration data from files.

- `exceptions`: Custom exceptions for error handling.

- `image_processing`: Utilities for image rectification and distortion removal.

- `tools`: Additional tools, such as ArUco dictionary identification.

Status: Development

Year of development: 2024

Author: Maksymilian Kisiel

Institution: Silesian University of Technology

Faculty: Faculty of Automatic Control, Electronics and Computer Science

Major: Informatics, master degree

Specialization: Interactive Three-Dimensional Graphics (IGT, pol. Interaktywna Grafika Trójwymiarowa, https://www.polsl.pl/rau6/en/igt-specjalization/)
"""

__version__ = "0.0.23"
__status__ = "Development"  # Allowed: "Prototype", "Beta", "Stable"

__all__ = [
    "calibration",
    "content_loaders",
    "exceptions",
    "image_processing",
    "tools",
]

# IMPORT SUBMODULES
from .calibration import (
    calibrate_camera, # calibrate single camera
    stereo_calibration, # stereo calibration
    calculate_fov, # calculate fov - horizontal and vertical
)

from .exceptions import exceptions # exceptions

from .content_loaders import (
    are_params_valid, # validate calibration parameters stored in files and return them if valid
    save_calibration, # save calibration parameters (used for all types of params - single, stereo, rectification)
    load_calibration, # load calibration parameters for single camera
    load_stereo_calibration, # load stereo calibration
    load_rectification_maps, # load rectification maps
)

from .image_processing import (
    remove_distortion, # remove distortion from single image
    stereo_rectify, # rectify stereo image after stereo calibration
)

from .tools import (
    find_aruco_dict # find aruco dictionary if we don't know
)

