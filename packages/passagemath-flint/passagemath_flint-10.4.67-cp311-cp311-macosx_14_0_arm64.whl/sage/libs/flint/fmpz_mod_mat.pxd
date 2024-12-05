# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/fmpz_mod_mat.h

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
    fmpz * fmpz_mod_mat_entry(const fmpz_mod_mat_t mat, slong i, slong j) noexcept
    void fmpz_mod_mat_set_entry(fmpz_mod_mat_t mat, slong i, slong j, const fmpz_t val) noexcept
    void fmpz_mod_mat_init(fmpz_mod_mat_t mat, slong rows, slong cols, const fmpz_t n) noexcept
    void fmpz_mod_mat_init_set(fmpz_mod_mat_t mat, const fmpz_mod_mat_t src) noexcept
    void fmpz_mod_mat_clear(fmpz_mod_mat_t mat) noexcept
    slong fmpz_mod_mat_nrows(const fmpz_mod_mat_t mat) noexcept
    slong fmpz_mod_mat_ncols(const fmpz_mod_mat_t mat) noexcept
    void _fmpz_mod_mat_set_mod(fmpz_mod_mat_t mat, const fmpz_t n) noexcept
    void fmpz_mod_mat_one(fmpz_mod_mat_t mat) noexcept
    void fmpz_mod_mat_zero(fmpz_mod_mat_t mat) noexcept
    void fmpz_mod_mat_swap(fmpz_mod_mat_t mat1, fmpz_mod_mat_t mat2) noexcept
    void fmpz_mod_mat_swap_entrywise(fmpz_mod_mat_t mat1, fmpz_mod_mat_t mat2) noexcept
    bint fmpz_mod_mat_is_empty(const fmpz_mod_mat_t mat) noexcept
    bint fmpz_mod_mat_is_square(const fmpz_mod_mat_t mat) noexcept
    void _fmpz_mod_mat_reduce(fmpz_mod_mat_t mat) noexcept
    void fmpz_mod_mat_randtest(fmpz_mod_mat_t mat, flint_rand_t state) noexcept
    void fmpz_mod_mat_window_init(fmpz_mod_mat_t window, const fmpz_mod_mat_t mat, slong r1, slong c1, slong r2, slong c2) noexcept
    void fmpz_mod_mat_window_clear(fmpz_mod_mat_t window) noexcept
    void fmpz_mod_mat_concat_horizontal(fmpz_mod_mat_t res, const fmpz_mod_mat_t mat1, const fmpz_mod_mat_t mat2) noexcept
    void fmpz_mod_mat_concat_vertical(fmpz_mod_mat_t res, const fmpz_mod_mat_t mat1, const fmpz_mod_mat_t mat2) noexcept
    void fmpz_mod_mat_print_pretty(const fmpz_mod_mat_t mat) noexcept
    bint fmpz_mod_mat_is_zero(const fmpz_mod_mat_t mat) noexcept
    void fmpz_mod_mat_set(fmpz_mod_mat_t B, const fmpz_mod_mat_t A) noexcept
    void fmpz_mod_mat_transpose(fmpz_mod_mat_t B, const fmpz_mod_mat_t A) noexcept
    void fmpz_mod_mat_set_fmpz_mat(fmpz_mod_mat_t A, const fmpz_mat_t B) noexcept
    void fmpz_mod_mat_get_fmpz_mat(fmpz_mat_t A, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_add(fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_sub(fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_neg(fmpz_mod_mat_t B, const fmpz_mod_mat_t A) noexcept
    void fmpz_mod_mat_scalar_mul_si(fmpz_mod_mat_t B, const fmpz_mod_mat_t A, slong c) noexcept
    void fmpz_mod_mat_scalar_mul_ui(fmpz_mod_mat_t B, const fmpz_mod_mat_t A, ulong c) noexcept
    void fmpz_mod_mat_scalar_mul_fmpz(fmpz_mod_mat_t B, const fmpz_mod_mat_t A, fmpz_t c) noexcept
    void fmpz_mod_mat_mul(fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    void _fmpz_mod_mat_mul_classical_threaded_pool_op(fmpz_mod_mat_t D, const fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B, int op, thread_pool_handle * threads, slong num_threads) noexcept
    void _fmpz_mod_mat_mul_classical_threaded_op(fmpz_mod_mat_t D, const fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B, int op) noexcept
    void fmpz_mod_mat_mul_classical_threaded(fmpz_mod_mat_t C, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_sqr(fmpz_mod_mat_t B, const fmpz_mod_mat_t A) noexcept
    void fmpz_mod_mat_mul_fmpz_vec(fmpz * c, const fmpz_mod_mat_t A, const fmpz * b, slong blen) noexcept
    void fmpz_mod_mat_mul_fmpz_vec_ptr(fmpz * const * c, const fmpz_mod_mat_t A, const fmpz * const * b, slong blen) noexcept
    void fmpz_mod_mat_fmpz_vec_mul(fmpz * c, const fmpz * a, slong alen, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_fmpz_vec_mul_ptr(fmpz * const * c, const fmpz * const * a, slong alen, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_trace(fmpz_t trace, const fmpz_mod_mat_t mat) noexcept
    slong fmpz_mod_mat_rref(slong * perm, fmpz_mod_mat_t mat) noexcept
    void fmpz_mod_mat_strong_echelon_form(fmpz_mod_mat_t mat) noexcept
    slong fmpz_mod_mat_howell_form(fmpz_mod_mat_t mat) noexcept
    int fmpz_mod_mat_inv(fmpz_mod_mat_t B, fmpz_mod_mat_t A) noexcept
    slong fmpz_mod_mat_lu(slong * P, fmpz_mod_mat_t A, int rank_check) noexcept
    void fmpz_mod_mat_solve_tril(fmpz_mod_mat_t X, const fmpz_mod_mat_t L, const fmpz_mod_mat_t B, int unit) noexcept
    void fmpz_mod_mat_solve_triu(fmpz_mod_mat_t X, const fmpz_mod_mat_t U, const fmpz_mod_mat_t B, int unit) noexcept
    int fmpz_mod_mat_solve(fmpz_mod_mat_t X, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    int fmpz_mod_mat_can_solve(fmpz_mod_mat_t X, const fmpz_mod_mat_t A, const fmpz_mod_mat_t B) noexcept
    void fmpz_mod_mat_similarity(fmpz_mod_mat_t M, slong r, fmpz_t d) noexcept
    void fmpz_mod_mat_charpoly(fmpz_mod_poly_t p, const fmpz_mod_mat_t M, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_mat_minpoly(fmpz_mod_poly_t p, const fmpz_mod_mat_t M, const fmpz_mod_ctx_t ctx) noexcept
