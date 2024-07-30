# PubChemQuery

![Downloads](https://img.shields.io/pypi/dm/PubChemQuery) ![PyPI](https://img.shields.io/pypi/v/PubChemQuery) ![Python Version](https://img.shields.io/pypi/pyversions/PubChemQuery.svg) ![License](https://img.shields.io/pypi/l/PubChemQuery) ![Coverage](https://codecov.io/gh/sinagilassi/PubChemQuery/branch/main/graph/badge.svg)

**PubChemQuery:** A Python Package for Accessing Chemical Information from PubChem

PubChemQuery is a Python package that provides a simple and intuitive API for retrieving chemical information from the PubChem database. With this package, you can easily fetch chemical data, including:

* CID (Compound ID) by name
* All CIDs by name
* 2D images by CID or name
* SDF (Structure Data File) by CID or name
* Compound properties, including:
    - Molecular formula and weight
    - SMILES and InChI representations
    - IUPAC name and title
    - Physicochemical properties (e.g., XLogP, exact mass, TPSA)
    - Structural features (e.g., bond and atom counts, stereochemistry)
    - 3D properties (e.g., volume, steric quadrupole moments, feature counts)
    - Fingerprint and conformer information

The package offers a straightforward interface, allowing users to access PubChem data with minimal code. Whether you're a chemist, researcher, or developer, PubChemQuery simplifies the process of integrating chemical information into your projects.

**Key Features:**

Retrieve chemical data by name or CID
Access 2D images and SDF files
Get compound properties, including physicochemical, structural, and 3D features
Easy-to-use API with minimal code required

**Simple and Concise API:**

There are only 7 functions that perform all of the above-mentioned tasks, making it easy to integrate PubChem data into your projects:

* get_cid_by_name(name): Get CID by name
* get_cids_by_name(name): Get all CIDs by name
* get_image_by_cid(cid): Get 2D image by CID
* get_image_by_name(name): Get 2D image by name
* get_structure_by_cid(cid): Get SDF by CID
* get_structure_by_name(name): Get SDF by name
* compound(cid_or_name): Create a compound object with properties and methods

**Getting Started:**

To use PubChemQuery, simply install the package and import it into your Python script. Refer to the example code snippets above for a quick start.

## Installation

Install PubChemQuery with pip

```python
  pip install pubchemquery
```

## Documentation

```python
import pubchemquery as pcq

# get a cid by name
cid = pcq.get_cid_by_name('benzene')
print(cid)

# get all cids by name
cids = pcq.get_cids_by_name('benzene')
print(type(cids), len(cids))

# get 2d image
image = pcq.get_image_by_cid('241')
print(image)

image = pcq.get_image_by_name('benzene')
print(image)

# get sdf by cid
sdf = pcq.get_structure_by_cid('241')
print(sdf)

# get sdf by name
sdf = pcq.get_structure_by_name('benzene')
print(sdf)

# make a compound by cid
cid = 2244
compound = pcq.compound(cid)
# name
name = '2-acetyloxybenzoic acid'
compound = pcq.compound(name)
print(compound)
# properties
print(compound.InChI)
print(compound.InChIKey)
print(compound.IUPACName)
print(compound.image)
```

## FAQ

For any question, contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/) 


## Authors

- [@sinagilassi](https://www.github.com/sinagilassi)
