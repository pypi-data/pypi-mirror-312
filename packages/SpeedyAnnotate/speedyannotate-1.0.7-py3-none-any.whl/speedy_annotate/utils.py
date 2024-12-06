"""
utils.py - Utility functions for the SpeedyAnnotate package.

This module contains utility functions used throughout the Speedy Annotate package.
"""

import yaml
import os
from typing import Dict, Union, Any, Optional, Tuple, List, Collection
from PyQt6.QtCore import *
import numpy as np
from PIL import Image
import glob
import pandas as pd
import logging
from logging import FileHandler, StreamHandler
import sys


class Connection:
    """
    A class to manage a single connection between a signal and a slot in a Qt application.
    """
    def __init__(self, signal: pyqtSignal, slot: callable):
        self.signal: pyqtSignal = signal
        self.slot: callable = slot
        self.connection = self.signal.connect(self.slot)

    def disconnect(self):
        """
        Disconnects the signal from the slot.
        """
        self.signal.disconnect(self.slot)


class ConnectionManager:
    """
    A class to manage multiple connections between signals and slots in a Qt application.
    """
    def __init__(self):
        self.connections = {}

    def connect(self, signal: Any, slot: callable):
        """
        Connects a signal to a slot and stores the connection in a dictionary.

        :param signal: QtCore.pyqtSignal, the signal to connect.
        :param slot: callable, the slot (function or method) to connect to the signal.
        """
        connection = Connection(signal, slot)
        self.connections[id(connection)] = connection

    def disconnect_all(self):
        """
        Disconnects all connections and clears the dictionary.
        """
        for connection in self.connections.values():
            if isinstance(connection, Connection):
                connection.disconnect()
        self.connections = {}


def find_relative_image_path(
        base_path: str,
        extensions: Collection[str] = ('png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif', 'dcm', 'dicom',)
) -> List[str]:
    """
    Recursively find all image files in a given directory and return their relative paths.

    :param base_path: The path to the directory to search.
    :param extensions: A list of file extensions to consider as image files. Default is ['png', 'jpg', 'jpeg', 'gif',
        'bmp', 'tiff', 'tif', 'dcm', 'dicom',].
    :return: A list of relative paths pointing to the image files.
    """
    all_images = []
    for extension in extensions:
        for image_path in glob.glob(f"{base_path}/**/*.{extension}", recursive=True):
            relative_path = os.path.relpath(image_path, start=base_path)
            all_images.append(relative_path)

    return all_images


def open_yml_file(
    config_path: str,
    app_mode: str,
    config_dir: str
) -> Dict:
    """
    Opens a config .yml file and returns the data. If the file does not exist, it will look
    for the default config file, otherwise, it will create a new default config file.

    :param config_path: str, the path to the config file.
    :param app_mode: str, the application mode.
    :param config_dir: str, the path to the resource directory.
    :return: dict, the loaded configuration data from the YAML file.
    """
    # print("*"*50)
    # print("Resource directory:", resource_dir)
    # print("*"*50)

    if not os.path.isfile(os.path.normpath(config_path)):
        # If the config file does not exist, look for the default config file
        print(f"Could not find config file at {os.path.normpath(config_path)}")
        if os.path.isfile(os.path.join(config_dir, 'config.yml')):
            print(f"Using default config file at "
                  f"{os.path.join(config_dir, 'config.yml')}")
            config_path = os.path.join(config_dir, 'config.yml')
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        else:
            # If the default config file does not exist, create a new one
            print(f"Could not find default config file at {os.path.join(config_dir, 'config.yml')}")
            print(f"Creating a new default config file at "
                  f"{os.path.join(config_dir, 'config.yml')}")
            config_data = create_default_config(app_mode, config_dir)
    else:
        # Open the config file and load the data
        with open(os.path.normpath(config_path), 'r') as f:
            config_data = yaml.safe_load(f)

    return config_data


def create_default_config(
    app_mode: str,
    resource_dir: str
) -> Dict:
    """
    Creates a default config file in the speedy_qc directory.

    :return: dict, the default configuration data.
    """
    if app_mode == 'speedy_iqa':
        default_config = {
            # 'checkboxes': ['QC1', 'QC2', 'QC3', 'QC4', 'QC5'],
            'radiobuttons_page1': [{'title': "Overall Quality", 'labels': [1, 2, 3, 4]}, ],
            'radiobuttons_page2': [
                {'title': "Contrast", 'labels': [1, 2, 3, 4]},
                {'title': "Noise", 'labels': [1, 2, 3, 4]},
                {'title': "Artefacts", 'labels': [1, 2, 3, 4]},
            ],
            # 'tristate_checkboxes': True,
            'task': 'General use',
        }
    else:
        default_config = {
            'checkboxes': [
                'QC1', 'QC2', 'QC3', 'QC4', 'QC5'
            ],
            'radiobuttons': [{'title': "Radiobuttons", 'labels': [1, 2, 3, 4]}, ],
            'tristate_checkboxes': True,
        }

    default_config['app_mode'] = app_mode
    default_config['backup_dir'] = os.path.normpath(os.path.abspath(os.path.expanduser('~/speedy_annotate/backups')))
    default_config['log_dir'] = os.path.normpath(os.path.abspath(os.path.expanduser('~/speedy_annotate/logs')))
    default_config['backup_interval'] = 5
    default_config['max_backups'] = 10

    save_path = os.path.normpath(os.path.join(resource_dir, 'config.yml'))

    # Save the default config to the speedy_qc directory
    with open(save_path, 'w') as f:
        yaml.dump(default_config, f)

    return default_config


