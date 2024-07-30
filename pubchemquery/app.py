# APP
# ----

# import packages/modules
import re
import time
# local
from .docs import PubChemAPI
from .docs import __version__


def main():
    print(f'PubChemQuery {__version__}')


def get_cid_by_inchi(inchi: str):
    '''
    Get a cid (only one) by inchi

    Parameters
    ----------
    inchi : str
        e.g. InChI=1S/C3H8/c1-3-2/h3H2,1-2H3

    Returns
    -------
    str
        cid
    '''
    try:
        res = PubChemAPI.get_cids_by_inchi(inchi)
        if len(res) == 0:
            return "Not Found!"
        res = res[0] if len(res) == 1 else res
        return res
    except Exception as e:
        print(e)


def get_cids_by_formula(formula):
    '''
    Get all cids by formula
    for instance, CH4

    Parameters
    ----------
    formula : str
        compound formula (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    str
        cid
    '''
    try:
        res = PubChemAPI.get_cids_by_formula(formula)
        if len(res) == 0:
            return "Not Found!"
        res = res[0] if len(res) == 1 else res
        return res
    except Exception as e:
        print(e)


def get_cid_by_name(name) -> str:
    '''
    Get a cid (only one) by name
    for instance, benzene cid

    Parameters
    ----------
    name : str
        compound name (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    str
        cid  
    '''
    try:
        res = PubChemAPI.get_cid_by_name(name, name_type='complete')
        res = res[0] if len(res) == 1 else "Not Found!"
        return res
    except Exception as e:
        print(e)


def get_cids_by_name(name) -> list[str]:
    '''
    Get a cid list by name (if available)
    for instance, all cids have a hydroxyl functional group

    Parameters
    ----------
    name : str
        compound name (https://pubchem.ncbi.nlm.nih.gov/)

    Returns
    -------
    list[str]
        cid list 
    '''
    try:
        res = PubChemAPI.get_cid_by_name(name, name_type='word')
        res = res if len(res) != 0 else []
        # log
        if len(res) == 0:
            print("Not Found!")
        return res
    except Exception as e:
        print(e)


def get_structure_by_cid(cid, file_format='SDF', record_type='3d', save_file=False, file_dir=''):
    '''
    Get a compound structure by cid

    Parameters
    ----------
    cid : int or str
        compound id
    file_format : str
        SDF, JSON
    record_type : str
        3d, 2d
    save_file : bool
        the sdf file is saved
    file_dir : str
        directory path, if it is empty, the current directory is selected.

    Returns
    -------
    str
        sdf string
    '''
    try:
        return PubChemAPI.get_sdf_by_cid(cid, file_format=file_format, record_type=record_type, save=save_file, location=file_dir)
    except Exception as e:
        print(e)


def get_similar_structures_cids_by_compound_id(val, compound_id='cid', similarity_type='fastsimilarity_2d') -> list:
    '''
    Get similar structures by cid

    Parameters
    ----------
    val : int or str
        compound id e.g. 297, 'C1=CC=CC=C1', 'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H'
    compound_id : str
        cid, SMILES, InChI (default: cid)
    similarity_type : str
        fastsimilarity_2d, fastsimilarity_3d (default: fastsimilarity_2d)

    Returns
    -------
    list[str]
        cid list
    '''
    try:
        res = PubChemAPI.get_similar_cids_by_compound_id(
            str(val), compound_id=compound_id, similarity_type=similarity_type)
        res = res if len(res) != 0 else []
        return res
    except Exception as e:
        print(e)


def get_structure_by_name(name, file_format='SDF', record_type='3d', save_file=False, file_dir=''):
    '''
    Get a compound structure by cid

    Parameters
    ----------
    name : str
        compound id
    file_format : str
        SDF, JSON
    record_type : str
        3d, 2d
    save_file : bool
        the sdf file is saved
    file_dir : str
        directory path, if it is empty, the current directory is selected.

    Returns
    -------
    str
        sdf string
    '''
    try:
        return PubChemAPI.get_sdf_by_name(name, file_format=file_format, record_type=record_type, save=save_file, location=file_dir)
    except Exception as e:
        print(e)


def get_image_by_cid(cid, image_format='2d', image_size='large'):
    '''
    Get compound structure image

    Parameters
    ----------
    cid : str,int
        compound id
    image_format : str
        3d, 2d (default: 2d)
    image_size : str
        small, large, 250x250

    Returns
    -------
    PIL.Image
        cid image
    '''
    try:
        return PubChemAPI.get_structure_image(cid=int(cid), image_format=image_format, image_size=image_size)
    except Exception as e:
        print(e)


def get_image_by_name(name, image_format='2d', image_size='large'):
    '''
    Get compound structure image

    Parameters
    ----------
    name : str
        compound name (IUPAC Name)
    image_format : str
        3d, 2d (default: 2d)
    image_size : str
        small, large, 250x250

    Returns
    -------
    PIL.Image
        cid image
    '''
    try:
        return PubChemAPI.get_structure_image(name=name, image_format=image_format, image_size=image_size)
    except Exception as e:
        print(e)


def compound(id: str, image_format='2d', image_size='large', similarity_type='fastsimilarity_2d'):
    '''
    make a compound by cid, then get its information

    Parameters
    ----------
    id: str or int
        compound cid or name (https://pubchem.ncbi.nlm.nih.gov/)
    image_format : str
        3d, 2d (default: 2d)
    image_size : str
        small, large, 250x250
    similarity_type : str
        fastsimilarity_2d, fastsimilarity_3d (default: fastsimilarity_2d)

    Returns
    -------
    object
        compound object with all properties
    '''
    try:
        # set
        cid = 0
        name = ''
        id = str(id)

        # check id is number
        pattern = re.compile(r'^\d+$')
        pattern_res = bool(pattern.match(id))

        if pattern_res is False:
            name = str(id).strip()
        else:
            cid = str(id)

        # compound obj
        if cid != 0:
            # check
            cid = str(cid).strip()
            # check compound name
            compound_obj = PubChemAPI(cid, '')
            # update properties
            compound_obj.update_properties()
            # sleep
            time.sleep(0.5)
            # update img
            img = PubChemAPI.get_structure_image(
                cid=int(cid), image_format=image_format, image_size=image_size)
            # update img prop
            compound_obj.image = img
            time.sleep(0.5)
            # search for similarities
            similar_cids = PubChemAPI.get_similar_cids_by_compound_id(
                cid, similarity_type=similarity_type)
            # update
            compound_obj.similar_structure_cids = similar_cids
            # return
            return compound_obj
        elif name != '':
            # check
            name = str(name).strip()
            # get cid
            _cid = PubChemAPI.get_cid_by_name(name, name_type='complete')
            # check
            if len(_cid) == 1:
                # update
                cid = str(_cid[0]).strip()
                # check compound name
                compound_obj = PubChemAPI(cid, name)
                # sleep
                time.sleep(0.5)
                # check
                if compound_obj:
                    # update properties
                    compound_obj.update_properties()
                # sleep
                time.sleep(0.5)
                # image
                img = PubChemAPI.get_structure_image(
                    name=name, image_format=image_format, image_size=image_size)
                # update img
                compound_obj.image = img
                # sleep
                time.sleep(0.5)
                # search for similarities
                similar_cids = PubChemAPI.get_similar_cids_by_compound_id(
                    cid, similarity_type=similarity_type)
                # update
                compound_obj.similar_structure_cids = similar_cids
                # return
                return compound_obj
            else:
                raise Exception(f"compound {name} not found!")
        else:
            raise Exception(f"{cid}/{name} format is not valid!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
