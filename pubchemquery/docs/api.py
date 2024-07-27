# API
# ----

# import packages/modules
import requests
import os
import json
import io
import time
from PIL import Image

# local
from .config import CID_FILE_PREFIX
from .util import UtilityAPI
from .util import CoreUtility


class PubChemAPI:
    '''
    load data from https://pubchem.ncbi.nlm.nih.gov/
    based on PUG REST
    '''
    _compound_cid = 0
    _compound_name = ''

    def __init__(self, compound_cid, compound_name):
        self._compound_cid = compound_cid
        self._compound_name = compound_name

    identity_mode = {
        0: 'same_connectivity',
        1: 'same_tautomer',
        2: 'same_stereo',
        3: 'same_isotope',
        4: 'same_stereo_isotope',
        5: 'nonconflicting_stereo',
        6: 'same_isotope_nonconflicting_stereo'
    }

    # property
    @property
    def compound_cid(self):
        return self._compound_cid

    @compound_cid.setter
    def compound_cid(self, value):
        self._compound_cid = value

    @property
    def compound_name(self):
        return self._compound_name

    @compound_name.setter
    def compound_name(self, value):
        self._compound_name = value

    @staticmethod
    def get_mat_by_cid(cid, file_format='JSON', record_type='3d', read=False, save=False, location=''):
        '''
        Query request by PUBCHEM_COMPOUND_CID

        Parameters
        ----------
        cid : str
            compound id (https://pubchem.ncbi.nlm.nih.gov/)
        file_format : str
            SDF, JSON
        record_type : str
            3d, 2d
        read : bool
            if read=False, return mat object
            if read=True, return mat string
        save : bool
            the sdf file is saved
        location : str
            directory path, if it is empty, the current directory is selected.


        return:
            mat string: if read=False,
            mat object: if read=True,

        '''
        try:
            if not file_format:
                raise Exception('file format is not set correctly.')

            if not record_type:
                raise Exception('record_type is not set correctly.')

            # check
            _file_format = file_format.capitalize()
            _cid = str(cid).strip()

            _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/{_file_format}?record_type={record_type}'

            if len(str(cid)) > 0:
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # print(reqResponse)
                if reqResponse == 200:
                    # content (string)
                    fileContent = res.text
                    # save a string file
                    fileName = UtilityAPI.SetName(cid)
                    fileFormat = file_format.lower()
                    fileLoc = os.path.join(location, fileName)

                    # check
                    if save is True:
                        # select file
                        if fileFormat == 'json':
                            # dict
                            fileSave = res.json()
                        else:
                            # string (sdf)
                            fileSave = fileContent

                        # save
                        _resStatus1 = CoreUtility.SaveFile(
                            fileSave, fileName, fileFormat, location)
                        if not _resStatus1:
                            raise Exception('error in saving the file')
                    # return
                    return fileContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_mat_by_cids(cids, file_format='JSON', record_type='3d', read=False, save=False, location=''):
        '''
        Query request by PUBCHEM_COMPOUND_CID

        Parameters
        ----------
        cids : list
            list of compound id (https://pubchem.ncbi.nlm.nih.gov/)
        file_format : str
            SDF, JSON
        record_type : str
            3d, 2d
        read : bool
            if read=False, return mat object
            if read=True, return mat string
        save : bool
            the sdf file is saved
        location : str
            directory path, if it is empty, the current directory is selected.

        Returns
        -------
        bool
            file content

        '''
        try:
            # check
            if not file_format:
                raise Exception('file format is not set correctly.')

            if not record_type:
                raise Exception('record_type is not set correctly.')

            # set time
            t1 = time.time()

            # check
            _file_format = file_format.capitalize()

            if len(cids) == 0:
                raise Exception('cid list is empty.')
            # size
            cidsSize = len(cids)
            # file list
            fileList = []
            # mat list
            matList = []
            # location
            _location = location.strip()
            isLocationExist = os.path.exists(_location)
            # check
            if not isLocationExist:
                raise Exception("file location does not exist.")

            for i in range(cidsSize):

                # manage request time
                time.sleep(0.5)

                _cid = str(cids[i]).strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/{_file_format}?record_type={record_type}'

                print(f"cid no. {i}: {_cid} at: {time.time()}")

                if len(_cid) > 0:
                    res = requests.get(_url)
                    # check
                    reqResponse = res.status_code
                    # print(reqResponse)
                    if reqResponse == 200:
                        # content (string)
                        fileContent = res.text
                        # save a string file
                        fileName = UtilityAPI.SetName(_cid)
                        fileFormat = file_format.lower()

                        # check
                        if save is True:
                            # select file
                            if fileFormat == 'json':
                                # dict
                                fileSave = res.json()
                            else:
                                # string (sdf)
                                fileSave = fileContent

                            _resStatus1 = CoreUtility.SaveFile(
                                fileSave, fileName, fileFormat, location)
                            if not _resStatus1:
                                raise Exception('error in saving the file')

                        # res
                        fileList.append(fileContent)
                    else:
                        raise Exception(
                            'request for {_cid} is refused, try again.')

            # set time
            t2 = time.time()
            elapsed = t2 - t1
            print('Elapsed time is %f seconds.' % elapsed)

            if read is True:
                return matList
            else:
                return fileList

        except Exception as e:
            print(e)

    @staticmethod
    def get_sdf_by_cid(cid, file_format='SDF', record_type='3d', read=False, save=False, location=''):
        '''
        Query request by PUBCHEM_COMPOUND_CID

        Parameters
        ----------
        cid : int
            compound id (https://pubchem.ncbi.nlm.nih.gov/)
        file_format : str
            SDF, JSON
        record_type : str
            3d, 2d
        read : bool
            if read=False, return mat object
            if read=True, return mat string
        save : bool
            the sdf file is saved
        location : str
            directory path, if it is empty, the current directory is selected.

        Returns
        -------
        bool
            file content
        '''
        try:
            _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/{file_format}?record_type={record_type}'

            if len(str(cid)) > 0:
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # print(reqResponse)
                if reqResponse == 200:
                    # content
                    sdfContent = res.text
                    # save a string file
                    fileName = f'cid_{str(cid)}.{file_format.lower()}'
                    fileLoc = os.path.join(location, fileName)

                    # check
                    if save is True:

                        file = open(fileLoc, 'w')
                        file.write(sdfContent)
                        file.close()
                        print(
                            f"SDF file is successfully created and saved in `{fileLoc}`")
                    # res
                    return sdfContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_sdf_by_cids(cids, record_type='3d', read=False, save=False, location=''):
        '''
        Query request by PUBCHEM_COMPOUND_CID

        Parameters
        ----------
        cids : list
            compound id (https://pubchem.ncbi.nlm.nih.gov/)
        record_type : str
            3d, 2d
        read : bool
            if read=False, return mat object
            if read=True, return mat string
        save : bool
            the sdf file is saved
        location : str

        Returns
        -------
        bool
            file content
        '''
        try:
            # set time
            t1 = time.time()

            if len(cids) == 0:
                raise Exception('cid list is empty.')
            # size
            cidsSize = len(cids)
            # sdf list
            sdfList = []
            # mat list
            matList = []
            # location
            _location = location.strip()
            isLocationExist = os.path.exists(_location)
            # check
            if not isLocationExist:
                raise Exception("file location does not exist.")

            for i in range(cidsSize):

                # manage request time
                time.sleep(0.5)

                _cid = str(cids[i]).strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/SDF?record_type={record_type}'

                print(f"cid no. {i}: {_cid} at: {time.time()}")

                if len(_cid) > 0:
                    res = requests.get(_url)
                    # check
                    reqResponse = res.status_code
                    # print(reqResponse)
                    if reqResponse == 200:
                        # content
                        sdfContent = res.text
                        # save a string file
                        fileName = 'cid_'+str(_cid)+'.sdf'
                        fileLoc = os.path.join(_location, fileName)

                        # check
                        if save is True:

                            file = open(fileLoc, 'w')
                            file.write(sdfContent)
                            file.close()
                            print(
                                f"SDF file is successfully created and saved in `{fileLoc}`")
                        # res
                        sdfList.append(sdfContent)
                    else:
                        raise Exception(
                            'request for {_cid} is refused, try again.')

            # set time
            t2 = time.time()
            elapsed = t2 - t1
            print('Elapsed time is %f seconds.' % elapsed)

            if read is True:
                return matList
            else:
                return sdfList

        except Exception as e:
            print(e)

    @staticmethod
    def get_sdf_by_name(name, record_type='3d', save=False, location=''):
        '''
        Query request by name

        Parameters
        ----------
        name : str
            compound name
        record_type : str
            3d, 2d
        save : bool
            the sdf file is saved
        location : str
            directory path, if it is empty, the current directory is selected.

        Returns
        -------
        bool
            file content
        '''
        try:
            _name = str(name).strip()

            if len(str(_name)) > 0:

                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{_name}/SDF?record_type={record_type}'

                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # print(reqResponse)
                if reqResponse == 200:
                    sdfContent = res.text
                    # check
                    if save is True:
                        # save a binary
                        _fname = str(_name)+"_"+record_type+'.sdf'
                        if len(location) == 0:
                            fileLoc = _fname
                        else:
                            fileLoc = os.path.join(location, _fname)

                        file = open(fileLoc, 'w')
                        file.write(sdfContent)
                        file.close()
                    return _fname, fileLoc
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_cid_by_name(name, name_type='word') -> list[str]:
        '''
        Get cid by searching name

        Parameters
        ----------
        name : str
            compound name (https://pubchem.ncbi.nlm.nih.gov/)
        name_type : str
            word (small part of molecule), complete (exact molecule)

        Returns
        -------
        list
            cid  
        '''
        try:
            _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/TXT?name_type={name_type}'

            if len(str(name)) > 0:
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # print(reqResponse)
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_sid_by_name(name):
        '''
        Get sids by searching name

        Parameters
        ----------
        name : str
            compound name (https://pubchem.ncbi.nlm.nih.gov/)

        Returns
        -------
        str
            sid list
        '''
        try:
            _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/sids/TXT'

            if len(str(name)) > 0:
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # print(reqResponse)
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_structure_image(name='', cid='', record_type='2d', image_size=''):
        '''
        Get compound structure image

        Parameters
        ----------
        name : str
            compound name
        cid : str
            compound id
        record_type : str
            3d, 2d
        image_size : str
            300, 500, 1000, 2000

        Returns
        -------
        Image
            image
        '''
        try:
            # check
            _record_type = record_type.strip()
            if _record_type not in ['2d', '3d']:
                raise Exception('record_type is not correctly set.')

            # check
            if len(name) > 0:
                _name = name.strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{_name}/PNG?record_type={_record_type}'
            elif len(cid) > 0:
                _cid = cid.strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/PNG?record_type={_record_type}'

            res = requests.get(_url)
            # check
            reqResponse = res.status_code
            # print(reqResponse)
            if reqResponse == 200:
                resContent = res.content
                in_memory_file = io.BytesIO(resContent)
                im = Image.open(in_memory_file)

                return im
            else:
                raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_structure_image_2d(name='', cid=0, image_size=''):
        '''
        Get compound structure image

        Parameters
        ----------
        name : str
            compound name
        cid : str
            compound id
        image_size : str
            small, large, 250x250

        Returns
        -------
        Image
            image
        '''
        try:
            # check
            if len(name) > 0:
                _name = name.strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{_name}/PNG?record_type=2d&image_size={image_size}'
            elif cid != 0:
                _cid = str(cid).strip()
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/PNG?record_type=2d&image_size={image_size}'

            res = requests.get(_url)
            # check
            reqResponse = res.status_code
            # print(reqResponse)
            if reqResponse == 200:
                resContent = res.content
                in_memory_file = io.BytesIO(resContent)
                im = Image.open(in_memory_file)
                return im
            else:
                raise Exception('request is refused, try again.')
        except Exception as e:
            print(e)

    @staticmethod
    def get_properties_by_cid(cid, properties=[], format_type="json"):
        '''
        Display compound structure as an image

        Parameters
        ----------
        cid : str
            compound id
        properties : list
            List of properties to retrieve. Possible values include:
            - MolecularFormula: Molecular formula.
            - MolecularWeight: The molecular weight is the sum of all atomic weights of the constituent atoms in a compound, measured in g/mol. In the absence of explicit isotope labelling, averaged natural abundance is assumed. If an atom bears an explicit isotope label, 100% isotopic purity is assumed at this location.
            - CanonicalSMILES: Canonical SMILES (Simplified Molecular Input Line Entry System) string.  It is a unique SMILES string of a compound, generated by a “canonicalization” algorithm.
            - IsomericSMILES: Isomeric SMILES string.  It is a SMILES string with stereochemical and isotopic specifications.
            - InChI: Standard IUPAC International Chemical Identifier (InChI).  It does not allow for user selectable options in dealing with the stereochemistry and tautomer layers of the InChI string.
            - InChIKey: Hashed version of the full standard InChI, consisting of 27 characters.
            - IUPACName: Chemical name systematically determined according to the IUPAC nomenclatures.
            - Title: The title used for the compound summary page.
            - XLogP: Computationally generated octanol-water partition coefficient or distribution coefficient. XLogP is used as a measure of hydrophilicity or hydrophobicity of a molecule.
            - ExactMass: The mass of the most likely isotopic composition for a single molecule, corresponding to the most intense ion/molecule peak in a mass spectrum.
            - MonoisotopicMass: The mass of a molecule, calculated using the mass of the most abundant isotope of each element.
            - TPSA: Topological polar surface area, computed by the algorithm described in the paper by Ertl et al.
            - Complexity: The molecular complexity rating of a compound, computed using the Bertz/Hendrickson/Ihlenfeldt formula.
            - Charge: The total (or net) charge of a molecule.
            - HBondDonorCount: Number of hydrogen-bond donors in the structure.
            - HBondAcceptorCount: Number of hydrogen-bond acceptors in the structure.
            - RotatableBondCount: Number of rotatable bonds.
            - HeavyAtomCount: Number of non-hydrogen atoms.
            - IsotopeAtomCount: Number of atoms with enriched isotope(s)
            - AtomStereoCount: Total number of atoms with tetrahedral (sp3) stereo [e.g., (R)- or (S)-configuration]
            - DefinedAtomStereoCount: Number of atoms with defined tetrahedral (sp3) stereo.
            - UndefinedAtomStereoCount: Number of atoms with undefined tetrahedral (sp3) stereo.
            - BondStereoCount: Total number of bonds with planar (sp2) stereo [e.g., (E)- or (Z)-configuration].
            - DefinedBondStereoCount: Number of atoms with defined planar (sp2) stereo.
            - UndefinedBondStereoCount: Number of atoms with undefined planar (sp2) stereo.
            - CovalentUnitCount: Number of covalently bound units.
            - Volume3D: Analytic volume of the first diverse conformer (default conformer) for a compound.
            - XStericQuadrupole3D: The x component of the quadrupole moment (Qx) of the first diverse conformer (default conformer) for a compound.
            - YStericQuadrupole3D: The y component of the quadrupole moment (Qy) of the first diverse conformer (default conformer) for a compound.
            - ZStericQuadrupole3D: The z component of the quadrupole moment (Qz) of the first diverse conformer (default conformer) for a compound.
            - FeatureCount3D: Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)
            - FeatureAcceptorCount3D: Number of hydrogen-bond acceptors of a conformer.
            - FeatureDonorCount3D: Number of hydrogen-bond donors of a conformer.
            - FeatureAnionCount3D: Number of anionic centers (at pH 7) of a conformer.
            - FeatureCationCount3D: Number of cationic centers (at pH 7) of a conformer.
            - FeatureRingCount3D: Number of rings of a conformer.
            - FeatureHydrophobeCount3D: Number of hydrophobes of a conformer.
            - ConformerModelRMSD3D: Conformer sampling RMSD in Å.
            - EffectiveRotorCount3D: Total number of 3D features (the sum of FeatureAcceptorCount3D, FeatureDonorCount3D, FeatureAnionCount3D, FeatureCationCount3D, FeatureRingCount3D and FeatureHydrophobeCount3D)
            - ConformerCount3D: The number of conformers in the conformer model for a compound.
            - Fingerprint2D: Base64-encoded PubChem Substructure Fingerprint of a molecule.
        format_type : str
            json, sdf

        Returns
        -------
        dict
            json format properties
        '''
        try:
            # cid
            _cid = str(cid).strip()
            # format type
            _format_type = str(format_type).strip().upper()
            # check
            if len(_cid) > 0:
                _properties = ",".join(properties)
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{_cid}/property/{_properties}/{_format_type}'

                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                # check
                if reqResponse == 200:
                    resContent = res.json()
                    # resContent = resContent.splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_formula(formula):
        '''
        Search for cids according to a formula

        Parameters
        ----------
        formula : str
            e.g. CH4

        Returns
        -------
        list
            cid list
        '''
        try:

            _formula = formula.strip()
            if len(_formula) > 0:
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{formula}/cids/TXT'

                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_similar_cids_by_cid(cid):
        '''
        Search for similar cids according to a cid

        Parameters
        ----------
        cid : str
            e.g. 297

        Returns
        -------
        list
            cid list
        '''
        try:
            _cid = str(cid).strip()
            if len(_cid) > 0:
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/{_cid}/cids/TXT'

                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')
        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_identity(cid, mode=0):
        '''
        Search for cids according to an identity

        Parameters
        ----------
        cid : str
            e.g. 297
        mode : int
            options:
            - 0: same connectivity
            - 1: same tautomers
            - 2: same stereo
            - 3: same isotope
            - 4: same stereo + isotope
            - 5: nonconflicting stereo
            - 6: same isotope + nonconflicting stereo

        Returns
        -------
        list
            cid list
        '''
        try:
            # mode list
            modeList = {
                0: 'same_connectivity',
                1: 'same_tautomer',
                2: 'same_stereo',
                3: 'same_isotope',
                4: 'same_stereo_isotope',
                5: 'nonconflicting_stereo',
                6: 'same_isotope_nonconflicting_stereo'
            }
            # check cid
            _cid = str(cid).strip()
            _mode = modeList.get(mode)

            if len(_cid) > -1:
                _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/cid/{_cid}/cids/TXT?identity_type={_mode}'
                # api
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()
                    # return
                    return resContent
                else:
                    raise Exception('request is refused, try again.')
        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_2d_similarity(cid,  max_records="all", threshold=90):
        '''
        Search for cids according to an 2d similarity

        Parameters
        ----------
        cid : str
            e.g. 297
        max_records : str
            number of records e.g. 10
        threshold : str
            minimum Tanimoto score for a hit e.g. 90

        Returns
        -------
        list
            cid list
        '''
        try:
            _cid = str(cid).strip()
            _threshold = str(threshold).strip()
            _max_records = str(max_records).strip()

            if len(_cid) > -1:
                # check
                if _max_records == 'all':
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{_cid}/cids/TXT?Threshold={_threshold}'
                else:
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/cid/{_cid}/cids/TXT?Threshold={_threshold}&MaxRecords={_max_records}'

                # url log
                res = requests.get(_url)

                # check
                reqResponse = res.status_code
                # check
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()
                    # res
                    return resContent
                else:
                    raise Exception('request is refused, try again.')
            else:
                raise Exception('cid is empty.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_3d_similarity(cid, max_records=all, threshold=90):
        '''
        Search for cids according to an 2d similarity

        Parameters
        ----------
        cid : str
            e.g. 297
        max_records : str
            number of records e.g. 10 (default: all)
        threshold : str
            minimum Tanimoto score for a hit e.g. 90 (default 90)

        Returns
        -------
        list
            cid list
        '''
        try:
            _cid = str(cid).strip()
            _threshold = int(threshold)
            _max_records = max_records

            if len(_cid) > -1:

                if _max_records == 'all':
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/{_cid}/cids/TXT?Threshold={_threshold}'
                else:
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_3d/cid/{_cid}/cids/TXT?Threshold={_threshold}&MaxRecords={_max_records}'

                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')

        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_structure_type(cid, structure_type=1, max_records='all'):
        '''
        Search for cids according to an cid [Substructure / Superstructure]

        Parameters
        ----------
        cid : str
            e.g. CH4: 297
        structure_type : str
            1: substructure
            2: superstructure
        max_records : str
            number of records e.g. 10

        Returns
        -------
        list
            cid list
        '''
        try:
            # set
            _cid = str(cid).strip()
            # check structure_type
            if structure_type == 1:
                _structure_type = 'fastsubstructure'
            elif structure_type == 2:
                _structure_type = 'fastsuperstructure'
            else:
                raise Exception('structure_type is not correctly set.')
            # max records
            _max_records = max_records

            if len(_cid) > -1:
                if _max_records == 'all':
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{_structure_type}/cid/{_cid}/cids/TXT'
                else:
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{_structure_type}/cid/{_cid}/cids/TXT?MaxRecords={_max_records}'
                # send req
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')
        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_smiles_structure(smiles, max_records=all):
        '''
        Search for cids according to an smiles [Substructure / Superstructure]

        Parameters
        ----------
        smiles : str
            e.g. CH4: C
        max_records : str
            number of records e.g. 10 (default: all)

        Returns
        -------
        list
            cid list
        '''
        try:
            # set
            _smiles = str(smiles).strip()
            _max_records = max_records

            if len(_smiles) > -1:
                if _max_records == 'all':
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smiles/{_smiles}/cids/TXT'
                else:
                    _url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smiles/{_smiles}/cids/TXT?MaxRecords={_max_records}'
                # send req
                res = requests.get(_url)
                # check
                reqResponse = res.status_code
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()

                    return resContent
                else:
                    raise Exception('request is refused, try again.')
        except Exception as e:
            print(e)

    @staticmethod
    def get_cids_by_molecular_formula(molecular_formula, max_records="all", allow_other_elements=True):
        '''
        Search for cids according to a molecular formula

        Parameters
        ----------
        molecular_formula : str
            e.g. CH4
        max_records : str
            number of records e.g. 10 (default: all)
        allow_other_elements : bool
            True: allow other elements
            False: not allow other elements

        Returns
        -------
        list
            cid list
        '''
        try:
            # set
            _name = str(molecular_formula).strip()
            _max_records = str(max_records).strip()
            _allow_other_elements = bool(allow_other_elements)
            if len(_name) > -1:
                # check
                if _max_records == 'all':
                    _url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{molecular_formula}/cids/TXT?AllowOtherElements={_allow_other_elements}"
                else:
                    _url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastformula/{molecular_formula}/cids/TXT?AllowOtherElements={_allow_other_elements}&MaxRecords={_max_records}"

                # url log
                res = requests.get(_url)

                # check
                reqResponse = res.status_code
                # check
                if reqResponse == 200:
                    resContent = res.text
                    resContent = str(resContent).splitlines()
                    # res
                    return resContent
                else:
                    raise Exception('request is refused, try again.')
            else:
                raise Exception('cid is empty.')

        except Exception as e:
            print(e)
