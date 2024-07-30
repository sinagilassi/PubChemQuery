from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

APP_NAME = 'PubChemQuery'
VERSION = '1.3.0'
DESCRIPTION = 'A Python Package for Accessing Chemical Information from PubChem (https://pubchem.ncbi.nlm.nih.gov/).'
LONG_DESCRIPTION = 'PubChemQuery is a Python package that provides a simple and intuitive API for retrieving chemical information from the PubChem database.'

# Setting up
setup(
    name=APP_NAME,
    version=VERSION,
    author="Sina Gilassi",
    author_email="<sina.gilassi@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    license='MIT',
    install_requires=['pandas', 'pillow', 'requests', 'urllib3'],
    keywords=['python', 'PubChem', 'PubChemAPI', 'PubChemQuery'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
