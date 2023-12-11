"""
e3_tests.py

e3 is used to generate Kc. The test cases assume that COF = ACO and ACO are provided.

Ar and Ar_prime use SAFER+
"""
import logging

from h import K_to_K_tilda, E, add_bytes_mod256, H
from e3 import e3
from constants import log

log.setLevel(logging.DEBUG)


def test_E(inp, L, ext_inp):
    rv = E(inp, L)
    assert rv == ext_inp


def test_Ar(key, inp, out):
    """Target out passed as hexstring.

    Eg: 'e9e5dfc1b3a79583e9e5dfc1b3a79583'
    """
    ct = Ar(key, inp, mode="enc")
    # pt = Ar(key, ct, mode='dec')
    # assert inp == pt
    log.debug("test_Ar ct : {}".format(ct.hex()))
    log.debug("test_Ar out: {}".format(out))
    assert ct.hex() == out


def test_e3(key, rand, cof, Kc):
    """Test from the test vector the reverse computation of Kc."""
    rv = e3(key, rand, cof)
    assert rv == Kc


def test_e3_1():
    """First test vector from the spec."""
    rand = bytearray.fromhex("00000000000000000000000000000000")
    aco = bytearray.fromhex("48afcdd4bd40fef76693b113")
    key = bytearray.fromhex("00000000000000000000000000000000")

    Keys = [i for i in range(18)]
    ComputedKeys, Ar, ComputedKeysPrime, ArPrime, ComputedKc = H(key, rand, aco, 12)
    print("test_e3_1 BEGIN ComputedKeys, Ar")
    round1 = bytearray.fromhex("00000000000000000000000000000000")
    assert Ar[1] == round1
    Keys[1] = bytearray.fromhex("00000000000000000000000000000000")
    assert ComputedKeys[1] == Keys[1]
    Keys[2] = bytearray.fromhex("4697b1baa3b7100ac537b3c95a28ac64")
    assert ComputedKeys[2] == Keys[2]
    # NOTE: this should be input to round2
    round2 = bytearray.fromhex("78d19f9307d2476a523ec7a8a026042a")
    assert Ar[2] == round2
    Keys[3] = bytearray.fromhex("ecabaac66795580df89af66e66dc053d")
    assert ComputedKeys[3] == Keys[3]
    Keys[4] = bytearray.fromhex("8ac3d8896ae9364943bfebd4969b68a0")
    assert ComputedKeys[4] == Keys[4]
    round3 = bytearray.fromhex("600265247668dda0e81c07bbb30ed503")
    assert Ar[3] == round3
    Keys[5] = bytearray.fromhex("5d57921fd5715cbb22c1be7bbc996394")
    assert ComputedKeys[5] == Keys[5]
    Keys[6] = bytearray.fromhex("2a61b8343219fdfb1740e6511d41448f")
    assert ComputedKeys[6] == Keys[6]
    round4 = bytearray.fromhex("d7552ef7cc9dbde568d80c2215bc4277")
    assert Ar[4] == round4
    Keys[7] = bytearray.fromhex("dd0480dee731d67f01a2f739da6f23ca")
    assert ComputedKeys[7] == Keys[7]
    Keys[8] = bytearray.fromhex("3ad01cd1303e12a1cd0fe0a8af82592c")
    assert ComputedKeys[8] == Keys[8]
    round5 = bytearray.fromhex("fb06bef32b52ab8f2a4f2b6ef7f6d0cd")
    assert Ar[5] == round5
    Keys[9] = bytearray.fromhex("7dadb2efc287ce75061302904f2e7233")
    assert ComputedKeys[9] == Keys[9]
    Keys[10] = bytearray.fromhex("c08dcfa981e2c4272f6c7a9f52e11538")
    assert ComputedKeys[10] == Keys[10]
    round6 = bytearray.fromhex("b46b711ebb3cf69e847a75f0ab884bdd")
    assert Ar[6] == round6
    Keys[11] = bytearray.fromhex("fc2042c708e409555e8c147660ffdfd7")
    assert ComputedKeys[11] == Keys[11]
    Keys[12] = bytearray.fromhex("fa0b21001af9a6b9e89e624cd99150d2")
    assert ComputedKeys[12] == Keys[12]
    round7 = bytearray.fromhex("c585f308ff19404294f06b292e978994")
    assert Ar[7] == round7
    Keys[13] = bytearray.fromhex("18b40784ea5ba4c80ecb48694b4e9c35")
    assert ComputedKeys[13] == Keys[13]
    Keys[14] = bytearray.fromhex("454d54e5253c0c4a8b3fcca7db6baef4")
    assert ComputedKeys[14] == Keys[14]
    # NOTE: round8 does not include last add_one
    round8 = bytearray.fromhex("2665fadb13acf952bf74b4ab12264b9f")
    assert Ar[8] == round8
    Keys[15] = bytearray.fromhex("2df37c6d9db52674f29353b0f011ed83")
    assert ComputedKeys[15] == Keys[15]
    Keys[16] = bytearray.fromhex("b60316733b1e8e70bd861b477e2456f1")
    assert ComputedKeys[16] == Keys[16]
    Keys[17] = bytearray.fromhex("884697b1baa3b7100ac537b3c95a28ac")
    assert ComputedKeys[17] == Keys[17]
    print("test_e3_1 END ComputedKeys, Ar")

    print("test_e3_1 BEGIN ComputedKeysPrime, ArPrime")
    round1 = bytearray.fromhex("5d3ecb17f26083df0b7f2b9b29aef87c")
    assert ArPrime[1] == round1
    Keys[1] = bytearray.fromhex("e9e5dfc1b3a

