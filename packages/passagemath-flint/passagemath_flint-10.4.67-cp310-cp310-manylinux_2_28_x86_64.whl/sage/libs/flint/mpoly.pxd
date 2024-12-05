# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/mpoly.h

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
    void mpoly_ctx_init(mpoly_ctx_t ctx, slong nvars, const ordering_t ord) noexcept
    void mpoly_ctx_clear(mpoly_ctx_t mctx) noexcept
    ordering_t mpoly_ordering_randtest(flint_rand_t state) noexcept
    void mpoly_ctx_init_rand(mpoly_ctx_t mctx, flint_rand_t state, slong max_nvars) noexcept
    int mpoly_ordering_isdeg(const mpoly_ctx_t ctx) noexcept
    int mpoly_ordering_isrev(const mpoly_ctx_t cth) noexcept
    void mpoly_ordering_print(ordering_t ord) noexcept
    void mpoly_monomial_add(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N) noexcept
    void mpoly_monomial_add_mp(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N) noexcept
    void mpoly_monomial_sub(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N) noexcept
    void mpoly_monomial_sub_mp(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N) noexcept
    int mpoly_monomial_overflows(ulong * exp2, slong N, ulong mask) noexcept
    int mpoly_monomial_overflows_mp(ulong * exp_ptr, slong N, flint_bitcnt_t bits) noexcept
    int mpoly_monomial_overflows1(ulong exp, ulong mask) noexcept
    void mpoly_monomial_set(ulong * exp2, const ulong * exp3, slong N) noexcept
    void mpoly_monomial_swap(ulong * exp2, ulong * exp3, slong N) noexcept
    void mpoly_monomial_mul_ui(ulong * exp2, const ulong * exp3, slong N, ulong c) noexcept
    bint mpoly_monomial_is_zero(const ulong * exp, slong N) noexcept
    bint mpoly_monomial_equal(const ulong * exp2, const ulong * exp3, slong N) noexcept
    void mpoly_get_cmpmask(ulong * cmpmask, slong N, ulong bits, const mpoly_ctx_t mctx) noexcept
    bint mpoly_monomial_lt(const ulong * exp2, const ulong * exp3, slong N, const ulong * cmpmask) noexcept
    bint mpoly_monomial_gt(const ulong * exp2, const ulong * exp3, slong N, const ulong * cmpmask) noexcept
    int mpoly_monomial_cmp(const ulong * exp2, const ulong * exp3, slong N, const ulong * cmpmask) noexcept
    int mpoly_monomial_divides(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N, ulong mask) noexcept
    int mpoly_monomial_divides_mp(ulong * exp_ptr, const ulong * exp2, const ulong * exp3, slong N, flint_bitcnt_t bits) noexcept
    int mpoly_monomial_divides1(ulong * exp_ptr, const ulong exp2, const ulong exp3, ulong mask) noexcept
    int mpoly_monomial_divides_tight(slong e1, slong e2, slong * prods, slong num) noexcept
    flint_bitcnt_t mpoly_exp_bits_required_ui(const ulong * user_exp, const mpoly_ctx_t mctx) noexcept
    flint_bitcnt_t mpoly_exp_bits_required_ffmpz(const fmpz * user_exp, const mpoly_ctx_t mctx) noexcept
    flint_bitcnt_t mpoly_exp_bits_required_pfmpz(fmpz * const * user_exp, const mpoly_ctx_t mctx) noexcept
    void mpoly_max_fields_ui_sp(ulong * max_fields, const ulong * poly_exps, slong len, ulong bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_max_fields_fmpz(fmpz * max_fields, const ulong * poly_exps, slong len, ulong bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_max_degrees_tight(slong * max_exp, ulong * exps, slong len, slong * prods, slong num) noexcept
    int mpoly_monomial_exists(slong * index, const ulong * poly_exps, const ulong * exp, slong len, slong N, const ulong * cmpmask) noexcept
    void mpoly_search_monomials(slong ** e_ind, ulong * e, slong * e_score, slong * t1, slong * t2, slong * t3, slong lower, slong upper, const ulong * a, slong a_len, const ulong * b, slong b_len, slong N, const ulong * cmpmask) noexcept
    int mpoly_term_exp_fits_ui(ulong * exps, ulong bits, slong n, const mpoly_ctx_t mctx) noexcept
    int mpoly_term_exp_fits_si(ulong * exps, ulong bits, slong n, const mpoly_ctx_t mctx) noexcept
    void mpoly_get_monomial_ui(ulong * exps, const ulong * poly_exps, ulong bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_get_monomial_ffmpz(fmpz * exps, const ulong * poly_exps, flint_bitcnt_t bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_get_monomial_pfmpz(fmpz ** exps, const ulong * poly_exps, flint_bitcnt_t bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_set_monomial_ui(ulong * exp1, const ulong * exp2, ulong bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_set_monomial_ffmpz(ulong * exp1, const fmpz * exp2, flint_bitcnt_t bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_set_monomial_pfmpz(ulong * exp1, fmpz * const * exp2, flint_bitcnt_t bits, const mpoly_ctx_t mctx) noexcept
    void mpoly_pack_vec_ui(ulong * exp1, const ulong * exp2, ulong bits, slong nfields, slong len) noexcept
    void mpoly_pack_vec_fmpz(ulong * exp1, const fmpz * exp2, flint_bitcnt_t bits, slong nfields, slong len) noexcept
    void mpoly_unpack_vec_ui(ulong * exp1, const ulong * exp2, ulong bits, slong nfields, slong len) noexcept
    void mpoly_unpack_vec_fmpz(fmpz * exp1, const ulong * exp2, flint_bitcnt_t bits, slong nfields, slong len) noexcept
    int mpoly_repack_monomials(ulong * exps1, ulong bits1, const ulong * exps2, ulong bits2, slong len, const mpoly_ctx_t mctx) noexcept
    void mpoly_pack_monomials_tight(ulong * exp1, const ulong * exp2, slong len, const slong * mults, slong num, slong bits) noexcept
    void mpoly_unpack_monomials_tight(ulong * e1, ulong * e2, slong len, slong * mults, slong num, slong bits) noexcept
    void mpoly_main_variable_terms1(slong * i1, slong * n1, const ulong * exp1, slong l1, slong len1, slong k, slong num, slong bits) noexcept
    int _mpoly_heap_insert(mpoly_heap_s * heap, ulong * exp, void * x, slong * next_loc, slong * heap_len, slong N, const ulong * cmpmask) noexcept
    void _mpoly_heap_insert1(mpoly_heap1_s * heap, ulong exp, void * x, slong * next_loc, slong * heap_len, ulong maskhi) noexcept
    void * _mpoly_heap_pop(mpoly_heap_s * heap, slong * heap_len, slong N, const ulong * cmpmask) noexcept
    void * _mpoly_heap_pop1(mpoly_heap1_s * heap, slong * heap_len, ulong maskhi) noexcept
