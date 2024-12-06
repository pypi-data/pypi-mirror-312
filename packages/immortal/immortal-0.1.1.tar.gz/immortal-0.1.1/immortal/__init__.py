from ctypes import CDLL, c_ssize_t, py_object
from pathlib import Path
from sys import getrefcount

immortal_c: object = CDLL(list(Path(__file__).absolute().parent.glob("immortal_c*.so"))[-1])

_Py_IMMORTAL_BIT: int = c_ssize_t.in_dll(immortal_c, "Py_IMMORTAL_BIT").value
_Py_IMMORTAL_REFCNT: c_ssize_t = c_ssize_t.in_dll(immortal_c, "Py_IMMORTAL_REFCNT")

def is_immortal(obj: object) -> bool:
    """Check whether an object is immortal."""
    return bool(getrefcount(obj) & _Py_IMMORTAL_BIT)


def immortalize(obj: object) -> None:
    """Immortalize an object (not recursive)."""
    immortal_c.set_refcount(py_object(obj), _Py_IMMORTAL_REFCNT)

__all__ = ("is_immortal", "immortalize")
