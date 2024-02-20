from typing import List
from setuptools import setup,find_packages
import setuptools




PROJECT_NAME = "Housing-Predictor"
VERSION = "0.0.4"
AUTHOR = "Moosa Shaik"
DESCRIPTION = "This is my first Machine Learning project"

REQUIREMENT_FILE_NAME = "requirements.txt"

HYPHEN_E_DOT = "-e ."

def get_requirements_list() -> List[str]:
    """
    This function is going to return all the requirements used in this project
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list
        


setup(
name = PROJECT_NAME,
version = VERSION,
author = AUTHOR,
description = DESCRIPTION,
packages=find_packages(),
install_requires = get_requirements_list()
)