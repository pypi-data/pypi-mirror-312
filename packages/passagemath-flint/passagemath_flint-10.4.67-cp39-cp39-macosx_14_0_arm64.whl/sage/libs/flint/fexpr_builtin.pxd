# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/fexpr_builtin.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    slong fexpr_builtin_lookup(const char * s) noexcept
    const char * fexpr_builtin_name(slong n) noexcept
    slong fexpr_builtin_length() noexcept
