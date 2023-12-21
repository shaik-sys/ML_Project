from setuptools import setup,find_packages
from typing import List



PROJECT_NAME = "Housing-Predictor"
VERSION = "0.0.2"
AUTHOR = "Moosa Shaik"
DESCRIPTION = "This is my first Machine Learning project"
PACKAGES = ["housing"]
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list() -> List["str"]:
    """
    This function is going to return all the requirements used in this project
    """
    with open(REQUIREMENT_FILE_NAME) as file_name:
        return file_name.readlines().remove("-e .")


setup(
name = PROJECT_NAME,
version = VERSION,
author = AUTHOR,
description = DESCRIPTION,
package = find_packages(),
install_requires = get_requirements_list()
)