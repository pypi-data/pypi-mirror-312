#define PY_SSIZE_T_CLEAN
#include<Python.h>

#define isize Py_ssize_t

const isize _SIZE = sizeof(isize) * 8;
const isize _ONE = 1;
// https://peps.python.org/pep-0683/#py-immortal-refcnt
// _Py_IMMORTAL_BIT - has the top-most available bit set (e.g. 2^62)
const isize Py_IMMORTAL_BIT = _ONE << (_SIZE - 2);
// _Py_IMMORTAL_REFCNT - has the two top-most available bits set
const isize Py_IMMORTAL_REFCNT = Py_IMMORTAL_BIT | (Py_IMMORTAL_BIT >> 1);

void set_refcount(PyObject *self, isize refs) {
    Py_SET_REFCNT(self, refs);
}
