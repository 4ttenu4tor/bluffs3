import logging
import pprint

from es import Kc_to_Kc_prime
from BitVector import BitVector
from constants import log, G1, G2

def test_Kc(name, g1, g2, Kc, Kc_mod_g1, Kc_prime):
    """Test from test vector the reverse computation of Kc."""
    quotient, remainder = Kc_prime.gf_divide_by_modulus(g2, 128)
    assert int(quotient) == int(Kc_mod_g1)
    log.debug("int(quotient): {}".format(int(quotient)))
    log.debug("int(remainder): {}".format(int(remainder)))

    mi = quotient.gf_MI(g1, 128)
    quotient2, remainder2 = quotient.gf_divide_by_modulus(g1, 128)
    mi2 = quotient.multiplicative_inverse(g1)
    log.debug("int(Kc): {}".format(int(Kc)))
    try:
        assert int(mi2) == int(Kc)
    except Exception:
        if mi2 is not None:
            log.debug("int(mi2): {}".format(int(mi2)))
        else:
            log.debug("mi2 is None")
        log.debug("Fail mi2")
    try:
        assert int(mi) == int(Kc)
    except Exception:
        log.debug("int(mi): {}".format(int(mi)))
        log.debug("Fail mi")
    try:
        assert int(remainder2) == int(Kc)
    except Exception:
        log.debug("int(remainder2): {}".format(int(remainder2)))
        log.debug("Fail remainder2")
    try:
        assert int(quotient2) == int(Kc)
    except Exception:
        log.debug("int(quotient2): {}".format(int(quotient2)))
        log.debug("Fail quotient2")

def test_g1_g2():
    # NOTE: L=1
    g1 = BitVector(intVal=0x011D, size=128)
    g1_t = BitVector(intVal=G1[1], size=128)
    assert int(g1) == int(g1_t)
    g2 = BitVector(intVal=0x00E275A0ABD218D4CF928B9BBF6CB08F, size=128)
    g2_t = BitVector(intVal=G2[1], size=128)
    assert int(g2) == int(g2_t)

    # NOTE: L=2
    g1 = BitVector(intVal=0x0001003F, size=128)
    g1_t = BitVector(intVal=G1[2], size=128)
    assert int(g1) == int(g1_t)
    g2 = BitVector(intVal=0x01E3F63D7659B37F18C258CFF6EFEF, size=128)
    g2_t = BitVector(intVal=G2[2], size=128)
    assert int(g2) == int(g2_t)

def test_Kc_prime_bit_vec():
    log.debug("Kc_prime(x) = g2(x) (Kc(x) mod g1(x))")
    one = BitVector(intVal=0x01, size=128)

    # NOTE: L=1
    g1 = BitVector(intVal=G1[1], size=128)
    g2 = BitVector(intVal=G2[1], size=128)
    Kc = BitVector(intVal=0xA2B230A493F281BB61A85B82A9D4A30E, size=128)
    Kc_prime = BitVector(intVal=0x7AA16F3959836BA322049A7B87F1D8A5, size=128)
    Kc_mod_g1 = BitVector(intVal=0x9F, size=128)

    Kc_mod_g1_t = Kc.gf_multiply_modular(one, g1, 128)
    assert Kc_mod_g1_t == Kc_mod_g1
    # NOTE: mutiplication increase the size of the vector
    Kc_prime_t = g2.gf_multiply(Kc_mod_g1)[128:]
    assert Kc_prime_t == Kc_prime

    # NOTE: L=2
    g1 = BitVector(intVal=G1[2], size=128)
    g2 = BitVector(intVal=G2[2], size=128)
    Kc = BitVector(intVal=0x64E7DF78BB7CCAA4614331235B3222AD, size=128)
    Kc_mod_g1 = BitVector(intVal=0x00001FF0, size=128)
    Kc_prime = BitVector(intVal=0x142057BB0BCEAC4C58BD142E1E710A50, size=128)

    Kc_mod_g1_t = Kc.gf_multiply_modular(one, g1, 128)
    assert Kc_mod_g1_t == Kc_mod_g1
    # NOTE: mutiplication increase the size of the vector
    Kc_prime_t = g2.gf_multiply(Kc_mod_g1)[128:]
    assert Kc_prime_t == Kc_prime

def test_Kc_prime():
    """pag 1511 L1 means that Kc negotiation ended up with L=1"""

    Kc = bytearray.fromhex("a2b230a493f281bb61a85b82a9d4a30e")
    Kc_prime = bytearray.fromhex("7aa16f3959836ba322049a7b87f1d8a5")
    rv = Kc_to_Kc_prime(Kc, 1)
    log.debug("test_Kc_prime L=1 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=1 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("64e7df78bb7ccaa4614331235b3222ad")
    Kc_prime = bytearray.fromhex("142057bb0bceac4c58bd142e1e710a50")
    rv = Kc_to_Kc_prime(Kc, 2)
    log.debug("test_Kc_prime L=2 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=2 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("575e5156ba685dc6112124acedb2c179")
    Kc_prime = bytearray.fromhex("d56d0adb8216cb397fe3c5911ff95618")
    rv = Kc_to_Kc_prime(Kc, 3)
    log.debug("test_Kc_prime L=3 rv      : {}".format(repr(rv)))
    log.debug("test_Kc_prime L=3 Kc_prime: {}".format(repr(Kc_prime)))
    assert rv == Kc_prime

    Kc = bytearray.fromhex("8917b4fc403b6db21596b86

