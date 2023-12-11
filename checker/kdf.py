#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
kdf.py
"""

import logging
from e1 import e1
from es import Kc_to_Kc_prime
from e3 import e3
from constants import log

log.setLevel(logging.INFO)

def kdf(LK, AU_RAND, EN_RAND, BTADDR, ENTROPY):
    """Generate KcPrime

    LK link key, 16 Bytes

    AU_RAND, 16 Bytes

    EN_RAND, 16 Bytes

    BTADD address (leftmost byte is MSB)

    ENTROPY  = [1, ..., 16]
    """
    assert isinstance(LK, bytearray) and len(LK) == 16
    assert isinstance(AU_RAND, bytearray) and len(AU_RAND) == 16
    assert isinstance(EN_RAND, bytearray) and len(EN_RAND) == 16
    assert isinstance(BTADDR, bytearray) and len(BTADDR) == 6
    assert isinstance(ENTROPY, int) and 1 <= ENTROPY <= 16

    BTADDR.reverse()
    _, COF = e1(LK, AU_RAND, BTADDR)
    log.debug("COF: {}".format(repr(COF)))
    # NOTE: redo reverse as it is passed by reference
    BTADDR.reverse()

    Kc = e3(LK, EN_RAND, COF)
    log.debug("Kc: {}".format(repr(Kc)))
    Kc.reverse()

    KcPrime = Kc_to_Kc_prime(Kc, ENTROPY)
    KcPrime.reverse()

    return KcPrime

