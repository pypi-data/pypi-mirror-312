# sage_setup: distribution = sagemath-categories
# Automatically generated by /private/var/folders/5q/zcc7tkt11f13mhczs1yfd4qc0000gn/T/build-env-so2vupi5/lib/python3.9/site-packages/sage_setup/autogen/interpreters/internal/generator.py.  Do not edit!

from cpython.ref cimport PyObject

from sage.ext.fast_callable cimport Wrapper

cdef class Wrapper_el(Wrapper):
    cdef int _n_args
    cdef object _list_constants
    cdef int _n_constants
    cdef PyObject** _constants
    cdef object _list_stack
    cdef int _n_stack
    cdef PyObject** _stack
    cdef object _domain
    cdef int _n_code
    cdef int* _code
