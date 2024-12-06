import gzip
import json
import os
import pickle
import sys
import threading
from typing import Union


class File:

    def __init__(self, file_path: str):
        """
        Initializes the File class object. Returns FileNotFoundError if file does not exist.

        :param file_path: Absolute path to file.
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File {file_path} does not exist. If you are passing a relative path, please pass the absolute path.")

        self.file_dir, self.file_name = os.path.split(file_path)
        self.file_ext = os.path.splitext(self.file_name)[1].lower()

    def read(self, mode: str = 'r', encoding: str = 'utf-8') -> Union[str, bytes]:
        """
        Reads the content of file. Returns a string or bytes.

        :param mode: Mode to open the file. Defaults to 'r'.
        :param encoding: Encoding mode. Defaults to 'utf-8'.
        """
        if self.file_ext in ['.gz', '.gzip']:
            with gzip.open(self.file_path, mode, encoding=encoding) as file:
                return file.read()
        elif self.file_ext == '.json':
            with open(self.file_path, mode, encoding=encoding) as file:
                return json.load(file)
        elif self.file_ext == '.pickle':
            with open(self.file_path, mode, encoding=encoding) as file:
                return pickle.load(file)
        else:
            with open(self.file_path, mode, encoding=encoding) as file:
                return file.read()

    def write(self, data: Union[str, bytes], mode: str = 'w', encoding: str = 'utf-8'):
        """
        Writes the content of file. Returns a string or bytes.

        :param data: Data to write to the file.
        :param mode: Mode to open the file. Defaults to 'w'.
        :param encoding: Encoding mode. Defaults to 'utf-8'.
        """
        if self.file_ext in ['.gz', '.gzip']:
            with gzip.open(self.file_path, mode, encoding=encoding) as file:
                file.write(data)
        elif self.file_ext == '.json':
            with open(self.file_path, mode, encoding=encoding) as file:
                json.dump(data, file)
        elif self.file_ext == '.pickle':
            with open(self.file_path, mode, encoding=encoding) as file:
                pickle.dump(data, file)
        else:
            with open(self.file_path, mode, encoding=encoding) as file:
                file.write(data)

    def append(self, data: Union[str, bytes], encoding: str = 'utf-8'):
        self.write(data, mode='a', encoding=encoding)

    def __str__(self):
        return f'File: {self.file_path}'

    def __repr__(self):
        return f'File({self.file_path})'


class ProgressPercentage:
    """
    Callback function to show progress of file upload.
    """

    def __init__(self, filename):
        """
        Initialize ProgressPercentage object.
        :param filename: Name of the file
        """
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """
        Show progress of file upload. To simplify, assume this is hooked up to a single filename
        :param bytes_amount: Bytes uploaded
        """
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s Bytes (%.2f%%)" % (self._filename, self._seen_so_far, self._size, percentage))
            sys.stdout.flush()
