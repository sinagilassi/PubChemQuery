# APP
# ----

# import packages/modules
import re
# local
from .docs import PubChemAPI
from .docs import __version__


def main():
    print(f'PubChemQuery {__version__}')


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
        res = res if len(res) == 0 else []
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


def get_image_by_cid(cid, image_format='2d', image_size='small'):
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


def get_image_by_name(name, image_format='2d', image_size='small'):
    '''
    Get compound structure image

    Parameters
    ----------
    name : str
        compound name (IUPACName)
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


def compound(id: str, image_format='2d', image_size='small'):
    '''
    make a compound by cid, then get its information

    Parameters
    ----------
    id: str or int
        compound cid or name (https://pubchem.ncbi.nlm.nih.gov/)

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
            # update img
            img = PubChemAPI.get_structure_image(
                cid=int(cid), image_format=image_format, image_size=image_size)
            # update img prop
            compound_obj.image = img
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
                # check
                if compound_obj:
                    # update properties
                    compound_obj.update_properties()
                # image
                img = PubChemAPI.get_structure_image(
                    name=name, image_format=image_format, image_size=image_size)
                # update img
                compound_obj.image = img
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
