# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/gr.h

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
    slong gr_ctx_sizeof_elem(gr_ctx_t ctx) noexcept
    int gr_ctx_clear(gr_ctx_t ctx) noexcept
    int gr_ctx_write(gr_stream_t out, gr_ctx_t ctx) noexcept
    int gr_ctx_print(gr_ctx_t ctx) noexcept
    int gr_ctx_println(gr_ctx_t ctx) noexcept
    int gr_ctx_get_str(char ** s, gr_ctx_t ctx) noexcept
    int gr_ctx_set_gen_name(gr_ctx_t ctx, const char * s) noexcept
    int gr_ctx_set_gen_names(gr_ctx_t ctx, const char ** s) noexcept
    void gr_init(gr_ptr res, gr_ctx_t ctx) noexcept
    void gr_clear(gr_ptr res, gr_ctx_t ctx) noexcept
    void gr_swap(gr_ptr x, gr_ptr y, gr_ctx_t ctx) noexcept
    void gr_set_shallow(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    gr_ptr gr_heap_init(gr_ctx_t ctx) noexcept
    void gr_heap_clear(gr_ptr x, gr_ctx_t ctx) noexcept
    gr_ptr gr_heap_init_vec(slong len, gr_ctx_t ctx) noexcept
    void gr_heap_clear_vec(gr_ptr x, slong len, gr_ctx_t ctx) noexcept
    int gr_randtest(gr_ptr res, flint_rand_t state, gr_ctx_t ctx) noexcept
    int gr_randtest_not_zero(gr_ptr res, flint_rand_t state, gr_ctx_t ctx) noexcept
    int gr_randtest_small(gr_ptr res, flint_rand_t state, gr_ctx_t ctx) noexcept
    int gr_write(gr_stream_t out, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_print(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_println(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_str(char ** s, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_set_str(gr_ptr res, const char * x, gr_ctx_t ctx) noexcept
    int gr_write_n(gr_stream_t out, gr_srcptr x, slong n, gr_ctx_t ctx) noexcept
    int gr_get_str_n(char ** s, gr_srcptr x, slong n, gr_ctx_t ctx) noexcept
    int gr_set(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_set_other(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_ctx_t ctx) noexcept
    int gr_set_ui(gr_ptr res, ulong x, gr_ctx_t ctx) noexcept
    int gr_set_si(gr_ptr res, slong x, gr_ctx_t ctx) noexcept
    int gr_set_fmpz(gr_ptr res, const fmpz_t x, gr_ctx_t ctx) noexcept
    int gr_set_fmpq(gr_ptr res, const fmpq_t x, gr_ctx_t ctx) noexcept
    int gr_set_d(gr_ptr res, double x, gr_ctx_t ctx) noexcept
    int gr_get_si(slong * res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_ui(ulong * res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_fmpz(fmpz_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_fmpq(fmpq_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_d(double * res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_set_fmpz_2exp_fmpz(gr_ptr res, const fmpz_t x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_get_fmpz_2exp_fmpz(fmpz_t res1, fmpz_t res2, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_fexpr(fexpr_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_get_fexpr_serialize(fexpr_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_set_fexpr(gr_ptr res, fexpr_vec_t inputs, gr_vec_t outputs, const fexpr_t x, gr_ctx_t ctx) noexcept
    int gr_zero(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_one(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_neg_one(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_gen(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_gens(gr_vec_t res, gr_ctx_t ctx) noexcept
    truth_t gr_is_zero(gr_srcptr x, gr_ctx_t ctx) noexcept
    truth_t gr_is_one(gr_srcptr x, gr_ctx_t ctx) noexcept
    truth_t gr_is_neg_one(gr_srcptr x, gr_ctx_t ctx) noexcept
    truth_t gr_equal(gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    truth_t gr_is_integer(gr_srcptr x, gr_ctx_t ctx) noexcept
    truth_t gr_is_rational(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_neg(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_add(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_add_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_add_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_add_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_add_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_add_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_add(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_sub(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_sub_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_sub_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_sub_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_sub_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_sub_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_sub(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_mul(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_mul_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_mul_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_mul_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_mul_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_mul_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_mul(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_addmul(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_addmul_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_addmul_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_addmul_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_addmul_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_addmul_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_submul(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_submul_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_submul_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_submul_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_submul_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_submul_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_mul_two(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_sqr(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_mul_2exp_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_mul_2exp_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    truth_t gr_is_invertible(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_inv(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_div(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_div_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_div_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_div_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_div_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_div_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_div(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_div_nonunique(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    truth_t gr_divides(gr_srcptr d, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_divexact(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_divexact_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_divexact_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_divexact_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_divexact_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_divexact(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_euclidean_div(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_euclidean_rem(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_euclidean_divrem(gr_ptr res1, gr_ptr res2, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_pow(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_pow_ui(gr_ptr res, gr_srcptr x, ulong y, gr_ctx_t ctx) noexcept
    int gr_pow_si(gr_ptr res, gr_srcptr x, slong y, gr_ctx_t ctx) noexcept
    int gr_pow_fmpz(gr_ptr res, gr_srcptr x, const fmpz_t y, gr_ctx_t ctx) noexcept
    int gr_pow_fmpq(gr_ptr res, gr_srcptr x, const fmpq_t y, gr_ctx_t ctx) noexcept
    int gr_pow_other(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_other_pow(gr_ptr res, gr_srcptr x, gr_ctx_t x_ctx, gr_srcptr y, gr_ctx_t ctx) noexcept
    truth_t gr_is_square(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_sqrt(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_rsqrt(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_gcd(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_lcm(gr_ptr res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_factor(gr_ptr c, gr_vec_t factors, gr_vec_t exponents, gr_srcptr x, int flags, gr_ctx_t ctx) noexcept
    int gr_numerator(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_denominator(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_floor(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_ceil(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_trunc(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_nint(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_abs(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_i(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_conj(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_re(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_im(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_sgn(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_csgn(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_arg(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_pos_inf(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_neg_inf(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_uinf(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_undefined(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_unknown(gr_ptr res, gr_ctx_t ctx) noexcept
    int gr_cmp(int * res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_cmp_other(int * res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_cmpabs(int * res, gr_srcptr x, gr_srcptr y, gr_ctx_t ctx) noexcept
    int gr_cmpabs_other(int * res, gr_srcptr x, gr_srcptr y, gr_ctx_t y_ctx, gr_ctx_t ctx) noexcept
    int gr_ctx_fq_prime(fmpz_t p, gr_ctx_t ctx) noexcept
    int gr_ctx_fq_degree(slong * deg, gr_ctx_t ctx) noexcept
    int gr_ctx_fq_order(fmpz_t q, gr_ctx_t ctx) noexcept
    int gr_fq_frobenius(gr_ptr res, gr_srcptr x, slong e, gr_ctx_t ctx) noexcept
    int gr_fq_multiplicative_order(fmpz_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_fq_norm(fmpz_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_fq_trace(fmpz_t res, gr_srcptr x, gr_ctx_t ctx) noexcept
    truth_t gr_fq_is_primitive(gr_srcptr x, gr_ctx_t ctx) noexcept
    int gr_fq_pth_root(gr_ptr res, gr_srcptr x, gr_ctx_t ctx) noexcept
