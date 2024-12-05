# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/fmpz.h

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
    fmpz PTR_TO_COEFF(__mpz_struct * ptr) noexcept
    __mpz_struct * COEFF_TO_PTR(fmpz f) noexcept
    __mpz_struct * _fmpz_new_mpz() noexcept
    void _fmpz_clear_mpz(fmpz f) noexcept
    void _fmpz_cleanup_mpz_content() noexcept
    void _fmpz_cleanup() noexcept
    __mpz_struct * _fmpz_promote(fmpz_t f) noexcept
    __mpz_struct * _fmpz_promote_val(fmpz_t f) noexcept
    void _fmpz_demote(fmpz_t f) noexcept
    void _fmpz_demote_val(fmpz_t f) noexcept
    bint _fmpz_is_canonical(const fmpz_t f) noexcept
    void fmpz_init(fmpz_t f) noexcept
    void fmpz_init2(fmpz_t f, ulong limbs) noexcept
    void fmpz_clear(fmpz_t f) noexcept
    void fmpz_init_set(fmpz_t f, const fmpz_t g) noexcept
    void fmpz_init_set_ui(fmpz_t f, ulong g) noexcept
    void fmpz_init_set_si(fmpz_t f, slong g) noexcept
    void fmpz_randbits(fmpz_t f, flint_rand_t state, flint_bitcnt_t bits) noexcept
    void fmpz_randtest(fmpz_t f, flint_rand_t state, flint_bitcnt_t bits) noexcept
    void fmpz_randtest_unsigned(fmpz_t f, flint_rand_t state, flint_bitcnt_t bits) noexcept
    void fmpz_randtest_not_zero(fmpz_t f, flint_rand_t state, flint_bitcnt_t bits) noexcept
    void fmpz_randm(fmpz_t f, flint_rand_t state, const fmpz_t m) noexcept
    void fmpz_randtest_mod(fmpz_t f, flint_rand_t state, const fmpz_t m) noexcept
    void fmpz_randtest_mod_signed(fmpz_t f, flint_rand_t state, const fmpz_t m) noexcept
    void fmpz_randprime(fmpz_t f, flint_rand_t state, flint_bitcnt_t bits, int proved) noexcept
    slong fmpz_get_si(const fmpz_t f) noexcept
    ulong fmpz_get_ui(const fmpz_t f) noexcept
    void fmpz_get_uiui(mp_limb_t * hi, mp_limb_t * low, const fmpz_t f) noexcept
    mp_limb_t fmpz_get_nmod(const fmpz_t f, nmod_t mod) noexcept
    double fmpz_get_d(const fmpz_t f) noexcept
    void fmpz_set_mpf(fmpz_t f, const mpf_t x) noexcept
    void fmpz_get_mpf(mpf_t x, const fmpz_t f) noexcept
    void fmpz_get_mpfr(mpfr_t x, const fmpz_t f, mpfr_rnd_t rnd) noexcept
    double fmpz_get_d_2exp(slong * exp, const fmpz_t f) noexcept
    void fmpz_get_mpz(mpz_t x, const fmpz_t f) noexcept
    int fmpz_get_mpn(mp_ptr * n, fmpz_t n_in) noexcept
    char * fmpz_get_str(char * str, int b, const fmpz_t f) noexcept
    void fmpz_set_si(fmpz_t f, slong val) noexcept
    void fmpz_set_ui(fmpz_t f, ulong val) noexcept
    void fmpz_set_d(fmpz_t f, double c) noexcept
    void fmpz_set_d_2exp(fmpz_t f, double d, slong exp) noexcept
    void fmpz_neg_ui(fmpz_t f, ulong val) noexcept
    void fmpz_set_uiui(fmpz_t f, mp_limb_t hi, mp_limb_t lo) noexcept
    void fmpz_neg_uiui(fmpz_t f, mp_limb_t hi, mp_limb_t lo) noexcept
    void fmpz_set_signed_uiui(fmpz_t f, ulong hi, ulong lo) noexcept
    void fmpz_set_signed_uiuiui(fmpz_t f, ulong hi, ulong mid, ulong lo) noexcept
    void fmpz_set_ui_array(fmpz_t out, const ulong * input, slong n) noexcept
    void fmpz_set_signed_ui_array(fmpz_t out, const ulong * input, slong n) noexcept
    void fmpz_get_ui_array(ulong * out, slong n, const fmpz_t input) noexcept
    void fmpz_get_signed_ui_array(ulong * out, slong n, const fmpz_t input) noexcept
    void fmpz_get_signed_uiui(ulong * hi, ulong * lo, const fmpz_t input) noexcept
    void fmpz_set_mpz(fmpz_t f, const mpz_t x) noexcept
    int fmpz_set_str(fmpz_t f, const char * str, int b) noexcept
    void fmpz_set_ui_smod(fmpz_t f, mp_limb_t x, mp_limb_t m) noexcept
    void flint_mpz_init_set_readonly(mpz_t z, const fmpz_t f) noexcept
    void flint_mpz_clear_readonly(mpz_t z) noexcept
    void fmpz_init_set_readonly(fmpz_t f, const mpz_t z) noexcept
    void fmpz_clear_readonly(fmpz_t f) noexcept
    int fmpz_read(fmpz_t f) noexcept
    int fmpz_fread(FILE * file, fmpz_t f) noexcept
    size_t fmpz_inp_raw(fmpz_t x, FILE * fin) noexcept
    int fmpz_print(const fmpz_t x) noexcept
    int fmpz_fprint(FILE * file, const fmpz_t x) noexcept
    size_t fmpz_out_raw(FILE * fout, const fmpz_t x ) noexcept
    size_t fmpz_sizeinbase(const fmpz_t f, int b) noexcept
    flint_bitcnt_t fmpz_bits(const fmpz_t f) noexcept
    mp_size_t fmpz_size(const fmpz_t f) noexcept
    int fmpz_sgn(const fmpz_t f) noexcept
    flint_bitcnt_t fmpz_val2(const fmpz_t f) noexcept
    void fmpz_swap(fmpz_t f, fmpz_t g) noexcept
    void fmpz_set(fmpz_t f, const fmpz_t g) noexcept
    void fmpz_zero(fmpz_t f) noexcept
    void fmpz_one(fmpz_t f) noexcept
    int fmpz_abs_fits_ui(const fmpz_t f) noexcept
    int fmpz_fits_si(const fmpz_t f) noexcept
    void fmpz_setbit(fmpz_t f, ulong i) noexcept
    int fmpz_tstbit(const fmpz_t f, ulong i) noexcept
    mp_limb_t fmpz_abs_lbound_ui_2exp(slong * exp, const fmpz_t x, int bits) noexcept
    mp_limb_t fmpz_abs_ubound_ui_2exp(slong * exp, const fmpz_t x, int bits) noexcept
    int fmpz_cmp(const fmpz_t f, const fmpz_t g) noexcept
    int fmpz_cmp_ui(const fmpz_t f, ulong g) noexcept
    int fmpz_cmp_si(const fmpz_t f, slong g) noexcept
    int fmpz_cmpabs(const fmpz_t f, const fmpz_t g) noexcept
    int fmpz_cmp2abs(const fmpz_t f, const fmpz_t g) noexcept
    bint fmpz_equal(const fmpz_t f, const fmpz_t g) noexcept
    bint fmpz_equal_ui(const fmpz_t f, ulong g) noexcept
    bint fmpz_equal_si(const fmpz_t f, slong g) noexcept
    bint fmpz_is_zero(const fmpz_t f) noexcept
    bint fmpz_is_one(const fmpz_t f) noexcept
    bint fmpz_is_pm1(const fmpz_t f) noexcept
    bint fmpz_is_even(const fmpz_t f) noexcept
    bint fmpz_is_odd(const fmpz_t f) noexcept
    void fmpz_neg(fmpz_t f1, const fmpz_t f2) noexcept
    void fmpz_abs(fmpz_t f1, const fmpz_t f2) noexcept
    void fmpz_add(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_add_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_add_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_sub(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_sub_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_sub_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_mul(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_mul_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_mul_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_mul2_uiui(fmpz_t f, const fmpz_t g, ulong x, ulong y) noexcept
    void fmpz_mul_2exp(fmpz_t f, const fmpz_t g, ulong e) noexcept
    void fmpz_one_2exp(fmpz_t f, ulong e) noexcept
    void fmpz_addmul(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_addmul_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_addmul_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_submul(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_submul_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_submul_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_fmma(fmpz_t f, const fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_t d) noexcept
    void fmpz_fmms(fmpz_t f, const fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_t d) noexcept
    void fmpz_cdiv_qr(fmpz_t f, fmpz_t s, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_fdiv_qr(fmpz_t f, fmpz_t s, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_tdiv_qr(fmpz_t f, fmpz_t s, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_ndiv_qr(fmpz_t f, fmpz_t s, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_cdiv_q(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_fdiv_q(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_tdiv_q(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_cdiv_q_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_fdiv_q_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_tdiv_q_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_cdiv_q_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_fdiv_q_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_tdiv_q_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_cdiv_q_2exp(fmpz_t f, const fmpz_t g, ulong exp) noexcept
    void fmpz_fdiv_q_2exp(fmpz_t f, const fmpz_t g, ulong exp) noexcept
    void fmpz_tdiv_q_2exp(fmpz_t f, const fmpz_t g, ulong exp) noexcept
    void fmpz_fdiv_r(fmpz_t s, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_cdiv_r_2exp(fmpz_t s, const fmpz_t g, ulong exp) noexcept
    void fmpz_fdiv_r_2exp(fmpz_t s, const fmpz_t g, ulong exp) noexcept
    void fmpz_tdiv_r_2exp(fmpz_t s, const fmpz_t g, ulong exp) noexcept
    ulong fmpz_cdiv_ui(const fmpz_t g, ulong h) noexcept
    ulong fmpz_fdiv_ui(const fmpz_t g, ulong h) noexcept
    ulong fmpz_tdiv_ui(const fmpz_t g, ulong h) noexcept
    void fmpz_divexact(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_divexact_si(fmpz_t f, const fmpz_t g, slong h) noexcept
    void fmpz_divexact_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_divexact2_uiui(fmpz_t f, const fmpz_t g, ulong x, ulong y) noexcept
    int fmpz_divisible(const fmpz_t f, const fmpz_t g) noexcept
    int fmpz_divisible_si(const fmpz_t f, slong g) noexcept
    int fmpz_divides(fmpz_t q, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_mod(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    ulong fmpz_mod_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_smod(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_preinvn_init(fmpz_preinvn_t inv, const fmpz_t f) noexcept
    void fmpz_preinvn_clear(fmpz_preinvn_t inv) noexcept
    void fmpz_fdiv_qr_preinvn(fmpz_t f, fmpz_t s, const fmpz_t g, const fmpz_t h, const fmpz_preinvn_t hinv) noexcept
    void fmpz_pow_ui(fmpz_t f, const fmpz_t g, ulong x) noexcept
    void fmpz_ui_pow_ui(fmpz_t f, ulong g, ulong x) noexcept
    int fmpz_pow_fmpz(fmpz_t f, const fmpz_t g, const fmpz_t x) noexcept
    void fmpz_powm_ui(fmpz_t f, const fmpz_t g, ulong e, const fmpz_t m) noexcept
    void fmpz_powm(fmpz_t f, const fmpz_t g, const fmpz_t e, const fmpz_t m) noexcept
    slong fmpz_clog(const fmpz_t x, const fmpz_t b) noexcept
    slong fmpz_clog_ui(const fmpz_t x, ulong b) noexcept
    slong fmpz_flog(const fmpz_t x, const fmpz_t b) noexcept
    slong fmpz_flog_ui(const fmpz_t x, ulong b) noexcept
    double fmpz_dlog(const fmpz_t x) noexcept
    int fmpz_sqrtmod(fmpz_t b, const fmpz_t a, const fmpz_t p) noexcept
    void fmpz_sqrt(fmpz_t f, const fmpz_t g) noexcept
    void fmpz_sqrtrem(fmpz_t f, fmpz_t r, const fmpz_t g) noexcept
    bint fmpz_is_square(const fmpz_t f) noexcept
    int fmpz_root(fmpz_t r, const fmpz_t f, slong n) noexcept
    bint fmpz_is_perfect_power(fmpz_t root, const fmpz_t f) noexcept
    void fmpz_fac_ui(fmpz_t f, ulong n) noexcept
    void fmpz_fib_ui(fmpz_t f, ulong n) noexcept
    void fmpz_bin_uiui(fmpz_t f, ulong n, ulong k) noexcept
    void _fmpz_rfac_ui(fmpz_t r, const fmpz_t x, ulong a, ulong b) noexcept
    void fmpz_rfac_ui(fmpz_t r, const fmpz_t x, ulong k) noexcept
    void fmpz_rfac_uiui(fmpz_t r, ulong x, ulong k) noexcept
    void fmpz_mul_tdiv_q_2exp(fmpz_t f, const fmpz_t g, const fmpz_t h, ulong exp) noexcept
    void fmpz_mul_si_tdiv_q_2exp(fmpz_t f, const fmpz_t g, slong x, ulong exp) noexcept
    void fmpz_gcd_ui(fmpz_t f, const fmpz_t g, ulong h) noexcept
    void fmpz_gcd(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_gcd3(fmpz_t f, const fmpz_t a, const fmpz_t b, const fmpz_t c) noexcept
    void fmpz_lcm(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_gcdinv(fmpz_t d, fmpz_t a, const fmpz_t f, const fmpz_t g) noexcept
    void fmpz_xgcd(fmpz_t d, fmpz_t a, fmpz_t b, const fmpz_t f, const fmpz_t g) noexcept
    void fmpz_xgcd_canonical_bezout(fmpz_t d, fmpz_t a, fmpz_t b, const fmpz_t f, const fmpz_t g) noexcept
    void fmpz_xgcd_partial(fmpz_t co2, fmpz_t co1, fmpz_t r2, fmpz_t r1, const fmpz_t L) noexcept
    slong _fmpz_remove(fmpz_t x, const fmpz_t f, double finv) noexcept
    slong fmpz_remove(fmpz_t rop, const fmpz_t op, const fmpz_t f) noexcept
    int fmpz_invmod(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    void fmpz_negmod(fmpz_t f, const fmpz_t g, const fmpz_t h) noexcept
    int fmpz_jacobi(const fmpz_t a, const fmpz_t n) noexcept
    int fmpz_kronecker(const fmpz_t a, const fmpz_t n) noexcept
    void fmpz_divides_mod_list(fmpz_t xstart, fmpz_t xstride, fmpz_t xlength, const fmpz_t a, const fmpz_t b, const fmpz_t n) noexcept
    int fmpz_bit_pack(mp_limb_t * arr, flint_bitcnt_t shift, flint_bitcnt_t bits, const fmpz_t coeff, int negate, int borrow) noexcept
    int fmpz_bit_unpack(fmpz_t coeff, mp_limb_t * arr, flint_bitcnt_t shift, flint_bitcnt_t bits, int negate, int borrow) noexcept
    void fmpz_bit_unpack_unsigned(fmpz_t coeff, const mp_limb_t * arr, flint_bitcnt_t shift, flint_bitcnt_t bits) noexcept
    void fmpz_complement(fmpz_t r, const fmpz_t f) noexcept
    void fmpz_clrbit(fmpz_t f, ulong i) noexcept
    void fmpz_combit(fmpz_t f, ulong i) noexcept
    void fmpz_and(fmpz_t r, const fmpz_t a, const fmpz_t b) noexcept
    void fmpz_or(fmpz_t r, const fmpz_t a, const fmpz_t b) noexcept
    void fmpz_xor(fmpz_t r, const fmpz_t a, const fmpz_t b) noexcept
    ulong fmpz_popcnt(const fmpz_t a) noexcept
    void fmpz_CRT_ui(fmpz_t out, const fmpz_t r1, const fmpz_t m1, ulong r2, ulong m2, int sign) noexcept
    void fmpz_CRT(fmpz_t out, const fmpz_t r1, const fmpz_t m1, const fmpz_t r2, const fmpz_t m2, int sign) noexcept
    void fmpz_multi_mod_ui(mp_limb_t * out, const fmpz_t input, const fmpz_comb_t comb, fmpz_comb_temp_t temp) noexcept
    void fmpz_multi_CRT_ui(fmpz_t output, mp_srcptr residues, const fmpz_comb_t comb, fmpz_comb_temp_t ctemp, int sign) noexcept
    void fmpz_comb_init(fmpz_comb_t comb, mp_srcptr primes, slong num_primes) noexcept
    void fmpz_comb_temp_init(fmpz_comb_temp_t temp, const fmpz_comb_t comb) noexcept
    void fmpz_comb_clear(fmpz_comb_t comb) noexcept
    void fmpz_comb_temp_clear(fmpz_comb_temp_t temp) noexcept
    void fmpz_multi_CRT_init(fmpz_multi_CRT_t CRT) noexcept
    int fmpz_multi_CRT_precompute(fmpz_multi_CRT_t CRT, const fmpz * moduli, slong len) noexcept
    void fmpz_multi_CRT_precomp(fmpz_t output, const fmpz_multi_CRT_t P, const fmpz * inputs, int sign) noexcept
    int fmpz_multi_CRT(fmpz_t output, const fmpz * moduli, const fmpz * values, slong len, int sign) noexcept
    void fmpz_multi_CRT_clear(fmpz_multi_CRT_t P) noexcept
    bint fmpz_is_strong_probabprime(const fmpz_t n, const fmpz_t a) noexcept
    bint fmpz_is_probabprime_lucas(const fmpz_t n) noexcept
    bint fmpz_is_probabprime_BPSW(const fmpz_t n) noexcept
    bint fmpz_is_probabprime(const fmpz_t p) noexcept
    bint fmpz_is_prime_pseudosquare(const fmpz_t n) noexcept
    bint fmpz_is_prime_pocklington(fmpz_t F, fmpz_t R, const fmpz_t n, mp_ptr pm1, slong num_pm1) noexcept
    void _fmpz_nm1_trial_factors(const fmpz_t n, mp_ptr pm1, slong * num_pm1, ulong limit) noexcept
    bint fmpz_is_prime_morrison(fmpz_t F, fmpz_t R, const fmpz_t n, mp_ptr pp1, slong num_pp1) noexcept
    void _fmpz_np1_trial_factors(const fmpz_t n, mp_ptr pp1, slong * num_pp1, ulong limit) noexcept
    bint fmpz_is_prime(const fmpz_t n) noexcept
    void fmpz_lucas_chain(fmpz_t Vm, fmpz_t Vm1, const fmpz_t A, const fmpz_t m, const fmpz_t n) noexcept
    void fmpz_lucas_chain_full(fmpz_t Vm, fmpz_t Vm1, const fmpz_t A, const fmpz_t B, const fmpz_t m, const fmpz_t n) noexcept
    void fmpz_lucas_chain_double(fmpz_t U2m, fmpz_t U2m1, const fmpz_t Um, const fmpz_t Um1, const fmpz_t A, const fmpz_t B, const fmpz_t n) noexcept
    void fmpz_lucas_chain_add(fmpz_t Umn, fmpz_t Umn1, const fmpz_t Um, const fmpz_t Um1, const fmpz_t Un, const fmpz_t Un1, const fmpz_t A, const fmpz_t B, const fmpz_t n) noexcept
    void fmpz_lucas_chain_mul(fmpz_t Ukm, fmpz_t Ukm1, const fmpz_t Um, const fmpz_t Um1, const fmpz_t A, const fmpz_t B, const fmpz_t k, const fmpz_t n) noexcept
    void fmpz_lucas_chain_VtoU(fmpz_t Um, fmpz_t Um1, const fmpz_t Vm, const fmpz_t Vm1, const fmpz_t A, const fmpz_t B, const fmpz_t Dinv, const fmpz_t n) noexcept
    int fmpz_divisor_in_residue_class_lenstra(fmpz_t fac, const fmpz_t n, const fmpz_t r, const fmpz_t s) noexcept
    void fmpz_nextprime(fmpz_t res, const fmpz_t n, int proved) noexcept
    void fmpz_primorial(fmpz_t res, ulong n) noexcept
    void fmpz_factor_euler_phi(fmpz_t res, const fmpz_factor_t fac) noexcept
    void fmpz_euler_phi(fmpz_t res, const fmpz_t n) noexcept
    int fmpz_factor_moebius_mu(const fmpz_factor_t fac) noexcept
    int fmpz_moebius_mu(const fmpz_t n) noexcept
    void fmpz_factor_divisor_sigma(fmpz_t res, ulong k, const fmpz_factor_t fac) noexcept
    void fmpz_divisor_sigma(fmpz_t res, ulong k, const fmpz_t n) noexcept

from .fmpz_macros cimport *
