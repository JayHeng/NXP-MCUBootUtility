#!/usr/bin/env python

# Copyright (c) 2014 Freescale Semiconductor, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# o Redistributions of source code must retain the above copyright notice, this list
#   of conditions and the following disclaimer.
#
# o Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
#
# o Neither the name of Freescale Semiconductor, Inc. nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, os
sys.path.append(os.path.abspath(".."))
from boot.memoryrange import MemoryRange
from ui import RTxxx_uidef
from ui import RTxxx_uidef_otp
from ui import uidef
from run import RTxxx_rundef
from gen import gendef

cpu = 'RW612'
board = 'RD'
compiler = 'iar'
build = 'Release'

availablePeripherals = 0x11
romUsbVid = '0x1FC9'
romUsbPid = '0x0020'
hasSdpReadRegisterCmd = None
bootHeaderType = gendef.kBootHeaderType_Vector
flashloaderUsbVid = '0x15A2'
flashloaderUsbPid = '0x0073'
flashloaderLoadAddr = None
flashloaderJumpAddr = None
availableCommands = 0x5EFDF
supportedPeripheralSpeed_uart = [4800, 9600, 19200, 57600, 115200] # @todo Verify
availableSecureBootTypes = RTxxx_uidef.kSecureBootType_Latest
hasRemappedFuse = None
availableBootDevices = [RTxxx_uidef.kBootDevice_FlexspiNor]
flexspiNorDevice = uidef.kFlexspiNorDevice_MXIC_MX25L12845G
flexspiNorMemBase0   = 0x18000000 # CM33 Secure
flexspiNorMemBase0Ns = 0x08000000 # CM33 Non-Secure
flexspiNorMemBase0Aliased = None
flexspiNorMemBase0AliasedNs =None
flexspiNorMem0MaxSize = RTxxx_rundef.kBootDeviceMemXipSize_FlexspiNor
flexspiNorMem0AliasedMaxSize = None
flexspiNorMemBase1   = None
flexspiNorMemBase1Ns = None
flexspiNorMemBase1Aliased = None
flexspiNorMemBase1AliasedNs =None
flexspiNorMem1MaxSize = None
flexspiNorMem1AliasedMaxSize = None
flexspiFreqs = ['30MHz', '50MHz', '60MHz', '80MHz', '100MHz', '120MHz', '133MHz', '166MHz', '200MHz']
xspiNorCfgInfoOffset = 0x400
xspiNorCfgInfoLen    = 0x200
xspiNorImgHdrOffset = 0x1000
flexspiNorEfuseBootCfg0Bits = None
isSipFlexspiNorDevice = False
isNonXipImageAppliableForXipableDeviceUnderClosedHab = None
hasFlexspiNorDualImageBoot = True
hasFlexspiNorEcc = False
isEccTypeSetInFuseMiscConf = None
isSwEccSetAsDefaultInNandOpt = None
hasMultiUsdhcBootInstance = True
hwAuthHashEngine = None

quadspiNorDevice = None
quadspiNorMemBase = None

ramFreeSpaceStart_LoadCommOpt        = 0x0010c000
ramFreeSpaceStart_LoadDekData        = None
ramFreeSpaceStart_LoadKeyBlobContext = None
ramFreeSpaceStart_LoadKeyBlobData    = None
ramFreeSpaceStart_LoadCfgBlock       = 0x0010d000
ramFreeSpaceStart_LoadPrdbOpt        = None
ramFreeSpaceStart_Rom                = None

registerAddrDict = None
registerDefnDict  = None

efusemapIndexDict = None
efusemapDefnDict  = None
efuseDescDiffDict = None

otpmapIndexDict = RTxxx_uidef_otp.otpmapIndexDict_RTxxx
otpmapDefnDict  = RTxxx_uidef_otp.otpmapDefnDict_RTxxx
otpDescDiffDict = None

ftfxNorMemBase = None
c040hdNorMemBase = None

sbLoaderVersion = gendef.kSbLoaderVersion_v2_0

# memory map
memoryRange = {
    # SRAM AHB-C bus, 1.1875MByte
    'sramc' : MemoryRange(0x00000000, 0x130000, 'state_sramc_mem.dat'),
    # SRAM AHB-C bus, 1.1875MByte
    'sramc_ns' : MemoryRange(0x10000000, 0x130000, 'state_sramc_ns_mem.dat'),
    # SRAM AHB-S bus, 1.1875MByte
    'srams' : MemoryRange(0x20000000, 0x130000, 'state_srams_mem.dat'),
    # SRAM AHB-S bus, 1.1875MByte
    'srams_ns' : MemoryRange(0x30000000, 0x130000, 'state_srams_ns_mem.dat'),

    # FLASH, 64KByte / 512MByte
    'flash': MemoryRange(0x00000000, 0x20000000, 'state_flash_mem.dat', True, 0x10000),

    # FlexSPI0 RAM Secure, 128MByte
    'flexspi1_ram' : MemoryRange(0x18000000, 0x08000000, 'state_flexspi1_mem.dat'),
    # FlexSPI0 RAM Non-Secure, 128MByte
    'flexspi1_ram_ns' : MemoryRange(0x08000000, 0x08000000, 'state_flexspi1_ns_mem.dat')
}

reservedRegionDict = {
    # SRAM, 512KB
    'sram' : [0x20203800, 0x20207EF8]
}
