import winreg
import sys
import os
import clr
from NaxToPy.Core.Constants.Constants import *
from NaxToPy.Core.Errors.N2PLog import N2PLog
from System.Diagnostics import FileVersionInfo


# Comprueba que la Version que el Usuario esta usando de Python esta dentro de las soportadas
def py_ver_comp() -> None:
    """ Function that checks if the python version is supported
    """
    py_version = sys.version.split(".")

    if int(py_version[0]) == 3 and int(py_version[1]) in SUP_PY_VER:
        return
    else:
        msg = N2PLog.Critical.C102(py_version)
        raise RuntimeError(msg)


# Funcion que devuelve la ruta donde se encuentran las librerias de NaxTo----------------------
def vizzer_libs() -> list[str, ...]:
    """Function that returns the paths where the NaxToModel libraries can be found. As there can exist several NaxTo
    versions, several paths may exist.

    Returns: 
        vizzer_libs: list[str]
    """
    vizzer_libs = []

    # Miro en LOCAL MACHINE, donde está instalado el NAXTOVIEW. Ahí se busca la libreria de NaxToModel.
    key_id = winreg.HKEY_LOCAL_MACHINE

    try:

        try:
            sub_key_id = winreg.OpenKeyEx(key_id, os.path.join("SOFTWARE", "IDAERO"))

        except:
            key_id = winreg.HKEY_CURRENT_USER
            sub_key_id = winreg.OpenKeyEx(key_id, os.path.join("SOFTWARE", "IDAERO"))


        naxto_ver = winreg.QueryInfoKey(sub_key_id)
        naxto_ver2 = list()

        for i in range(naxto_ver[0]):

            # De todas las claves de Registro en la carpeta de IDAERO busca solo las de NAXTOVIEW
            if winreg.EnumKey(sub_key_id, i).split("_")[0] == "NAXTOVIEW":
                naxto_ver2.append(winreg.EnumKey(sub_key_id, i))

        # Se busca en la version mas nueva. Si no en la anterior.
        naxto_ver2.sort()

        if len(naxto_ver2) == 0:
            msg = N2PLog.Critical.C107()
            raise ImportError(msg)

        for i in range(len(naxto_ver2)):
            vizzer_key = winreg.OpenKeyEx(key_id, os.path.join("SOFTWARE", "IDAERO", naxto_ver2[i]))
            vizzer_libs.append(winreg.QueryValueEx(vizzer_key, "Path")[0])

        vizzer_libs2 = [os.path.join(lib, "bin") for lib in vizzer_libs]



    except RuntimeError:
        msg = N2PLog.Critical.C107()
        raise ImportError(msg)

    return vizzer_libs2


# ---------------------------------------------------------------------------------------------
def open_idaero_key() -> winreg.HKEYType:
    """Returns the Windows Register Key for the IDAERO software (NAXTOVIEW) in CURRENT_USER

    Returns:
        naxto_key: winreg.HKEYType

    """
    reg_path = r"SOFTWARE\IDAERO"

    # Se crea o se abre la clave CURRENT_USER\SOFTWARE\IDAERO
    idaero_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)

    # Se crea o se abre la clave CURRENT_USER\SOFTWARE\IDAERO\NAXTOVIEW_202XRY donde X e Y serán los que corresponda
    naxto_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path + r"\NAXTOVIEW_" + NAXTO_VERSION)

    # Se devuelve la clave de NAXTOVIEW que es donde se modifica el valor Path
    return naxto_key


def open_localmachine_key() -> winreg.HKEYType:
    """Returns the Windows Register Key for the IDAERO software (NAXTOVIEW) in LOCAL_MACHINE

    Returns:
        naxto_key: winreg.HKEYType

    """
    reg_path = r"SOFTWARE\IDAERO"

    # Se crea o se abre la clave LOCAL_MACHINE\SOFTWARE\IDAERO\NAXTOVIEW_202XRY donde X e Y serán los que corresponda
    naxto_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path + r"\NAXTOVIEW_" + NAXTO_VERSION)

    # Se devuelve la clave de NAXTOVIEW que es donde se busca el valor Path
    return naxto_key
# ---------------------------------------------------------------------------------------------


def create_register() -> None:
    """Function that creates a path variable in the register.

    By default, NaxToPy uses the NaxTo that is installed. If NaxToPy from .exe or from developer is used, the register
    don't have the path variable, and NaxTo is not installed it must be created at Software/Idaero/NaxToView

    Returns:
        None.
    """
    try:
        naxto_key = open_idaero_key()
        try:
            path = winreg.QueryValueEx(naxto_key, "Path")

        except FileNotFoundError:
            try:
                naxto_machine = open_localmachine_key()
                path = winreg.QueryValueEx(naxto_machine, "Path")
            except:
                path = ""

        if not path:
            # La ruta que vamos a meter es la de la carpeta en la que esta una carpeta llamada bin. En ella
            # estan las bibliotecas de NaxTo. Debe funcionar esta carpeta para los ejecutables y para las
            # versiones de desarrollo. En las salidas normales este path no debe estar.
            naxtopy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
            winreg.SetValueEx(naxto_key, "Path", 0, winreg.REG_SZ, naxtopy_path + "\\")
            N2PLog.Warning.W102(naxtopy_path)

    except Exception as e:
        msg = N2PLog.Error.E112(e)
        raise Exception(msg)