def setup_logging(log_out_path: str) -> Tuple[logging.Logger, logging.Logger]:
    """
    Sets up the logging for the application. Creates two loggers: one for logging to a file and another for console
    output. Changed from using a .conf file due to issues with making it OS-agnostic.

    :param log_out_path: The path to the directory where the log file will be saved. :param resource_directory: The
        path to the resource directory, not directly used here but can be utilized for additional configurations.
    :return: A tuple (file_logger, console_logger), where file_logger is configured to log to a file,
        and console_logger is configured for console output.
    """
    full_log_file_path = os.path.normpath(os.path.expanduser(os.path.join(log_out_path, "speedy_iqa.log")))
    os.makedirs(os.path.dirname(full_log_file_path), exist_ok=True)

    # Configure logger for file output
    file_logger = logging.getLogger('fileLogger')
    file_logger.setLevel(logging.DEBUG)
    file_logger.propagate = False
    fileHandler = FileHandler(full_log_file_path, mode='a')
    fileHandler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    )
    file_logger.addHandler(fileHandler)

    # Configure logger for console output
    console_logger = logging.getLogger('consoleLogger')
    console_logger.setLevel(logging.DEBUG)
    console_logger.propagate = False
    consoleHandler = StreamHandler(sys.stdout)
    consoleHandler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    )
    console_logger.addHandler(consoleHandler)

    return file_logger, console_logger


def bytescale(
        arr: np.ndarray,
        low: Optional[float] = None,
        high: Optional[float] = None,
        a: float = 0,
        b: float = 255
) -> np.ndarray:
    """
    Linearly rescale values in an array. By default, it scales the values to the byte range (0-255).

    :param arr: The array to rescale.
    :type arr: np.ndarray
    :param low: Lower boundary of the output interval. All values smaller than low are clipped to low.
    :type low: float
    :param high: Upper boundary of the output interval. All values larger than high are clipped to high.
    :type high: float
    :param a: Lower boundary of the input interval.
    :type a: float
    :param b: Upper boundary of the input interval.
    :type b: float
    :return: The rescaled array.
    :rtype: np.ndarray
    """

    arr = arr.astype(float)  # to ensure floating point division

    # Clip to specified high/low values, if any
    if low is not None:
        arr = np.maximum(arr, low)
    if high is not None:
        arr = np.minimum(arr, high)

    min_val, max_val = np.min(arr), np.max(arr)

    if np.isclose(min_val, max_val):  # avoid division by zero
        return np.full_like(arr, a, dtype=np.uint8)

    # Normalize between a and b
    return (((b - a) * (arr - min_val) / (max_val - min_val)) + a).astype(np.uint8)


def bytescale_v2(
        arr: np.ndarray,
        low: Optional[float] = None,
        high: Optional[float] = None,
        a: float = 0,
        b: float = 255,
        dtype: Optional[np.dtype] = None
) -> np.ndarray:
    """
    Linearly rescale values in an array without forcing the output into an 8-bit array. By default, scales to the
    range [0, 255].

    :param arr: The array to rescale.
    :param low: Lower boundary of the output interval. All values smaller than low are clipped to low.
    :param high: Upper boundary of the output interval. All values larger than high are clipped to high.
    :param a: Lower boundary of the rescaled interval.
    :param b: Upper boundary of the rescaled interval.
    :param dtype: Optional dtype for the output array. If None, the input array's dtype is preserved.
    :return: The rescaled array.
    """
    arr = arr.astype(float)  # Ensure floating point operations

    # Clip to specified low/high values, if any
    if low is not None:
        arr = np.maximum(arr, low)
    if high is not None:
        arr = np.minimum(arr, high)

    min_val, max_val = np.min(arr), np.max(arr)

    if np.isclose(min_val, max_val):  # Avoid division by zero
        return np.full_like(arr, a, dtype=dtype or arr.dtype)

    # Normalize to [a, b]
    scaled = (((b - a) * (arr - min_val) / (max_val - min_val)) + a)

    # Cast to the specified dtype or preserve input dtype
    return scaled.astype(dtype or arr.dtype)


