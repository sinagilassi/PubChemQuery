# UTIL
# -----

# import packages/modules
import os
import json
# local
from config import CID_FILE_PREFIX


class CoreUtility():
    '''
    core utility class
    '''

    def __init__(self):
        pass

    @staticmethod
    def SaveFile(fileContent, fileName, fileFormat, fileDir, logMessage='file is successfully created and saved in'):
        '''
        Save a file with respect to a format

        Parameters
        ----------
        fileContent : str
            file content
        fileName : str
            file name
        fileFormat : str
            file format
        fileDir : str
            file directory
        logMessage : str
            log message (default, file is successfully created and saved in)

        Returns
        -------
        bool
            True if file is successfully created and saved in

        '''
        try:
            # set
            _fileFormat = str(fileFormat).lower()
            # file full name with format
            _fileFullName = fileName + f'.{_fileFormat}'
            # file full location
            fileLoc = os.path.join(fileDir, _fileFullName)

            # check
            if not os.path.isdir(fileDir):
                raise Exception('file directory is not valid.')

            # open file
            with open(fileLoc, 'w') as f:
                # check
                if _fileFormat == 'sdf':
                    # save
                    f.write(fileContent)
                    f.close()
                # FIXME
                if _fileFormat == 'json-string':
                    # save
                    json.dumps(fileContent, f, indent=5)
                    f.close()
                if _fileFormat == 'json':
                    # save ()
                    json.dump(fileContent, f, indent=5)
                    f.close()
            # log
            print(f"the {_fileFormat + logMessage} `{fileLoc}`")
            # return
            return True
        except Exception as e:
            print(e)


class UtilityAPI():
    '''
    utility api class
    '''

    def __init__(self):
        pass

    @staticmethod
    def SetName(cid, file_name_prefix='cid'):
        '''
        Create a name for a file

        Parameters
        ----------
        cid : int
            compound id
        file_name_prefix : str
            file name prefix (default, cid)

        Returns
        -------
        str
            file name
        '''
        try:
            if file_name_prefix == 'cid':
                fileName = f'{CID_FILE_PREFIX}{str(cid)}'
            # res
            return fileName
        except Exception as e:
            print(e)