# ----------------------------------------------------------------------------------------------------------------------


def destroy_register() -> None:
    """Function that destroy the register path for developers or .exe files of NaxToPy.

    Returns:
        None
    """
    naxto_key = open_idaero_key()
    try:
        naxto_path = winreg.QueryValueEx(naxto_key, "Path")[0]
        if "GIT_REPOSITORIES" not in naxto_path:
            winreg.DeleteValue(naxto_key, "Path")
            N2PLog.Warning.W103()
    except Exception as e:
        N2PLog.Warning.W106(e)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
def compatible_vizzer(vizzer_libs: list, backup: str = None) -> tuple[str, bool]:
    """Returns the path of the NaxToModel this NaxToPy version is compatible with"""

    # Se busca si alguna de las rutas contiene la version para la que esta preparado esta version
    for lib in vizzer_libs:
        if NAXTO_VERSION in lib:
            lib_path = lib + "\\" + VIZZER_CLASSES_DLL

            # Si alguna es de esta version hay que ver si el assembly, que cambia con cada step es compatible.
            # Previamente se verifica que el archivo existe:
            if os.path.exists(lib_path):
                versionInfo = FileVersionInfo.GetVersionInfo(lib_path)
                assemblyVersion = versionInfo.FileVersion

                N2PLog.Debug.D200(assemblyVersion)

                # Se va a suponer que la todos los steps de una version NaxTo son compatibles con todos los steps de
                # una version de NaxToPy: NaxTo 2024.1.X <---> 2.0.Y
                return lib_path, True

    if not backup:
        N2PLog.Warning.W104(NAXTO_VERSION)

    # Comprobamos si hay alguna version que contenga una dll compatible
    for lib in vizzer_libs:
        lib_path = lib + "\\" + VIZZER_CLASSES_DLL
        if not os.path.exists(lib_path):
            continue
        versionInfo = FileVersionInfo.GetVersionInfo(lib_path)
        assemblyVersion = versionInfo.FileVersion

        if not backup:
            backup = lib_path
            N2PLog.Warning.W105()

        if assemblyVersion in VIZZER_COMPATIBILITY:
            return lib_path, True


    # Si ninguna libreria es compatible se prueba con una de ellas, la primera que exista. Pero se indica que no es
    # compatible. Mas adelante se comprubea si dentro de la libreria se indica que esta version de NaxToPy es compatible
    # con ella
    if backup:
        return backup, False
    else:
        msg = N2PLog.Critical.C110(VERSION, NAXTO_VERSION)
        raise ImportError(msg)
# ---------------------------------------------------------------------------------------------


def _naxto_gen(vizzer: str) -> str:
    dir_viz = os.path.dirname(vizzer)
    if "GIT_REPOSITORIES" in dir_viz:
        return os.path.join(r"C:\GIT_REPOSITORIES\NAXTO\NAXTOLibsDebug\NAXLicense\v.4.0", "NaxToLicense.dll")
    return os.path.join(dir_viz, "NaxToLicense.dll")


# Inicializador para encontrar la libreria de NaxToModel
def __reference_finder():
    # La ruta cambia si se tiene el repositorio de NaxToView
    developer_vizzer = DEVELOPER_VIZZER + "\\" + VIZZER_CLASSES_DLL
    compatible = True
    list_libs = vizzer_libs()

    # Si se crea un .exe queremos que encuentre unas nuevas librerias distribuibles, que estarán en la carpeta temporal que se
    # crea cuando se ejecuta el .exe. Tampoco se ejecutan los modulos del reference finder
    if getattr(sys, 'frozen', False):
        destroy_register()
        create_register()
        exe_dir = sys._MEIPASS
        vizzer_path = exe_dir + "\\bin\\NaxToModel.dll"

        # Si ya existe una verison instalada de NaxTo con este NaxToPy se usara NaxToModel.dll de la version instalada. Luego,
        # cualquier NaxToModel.dll simepre va a tirar de las dll de instalación si son compatible porque es lo que hay en el
        # registro
        vizzer_path, possible_compatible = compatible_vizzer(list_libs, vizzer_path)

        N2PLog.Info.I107()

    elif os.path.isfile(developer_vizzer):
        if VERSION.split(".")[-1][0:3] == "dev":
            destroy_register()
            create_register()

        vizzer_path = developer_vizzer
        N2PLog.Info.I108()

    else:
        destroy_register()
        # Compruebo que la version de python es compatible
        py_ver_comp()
        # Busco todas las NaxToModel

        vizzer_path, compatible = compatible_vizzer(list_libs)

    # Llamada a las librerias
    try:
        clr.AddReference(vizzer_path)
        if not compatible:
            from NaxToModel import Global
            if VERSION in list(Global.NAXTOPY_COMPATIBILITY):
                pass
            else:
                msg = N2PLog.Critical.C113(vizzer_path, VERSION, list(Global.NAXTOPY_COMPATIBILITY))
                raise ImportError(msg)
        N2PLog.Info.I109()
        N2PLog.Debug.D101(vizzer_path)
        naxto_c = _naxto_gen(vizzer_path)
        clr.AddReference(naxto_c)
    except:
        msg = N2PLog.Critical.C103()
        raise ImportError(msg)

    N2PLog.Info.I100()
# ---------------------------------------------------------------------------------------------
