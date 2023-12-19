#! /usr/bin/env python

# Copyright (c) 2013 Freescale Semiconductor, Inc.
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
import commands, memoryrange, peripherals
sys.path.append(os.path.abspath(".."))
from utils import misc

##
# Bootloader target definition.
class Target(object):

    def __init__(self, cpu, board='', build='', **kwargs):
                #baseDir='.', elfFile=None, memory={}, availableCommands=0,
                #availablePeripherals=0, deviceMemoryAccessable=False, systemDeviceId=0, isBootROM=False, isCrcCheckSupported=False):
        self.cpu = cpu
        self.board = board
        self.build = build

        self.baseDir = misc.get_dict_default(kwargs, 'baseDir', '.')
        self.memoryRange = misc.get_dict_default(kwargs, 'memoryRange', {})
        self.reservedRegionDict = misc.get_dict_default(kwargs, 'reservedRegionDict', {})
        self.availableCommands = misc.get_dict_default(kwargs, 'availableCommands', 0)
        self.availablePeripherals = misc.get_dict_default(kwargs, 'availablePeripherals', 0)
        self.romUsbVid = misc.get_dict_default(kwargs, 'romUsbVid', None)
        self.romUsbPid = misc.get_dict_default(kwargs, 'romUsbPid', None)
        self.hasSdpReadRegisterCmd = misc.get_dict_default(kwargs, 'hasSdpReadRegisterCmd', None)
        self.bootHeaderType = misc.get_dict_default(kwargs, 'bootHeaderType', None)
        self.flashloaderUsbVid = misc.get_dict_default(kwargs, 'flashloaderUsbVid', None)
        self.flashloaderUsbPid = misc.get_dict_default(kwargs, 'flashloaderUsbPid', None)
        self.flashloaderLoadAddr = misc.get_dict_default(kwargs, 'flashloaderLoadAddr', None)
        self.flashloaderJumpAddr = misc.get_dict_default(kwargs, 'flashloaderJumpAddr', None)
        self.supportedPeripheralSpeed_uart = misc.get_dict_default(kwargs, 'supportedPeripheralSpeed_uart', None)
        self.availableSecureBootTypes = misc.get_dict_default(kwargs, 'availableSecureBootTypes', None)
        self.hasRemappedFuse = misc.get_dict_default(kwargs, 'hasRemappedFuse', None)
        self.availableBootDevices = misc.get_dict_default(kwargs, 'availableBootDevices', None)
        self.flexspiNorDevice = misc.get_dict_default(kwargs, 'flexspiNorDevice', None)
        self.flexspiNorMemBase = misc.get_dict_default(kwargs, 'flexspiNorMemBase0', None)
        self.flexspiNorMemMaxSize = misc.get_dict_default(kwargs, 'flexspiNorMem0MaxSize', None)
        self.flexspiNorMemBase0 = misc.get_dict_default(kwargs, 'flexspiNorMemBase0', None)
        self.flexspiNorMemBase0Ns = misc.get_dict_default(kwargs, 'flexspiNorMemBase0Ns', None)
        self.flexspiNorMemBase0Aliased = misc.get_dict_default(kwargs, 'flexspiNorMemBase0Aliased', None)
        self.flexspiNorMemBase0AliasedNs = misc.get_dict_default(kwargs, 'flexspiNorMemBase0AliasedNs', None)
        self.flexspiNorMem0MaxSize = misc.get_dict_default(kwargs, 'flexspiNorMem0MaxSize', None)
        self.flexspiNorMem0AliasedMaxSize = misc.get_dict_default(kwargs, 'flexspiNorMem0AliasedMaxSize', None)
        self.flexspiNorMemBase1 = misc.get_dict_default(kwargs, 'flexspiNorMemBase1', None)
        self.flexspiNorMemBase1Ns = misc.get_dict_default(kwargs, 'flexspiNorMemBase1Ns', None)
        self.flexspiNorMemBase1Aliased = misc.get_dict_default(kwargs, 'flexspiNorMemBase1Aliased', None)
        self.flexspiNorMemBase1AliasedNs = misc.get_dict_default(kwargs, 'flexspiNorMemBase1AliasedNs', None)
        self.flexspiNorMem1MaxSize = misc.get_dict_default(kwargs, 'flexspiNorMem1MaxSize', None)
        self.flexspiNorMem1AliasedMaxSize = misc.get_dict_default(kwargs, 'flexspiNorMem1AliasedMaxSize', None)
        self.flexspiFreqs = misc.get_dict_default(kwargs, 'flexspiFreqs', None)
        self.xspiNorCfgInfoOffset = misc.get_dict_default(kwargs, 'xspiNorCfgInfoOffset', None)
        self.xspiNorCfgInfoLen = misc.get_dict_default(kwargs, 'xspiNorCfgInfoLen', None)
        self.xspiNorImgHdrOffset = misc.get_dict_default(kwargs, 'xspiNorImgHdrOffset', None)
        self.flexspiNorEfuseBootCfg0Bits = misc.get_dict_default(kwargs, 'flexspiNorEfuseBootCfg0Bits', None)
        self.isNonXipImageAppliableForXipableDeviceUnderClosedHab = misc.get_dict_default(kwargs, 'isNonXipImageAppliableForXipableDeviceUnderClosedHab', None)
        self.isSipFlexspiNorDevice = misc.get_dict_default(kwargs, 'isSipFlexspiNorDevice', None)
        self.hasFlexspiNorDualImageBoot = misc.get_dict_default(kwargs, 'hasFlexspiNorDualImageBoot', None)
        self.hasFlexspiNorEcc = misc.get_dict_default(kwargs, 'hasFlexspiNorEcc', None)
        self.isEccTypeSetInFuseMiscConf = misc.get_dict_default(kwargs, 'isEccTypeSetInFuseMiscConf', None)
        self.isSwEccSetAsDefaultInNandOpt = misc.get_dict_default(kwargs, 'isSwEccSetAsDefaultInNandOpt', None)
        self.hasMultiUsdhcBootInstance = misc.get_dict_default(kwargs, 'hasMultiUsdhcBootInstance', None)
        self.hwAuthHashEngine = misc.get_dict_default(kwargs, 'hwAuthHashEngine', None)

        self.quadspiNorDevice = misc.get_dict_default(kwargs, 'quadspiNorDevice', None)
        self.quadspiNorMemBase = misc.get_dict_default(kwargs, 'quadspiNorMemBase', None)

        self.ramFreeSpaceStart_LoadCommOpt = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadCommOpt', None)
        self.ramFreeSpaceStart_LoadDekData = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadDekData', None)
        self.ramFreeSpaceStart_LoadKeyBlobContext = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadKeyBlobContext', None)
        self.ramFreeSpaceStart_LoadKeyBlobData = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadKeyBlobData', None)
        self.ramFreeSpaceStart_LoadCfgBlock = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadCfgBlock', None)
        self.ramFreeSpaceStart_LoadPrdbOpt = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_LoadPrdbOpt', None)
        self.ramFreeSpaceStart_Rom = misc.get_dict_default(kwargs, 'ramFreeSpaceStart_Rom', None)

        self.registerAddrDict = misc.get_dict_default(kwargs, 'registerAddrDict', None)
        self.registerDefnDict = misc.get_dict_default(kwargs, 'registerDefnDict', None)
        self.efusemapIndexDict = misc.get_dict_default(kwargs, 'efusemapIndexDict', None)
        self.efusemapDefnDict = misc.get_dict_default(kwargs, 'efusemapDefnDict', None)
        self.efuseDescDiffDict = misc.get_dict_default(kwargs, 'efuseDescDiffDict', None)
        self.otpmapIndexDict = misc.get_dict_default(kwargs, 'otpmapIndexDict', None)
        self.otpmapDefnDict = misc.get_dict_default(kwargs, 'otpmapDefnDict', None)
        self.otpDescDiffDict = misc.get_dict_default(kwargs, 'otpDescDiffDict', None)

        self.ftfxNorMemBase = misc.get_dict_default(kwargs, 'ftfxNorMemBase', None)
        self.c040hdNorMemBase = misc.get_dict_default(kwargs, 'c040hdNorMemBase', None)

        self.sbLoaderVersion = misc.get_dict_default(kwargs, 'sbLoaderVersion', None)

    ##
    # @brief Check if a command is supported by the target.
    #
    # @return True if the command is supported. False if not.
    def isCommandSupported(self, tag):
        return bool(commands.Commands[tag].propertyMask & self.availableCommands)

    ##
    # @brief Check if a peripheral is supported by the target.
    #
    # @return True if the peripheral is supported. False if not.
    def isPeripheralSupported(self, name):
        return bool(peripherals.PeripheralMasks[name].propertyMask & self.availablePeripherals)



