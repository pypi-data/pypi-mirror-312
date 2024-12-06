import setuptools

import pathlib

PROJECT_NAME = "benp_thou_pound"
VERSION = "0.0.1"
SHORT_DESCRIPTION = "A library for quick data analysis while watch shows with bariatric surgery."
SOURCE_CODE_LINK= "https://github.com/Ben-Payton/benp_thou_pound"
DOCUMENTATION_LINK = "https://github.com/Ben-Payton/benp_thou_pound/blob/main/README.md" 
REQUIRED_DEPENDANCIES = ["numpy","scipy","matplotlib","pandas"]


setuptools.setup(
    name = PROJECT_NAME,
    version = VERSION,
    description= SHORT_DESCRIPTION,
    long_description= pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author = "Ben Payton",
    project_urls = {
        "Documentation" : DOCUMENTATION_LINK,
        "Source" : SOURCE_CODE_LINK
    },
    install_requires = REQUIRED_DEPENDANCIES,
    packages=setuptools.find_packages()
    )
