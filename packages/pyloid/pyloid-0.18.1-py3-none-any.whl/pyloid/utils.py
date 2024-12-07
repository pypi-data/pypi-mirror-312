import sys
import os
import platform
from typing import Optional


def get_production_path(path: Optional[str] = None) -> Optional[str]:
    """
    Returns the path to the resource files in a production environment.
    If running as a regular Python script, returns None.

    Returns
    -------
    str | None
        The path to the resource files if in a production environment, 
        otherwise None.

    Examples
    --------
    >>> from pyloid.utils import get_production_path
    >>> path = get_production_path("assets/icon.ico")
    >>> if path:
    >>>     print(f"Production path: {path}")
    >>> else:
    >>>     print("Not in a production environment.")
    """
    if getattr(sys, 'frozen', False) or '__compiled__' in globals():
        # Nuitka
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller
            base_path = sys._MEIPASS
        else:
            # Nuitka의 경우 실행 파일이 있는 디렉토리를 기준으로 함
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        return os.path.join(base_path, path) if path else base_path
    else:
        # 일반 Python 스크립트로 실행 중일 때
        return None


def is_production() -> bool:
    """
    Checks if the current environment is a production environment.

    Returns
    -------
    bool
        True if in a production environment, False otherwise.

    Examples
    --------
    >>> from pyloid.utils import is_production
    >>> if is_production():
    >>>     print("Running in production environment.")
    >>> else:
    >>>     print("Not in production environment.")
    """
    return getattr(sys, 'frozen', False) or '__compiled__' in globals()


def get_platform() -> str:
    """
    Returns the name of the current system's platform.

    This function uses `platform.system()` to return the name of the current operating system.

    Returns
    -------
    "Windows" | "Darwin" | "Linux"
        - "Windows" for Windows systems
        - "Darwin" for macOS systems
        - "Linux" for Linux systems

    Examples
    --------
    >>> from pyloid.utils import get_platform
    >>> platform_name = get_platform()
    >>> print(platform_name)
    Windows
    """
    return platform.system()

def get_absolute_path(path: str) -> str:
    """
    Returns the absolute path of the given relative path.
    
    Parameters
    ----------
    path : str
        The relative path to get the absolute path of.

    Returns
    -------
    str
        The absolute path of the given relative path.
        
    Examples
    --------
    >>> from pyloid.utils import get_absolute_path
    >>> absolute_path = get_absolute_path("assets/icon.ico")
    >>> print(absolute_path)
    C:/Users/aaaap/Documents/pyloid/pyloid/assets/icon.ico
    """
    return os.path.normpath(os.path.abspath(path))

