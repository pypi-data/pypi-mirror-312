from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Any

from ..exceptions.exceptions import StereoCalibrationParamsPathNotProvided, CalibrationParamsWrongFormat

from json import load as jload
from numpy import array as npArray
from numpy import ndarray as npNdArray

# To avoid creating a class at runtime, for type-hinting alone.
if TYPE_CHECKING:
    # Map the `dict` fields here
    class StereoCalibrationParams(TypedDict):
        reprojectionError: float
        fov_left: tuple[float, float]
        fov_right: tuple[float, float]
        baseline: float
        cameraMatrix_left: npNdArray
        distortionCoefficients_left: npNdArray
        cameraMatrix_right: npNdArray
        distortionCoefficients_right: npNdArray
        rotationMatrix: npNdArray
        translationVector: npNdArray
        essentialMatrix: npNdArray
        fundamentalMatrix: npNdArray


def load_stereo_calibration(calibrationParamsPath: str) -> StereoCalibrationParams:
    """
    Load the stereo camera calibration from a specified JSON file.

    :param str calibrationParamsPath: Path to the JSON calibration file.
    :return:
        StereoCalibrationParams - A dictionary containing the stereo calibration parameters, which includes:
        - **reprojectionError** (float): RMS re-projection error indicating the calibration accuracy.\n
        - **fov_left** (tuple[float, float]): Horizontal and vertical FOV for the left camera in degrees.
        - **fov_right** (tuple[float, float]): Horizontal and vertical FOV for the right camera in degrees.
        - **baseline** (float): Distance between the two camera centers, crucial for depth estimation.
        - **cameraMatrix_left** (np.ndarray): Intrinsic camera matrix for the left camera.
        - **distortionCoefficients_left** (np.ndarray): Distortion coefficients for the left camera.
        - **cameraMatrix_right** (np.ndarray): Intrinsic camera matrix for the right camera.
        - **distortionCoefficients_right** (np.ndarray): Distortion coefficients for the right camera.
        - **rotationMatrix** (np.ndarray): Rotation matrix aligning the right camera's coordinate system to the left.
        - **translationVector** (np.ndarray): Translation vector defining the relative position of the right camera to the left.
        - **essentialMatrix** (np.ndarray): Encodes rotation and translation between the cameras for 3D reconstruction.
        - **fundamentalMatrix** (np.ndarray): Relates corresponding points in the left and right images.

    :raises StereoCalibrationParamsPathNotProvided: If the path is missing or not a string.
    :raises CalibrationParamsWrongFormat: If the calibration file is not in the correct format or parameters are empty.
    """
    # Check if the provided path is valid
    if not calibrationParamsPath or not isinstance(calibrationParamsPath, str):
        raise StereoCalibrationParamsPathNotProvided("Path must be a non-empty string.")

    with open(calibrationParamsPath, "r") as file:
        jsonDump = jload(file)

    try:
        reprojectionError = jsonDump["reprojectionError"]
        fov_left = tuple(jsonDump["fov_left"])
        fov_right = tuple(jsonDump["fov_right"])
        baseline = jsonDump["baseline"]
        cameraMatrix_left = npArray(jsonDump["cameraMatrix_left"])
        distortionCoefficients_left = npArray(jsonDump["distortionCoefficients_left"])
        cameraMatrix_right = npArray(jsonDump["cameraMatrix_right"])
        distortionCoefficients_right = npArray(jsonDump["distortionCoefficients_right"])
        rotationMatrix = npArray(jsonDump["rotationMatrix"])
        translationVector = npArray(jsonDump["translationVector"])
        essentialMatrix = npArray(jsonDump["essentialMatrix"])
        fundamentalMatrix = npArray(jsonDump["fundamentalMatrix"])

        # Validate each field with proper checks
        if not isinstance(reprojectionError, float):
            raise CalibrationParamsWrongFormat

        if not isinstance(fov_left, tuple) or len(fov_left) != 2 or not all(isinstance(f, float) for f in fov_left):
            raise CalibrationParamsWrongFormat

        if not isinstance(fov_right, tuple) or len(fov_right) != 2 or not all(isinstance(f, float) for f in fov_right):
            raise CalibrationParamsWrongFormat

        if not isinstance(baseline, float):
            raise CalibrationParamsWrongFormat

        if (not cameraMatrix_left.size) or not isinstance(cameraMatrix_left, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not distortionCoefficients_left.size) or not isinstance(distortionCoefficients_left, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not cameraMatrix_right.size) or not isinstance(cameraMatrix_right, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not distortionCoefficients_right.size) or not isinstance(distortionCoefficients_right, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not rotationMatrix.size) or not isinstance(rotationMatrix, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not translationVector.size) or not isinstance(translationVector, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not essentialMatrix.size) or not isinstance(essentialMatrix, npNdArray):
            raise CalibrationParamsWrongFormat

        if (not fundamentalMatrix.size) or not isinstance(fundamentalMatrix, npNdArray):
            raise CalibrationParamsWrongFormat

        # Return the validated parameters in a descriptive structure
        return {
            "reprojectionError": reprojectionError,
            "fov_left": fov_left,
            "fov_right": fov_right,
            "baseline": baseline,
            "cameraMatrix_left": cameraMatrix_left,
            "distortionCoefficients_left": distortionCoefficients_left,
            "cameraMatrix_right": cameraMatrix_right,
            "distortionCoefficients_right": distortionCoefficients_right,
            "rotationMatrix": rotationMatrix,
            "translationVector": translationVector,
            "essentialMatrix": essentialMatrix,
            "fundamentalMatrix": fundamentalMatrix,
        }

    except KeyError as e:
        raise CalibrationParamsWrongFormat(f"Missing key in JSON data: {e}")
