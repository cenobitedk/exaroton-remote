"""Windows startup registry helpers. Gracefully no-ops on non-Windows."""
import sys

APP_NAME = "ExarotonRemote"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _exe_path() -> str:
    """Return the path to use in the registry — the frozen exe or the script."""
    if getattr(sys, "frozen", False):
        return sys.executable
    return f'"{sys.executable}" "{__file__.replace("startup.py", "app.py")}"'


def is_enabled() -> bool:
    if sys.platform != "win32":
        return False
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def enable():
    if sys.platform != "win32":
        return
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _exe_path())
    winreg.CloseKey(key)


def disable():
    if sys.platform != "win32":
        return
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass


def toggle() -> bool:
    """Toggle auto-start. Returns new state."""
    if is_enabled():
        disable()
        return False
    else:
        enable()
        return True
