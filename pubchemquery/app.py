# APP
# ----

# import packages/modules
import os
import json
# local
from .docs import PubChemAPI
from .docs import __version__


def get_cid_by_name(name, name_type='word'):
    '''
    Get cid by name

    Parameters
    ----------
    name : str
        compound name (https://pubchem.ncbi.nlm.nih.gov/)
    name_type : str, optional
        word (small part of molecule), complete (exact molecule)

    Returns
    -------
    list
        cid list 
    '''
    try:
        return PubChemAPI.get_cid_by_name(name)
    except Exception as e:
        print(e)
