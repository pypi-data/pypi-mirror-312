"""Constant values used in the package."""

import os

ENCODING = "utf-8"
DOC_FILENAME_PATTERN = r"^(eip|erc)\-(\d+).md$"
IGNORE_FILES = []
IGNORE_EIP_ATTRS = ["raw"]
IGNORE_EIP_ATTR_TYPES = ["<class 'function'>", "<class 'method'>"]
# TODO: Support more systems?
DATA_PATH = os.environ.get("EIPS_DATA_PATH", "~/.config/eips")
REPO_DIR = "repo"
EIPS_DIR = "EIPS"
ERCS_DIR = "ERCS"