def convert_to_checkstate(value: int) -> Qt.CheckState:
    """
    Converts an integer value to a Qt.CheckState value for tri-state checkboxes.

    :param value: int, the value to convert.
    :type: int
    :return: The converted value.
    :rtype: Qt.CheckState
    """
    if int(value) == 0:
        return Qt.CheckState.Unchecked
    elif int(value) == 1:
        return Qt.CheckState.PartiallyChecked
    elif int(value) == 2:
        return Qt.CheckState.Checked
    else:
        raise("Invalid value for tri-state checkbox:", value)


def create_icns(
        png_path: str,
        icns_path: str,
        sizes: Optional[Union[Tuple[int], List[int]]] = (16, 32, 64, 128, 256, 512, 1024)
):
    """
    Create a .icns file from a .png file.

    :param png_path: Path to the .png file.
    :param icns_path: Path to save the .icns file.
    :param sizes: Tuple or list of sizes to include in the .icns file. Default is (16, 32, 64, 128, 256
        512, 1024).
    """

    img = Image.open(png_path)
    icon_sizes = []

    for size in sizes:
        # Resize while maintaining aspect ratio (thumbnail method maintains aspect ratio)
        copy = img.copy()
        copy.thumbnail((size, size))

        # Create new image and paste the resized image into it, centering it
        new_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        new_image.paste(copy, ((size - copy.width) // 2, (size - copy.height) // 2))

        icon_sizes.append(new_image)

    if icns_path.endswith('.icns'):
        icns_path = icns_path[:-5]

    # Save the images as .icns
    icon_sizes[0].save(f'{icns_path}.icns', format='ICNS', append_images=icon_sizes[1:])


def invert_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Invert a grayscale image.

    :param image: The grayscale image to invert.
    :return: The inverted image.
    """
    return np.max(image) + np.min(image) - image


def expand_dict_column(df: pd.DataFrame, column_name: str) -> Tuple[pd.DataFrame, List[str]]:
    """
    Expand a column containing dictionaries into new columns.

    :param df: DataFrame containing the dictionary column.
    :param column_name: Name of the column to expand.
    :return: DataFrame with expanded columns and a list of the new column names.
    """
    # Use apply to create a new DataFrame with the expanded columns
    expanded_df = df[column_name].apply(pd.Series)

    # Concatenate the expanded DataFrame with the original DataFrame
    result_df = pd.concat([df, expanded_df], axis=1)

    # Drop the original dictionary column
    result_df.drop(column_name, axis=1, inplace=True)

    new_columns = expanded_df.columns

    for col in new_columns:
        result_df = result_df.rename(columns={col: col.lower().replace(" ", "_")})
    new_columns = [col.lower().replace(" ", "_") for col in new_columns]

    return result_df, new_columns


def make_column_categorical(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Convert a column with float values to categorical values '1', '2', '3', '4', and 'Blank'.

    :param df: DataFrame containing the column to convert.
    :param column_name: Name of the column to make categorical.
    :return: DataFrame with the specified column as categorical.
    """
    # Define the bin edges for categorization
    bin_edges = [0, 1, 2, 3, 4, np.inf]

    # Define labels for each category
    labels = ['1', '2', '3', '4', 'Blank']

    # Use pd.cut() to categorize the values
    df[column_name] = pd.cut(df[column_name], bins=bin_edges, labels=labels, right=False)

    return df


def generate_image_variants(img_array: np.ndarray, output_folder: str):
    """
    Generate image variants with different data types and save them to the output folder.

    :param img_array: Input image as a NumPy array.
    :param output_folder: Path to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define data type ranges
    dtype_ranges = {
        "uint8": (0, 255, np.uint8),
        "int8": (-128, 127, np.int8),
        "uint16": (0, 65535, np.uint16),
        "int16": (-32768, 32767, np.int16),
        "uint32": (0, 4294967295, np.uint32),
        "int32": (-2147483648, 2147483647, np.int32),
        "float32": (0.0, 1.0, np.float32),
        "float64": (0.0, 1.0, np.float64),
    }

    for dtype, (a, b, dt) in dtype_ranges.items():
        if "int" in dtype and dtype != "uint8":
            # Signed integers: Shift and normalize to [0, full_range]
            shift = abs(a)
            shifted_array = img_array + shift  # Shift to make all values non-negative
            normalized_array = bytescale_v2(shifted_array, a=0, b=255, dtype=np.uint8)

            # Debugging step
            print(f"{dtype}: Min={shifted_array.min()}, Max={shifted_array.max()}, Unique={len(np.unique(shifted_array))}")
        else:
            # Unsigned integers and floating points
            normalized_array = bytescale_v2(img_array, a=a, b=b, dtype=dt)

            # Debugging step
            print(f"{dtype}: Min={normalized_array.min()}, Max={normalized_array.max()}, Unique={len(np.unique(normalized_array))}")

        # Save the visualized image
        output_path = os.path.join(output_folder, f"{dtype}.tiff")
        Image.fromarray(normalized_array).save(output_path)
        print(f"Saved {dtype} image at {output_path}")
