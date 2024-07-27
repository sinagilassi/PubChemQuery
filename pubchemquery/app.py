# APP
# ----

# import packages/modules
import os
import json
# local
from .docs import PubChemAPI
from .docs import __version__


def get_cid_by_name(name) -> list[str]:
    '''
    Get a cid by name
    for instance, benzene cid

    Parameters
    ----------
    name : str
        compound name (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    list
        cid list 
    '''
    try:
        return PubChemAPI.get_cid_by_name(name, name_type='complete')
    except Exception as e:
        print(e)


def get_cids_by_name(name) -> list[str]:
    '''
    Get a cid list by name
    for instance, all cids have a hydroxyl functional group

    Parameters
    ----------
    name : str
        compound name (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    list
        cid list 
    '''
    try:
        return PubChemAPI.get_cid_by_name(name, name_type='word')
    except Exception as e:
        print(e)


def get_2d_image_by_cid(cid, image_size='small'):
    '''
    Get compound structure image

    Parameters
    ----------
    cid : str,int
        compound id
    image_size : str
        small, large, 250x250

    Returns
    -------
    Image
        image
    '''
    try:
        return PubChemAPI.get_structure_image_2d(cid=cid, image_size=image_size)
    except Exception as e:
        print(e)


def compound(cid=0, name=''):
    '''
    make a compound by cid, then get its information

    Parameters
    ----------
    cid : str
        compound id (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    object
        compound object
    '''
    try:
        # compound obj
        if cid != 0:
            # name
            compound_name = PubChemAPI.get_properties_by_cid(
                cid, ['IUPACName'])
            compound_obj = PubChemAPI(cid, compound_name)
        return compound_obj
    except Exception as e:
        print(e)
