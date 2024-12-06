# Copyright (c) Idaero Solutions.
# Distributed under the terms of the LICENSE file located in NaxToPy-<version>.dist-info.

"""Module with all the required functions to load the C# dinamic libraries"""

from enum import Enum
import sys
import os
import winreg
import clr

from NaxToPy.Core.Constants.Constants import (
    DEVELOPER_VIZZER, VIZZER_CLASSES_DLL, VERSION, NAXTO_VERSION, NAXTO_STEP, VIZZER_COMPATIBILITY
)
from NaxToPy import N2PLog

class _RunType(Enum):
    """Enumeration for different runtime environments."""
    RELEASE = 0
    EXE = 1
    DEVELOPE = 2


def _check_run_type() -> _RunType:
    """Returns a RunType value:
        - RELEASE
        - EXE
        - DEVELOPE
    """
    dev_dll_path = os.path.join(DEVELOPER_VIZZER, VIZZER_CLASSES_DLL)

    if getattr(sys, 'frozen', False):  # PyInstaller EXE
        return _RunType.EXE
    
    elif os.path.exists(dev_dll_path):  # Development environment
        return _RunType.DEVELOPE
    
    else:
        return _RunType.RELEASE  # Default to RELEASE
    

def _search_naxtomodel() -> str:
    """Searchs in the register for the installed version of NaxTo and returns the NaxToModel.dll path.    
    """

    # Check first in LOCAL_MACHINE
    naxto_paths = _read_register(winreg.HKEY_LOCAL_MACHINE)

    # If fails, check in CURRENT_USER
    if naxto_paths is None:
        naxto_paths = _read_register(winreg.HKEY_CURRENT_USER)

    # If fails again, return None
    if naxto_paths is None:
        return None
    
    compatible_path = _check_compatibility(naxto_paths) + f"bin\\{VIZZER_CLASSES_DLL}"
    return compatible_path


def _check_compatibility(naxto_paths: list[tuple[str,str]]) -> str:
    """Searchs what of the NaxTo versions that are installed is compatible with this NaxToPy version 
    
    Returns: Path [str]
    """
    for version, path in naxto_paths:
        # Version is NAXTOVIEW_202XRY, so only the 202XRY is checked
        if version.split("_")[1] == NAXTO_VERSION:
            return path
        
    # If no compatible, return None
    return None


def _search_license(path: str) -> str:
    """Search for NaxToLicense.dll path"""
    return os.path.join(os.path.dirname(path), "NaxToLicense.dll")


def _read_register(keyType: int) -> str:
    """Try to read the instalation path of NaxTo. 
    
    - Returns a tuple ordered from newer to older with the version and the path.
    - Returns None if fails.
    
    Returns:
        list[tuple[NAXTOVIEW_VERSION, PATH]]
    """
    try:
        # Open the key for IDAERO sub keys
        with winreg.OpenKey(keyType, "SOFTWARE\\IDAERO") as idaerokey:
            # Save how many subkeys there are in IDAERO
            num_naxto_keys, _, _ = winreg.QueryInfoKey(idaerokey)

            naxto_versions = []
            for i in range(num_naxto_keys):
                # Searchs only for the NAXTOVIEW subkeys in the IDAERO key
                if winreg.EnumKey(idaerokey, i).split("_")[0] == "NAXTOVIEW":
                    naxto_versions.append(winreg.EnumKey(idaerokey, i))
    except:
        return None
    
    else:
        naxto_versions.sort(reverse=True)  # Ordered from newer to older
        naxto_paths = []  # List of tuples with the version and the path of the version
        for version in naxto_versions:
            with winreg.OpenKey(keyType, f"SOFTWARE\\IDAERO\\{version}") as naxto_key:
                path = winreg.QueryValueEx(naxto_key, "Path")[0]
                naxto_paths.append((version, path))
        
        return naxto_paths


def _write_register() -> None:
    """Opens the Windows Register and generates the IDAERO key in LOCAL_MACHINE or in CURRENT_USER if fails and write the Path value    
    """

    keyType: winreg.HKEYType = None

    # We try to use the LOCAL_MACHINE first
    try:
        keyType = winreg.HKEY_LOCAL_MACHINE
        naxto_key = winreg.CreateKey(keyType, f"SOFTWARE\\IDAERO\\NAXTOVIEW_{NAXTO_VERSION}")
        
    # We use the CURRENT_USER if fails
    except:
        keyType = winreg.HKEY_CURRENT_USER
        naxto_key = winreg.CreateKey(keyType, f"SOFTWARE\\IDAERO\\NAXTOVIEW_{NAXTO_VERSION}")

    try:
        # We search where this file is placed. It will be in a TEMP dicrectory. Then we go up 3 directories
        naxtopy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

        winreg.SetValueEx(naxto_key, "Path", 0, winreg.REG_SZ, naxtopy_path + "\\")
        naxto_key.Close()
    except Exception as e:
        naxto_key.Close()
        msg = N2PLog.Error.E112(e)
        raise Exception(msg)

    return None


def _clean_register() -> None:
    """Function that cleans the Register from passed NaxToPy EXE type runs"""

    def delete_register(keyType: int):
        """Auxiliar function that actually delete the key"""

        # Key is open with access equal to KEY_READ (default) to be read
        with winreg.OpenKey(keyType, f"SOFTWARE\\IDAERO\\NAXTOVIEW_{NAXTO_VERSION}") as naxto_key:
            path = winreg.QueryValueEx(naxto_key, "Path")[0]
        if "TEMP" in path:
            # Key is open with access equal to KEY_SET_VALUE to be deleted
            with winreg.OpenKey(keyType, f"SOFTWARE\\IDAERO\\NAXTOVIEW_{NAXTO_VERSION}", 0, winreg.KEY_SET_VALUE) as naxto_key:
                winreg.DeleteValue(naxto_key, "Path")
    
    try:
        delete_register(winreg.HKEY_LOCAL_MACHINE)
    except PermissionError:
        pass
    except FileNotFoundError:
        pass

    try:
        delete_register(winreg.HKEY_CURRENT_USER)
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    


def _reference_finder() -> None:
    """Main function that loads the required dlls.
    
    In order to load the dlls, some checks must be done:
        1. NaxToPy Version
        2. NaxTo Compatibility
        3. Type of running: .exe, develope, release
        4. Where the libraries are placed
        5. If EXE but it has same version as the installed (RELEASE) use the installed
        5. Load the libraries
    """

    # Check the type of run. Depending of the ruing type the libraries will be search in a place.
    run_type = _check_run_type()

    if run_type == _RunType.RELEASE:
        naxtomodel_path = _search_naxtomodel()
        if naxtomodel_path is None:
            raise RuntimeError
        seconddll_path = _search_license(naxtomodel_path)

    elif run_type == _RunType.DEVELOPE:
        naxtomodel_path = os.path.join(DEVELOPER_VIZZER, VIZZER_CLASSES_DLL)
        seconddll_path = os.path.join(r"C:\GIT_REPOSITORIES\NAXTO\NAXTOLibsDebug\NAXLicense\v.4.0", "NaxToLicense.dll")

    elif run_type == _RunType.EXE:
        naxtomodel_path = _search_naxtomodel()

        if naxtomodel_path is None:
            naxtomodel_path = sys._MEIPASS + "\\bin\\NaxToModel.dll"
            _write_register()

        seconddll_path = _search_license(naxtomodel_path)

    try:
        clr.AddReference(naxtomodel_path)
    except:
        raise ImportError
    else:
        clr.AddReference(seconddll_path)