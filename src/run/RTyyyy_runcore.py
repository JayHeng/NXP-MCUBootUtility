#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import RTyyyy_rundef
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gendef
from gen import RTyyyy_gencore
from gen import RTyyyy_gendef
from fuse import RTyyyy_fusedef
from ui import RTyyyy_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from mem import RTyyyy_memdef
from boot import bltest
from boot import target
from utils import misc

def RTyyyy_createTarget(device, exeBinRoot ):
    # Build path to target directory and config file.
    cpu = "MIMXRT1052"
    if device == uidef.kMcuDevice_iMXRT1011:
        cpu = "MIMXRT1011"
    elif device == uidef.kMcuDevice_iMXRT1015:
        cpu = "MIMXRT1015"
    elif device == uidef.kMcuDevice_iMXRT102x:
        cpu = "MIMXRT1021"
    elif device == uidef.kMcuDevice_iMXRT1024:
        cpu = "MIMXRT1024"
    elif device == uidef.kMcuDevice_iMXRT104x:
        cpu = "MIMXRT1042"
    elif device == uidef.kMcuDevice_iMXRT105x:
        cpu = "MIMXRT1052"
    elif device == uidef.kMcuDevice_iMXRT106x:
        cpu = "MIMXRT1062"
    elif device == uidef.kMcuDevice_iMXRT1060X:
        cpu = "MIMXRT1062X"
    elif device == uidef.kMcuDevice_iMXRT1064:
        cpu = "MIMXRT1064"
    elif device == uidef.kMcuDevice_iMXRT116x:
        cpu = "MIMXRT1166"
    elif device == uidef.kMcuDevice_iMXRT117x:
        cpu = "MIMXRT1176"
    elif device == uidef.kMcuDevice_iMXRT118x:
        cpu = "MIMXRT1189"
    else:
        pass
    targetBaseDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'targets', cpu)

    # Check for existing target directory.
    if not os.path.isdir(targetBaseDir):
        targetBaseDir = os.path.join(os.path.dirname(exeBinRoot), 'src', 'targets', cpu)
        if not os.path.isdir(targetBaseDir):
            raise ValueError("Missing target directory at path %s" % targetBaseDir)

    targetConfigFile = os.path.join(targetBaseDir, 'bltargetconfig.py')

    # Check for config file existence.
    if not os.path.isfile(targetConfigFile):
        raise RuntimeError("Missing target config file at path %s" % targetConfigFile)

    # Build locals dict by copying our locals and adjusting file path and name.
    targetConfig = locals().copy()
    targetConfig['__file__'] = targetConfigFile
    targetConfig['__name__'] = 'bltargetconfig'

    # Execute the target config script.
    execfile(targetConfigFile, globals(), targetConfig)

    # Create the target object.
    tgt = target.Target(**targetConfig)

    return tgt, targetBaseDir

##
# @brief
class secBootRTyyyyRun(RTyyyy_gencore.secBootRTyyyyGen):

    def __init__(self, parent):
        RTyyyy_gencore.secBootRTyyyyGen.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_initRun()

    def RTyyyy_initRun( self ):
        self.blhost = None
        self.sdphost = None
        self.tgt = None
        self.cpuDir = None
        self.sdphostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'sdphost', 'win', 'vectors')
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost2_3', 'win', 'vectors')

        self.RTyyyy_isDeviceEnabledToOperate = True
        self.bootDeviceMemId = None
        self.bootDeviceMemBase = None
        self.semcNandImageCopies = None
        self.semcNandBlockSize = None
        self.flexspiNandImageCopies = None
        self.flexspiNandBlockSize = None
        self.isFlexspiNorErasedForImage = False
        self.isFlexspiNandBlockAddr = None

        self.mcuDeviceHabStatus = None
        self.mcuDeviceBtFuseSel = None
        self.mcuDeviceHwCryptoKey0Sel = None
        self.mcuDeviceHwCryptoKey1Sel = None

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

        self.sbLastSharedFuseBootCfg1 = RTyyyy_fusedef.kEfuseValue_Invalid
        self.sbLastSharedFuseOtfadCfg = RTyyyy_fusedef.kEfuseValue_Invalid

        self.RTyyyy_createMcuTarget()

    def RTyyyy_createMcuTarget( self ):
        self.tgt, self.cpuDir = RTyyyy_createTarget(self.mcuDevice, self.exeBinRoot)

    def RTyyyy_updateFlexspiNorMemBase( self ):
        # Set main flexspi nor XIP region
        if self.flexspiBootInstance == 0:
            self.tgt.flexspiNorMemBase = self.tgt.flexspiNorMemBase0
        elif self.flexspiBootInstance == 1:
            self.tgt.flexspiNorMemBase = self.tgt.flexspiNorMemBase1
        else:
            pass

    def RTyyyy_getUsbid( self ):
        self.RTyyyy_createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def RTyyyy_connectToDevice( self , connectStage):
        if connectStage == uidef.kConnectStage_Rom:
            # Create the target object.
            self.RTyyyy_createMcuTarget()
            xhost = None
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                xhost = 'sdp_'
            elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                xhost = ''
            else:
                pass
            if self.isUartPortSelected:
                xPeripheral = xhost + 'uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                xPeripheral = xhost + 'usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.romUsbVid
                usbPid = self.tgt.romUsbPid
            else:
                pass
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                self.sdphost = bltest.createBootloader(self.tgt,
                                                       self.sdphostVectorsDir,
                                                       xPeripheral,
                                                       uartBaudrate, uartComPort,
                                                       usbVid, usbPid)
            elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                self.blhost = bltest.createBootloader(self.tgt,
                                                      self.blhostVectorsDir,
                                                      xPeripheral,
                                                      uartBaudrate, uartComPort,
                                                      usbVid, usbPid,
                                                      True)
            else:
                pass
        elif connectStage == uidef.kConnectStage_Flashloader:
            if self.isUartPortSelected:
                blPeripheral = 'uart'
                uartComPort = self.uartComPort
                uartBaudrate = int(self.uartBaudrate)
                usbVid = ''
                usbPid = ''
            elif self.isUsbhidPortSelected:
                blPeripheral = 'usb'
                uartComPort = ''
                uartBaudrate = ''
                usbVid = self.tgt.flashloaderUsbVid
                usbPid = self.tgt.flashloaderUsbPid
            else:
                pass
            self.blhost = bltest.createBootloader(self.tgt,
                                                  self.blhostVectorsDir,
                                                  blPeripheral,
                                                  uartBaudrate, uartComPort,
                                                  usbVid, usbPid,
                                                  True)
        elif connectStage == uidef.kConnectStage_Reset:
            self.tgt = None
        else:
            pass

    def RTyyyy_pingRom( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            status, results, cmdStr = self.sdphost.errorStatus()
            self.printLog(cmdStr)
            return (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled)
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
            self.printLog(cmdStr)
            return (status == boot.status.kStatus_Success)
        else:
            pass

    def _getDeviceRegisterBySdphost( self, regAddr, regName, needToShow=True):
        if self.tgt.hasSdpReadRegisterCmd:
            filename = 'readReg.dat'
            filepath = os.path.join(self.sdphostVectorsDir, filename)
            status, results, cmdStr = self.sdphost.readRegister(regAddr, 32, 4, filename)
            self.printLog(cmdStr)
            if (status == boot.status.kSDP_Status_HabEnabled or status == boot.status.kSDP_Status_HabDisabled):
                regVal = self.getVal32FromBinFile(filepath)
                if needToShow:
                    self.printDeviceStatus(regName + " = " + self.convertLongIntHexText(str(hex(regVal))))
                return regVal
            else:
                if needToShow:
                    self.printDeviceStatus(regName + " = --------")
                return None
            try:
                os.remove(filepath)
            except:
                pass
        else:
            return None

    def _readMcuDeviceRegisterUuid( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_OCOTP_UUID1'], 'OCOTP->UUID[31:00]')
            self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_OCOTP_UUID2'], 'OCOTP->UUID[63:32]')
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            self.getMcuDeviceBootloaderUniqueId()

    def _readMcuDeviceRegisterSrcSmbr( self ):
        self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_SRC_SBMR1'], 'SRC->SBMR1')
        sbmr2 = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_SRC_SBMR2'], 'SRC->SBMR2')
        if sbmr2 != None:
            bmod = ((sbmr2 & self.tgt.registerDefnDict['kRegisterMask_SRC_SBMR2_Bmod']) >> self.tgt.registerDefnDict['kRegisterShift_SRC_SBMR2_Bmod'])
            if bmod == 0:
                self.printDeviceStatus('BMOD[1:0] = 2\'b00 (Boot From Fuses)')
            elif bmod == 1:
                self.printDeviceStatus('BMOD[1:0] = 2\'b01 (Serial Downloader)')
            elif bmod == 2:
                self.printDeviceStatus('BMOD[1:0] = 2\'b10 (Internal Boot)')
            else:
                self.printDeviceStatus('BMOD[1:0] = 2\'b11 (Reserved)')

    def RTyyyy_getMcuDeviceInfoViaRom( self ):
        self.printDeviceStatus("--------MCU Device ROM Info--------")
        self._readMcuDeviceRegisterUuid()
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            # RT10yy supports SDP protocol, but some device(RT1011) doesn't support Read Register command
            self._readMcuDeviceRegisterSrcSmbr()
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            # RT11yy doesn't support SDP protocol
            self.getMcuDeviceBootloaderVersion()

    def getFlexramInfoViaRom( self ):
        self.printDeviceStatus("----------FlexRAM memory-----------")
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            #gpr16 = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_IOMUXC_GPR_GPR16'], 'IOMUXC_GPR->GPR16')
            #if gpr16 == None:
            #    return
            #if not (gpr16 & self.tgt.registerDefnDict['kRegisterMask_IOMUXC_GPR_GPR16_FlexramBankCfgSel']):
            if True:
                miscConf0 = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_OCOTP_FlexramCfg'], 'OCOTP->MISC_CONF0[31:00]')
                if miscConf0 != None:
                    self.printDeviceStatus('Assume that FlexRAM configuration is from eFuse')
                    defaultFlexramPart = (miscConf0 & RTyyyy_fusedef.kEfuseMask_DefaultFlexramPart) >> RTyyyy_fusedef.kEfuseShift_DefaultFlexramPart
                    self.printDeviceStatus(self.tgt.efuseDescDiffDict['0x6d0_miscconf0_bit19_16']['Default_FlexRAM_Partion'][defaultFlexramPart])
            else:
                #gpr17 = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_IOMUXC_GPR_GPR17'], 'IOMUXC_GPR->GPR17')
                #if gpr17 != None:
                #    self.printDeviceStatus('FlexRAM configuration is from IOMUXC_GPR Register')
                pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            pass

    def getMcuDeviceHabStatus( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            if self.tgt.hasSdpReadRegisterCmd:
                secConfig = self._getDeviceRegisterBySdphost( self.tgt.registerAddrDict['kRegisterAddr_SRC_SBMR2'], '', False)
                if secConfig != None:
                    self.mcuDeviceHabStatus = ((secConfig & self.tgt.registerDefnDict['kRegisterMask_SRC_SBMR2_SecConfig']) >> self.tgt.registerDefnDict['kRegisterShift_SRC_SBMR2_SecConfig'])
                    if self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_FAB:
                        self.printDeviceStatus('Life Cycle status = FAB')
                    elif self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Open:
                        self.printDeviceStatus('Life Cycle status = HAB Open')
                    elif self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Closed0 or self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Closed1:
                        self.printDeviceStatus('Life Cycle status = HAB Closed')
                    else:
                        pass
            else:
                status, results, cmdStr = self.sdphost.errorStatus()
                self.printLog(cmdStr)
                if status == boot.status.kSDP_Status_HabEnabled:
                    self.mcuDeviceHabStatus = RTyyyy_fusedef.kHabStatus_Closed0
                    self.printDeviceStatus('Life Cycle status = HAB Closed')
                elif status == boot.status.kSDP_Status_HabDisabled:
                    self.mcuDeviceHabStatus = RTyyyy_fusedef.kHabStatus_Open
                    self.printDeviceStatus('Life Cycle status = HAB Open')
                else:
                    pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_FlashSecurityState)
            self.printLog(cmdStr)
            if status == boot.status.kStatus_Success:
                if results[0] == 0:
                    self.mcuDeviceHabStatus = RTyyyy_fusedef.kHabStatus_Open
                    self.printDeviceStatus('Life Cycle status = HAB Open')
                else:
                    self.mcuDeviceHabStatus = RTyyyy_fusedef.kHabStatus_Closed0
                    self.printDeviceStatus('Life Cycle status = HAB Closed')
            else:
                pass
        else:
            pass

    def _selectFlashloader( self ):
        flSrecFile = None
        flBinFile = None
        flLoadAddr = None
        flJumpAddr = None
        flSrecFile = os.path.join(self.cpuDir, 'flashloader_user.srec')
        if os.path.isfile(flSrecFile):
            flBinFile, flLoadAddr, flJumpAddr = self.genUserFlashloader(flSrecFile)
        else:
            if self.flashloaderResident == None:
                flBinFile = None
                if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                    flBinFile = os.path.join(self.cpuDir, 'ivt_flashloader.bin')
                elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                    if (self.tgt.flexspiNorMemBase >> 28) % 2:
                        flBinFile = os.path.join(self.cpuDir, 'cntr_flashloader_s.bin')
                    else:
                        flBinFile = os.path.join(self.cpuDir, 'cntr_flashloader_ns.bin')
                else:
                    pass
                flSrecFile = os.path.join(self.cpuDir, 'flashloader.srec')
                flLoadAddr = self.tgt.flashloaderLoadAddr
                flJumpAddr = self.tgt.flashloaderJumpAddr
            elif self.flashloaderResident == 'itcm' or \
                 self.flashloaderResident == 'dtcm' or \
                 self.flashloaderResident == 'ocram':
                flSrecFile = os.path.join(self.cpuDir, 'flexram_loader', self.flashloaderResident, 'flashloader.srec')
                flBinFile = os.path.join(self.cpuDir, 'flexram_loader', self.flashloaderResident, 'ivt_flashloader.bin')
                if self.flashloaderResident == 'ocram':
                    flLoadAddr = self.tgt.reservedRegionDict['ram'][1] + 1 + 0x200
                else:
                    flLoadAddr = self.tgt.memoryRange[self.flashloaderResident].start + 0x200
                flJumpAddr = flLoadAddr + RTyyyy_gendef.kIvtOffset_RAM_FLASHLOADER
            else:
                pass
        return flSrecFile, flBinFile, flLoadAddr, flJumpAddr

    def RTyyyy_jumpToFlashloader( self ):
        flashloaderSrecFile, flashloaderBinFile, flashloaderLoadAddr, flashloaderJumpAddr = self._selectFlashloader()
        if flashloaderBinFile == None:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_InvalidUserFl'][self.languageIndex])
            return False
        if self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Closed0 or self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Closed1:
            flashloaderBinFile = self.genSignedFlashloader(flashloaderSrecFile)
            if flashloaderBinFile == None:
                return False
        elif self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_FAB or self.mcuDeviceHabStatus == RTyyyy_fusedef.kHabStatus_Open:
            pass
        else:
            pass
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            status, results, cmdStr = self.sdphost.writeFile(flashloaderLoadAddr, flashloaderBinFile)
            self.printLog(cmdStr)
            if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
                return False
            status, results, cmdStr = self.sdphost.jumpAddress(flashloaderJumpAddr)
            self.printLog(cmdStr)
            if status != boot.status.kSDP_Status_HabEnabled and status != boot.status.kSDP_Status_HabDisabled:
                return False
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            status, results, cmdStr = self.blhost.loadImage(flashloaderBinFile)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        else:
            pass
        return True

    def RTyyyy_pingFlashloader( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def RTyyyy_readMcuDeviceFuseByBlhost( self, fuseIndex, fuseName, needToShow=True):
        if not self.RTyyyy_isDeviceEnabledToOperate and self.isSbFileEnabledToGen:
            return RTyyyy_fusedef.kEfuseValue_Blank
        status, results, cmdStr = self.blhost.efuseReadOnce(fuseIndex)
        self.printLog(cmdStr)
        if (status == boot.status.kStatus_Success):
            if needToShow:
                self.printDeviceStatus(fuseName + " = " + self.convertLongIntHexText(str(hex(results[1]))))
            if self.isSbFileEnabledToGen:
                if fuseIndex == self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG1'] and self.sbLastSharedFuseBootCfg1 == RTyyyy_fusedef.kEfuseValue_Invalid:
                    self.sbLastSharedFuseBootCfg1 = results[1]
                if fuseIndex == self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_CFG'] and self.sbLastSharedFuseOtfadCfg == RTyyyy_fusedef.kEfuseValue_Invalid:
                    self.sbLastSharedFuseOtfadCfg = results[1]
            return results[1]
        else:
            if needToShow:
                self.printDeviceStatus(fuseName + " = --------")
            return None

    def _readMcuDeviceFuseTester( self ):
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_TESTER0'], '(0x410) TESTER0')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_TESTER1'], '(0x420) TESTER1')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_TESTER2'], '(0x430) TESTER2')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_TESTER3'], '(0x440) TESTER3')

    def _RTyyyy_readMcuDeviceFuseBootCfg( self ):
        cfg0txt = ''
        cfg1txt = ''
        cfg2txt = ''
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            cfg0txt = '(0x450)'
            cfg1txt = '(0x460)'
            cfg2txt = '(0x470)'
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                cfg0txt = '(0x940)'
                cfg1txt = '(0x950)'
                cfg2txt = '(0x960)'
            elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                cfg0txt = '(0x18)'
                cfg1txt = '(0x19)'
                cfg2txt = '(0x1a)'
            else:
                pass
        else:
            pass
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG0'], cfg0txt+' SYSBT_CFG0')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG1'], cfg1txt+' SYSBT_CFG1')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG2'], cfg2txt+' SYSBT_CFG2')
        if self.mcuDevice == uidef.kMcuDevice_iMXRT1060X:
            # It is ROM patch implementation (Move SPI_EN to fuse 0x6D0[20]
            sipBit = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_MISC_CONF0'], '', False)
            if sipBit != None:
                self.flexspiBootInstanceFromFuse = (sipBit & 0x100000) >> 20
                self.getFlexspiBootInstance()

    def _genOtpmkDekFile( self, otpmk4, otpmk5, otpmk6, otpmk7 ):
        try:
            os.remove(self.otpmkDekFilename)
        except:
            pass
        self.fillVal32IntoBinFile(self.otpmkDekFilename, otpmk4)
        self.fillVal32IntoBinFile(self.otpmkDekFilename, otpmk5)
        self.fillVal32IntoBinFile(self.otpmkDekFilename, otpmk6)
        self.fillVal32IntoBinFile(self.otpmkDekFilename, otpmk7)

    def _readMcuDeviceFuseOtpmkDek( self ):
        otpmk4 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTPMK4'], '', False)
        otpmk5 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTPMK5'], '', False)
        otpmk6 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTPMK6'], '', False)
        otpmk7 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTPMK7'], '', False)
        if otpmk4 != None and otpmk5 != None and otpmk6 != None and otpmk7 != None:
            self._genOtpmkDekFile(otpmk4, otpmk5, otpmk6, otpmk7)

    def _readMcuDeviceFuseSrk( self ):
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK0'], '(0x580) SRK0')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK1'], '(0x590) SRK1')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK2'], '(0x5A0) SRK2')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK3'], '(0x5B0) SRK3')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK4'], '(0x5C0) SRK4')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK5'], '(0x5D0) SRK5')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK6'], '(0x5E0) SRK6')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK7'], '(0x5F0) SRK7')

    def _readMcuDeviceFuseSwGp2( self ):
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_0'], '(0x690) SW_GP2_0')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_1'], '(0x6A0) SW_GP2_1')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_2'], '(0x6B0) SW_GP2_2')
        self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_3'], '(0x6C0) SW_GP2_3')

    def _getMcuDeviceLifeCycleStatus( self ):
        if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
            pass
        elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
            sentinelMiscCtrl5 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_SentinelMiscCtrl5'], '', False)
            if sentinelMiscCtrl5 != None:
                lcFab = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleFAB']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleFAB'])
                lcNxpProvisioned = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleNxpProvisioned']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleNxpProvisioned'])
                lcOemOpen = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleOemOpen']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleOemOpen'])
                lcOemClosed = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleOemClosed']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleOemClosed'])
                lcFrOem = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleFrOem']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleFrOem'])
                lcFrNxp = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleFrNxp']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleFrNxp'])
                lcCancelNr = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleCancelNr']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleCancelNr'])
                lcNrLocked = ((sentinelMiscCtrl5 & self.tgt.efusemapDefnDict['kEfuseMask_LifeCycleNrLocked']) >> self.tgt.efusemapDefnDict['kEfuseShift_LifeCycleNrLocked'])

                self.printDeviceStatus('Life Cycle status - FAB = '+str(lcFab))
                self.printDeviceStatus('Life Cycle status - NXP_PROVISIONED = '+str(lcNxpProvisioned))
                self.printDeviceStatus('Life Cycle status - OEM_OPEN = '+str(lcOemOpen))
                self.printDeviceStatus('Life Cycle status - OEM_CLOSED = '+str(lcOemClosed))
                self.printDeviceStatus('Life Cycle status - FR_OEM = '+str(lcFrOem))
                self.printDeviceStatus('Life Cycle status - FR_NXP = '+str(lcFrNxp))
                self.printDeviceStatus('Life Cycle status - CANCEL_NR = '+str(lcCancelNr))
                self.printDeviceStatus('Life Cycle status - NR_LOCKED = '+str(lcNrLocked))
        else:
            pass

    def getMcuDeviceInfoViaFlashloader( self ):
        self.printDeviceStatus("--------MCU Flashloader Info-------")
        self.getMcuDeviceBootloaderVersion()
        self.printDeviceStatus("--------MCU device eFusemap--------")
        self._RTyyyy_readMcuDeviceFuseBootCfg()
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            #self._readMcuDeviceFuseTester()
            #self._readMcuDeviceFuseOtpmkDek()
            #self._readMcuDeviceFuseSrk()
            #self._readMcuDeviceFuseSwGp2()
            pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            self._getMcuDeviceLifeCycleStatus()
        else:
            pass

    def getMcuDeviceBtFuseSel( self ):
        btFuseSel = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_BtFuseSel'], '', False)
        if btFuseSel != None:
            self.mcuDeviceBtFuseSel = ((btFuseSel & self.tgt.efusemapDefnDict['kEfuseMask_BtFuseSel']) >> self.tgt.efusemapDefnDict['kEfuseShift_BtFuseSel'])
            if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                if self.mcuDeviceBtFuseSel == 0:
                    self.printDeviceStatus('BT_FUSE_SEL = 1\'b0')
                    self.printDeviceStatus('  When BMOD[1:0] = 2\'b00 (Boot From Fuses), no app in boot device, MCU enters serial downloader mode directly')
                    self.printDeviceStatus('  When BMOD[1:0] = 2\'b10 (Internal Boot), MCU boots app according to both BOOT_CFGx pins and Fuse BOOT_CFGx')
                elif self.mcuDeviceBtFuseSel == 1:
                    self.printDeviceStatus('BT_FUSE_SEL = 1\'b1')
                    self.printDeviceStatus('  When BMOD[1:0] = 2\'b00 (Boot From Fuses), there is app in boot device, MCU boots app according to Fuse BOOT_CFGx')
                    self.printDeviceStatus('  When BMOD[1:0] = 2\'b10 (Internal Boot), MCU boots app according to Fuse BOOT_CFGx only')
                else:
                    pass
            elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                forceBtFromFuse = ((btFuseSel & self.tgt.efusemapDefnDict['kEfuseMask_ForceBtFromFuse']) >> self.tgt.efusemapDefnDict['kEfuseShift_ForceBtFromFuse'])
                if forceBtFromFuse == 0:
                    self.printDeviceStatus('FORCE_BT_FROM_FUSE = 1\'b0, Boot mode determined by BOOT_MODE pins')
                elif forceBtFromFuse == 1:
                    self.printDeviceStatus('FORCE_BT_FROM_FUSE = 1\'b1, Boot mode determined by Fuse BOOT_MODE_FROM_FUSE')
                else:
                    pass

    def _getDeviceRegisterByBlhost( self, regAddr, regName, needToShow=True):
        filename = 'readReg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(regAddr, 4, filename)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            regVal = self.getVal32FromBinFile(filepath)
            if needToShow:
                self.printDeviceStatus(regName + " = " + self.convertLongIntHexText(str(hex(regVal))))
            return regVal
        else:
            if needToShow:
                self.printDeviceStatus(regName + " = --------")
            return None
        try:
            os.remove(filepath)
        except:
            pass

    def _showFlexramAccordingToBankCfg( self, flexramBankCfg ):
        if flexramBankCfg != 0:
            banks = self.tgt.memoryRange['itcm'].length / RTyyyy_memdef.kFlexramBankSize
            itcmBanks = 0
            dtcmBanks = 0
            ocramBanks = 0
            for bank in range(banks):
                bankId = (flexramBankCfg >> (bank *2)) & 0x3
                if bankId == RTyyyy_memdef.kFlexramBankId_Ocram:
                    ocramBanks += 1
                elif bankId == RTyyyy_memdef.kFlexramBankId_Dtcm:
                    dtcmBanks += 1
                elif bankId == RTyyyy_memdef.kFlexramBankId_Itcm:
                    itcmBanks += 1
                else:
                    pass
            itcmSizeInKB = itcmBanks * RTyyyy_memdef.kFlexramBankSize / 0x400
            dtcmSizeInKB = dtcmBanks * RTyyyy_memdef.kFlexramBankSize / 0x400
            ocramSizeInKB = ocramBanks * RTyyyy_memdef.kFlexramBankSize / 0x400
            self.printDeviceStatus(str(itcmSizeInKB) + "KB ITCM, " + str(dtcmSizeInKB) + "KB DTCM, " + str(ocramSizeInKB) + "KB OCRAM")
        else:
            self.printDeviceStatus("0KB ITCM, 0KB DTCM, 0KB OCRAM")

    def getFlexramInfoViaFlashloader( self ):
        self.printDeviceStatus("----------FlexRAM memory-----------")
        gpr16 = self._getDeviceRegisterByBlhost( self.tgt.registerAddrDict['kRegisterAddr_IOMUXC_GPR_GPR16'], 'IOMUXC_GPR->GPR16')
        if gpr16 == None:
            return
        if not (gpr16 & self.tgt.registerDefnDict['kRegisterMask_IOMUXC_GPR_GPR16_FlexramBankCfgSel']):
            self.printDeviceStatus('FlexRAM configuration is from eFuse')
            flexramCfg = self._getDeviceRegisterByBlhost( self.tgt.registerAddrDict['kRegisterAddr_OCOTP_FlexramCfg'], 'OCOTP->MISC_CONF0[31:00]')
            if flexramCfg != None:
                defaultFlexramPart = (flexramCfg & self.tgt.efusemapDefnDict['kEfuseMask_DefaultFlexramPart']) >> self.tgt.efusemapDefnDict['kEfuseShift_DefaultFlexramPart']
                if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                    self.printDeviceStatus("FlexRAM Partion =" + self.tgt.efuseDescDiffDict['0x6d0_miscconf0_bit19_16']['Default_FlexRAM_Partion'][defaultFlexramPart])
                elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                    self.printDeviceStatus("FlexRAM Partion =" + self.tgt.efuseDescDiffDict['0xc70_flexramcfg_bit21_16']['Default_FlexRAM_Partion'][defaultFlexramPart])
                else:
                    pass
        else:
            self.printDeviceStatus('FlexRAM configuration is from IOMUXC_GPR Register')
            gpr17 = self._getDeviceRegisterByBlhost( self.tgt.registerAddrDict['kRegisterAddr_IOMUXC_GPR_GPR17'], 'IOMUXC_GPR->GPR17')
            if gpr17 != None:
                flexramBankCfg = (gpr17 & self.tgt.registerDefnDict['kRegisterMask_IOMUXC_GPR_GPR17_FlexramBankCfg']) >> self.tgt.registerDefnDict['kRegisterShift_IOMUXC_GPR_GPR17_FlexramBankCfg']
                self._showFlexramAccordingToBankCfg(flexramBankCfg)

    def _RTyyyy_prepareForBootDeviceOperation ( self ):
        if self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNor
            self.bootDeviceMemBase = self.tgt.flexspiNorMemBase
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNand
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_FlexspiNand
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SemcNor
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_SemcNor
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SemcNand
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_SemcNand
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_UsdhcSd
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_UsdhcSd
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_UsdhcMmc
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_UsdhcMmc
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SpiNor
            self.bootDeviceMemBase = RTyyyy_rundef.kBootDeviceMemBase_LpspiNor
        else:
            pass

    def _getSemcNandDeviceInfo ( self ):
        filename = 'semcNandFcb.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase + RTyyyy_rundef.kSemcNandFcbInfo_StartAddr, RTyyyy_rundef.kSemcNandFcbInfo_Length, filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        fingerprint = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_Fingerprint)
        semcTag = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_SemcTag)
        if fingerprint == RTyyyy_rundef.kSemcNandFcbTag_Fingerprint and semcTag == RTyyyy_rundef.kSemcNandFcbTag_Semc:
            firmwareCopies = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_FirmwareCopies)
            pageByteSize = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_PageByteSize)
            pagesInBlock = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_PagesInBlock)
            blocksInPlane = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_BlocksInPlane)
            planesInDevice = self.getVal32FromBinFile(filepath, RTyyyy_rundef.kSemcNandFcbOffset_PlanesInDevice)
            self.printDeviceStatus("Page Size         = " + self.showAsOptimalMemoryUnit(pageByteSize))
            self.printDeviceStatus("Pages In Block    = " + str(pagesInBlock))
            self.printDeviceStatus("Blocks In Plane   = " + str(blocksInPlane))
            self.printDeviceStatus("Planes In Device  = " + str(planesInDevice))
            self.semcNandImageCopies = firmwareCopies
            self.semcNandBlockSize = pageByteSize * pagesInBlock
            self.comMemWriteUnit = pageByteSize
            self.comMemEraseUnit = pageByteSize * pagesInBlock
            self.comMemReadUnit = pageByteSize
        else:
            self.printDeviceStatus("Page Size         = --------")
            self.printDeviceStatus("Pages In Block    = --------")
            self.printDeviceStatus("Blocks In Plane   = --------")
            self.printDeviceStatus("Planes In Device  = --------")
            return False
        try:
            os.remove(filepath)
        except:
            pass
        return True

    def _getSemcNorDeviceInfo ( self ):
        filename = 'SemcNorCfg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase, 0x2D, filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        # flexspiTag = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_FlexspiTag)
        # if flexspiTag == rundef.kFlexspiNorCfgTag_Flexspi:
        #     pageByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_PageByteSize)
        #     sectorByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_SectorByteSize)
        #     blockByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_BlockByteSize)
        #     self.printDeviceStatus("Page Size   = " + self.showAsOptimalMemoryUnit(pageByteSize))
        #     self.printDeviceStatus("Sector Size = " + self.showAsOptimalMemoryUnit(sectorByteSize))
        #     self.printDeviceStatus("Block Size  = " + self.showAsOptimalMemoryUnit(blockByteSize))
        #     self.comMemWriteUnit = pageByteSize
        #     self.comMemEraseUnit = sectorByteSize
        #     self.comMemReadUnit = pageByteSize
        # else:
        #     self.printDeviceStatus("Page Size   = --------")
        #     self.printDeviceStatus("Sector Size = --------")
        #     self.printDeviceStatus("Block Size  = --------")
        #     return False
        # try:
        #     os.remove(filepath)
        # except:
        #     pass
        return True

    def _getFlexspiNorDeviceInfo ( self, useDefault=False ):
        if not self.RTyyyy_isDeviceEnabledToOperate and self.isSbFileEnabledToGen:
            return True
        filename = 'flexspiNorCfg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        flexspiTag = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_FlexspiTag)
        if flexspiTag == rundef.kFlexspiNorCfgTag_Flexspi:
            pageByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_PageByteSize)
            sectorByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_SectorByteSize)
            blockByteSize = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_BlockByteSize)
            self.printDeviceStatus("Page Size   = " + self.showAsOptimalMemoryUnit(pageByteSize))
            self.printDeviceStatus("Sector Size = " + self.showAsOptimalMemoryUnit(sectorByteSize))
            self.printDeviceStatus("Block Size  = " + self.showAsOptimalMemoryUnit(blockByteSize))
            if pageByteSize != 0 and pageByteSize != 0xffffffff:
                self.comMemWriteUnit = pageByteSize
                self.comMemReadUnit = pageByteSize
            if sectorByteSize != 0 and sectorByteSize != 0xffffffff:
                self.comMemEraseUnit = sectorByteSize
            if blockByteSize != 0 and blockByteSize != 0xffffffff:
                if self.isInfineonMirrorBitDevice():
                    self.comMemEraseUnit = blockByteSize
        else:
            if not useDefault:
                self.printDeviceStatus("Page Size   = --------")
                self.printDeviceStatus("Sector Size = --------")
                self.printDeviceStatus("Block Size  = --------")
                return False
            else:
                pageByteSize = rundef.kXspiNorDefaultMemInfo_PageSize
                sectorByteSize = rundef.kXspiNorDefaultMemInfo_SectorSize
                blockByteSize = rundef.kXspiNorDefaultMemInfo_BlockSize
                self.printDeviceStatus("Page Size   = * " + self.showAsOptimalMemoryUnit(pageByteSize))
                self.printDeviceStatus("Sector Size = * " + self.showAsOptimalMemoryUnit(sectorByteSize))
                self.printDeviceStatus("Block Size  = * " + self.showAsOptimalMemoryUnit(blockByteSize))
                self.printDeviceStatus("Note: Cannot get correct FDCB, just use default memory info here")
                self.comMemWriteUnit = pageByteSize
                self.comMemEraseUnit = sectorByteSize
                self.comMemReadUnit = pageByteSize
        try:
            os.remove(filepath)
        except:
            pass
        return True

    def _calcFlexspiNandDeviceInfo ( self ):
        flexspiNandOpt0, flexspiNandOpt1, flexspiNandFcbOpt, flexspiNandImageInfoList, flexspiNandDeviceModel = uivar.getBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_FlexspiNand)
        imageCopies = 1
        while (imageCopies <= 8):
            if flexspiNandImageInfoList[imageCopies - 1] == None:
                imageCopies -= 1
                break
            else:
                imageCopies += 1
        self.flexspiNandImageCopies = imageCopies
        pageSize = ((flexspiNandOpt0 & 0x000000F0) >> 4) * 1024
        pagesPerBlock = (flexspiNandOpt0 & 0x00000F00) >> 8
        if pagesPerBlock == 0:
            pagesPerBlock = 64
        elif pagesPerBlock == 1:
            pagesPerBlock = 128
        elif pagesPerBlock == 2:
            pagesPerBlock = 256
        elif pagesPerBlock == 3:
            pagesPerBlock = 32
        else:
            pass
        self.flexspiNandBlockSize = pageSize * pagesPerBlock
        self.comMemWriteUnit = pageSize
        self.comMemEraseUnit = pageSize * pagesPerBlock
        self.comMemReadUnit = pageSize

    def _getFlexspiNandDeviceInfo ( self ):
        self._calcFlexspiNandDeviceInfo()
        self.printDeviceStatus("Page Size         = " + self.showAsOptimalMemoryUnit(self.comMemWriteUnit))
        self.printDeviceStatus("Pages In Block    = " + str(self.comMemEraseUnit / self.comMemWriteUnit))

    def _getLpspiNorDeviceInfo ( self ):
        pageByteSize = 0
        sectorByteSize = 0
        totalByteSize = 0
        lpspiNorOpt0, lpspiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
        val = (lpspiNorOpt0 & 0x0000000F) >> 0
        if val <= 2:
            pageByteSize = int(math.pow(2, val + 8))
        else:
            pageByteSize = int(math.pow(2, val + 2))
        val = (lpspiNorOpt0 & 0x000000F0) >> 4
        if val <= 1:
            sectorByteSize = int(math.pow(2, val + 12))
        else:
            sectorByteSize = int(math.pow(2, val + 13))
        val = (lpspiNorOpt0 & 0x00000F00) >> 8
        if val <= 11:
            totalByteSize = int(math.pow(2, val + 19))
        else:
            totalByteSize = int(math.pow(2, val + 3))
        self.printDeviceStatus("Page Size   = " + self.showAsOptimalMemoryUnit(pageByteSize))
        self.printDeviceStatus("Sector Size = " + self.showAsOptimalMemoryUnit(sectorByteSize))
        self.printDeviceStatus("Total Size  = " + self.showAsOptimalMemoryUnit(totalByteSize))
        self.comMemWriteUnit = pageByteSize
        self.comMemEraseUnit = sectorByteSize
        self.comMemReadUnit = pageByteSize
        return True

    def getBootDeviceInfoViaFlashloader ( self ):
        if self.toolRunMode == uidef.kToolRunMode_SblOta:
            self._RTyyyy_prepareForBootDeviceOperation()
        if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            self.printDeviceStatus("--------SEMC NAND memory----------")
            self._getSemcNandDeviceInfo()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor:
            self.printDeviceStatus("--------SEMC NOR memory-----------")
            self._getSemcNorDeviceInfo()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
            self.printDeviceStatus("--------FlexSPI NOR memory--------")
            if not self._getFlexspiNorDeviceInfo(False):
                if not self._eraseFlexspiNorForConfigBlockLoading():
                    return False
                if not self._programFlexspiNorConfigBlock():
                    return False
                self._getFlexspiNorDeviceInfo(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            self.printDeviceStatus("--------FlexSPI NAND memory-------")
            self._getFlexspiNandDeviceInfo()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            self.printDeviceStatus("--------LPSPI NOR/EEPROM memory---")
            self._getLpspiNorDeviceInfo()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd:
            self.printDeviceStatus("--------uSDHC SD Card info--------")
            self.getUsdhcSdMmcDeviceInfo()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            self.printDeviceStatus("--------uSDHC (e)MMC Card info----")
            self.getUsdhcSdMmcDeviceInfo()
        else:
            pass

    def _RTyyyy_addFlashActionIntoSbAppBdContent(self, actionContent ):
        self.sbAppBdContent += actionContent
        self.sbAppFlashBdContent += actionContent

    def _isFlexspiNorConfigBlockRegionBlank( self ):
        filename = 'flexspiNorCfg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, filename, rundef.kBootDeviceMemId_FlexspiNor)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        for offset in range(self.tgt.xspiNorCfgInfoLen):
            value = self.getVal8FromBinFile(filepath, offset)
            if value != rundef.kFlexspiNorContent_Blank8:
                return False
        try:
            os.remove(filepath)
        except:
            pass
        return True

    def _getAlignedFlexspiNorEraseRange( self, addr, length ):
        memEraseUnit = self.convertComMemEraseUnit(self.comMemEraseUnit)
        alignedMemStart = misc.align_down(addr, memEraseUnit)
        alignedMemLength = misc.align_up(length, memEraseUnit)
        return alignedMemStart, alignedMemLength

    def _eraseFlexspiNorForConfigBlockLoading( self ):
        status = boot.status.kStatus_Success
        rangeStart, rangeLen = self._getAlignedFlexspiNorEraseRange(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen)
        if self.RTyyyy_isDeviceEnabledToOperate:
            if not self._isFlexspiNorConfigBlockRegionBlank():
                status, results, cmdStr = self.blhost.flashEraseRegion(rangeStart, rangeLen, rundef.kBootDeviceMemId_FlexspiNor)
                self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(rangeStart))) + ".." + self.convertLongIntHexText(str(hex(rangeStart + rangeLen))) + ";\n")
        return (status == boot.status.kStatus_Success)

    def _programFlexspiNorConfigBlock ( self ):
        #if not self.tgt.isSipFlexspiNorDevice:
        if True:
            status = boot.status.kStatus_Success
            if self.isFdcbFromSrcApp:
                if self.RTyyyy_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.writeMemory(self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset, self.fdcbBinFilename, self.bootDeviceMemId)
                    self.printLog(cmdStr)
            else:
                # 0xf000000f is the tag to notify Flashloader to program FlexSPI NOR config block to the start of device
                if self.RTyyyy_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCfgBlock, 0x4, rundef.kFlexspiNorCfgInfo_Notify)
                    self.printLog(cmdStr)
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(rundef.kFlexspiNorCfgInfo_Notify))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCfgBlock))) + ";\n")
                if status != boot.status.kStatus_Success:
                    return False
                if self.RTyyyy_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCfgBlock)
                    self.printLog(cmdStr)
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCfgBlock))) + ";\n")
            if self.isSbFileEnabledToGen:
                return True
            else:
                return (status == boot.status.kStatus_Success)
        else:
            status, results, cmdStr = self.blhost.writeMemory(self.bootDeviceMemBase, os.path.join(self.cpuDir, 'sip_flash_config.bin'), self.bootDeviceMemId)
            self.printLog(cmdStr)
            return (status == boot.status.kStatus_Success)

    def RTyyyy_setFlexspiInstance( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            # In RT1170 flashloader, 0xFC900001/0xFC900002 is used to switch FlexSPI instance
            #  0xFC900001 -> Primary instance
            #  0xFC900002 -> Secondary instance
            configOpt = rundef.kFlexspiDevCfgInfo_Instance + self.flexspiBootInstance
            status = boot.status.kStatus_Success
            if self.RTyyyy_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt, 0x4, configOpt)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(configOpt))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
            if self.RTyyyy_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCommOpt)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
        else:
            pass

    def RTyyyy_configureBootDevice ( self ):
        flexspiNorDeviceModel = None
        configOptList = []
        if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, semcNandImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([semcNandOpt, semcNandFcbOpt])
            for i in range(len(semcNandImageInfoList)):
                if semcNandImageInfoList[i] != None:
                    configOptList.extend([semcNandImageInfoList[i]])
                else:
                    break
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor:
            semcNorOpt, semcNorSetting, semcNorDeviceModel= uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([semcNorOpt])
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
            self.getFlexspiBootInstance()
            self.RTyyyy_updateFlexspiNorMemBase()
            flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(uidef.kBootDevice_XspiNor)
            configOptList.extend([flexspiNorOpt0, flexspiNorOpt1])
            self.RTyyyy_setFlexspiInstance()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            self.getFlexspiBootInstance()
            flexspiNandOpt0, flexspiNandOpt1, flexspiNandFcbOpt, flexspiNandImageInfoList, flexspiNandDeviceModel = uivar.getBootDeviceConfiguration(self.bootDevice)
            self.isFlexspiNandBlockAddr = (flexspiNandFcbOpt & 0x00000F00) >> 8
            configOptList.extend([flexspiNandFcbOpt, self.tgt.ramFreeSpaceStart_LoadCommOpt + (flexspiNandFcbOpt & 0x0000000F) * 4])
            for i in range(len(flexspiNandImageInfoList)):
                if flexspiNandImageInfoList[i] != None:
                    configOptList.extend([flexspiNandImageInfoList[i]])
                else:
                    break
            configOptList.extend([flexspiNandOpt0])
            if ((flexspiNandOpt0 & 0x0F000000) >> 24) == 1:
                configOptList.extend([flexspiNandOpt1])
            self.RTyyyy_setFlexspiInstance()
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            lpspiNorOpt0, lpspiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([lpspiNorOpt0, lpspiNorOpt1])
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd:
            usdhcSdOpt = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([usdhcSdOpt])
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            usdhcMmcOpt0, usdhcMmcOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([usdhcMmcOpt0, usdhcMmcOpt1])
        else:
            pass
        self._RTyyyy_prepareForBootDeviceOperation()
        status = boot.status.kStatus_Success
        if flexspiNorDeviceModel == uidef.kFlexspiNorDevice_FDCB:
            if self.RTyyyy_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.writeMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt, self.cfgFdcbBinFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " cfgFdcbBinFile > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
        else:
            for i in range(len(configOptList)):
                if self.RTyyyy_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt + 4 * i, 0x4, configOptList[i])
                    self.printLog(cmdStr)
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(configOptList[i]))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt + 4 * i))) + ";\n")
                if status != boot.status.kStatus_Success:
                    return False
        if self.RTyyyy_isDeviceEnabledToOperate:
            status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCommOpt)
            self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
        if status != boot.status.kStatus_Success:
            return False
        return True

    def _showOtpmkDek( self ):
        if os.path.isfile(self.otpmkDekFilename):
            self.clearOtpmkDekData()
            keyWords = RTyyyy_gendef.kSecKeyLengthInBits_DEK / 32
            for i in range(keyWords):
                val32 = self.getVal32FromBinFile(self.otpmkDekFilename, (i * 4))
                self.printOtpmkDekData(self.getFormattedHexValue(val32))

    def _eraseFlexspiNorForImageLoading( self ):
        imageLen = 0
        if self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
            imageLen = RTyyyy_gendef.kContainerOffset_NOR + os.path.getsize(self.destAppContainerFilename)
        elif self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
            imageLen = os.path.getsize(self.destAppFilename)
        rangeStart, rangeLen = self._getAlignedFlexspiNorEraseRange(self.tgt.flexspiNorMemBase, imageLen)
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(rangeStart))) + ".." + self.convertLongIntHexText(str(hex(rangeStart + rangeLen))) + ";\n")
        else:
            status, results, cmdStr = self.blhost.flashEraseRegion(rangeStart, rangeLen, rundef.kBootDeviceMemId_FlexspiNor)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        self.isFlexspiNorErasedForImage = True
        return True

    def prepareForFixedOtpmkEncryption( self ):
        self._RTyyyy_prepareForBootDeviceOperation()
        #self._showOtpmkDek()
        if not self._eraseFlexspiNorForImageLoading():
            return False
        otpmkKeyCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_OtpmkKey)
        otpmkKeyOpt = otpmkKeyCommDict['opt']
        otpmkEncryptedRegionStartList = otpmkKeyCommDict['regionStartList'][:]
        otpmkEncryptedRegionLengthOrEndList = otpmkKeyCommDict['regionLengthList'][:]
        # Prepare PRDB options
        if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
            #---------------------------------------------------------------------------
            # 0xe0120000 is an option for PRDB contruction and image encryption
            # bit[31:28] tag, fixed to 0x0E
            # bit[27:24] Key source, fixed to 0 for A0 silicon
            # bit[23:20] AES mode: 1 - CTR mode
            # bit[19:16] Encrypted region count (maximum of 3)
            # bit[15:00] reserved in A0
            #---------------------------------------------------------------------------
            encryptedRegionCnt = (otpmkKeyOpt & 0x000F0000) >> 16
            if encryptedRegionCnt == 0:
                otpmkKeyOpt = (otpmkKeyOpt & 0xFFF0FFFF) | (0x1 << 16)
                encryptedRegionCnt = 1
                otpmkEncryptedRegionStartList[0] = self.tgt.flexspiNorMemBase + RTyyyy_gendef.kIvtOffset_NOR
                # For BEE, it should be length
                otpmkEncryptedRegionLengthOrEndList[0] = misc.align_up(os.path.getsize(self.destAppFilename), RTyyyy_gendef.kSecFacRegionAlignedUnit_Bee) - RTyyyy_gendef.kIvtOffset_NOR
            else:
                pass
        elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
            #---------------------------------------------------------------------------
            # 0xe0001100 is an option for PRDB contruction and image encryption
            # bit[31:28] tag, fixed to 0x0E
            # bit[27:16] Reserved
            # bit[15:12] Key source. 1 for SNVS[255:128], 0 for SNVS[127:0]
            # bit[11:08] Encrypted region count (maximum of 4)
            # bit[07:00] Redundant image offset in 256K. 0 for no redundant image
            encryptedRegionCnt = (otpmkKeyOpt & 0x00000F00) >> 8
            if encryptedRegionCnt == 0:
                otpmkKeyOpt = (otpmkKeyOpt & 0xFFFFF0FF) | (0x1 << 8)
                encryptedRegionCnt = 1
                otpmkEncryptedRegionStartList[0] = self.tgt.flexspiNorMemBase + RTyyyy_gendef.kIvtOffset_NOR
                # For OTFAD, it should be end
                otpmkEncryptedRegionLengthOrEndList[0] = self.tgt.flexspiNorMemBase + misc.align_up(os.path.getsize(self.destAppFilename), RTyyyy_gendef.kSecFacRegionAlignedUnit_Otfad) - 1
            else:
                for i in range(encryptedRegionCnt):
                    otpmkEncryptedRegionLengthOrEndList[i] = otpmkEncryptedRegionStartList[i] + otpmkEncryptedRegionLengthOrEndList[i] - 1
        else:
            pass
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(otpmkKeyOpt))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadPrdbOpt))) + ";\n")
        else:
            status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadPrdbOpt, 0x4, otpmkKeyOpt)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        for i in range(encryptedRegionCnt):
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(otpmkEncryptedRegionStartList[i]))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadPrdbOpt + i * 8 + 4))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(otpmkEncryptedRegionLengthOrEndList[i]))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadPrdbOpt + i * 8 + 8))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadPrdbOpt + i * 8 + 4, 0x4, otpmkEncryptedRegionStartList[i])
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadPrdbOpt + i * 8 + 8, 0x4, otpmkEncryptedRegionLengthOrEndList[i])
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadPrdbOpt))) + ";\n")
        else:
            status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadPrdbOpt)
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        if not self._programFlexspiNorConfigBlock():
            return False
        return True

    def _isDeviceFuseSrkRegionReadyForBurn( self, srkFuseFilename ):
        isReady = True
        isBlank = True
        keyWords = RTyyyy_gendef.kSecKeyLengthInBits_SRK / 32
        for i in range(keyWords):
            srk = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK0'] + i, '(' + str(hex(0x580 + i * 0x10)) + ') ' + 'SRK' + str(i), False)
            if srk == None:
                isReady = False
                break
            elif srk != 0:
                isBlank = False
                val32 = self.getVal32FromBinFile(srkFuseFilename, (i * 4))
                if srk != val32:
                    isReady = False
                    break
        return isReady, isBlank

    def RTyyyy_burnMcuDeviceFuseByBlhost( self, fuseIndex, fuseValue, actionFrom=RTyyyy_rundef.kActionFrom_AllInOne):
        status = boot.status.kStatus_Success
        if self.isSbFileEnabledToGen:
            if actionFrom == RTyyyy_rundef.kActionFrom_AllInOne:
                if fuseIndex == self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG1']:
                    fuseValue = fuseValue | self.sbLastSharedFuseBootCfg1
                    self.sbLastSharedFuseBootCfg1 = fuseValue
                elif fuseIndex == self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_CFG']:
                    fuseValue = fuseValue | self.sbLastSharedFuseOtfadCfg
                    self.sbLastSharedFuseOtfadCfg = fuseValue
                else:
                    pass
                sbAppBdContent = "    load fuse 0x" + self.getFormattedFuseValue(fuseValue) + " > " + self.convertLongIntHexText(str(hex(fuseIndex))) + ";\n"
                self.sbAppBdContent += sbAppBdContent
                self.sbAppEfuseBdContent += sbAppBdContent
                self.isEfuseOperationInSbApp = True
            elif actionFrom == RTyyyy_rundef.kActionFrom_BurnFuse:
                self.sbUserEfuseBdContent += "    load fuse 0x" + self.getFormattedFuseValue(fuseValue) + " > " + self.convertLongIntHexText(str(hex(fuseIndex))) + ";\n"
            else:
                pass
        else:
            status, results, cmdStr = self.blhost.efuseProgramOnce(fuseIndex, self.getFormattedFuseValue(fuseValue))
            self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def burnSrkData ( self ):
        if self.isHabCertFastBoot:
            return True
        if os.path.isfile(self.srkFuseFilename):
            isReady, isBlank = self._isDeviceFuseSrkRegionReadyForBurn(self.srkFuseFilename)
            if isReady:
                if isBlank:
                    keyWords = RTyyyy_gendef.kSecKeyLengthInBits_SRK / 32
                    for i in range(keyWords):
                        val32 = self.getVal32FromBinFile(self.srkFuseFilename, (i * 4))
                        burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SRK0'] + i, val32)
                        if not burnResult:
                            self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnSrk'][self.languageIndex])
                            return False
                return True
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_srkHasBeenBurned'][self.languageIndex])
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['certGenError_srkNotGen'][self.languageIndex])
        return False

    def _isDeviceFuseSwGp2RegionReadyForBurn( self, swgp2DekFilename ):
        isReady = True
        isBlank = True
        keyWords = RTyyyy_gendef.kSecKeyLengthInBits_DEK / 32
        for i in range(keyWords):
            dek = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_0'] + i, '(' + str(hex(0x690 + i * 0x10)) + ') ' + 'SW_GP2_' + str(i), False)
            if dek == None:
                isReady = False
                break
            elif dek != 0:
                isBlank = False
                val32 = self.getVal32FromBinFile(swgp2DekFilename, (i * 4))
                if dek != val32:
                    isReady = False
                    break
        return isReady, isBlank

    def _isDeviceFuseGp4RegionReadyForBurn( self, gp4DekFilename ):
        isReady = True
        isBlank = True
        keyWords = RTyyyy_gendef.kSecKeyLengthInBits_DEK / 32
        for i in range(keyWords):
            dek = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_GP4_0'] + i, '(' + str(hex(0x8C0 + i * 0x10)) + ') ' + 'GP4_' + str(i), False)
            if dek == None:
                isReady = False
                break
            elif dek != 0:
                isBlank = False
                val32 = self.getVal32FromBinFile(gp4DekFilename, (i * 4))
                if dek != val32:
                    isReady = False
                    break
        return isReady, isBlank

    def _isDeviceFuseUserKey5RegionReadyForBurn( self, userkey5DekFilename ):
        isReady = True
        isBlank = True
        keyWords = RTyyyy_gendef.kSecKeyLengthInBits_DEK / 32
        for i in range(keyWords):
            dek = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_USER_KEY5_0'] + i, '(' + str(hex(0x1000 + i * 0x10)) + ') ' + 'USER_KEY5_' + str(i), False)
            if dek == None:
                isReady = False
                break
            elif dek != 0:
                isBlank = False
                val32 = self.getVal32FromBinFile(userkey5DekFilename, (i * 4))
                if dek != val32:
                    isReady = False
                    break
        return isReady, isBlank

    def _lockFuseSwGp2( self ):
        if not self.isAutomaticEfuseLocker:
            return True
        lock = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_LOCK'], '', False)
        if lock != None:
            lock = ((RTyyyy_fusedef.kEfuseMask_WLockSwGp2 | RTyyyy_fusedef.kEfuseMask_RLockSwGp2) | lock) ^ lock
            if self.isSbFileEnabledToGen:
                lock = (RTyyyy_fusedef.kEfuseMask_WLockSwGp2 | RTyyyy_fusedef.kEfuseMask_RLockSwGp2)
            burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_LOCK'], lock)
            if not burnResult:
                #self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnSwgp2Lock'][self.languageIndex])
                #return False
                pass
        return True

    def _lockFuseGp4( self ):
        if not self.isAutomaticEfuseLocker:
            return True
        lock = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_LOCK'], '', False)
        if lock != None:
            lock = ((RTyyyy_fusedef.kEfuseMask_WLockGp4 | RTyyyy_fusedef.kEfuseMask_RLockGp4) | lock) ^ lock
            if self.isSbFileEnabledToGen:
                lock = (RTyyyy_fusedef.kEfuseMask_WLockGp4 | RTyyyy_fusedef.kEfuseMask_RLockGp4)
            burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_LOCK'], lock)
            if not burnResult:
                #self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnGp4Lock'][self.languageIndex])
                #return False
                pass
        return True

    def burnHwCryptoDekData ( self ):
        needToBurnSwGp2 = False
        needToBurnGp4 = False
        needToBurnUserKey5 = False
        swgp2DekFilename = None
        gp4DekFilename = None
        userkey5DekFilename = None
        userKeyCtrlDict, userKeyCmdDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_UserKeys)
        if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
            if userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_Engine1 or userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_BothEngines:
                if userKeyCtrlDict['engine1_key_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                    needToBurnSwGp2 = True
                    swgp2DekFilename = self.beeDek1Filename
                elif userKeyCtrlDict['engine1_key_src'] == RTyyyy_uidef.kUserKeySource_GP4:
                    needToBurnGp4 = True
                    gp4DekFilename = self.beeDek1Filename
                else:
                    pass
            if userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_Engine0 or userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_BothEngines:
                if userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                    needToBurnSwGp2 = True
                    swgp2DekFilename = self.beeDek0Filename
                elif userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_GP4:
                    needToBurnGp4 = True
                    gp4DekFilename = self.beeDek0Filename
                else:
                    pass
        elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
            if userKeyCtrlDict['kek_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                needToBurnSwGp2 = True
                swgp2DekFilename = self.otfadDek0Filename
            elif userKeyCtrlDict['kek_src'] == RTyyyy_uidef.kUserKeySource_USER_KEY5:
                needToBurnUserKey5 = True
                userkey5DekFilename = self.otfadDek0Filename
            else:
                pass
        else:
            pass
        keyWords = RTyyyy_gendef.kSecKeyLengthInBits_DEK / 32
        if needToBurnSwGp2:
            isReady, isBlank = self._isDeviceFuseSwGp2RegionReadyForBurn(swgp2DekFilename)
            if isReady or self.isSbFileEnabledToGen:
                if isBlank or self.isSbFileEnabledToGen:
                    for i in range(keyWords):
                        val32 = self.getVal32FromBinFile(swgp2DekFilename, (i * 4))
                        burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_SW_GP2_0'] + i, val32)
                        if not burnResult:
                            self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnSwgp2'][self.languageIndex])
                            return False
                    if not self._lockFuseSwGp2():
                        return False
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_swgp2HasBeenBurned'][self.languageIndex], "Note")
        else:
            pass
        if needToBurnGp4:
            isReady, isBlank = self._isDeviceFuseGp4RegionReadyForBurn(gp4DekFilename)
            if isReady or self.isSbFileEnabledToGen:
                if isBlank or self.isSbFileEnabledToGen:
                    for i in range(keyWords):
                        val32 = self.getVal32FromBinFile(gp4DekFilename, (i * 4))
                        burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_GP4_0'] + i, val32)
                        if not burnResult:
                            self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnGp4'][self.languageIndex])
                            return False
                    if not self._lockFuseGp4():
                        return False
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_gp4HasBeenBurned'][self.languageIndex], "Note")
        else:
            pass
        if needToBurnUserKey5:
            isReady, isBlank = self._isDeviceFuseUserKey5RegionReadyForBurn(userkey5DekFilename)
            if isReady or self.isSbFileEnabledToGen:
                if isBlank or self.isSbFileEnabledToGen:
                    for i in range(keyWords):
                        val32 = self.getVal32FromBinFile(userkey5DekFilename, (i * 4))
                        burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_USER_KEY5_0'] + i, val32)
                        if not burnResult:
                            self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnUserkey5'][self.languageIndex])
                            return False
                    #if not self._lockFuseUserKey5():
                    #    return False
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_userkey5HasBeenBurned'][self.languageIndex], "Note")
        else:
            pass
        return True

    def _genDestEncAppFileWithoutCfgBlock( self ):
        destEncAppPath, destEncAppFile = os.path.split(self.destEncAppFilename)
        destEncAppName, destEncAppType = os.path.splitext(destEncAppFile)
        destEncAppName += '_nocfgblock'
        self.destEncAppNoCfgBlockFilename = os.path.join(destEncAppPath, destEncAppName + destEncAppType)
        imageLen = os.path.getsize(self.destEncAppFilename)
        imageData = None
        with open(self.destEncAppFilename, 'rb') as fileObj:
            imageData = fileObj.read(imageLen)
            if len(imageData) > self.tgt.xspiNorCfgInfoLen:
                imageData = imageData[self.tgt.xspiNorCfgInfoLen:len(imageData)]
            fileObj.close()
        with open(self.destEncAppNoCfgBlockFilename, 'wb') as fileObj:
            fileObj.write(imageData)
            fileObj.close()

    def _genDestEncAppFileWithoutKeyblobAndCfgBlock( self ):
        destEncAppPath, destEncAppFile = os.path.split(self.destEncAppFilename)
        destEncAppName, destEncAppType = os.path.splitext(destEncAppFile)
        destEncAppName += '_nokeyblob_nocfgblock'
        self.destEncAppNoKeyblobAndCfgBlockFilename = os.path.join(destEncAppPath, destEncAppName + destEncAppType)
        imageLen = os.path.getsize(self.destEncAppFilename)
        imageData = None
        with open(self.destEncAppFilename, 'rb') as fileObj:
            imageData = fileObj.read(imageLen)
            if len(imageData) > self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen:
                imageData = imageData[self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen:len(imageData)]
            fileObj.close()
        with open(self.destEncAppNoKeyblobAndCfgBlockFilename, 'wb') as fileObj:
            fileObj.write(imageData)
            fileObj.close()

    def _extractOtfadKeyblobFromDestEncAppFile( self ):
        imageLen = os.path.getsize(self.destEncAppFilename)
        imageData = None
        with open(self.destEncAppFilename, 'rb') as fileObj:
            imageData = fileObj.read(imageLen)
            if len(imageData) > RTyyyy_memdef.kMemBlockOffset_HwCryptoKeyBlob + RTyyyy_memdef.kMemBlockSize_HwCryptoKeyBlob:
                imageData = imageData[RTyyyy_memdef.kMemBlockOffset_HwCryptoKeyBlob:RTyyyy_memdef.kMemBlockOffset_HwCryptoKeyBlob + RTyyyy_memdef.kMemBlockSize_HwCryptoKeyBlob]
            fileObj.close()
        with open(self.otfadKeyblobFilenname, 'wb') as fileObj:
            fileObj.write(imageData)
            fileObj.close()

    def _programFlexspiNorOtfadKeyBlob( self ):
        otfadKeyblobLoadAddr = self.bootDeviceMemBase + RTyyyy_memdef.kMemBlockOffset_HwCryptoKeyBlob
        status = boot.status.kStatus_Success
        if self.isSbFileEnabledToGen:
            self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " otfadKeyblobFile > " + self.convertLongIntHexText(str(hex(otfadKeyblobLoadAddr))) + ";\n")
            status = boot.status.kStatus_Success
        else:
            status, results, cmdStr = self.blhost.writeMemory(otfadKeyblobLoadAddr, self.otfadKeyblobFilenname, self.bootDeviceMemId)
            self.printLog(cmdStr)
        return status == boot.status.kStatus_Success

    def RTyyyy_flashXmcdBinary ( self ):
        xmcdSettingsDict = uivar.getBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_Xmcd)
        status = boot.status.kStatus_Success
        if xmcdSettingsDict['isXmcdEnabled']:
            status, results, cmdStr = self.blhost.writeMemory(self.bootDeviceMemBase + self.destAppXmcdOffset, self.xmcdBinFilename, self.bootDeviceMemId)
            self.printLog(cmdStr)
        return status

    def RTyyyy_flashBootableImage ( self ):
        self._RTyyyy_prepareForBootDeviceOperation()
        imageLen = 0
        if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
            imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, semcNandImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            for i in range(self.semcNandImageCopies):
                imageLoadAddr = self.bootDeviceMemBase + (semcNandImageInfoList[i] >> 16) * self.semcNandBlockSize
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ".." + self.convertLongIntHexText(str(hex(imageLoadAddr + memEraseLen))) + ";\n")
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
                else:
                    status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
                    status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor:
            semcNorOpt, semcNorSetting, semcNorDeviceModel = uivar.getBootDeviceConfiguration(self.bootDevice)
            memEraseLen = self.destAppBinaryBytes+self.destAppVectorAddress
            imageLoadAddr = self.bootDeviceMemBase
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ".." + self.convertLongIntHexText(str(hex(imageLoadAddr + memEraseLen))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename,
                                                                  self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
            image0Size = 0
            if not self.isFlexspiNorErasedForImage:
                if not self._eraseFlexspiNorForImageLoading():
                    return False
                if self.secureBootType == RTyyyy_uidef.kSecureBootType_Development or \
                   self.secureBootType == RTyyyy_uidef.kSecureBootType_HabAuth or \
                   (self.secureBootType in RTyyyy_uidef.kSecureBootType_HwCrypto and self.keyStorageRegion == RTyyyy_uidef.kKeyStorageRegion_FlexibleUserKeys):
                    if not self._programFlexspiNorConfigBlock():
                        self.isFlexspiNorErasedForImage = False
                        self.isFdcbFromSrcApp = False
                        return False
            flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
            # Check if dual image boot is enabled
            if self.tgt.hasFlexspiNorDualImageBoot and ((flexspiNorDualImageInfoList[2] & 0xFFFF) != 0):
                if flexspiNorDualImageInfoList[0] == 0xffffffff:
                    self.flexspiNorImage0Version = flexspiNorDualImageInfoList[0]
                else:
                    self.flexspiNorImage0Version = flexspiNorDualImageInfoList[0] + ((flexspiNorDualImageInfoList[0] ^ 0xFFFF) << 16)
            if self.flexspiNorImage0Version != None and self.flexspiNorImage0Version != rundef.kFlexspiNorContent_Blank32:
                versionLoadAddr = self.bootDeviceMemBase + gendef.kImgVerOffset_NOR
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(self.flexspiNorImage0Version))) + " > " + self.convertLongIntHexText(str(hex(versionLoadAddr))) + ";\n")
                    status = boot.status.kStatus_Success
                else:
                    status, results, cmdStr = self.blhost.fillMemory(versionLoadAddr, 0x4, self.flexspiNorImage0Version)
                    self.printLog(cmdStr)
            if self.secureBootType in RTyyyy_uidef.kSecureBootType_HwCrypto and self.keyStorageRegion == RTyyyy_uidef.kKeyStorageRegion_FlexibleUserKeys:
                destEncAppFilename = None
                if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
                    self._genDestEncAppFileWithoutCfgBlock()
                    destEncAppFilename = self.destEncAppNoCfgBlockFilename
                elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
                    self._genDestEncAppFileWithoutKeyblobAndCfgBlock()
                    destEncAppFilename = self.destEncAppNoKeyblobAndCfgBlockFilename
                else:
                    pass
                imageLoadAddr = self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
                    status = boot.status.kStatus_Success
                else:
                    status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, destEncAppFilename, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                if self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
                    self._extractOtfadKeyblobFromDestEncAppFile()
                    if not self._programFlexspiNorOtfadKeyBlob():
                        self.isFlexspiNorErasedForImage = False
                        self.isFdcbFromSrcApp = False
                        return False
                else:
                    pass
                image0Size = imageLoadAddr - self.bootDeviceMemBase + os.path.getsize(destEncAppFilename)
            else:
                headerOffset = 0
                destAppFileToLoad = None
                if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                    headerOffset = RTyyyy_gendef.kIvtOffset_NOR
                    destAppFileToLoad = self.destAppNoPaddingFilename
                elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                    headerOffset = RTyyyy_gendef.kContainerOffset_NOR
                    destAppFileToLoad = self.destAppContainerFilename
                    status = self.RTyyyy_flashXmcdBinary()
                    if status != boot.status.kStatus_Success:
                        return False
                imageLoadAddr = self.bootDeviceMemBase + headerOffset
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
                    status = boot.status.kStatus_Success
                else:
                    status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, destAppFileToLoad, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                image0Size = imageLoadAddr - self.bootDeviceMemBase + os.path.getsize(destAppFileToLoad)
            self.isFlexspiNorErasedForImage = False
            self.isFdcbFromSrcApp = False
            if status != boot.status.kStatus_Success:
                return False
            else:
                # Check if dual image boot is enabled
                if self.tgt.hasFlexspiNorDualImageBoot and ((flexspiNorDualImageInfoList[2] & 0xFFFF) != 0):
                    image1Start = self.bootDeviceMemBase + (flexspiNorDualImageInfoList[2] & 0xFFFF) * 256 * 1024
                    image1Size = image0Size
                    if flexspiNorDualImageInfoList[1] == 0xffffffff:
                        self.flexspiNorImage1Version = flexspiNorDualImageInfoList[1]
                    else:
                        self.flexspiNorImage1Version = flexspiNorDualImageInfoList[1] + ((flexspiNorDualImageInfoList[1] ^ 0xFFFF) << 16)
                    if not self.flash2ndBootableImageIntoFlexspiNor(image1Start, image1Size, self.flexspiNorImage1Version, self.flexspiNorImage0Version):
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            self._calcFlexspiNandDeviceInfo()
            flexspiNandOpt0, flexspiNandOpt1, flexspiNandFcbOpt, flexspiNandImageInfoList, flexspiNandDeviceModel = uivar.getBootDeviceConfiguration(self.bootDevice)
            isAddressTypeBlockIdx = (((flexspiNandFcbOpt & 0x00000F00) >> 8) == 1)
            loadRegionStart = 0
            loadRegionEnd = 0
            for i in range(self.flexspiNandImageCopies):
                if isAddressTypeBlockIdx:
                    loadRegionStart = flexspiNandImageInfoList[i] >> 16
                    loadRegionEnd = loadRegionStart + flexspiNandImageInfoList[i] & 0xFFFF
                else:
                    loadRegionStart = self.bootDeviceMemBase + (flexspiNandImageInfoList[i] >> 16) * self.flexspiNandBlockSize
                    loadRegionEnd = loadRegionStart + (flexspiNandImageInfoList[i] & 0xFFFF) * self.flexspiNandBlockSize
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(loadRegionStart))) + ".." + self.convertLongIntHexText(str(hex(loadRegionEnd))) + ";\n")
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(loadRegionStart))) + ";\n")
                else:
                    status, results, cmdStr = self.blhost.flashEraseRegion(loadRegionStart, loadRegionEnd - loadRegionStart, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
                    status, results, cmdStr = self.blhost.writeMemory(loadRegionStart, self.destAppFilename, self.bootDeviceMemId)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            imageLoadAddr = self.bootDeviceMemBase
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ".." + self.convertLongIntHexText(str(hex(imageLoadAddr + memEraseLen))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd or \
             self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            headerOffset = 0
            destAppFileToLoad = None
            if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                headerOffset = RTyyyy_gendef.kIvtOffset_NAND_SD_EEPROM
                destAppFileToLoad = self.destAppNoPaddingFilename
            elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                headerOffset = RTyyyy_gendef.kContainerOffset_SD
                destAppFileToLoad = self.destAppContainerFilename
                imageLen = os.path.getsize(destAppFileToLoad) + headerOffset
                status = self.RTyyyy_flashXmcdBinary()
                if status != boot.status.kStatus_Success:
                    return False
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            imageLoadAddr = self.bootDeviceMemBase + headerOffset
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ".." + self.convertLongIntHexText(str(hex(imageLoadAddr + memEraseLen))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, destAppFileToLoad, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
        else:
            pass
        if self.isConvertedAppUsed:
            try:
                os.remove(self.srcAppFilename)
            except:
                pass
            self.isConvertedAppUsed = False
        return True

    def _getMcuDeviceSemcNandCfg( self ):
        semcNandCfg = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_SemcNandCfg'], '', False)
        return semcNandCfg

    def _getMcuDeviceLpspiCfg( self ):
        lpspiCfg = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_LpspiCfg'], '', False)
        return lpspiCfg

    def _burnCommonMcuFuseBits( self, fuseIndexStr, fuseMaskStr, fuseShiftStr, setFuseBits ):
            getFuseWord = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIndexStr], '', False)
            getFuseBits = (getFuseWord & self.tgt.efusemapDefnDict[fuseMaskStr]) >> self.tgt.efusemapDefnDict[fuseShiftStr]
            if setFuseBits != getFuseBits:
                if getFuseBits != 0:
                    return False
                setFuseWord = (getFuseWord & (~self.tgt.efusemapDefnDict[fuseMaskStr]) | (setFuseBits << self.tgt.efusemapDefnDict[fuseShiftStr]))
                burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIndexStr], setFuseWord)
                return burnResult 
            else:
                return True

    def RTyyyy_burnBootDeviceFuses( self ):
        if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            setSemcNandCfg = 0
            semcNandOpt, semcNandFcbOpt, imageInfo = uivar.getBootDeviceConfiguration(self.bootDevice)
            # Set Device Ecc Status
            eccStatus = (semcNandOpt & 0x00020000) >> 17
            setSemcNandCfg = (setSemcNandCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_RawNandEccStatus']) | (eccStatus << self.tgt.efusemapDefnDict['kEfuseShift_RawNandEccStatus']))
            # Set I/O Port Size
            portSize = (semcNandOpt & 0x00000300) >> 8
            if portSize <= 1:
                portSize = 0
            else:
                portSize = 1
            setSemcNandCfg = (setSemcNandCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_RawNandPortSize']) | (portSize << self.tgt.efusemapDefnDict['kEfuseShift_RawNandPortSize']))
            if self.tgt.isEccTypeSetInFuseMiscConf:
                # Set ECC Check Type
                eccType = (semcNandOpt & 0x00010000) >> 16
                if self.tgt.isSwEccSetAsDefaultInNandOpt:
                    eccType = (eccType + 1) % 2
                setSemcNandCfg = (setSemcNandCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_RawNandEccEdoSet']) | (eccType << self.tgt.efusemapDefnDict['kEfuseShift_RawNandEccEdoSet']))
            else:
                # Set EDO mode
                edoMode = (semcNandOpt & 0x00000008) >> 3
                setSemcNandCfg = (setSemcNandCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_RawNandEccEdoSet']) | (edoMode << self.tgt.efusemapDefnDict['kEfuseShift_RawNandEccEdoSet']))
            getSemcNandCfg = self._getMcuDeviceSemcNandCfg()
            if getSemcNandCfg != None:
                destSemcNandCfg = setSemcNandCfg | getSemcNandCfg
                if (destSemcNandCfg & (self.tgt.efusemapDefnDict['kEfuseMask_RawNandEccStatus'] | self.tgt.efusemapDefnDict['kEfuseMask_RawNandPortSize'] | self.tgt.efusemapDefnDict['kEfuseMask_RawNandEccEdoSet'])) != setSemcNandCfg:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_miscConf1HasBeenBurned'][self.languageIndex])
                    return False
                else:
                    destSemcNandCfg = destSemcNandCfg ^ getSemcNandCfg
                    burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_SemcNandCfg'], destSemcNandCfg)
                    if not burnResult:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnMiscConf1'][self.languageIndex])
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
            if self.tgt.hasFlexspiNorDualImageBoot:
                flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
                flexspiNorImage1Offset = (flexspiNorDualImageInfoList[2] & 0xFFFF)
                flexspiNorImage1Size = ((flexspiNorDualImageInfoList[2] >> 16) & 0xFFFF)
                if flexspiNorImage1Offset != 0:
                    if not self._burnCommonMcuFuseBits('kEfuseLocation_FlexspiNorDualImageBootCfg', 'kEfuseMask_FlexspiNorImage1Info', 'kEfuseShift_FlexspiNorImage1Info', (flexspiNorImage1Offset << 4) + flexspiNorImage1Size):
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnDualImageMiscConf'][self.languageIndex])
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            pass
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            setLpspiCfg = 0
            # Set EEPROM enable
            setLpspiCfg = setLpspiCfg | self.tgt.efusemapDefnDict['kEfuseMask_EepromEnable']
            lpspiNorOpt0, lpspiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            # Set Spi Index
            spiIndex = ((lpspiNorOpt0 & 0x00F00000) >> 20) - 1
            setLpspiCfg = (setLpspiCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_LpspiIndex']) | (spiIndex << self.tgt.efusemapDefnDict['kEfuseShift_LpspiIndex']))
            # Set Spi Speed
            spiSpeed = (lpspiNorOpt1 & 0x0000000F) >> 0
            setLpspiCfg = (setLpspiCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_LpspiSpeed']) | (spiSpeed << self.tgt.efusemapDefnDict['kEfuseShift_LpspiSpeed']))
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                # Set Spi Addressing
                spiAddressing = 0
                val = (lpspiNorOpt0 & 0x00000F00) >> 8
                totalByteSize = 0
                if val <= 11:
                    totalByteSize = int(math.pow(2, val + 19))
                else:
                    totalByteSize = int(math.pow(2, val + 3))
                if totalByteSize > (64 * 1024):
                    spiAddressing = RTyyyy_fusedef.kSpiAddressing_3Bytes
                else:
                    spiAddressing = RTyyyy_fusedef.kSpiAddressing_2Bytes
                setLpspiCfg = (setLpspiCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_SpiAddressing']) | (spiAddressing << self.tgt.efusemapDefnDict['kEfuseShift_SpiAddressing']))
            elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                pass
            else:
                pass
            getLpspiCfg = self._getMcuDeviceLpspiCfg()
            if getLpspiCfg != None:
                destLpspiCfg = setLpspiCfg | getLpspiCfg
                if (destLpspiCfg & (self.tgt.efusemapDefnDict['kEfuseMask_EepromEnable'] | self.tgt.efusemapDefnDict['kEfuseMask_LpspiIndex'] | self.tgt.efusemapDefnDict['kEfuseMask_SpiAddressing'] | self.tgt.efusemapDefnDict['kEfuseMask_LpspiSpeed'])) != setLpspiCfg:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_miscConf0HasBeenBurned'][self.languageIndex])
                    return False
                else:
                    destLpspiCfg = destLpspiCfg ^ getLpspiCfg
                    burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_LpspiCfg'], destLpspiCfg)
                    if not burnResult:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnMiscConf0'][self.languageIndex])
                        return False
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd:
            pass
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            pass
        else:
            pass
        return True

    def _getMcuDeviceHwCryptoKeySel( self ):
        hwCryptoKeySel = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_HwCryptoKeySel'], '', False)
        if hwCryptoKeySel != None:
            self.mcuDeviceHwCryptoKey0Sel = ((hwCryptoKeySel & self.tgt.efusemapDefnDict['kEfuseMask_HwCryptoKey0Sel']) >> self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey0Sel'])
            self.mcuDeviceHwCryptoKey1Sel = ((hwCryptoKeySel & self.tgt.efusemapDefnDict['kEfuseMask_HwCryptoKey1Sel']) >> self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey1Sel'])
        return hwCryptoKeySel

    def burnHwCryptoKeySel( self ):
        setHwCryptoKey0Sel = None
        setHwCryptoKey1Sel = None
        if self.keyStorageRegion == RTyyyy_uidef.kKeyStorageRegion_FixedOtpmkKey:
            otpmkKeyCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_OtpmkKey)
            otpmkKeyOpt = otpmkKeyCommDict['opt']
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
                encryptedRegionCnt = (otpmkKeyOpt & 0x000F0000) >> 16
                # One PRDB means one BEE_KEY, no matter how many FAC regions it has
                if encryptedRegionCnt >= 0:
                    setHwCryptoKey0Sel = RTyyyy_fusedef.kBeeKeySel_FromOtpmkHigh
                #if encryptedRegionCnt > 1:
                #    setHwCryptoKey1Sel = RTyyyy_fusedef.kBeeKeySel_FromOtpmkHigh
            elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
                keySource = (otpmkKeyOpt & 0x0000F000) >> 12
                if keySource == 0:
                    setHwCryptoKey0Sel = RTyyyy_fusedef.kOtfadKeySel_FromOtpmkLow
                elif keySource == 1:
                    setHwCryptoKey0Sel = RTyyyy_fusedef.kOtfadKeySel_FromOtpmkHigh
                else:
                    pass
            else:
                pass
        elif self.keyStorageRegion == RTyyyy_uidef.kKeyStorageRegion_FlexibleUserKeys:
            userKeyCtrlDict, userKeyCmdDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_UserKeys)
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
                if userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_Engine0 or userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_BothEngines:
                    if userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_OTPMK:
                        setHwCryptoKey0Sel = RTyyyy_fusedef.kBeeKeySel_FromOtpmkHigh
                    elif userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                        setHwCryptoKey0Sel = RTyyyy_fusedef.kBeeKeySel_FromSwGp2
                    elif userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_GP4:
                        setHwCryptoKey0Sel = RTyyyy_fusedef.kBeeKeySel_FromGp4
                    else:
                        pass
                if userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_Engine1 or userKeyCtrlDict['engine_sel'] == RTyyyy_uidef.kUserEngineSel_BothEngines:
                    if userKeyCtrlDict['engine0_key_src'] == RTyyyy_uidef.kUserKeySource_OTPMK:
                        setHwCryptoKey1Sel = RTyyyy_fusedef.kBeeKeySel_FromOtpmkHigh
                    elif userKeyCtrlDict['engine1_key_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                        setHwCryptoKey1Sel = RTyyyy_fusedef.kBeeKeySel_FromSwGp2
                    elif userKeyCtrlDict['engine1_key_src'] == RTyyyy_uidef.kUserKeySource_GP4:
                        setHwCryptoKey1Sel = RTyyyy_fusedef.kBeeKeySel_FromGp4
                    else:
                        pass
            elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
                if userKeyCtrlDict['kek_src'] == RTyyyy_uidef.kUserKeySource_SW_GP2:
                    setHwCryptoKey0Sel = RTyyyy_fusedef.kOtfadKeySel_FromSwGp2
                elif userKeyCtrlDict['kek_src'] == RTyyyy_uidef.kUserKeySource_USER_KEY5:
                    setHwCryptoKey0Sel = RTyyyy_fusedef.kOtfadKeySel_FromUserKey5
                else:
                    pass
            else:
                pass
        else:
            pass
        getHwCryptoKeySel = self._getMcuDeviceHwCryptoKeySel()
        if getHwCryptoKeySel != None:
            destHwCryptoKeySel = 0
            if setHwCryptoKey0Sel != None:
                destHwCryptoKeySel = getHwCryptoKeySel | (setHwCryptoKey0Sel << self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey0Sel'])
                currHwCryptoKey0Sel = ((getHwCryptoKeySel & self.tgt.efusemapDefnDict['kEfuseMask_HwCryptoKey0Sel']) >> self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey0Sel'])
                if currHwCryptoKey0Sel and currHwCryptoKey0Sel != setHwCryptoKey0Sel:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_hwCryptoKey0SelHasBeenBurned'][self.languageIndex])
                    return False
            else:
                destHwCryptoKeySel = getHwCryptoKeySel
            if setHwCryptoKey1Sel != None:
                destHwCryptoKeySel = destHwCryptoKeySel | (setHwCryptoKey1Sel << self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey1Sel'])
                currHwCryptoKey1Sel = ((getHwCryptoKeySel & self.tgt.efusemapDefnDict['kEfuseMask_HwCryptoKey1Sel']) >> self.tgt.efusemapDefnDict['kEfuseShift_HwCryptoKey1Sel'])
                if currHwCryptoKey1Sel and currHwCryptoKey1Sel != setHwCryptoKey1Sel:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_hwCryptoKey1SelHasBeenBurned'][self.languageIndex])
                    return False
            destHwCryptoKeySel = destHwCryptoKeySel ^ getHwCryptoKeySel
            burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_HwCryptoKeySel'], destHwCryptoKeySel)
            if not burnResult:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnHwCryptoKeyxSel'][self.languageIndex])
                return False
        return True

    def enableOtfad( self ):
        getOtfadCfg = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_OtfadEnable'], '', False)
        if getOtfadCfg != None:
            destOtfadCfg = 0
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                destOtfadCfg = getOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_OtfadEnable'])
            elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                destOtfadCfg = getOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_OtfadKeyblobEnable'])
                destOtfadCfg = destOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_OtfadKeyblobCrcEnable'])
                destOtfadCfg = destOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_Otfad2KeyblobEnable'])
                destOtfadCfg = destOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_Otfad2KeyblobCrcEnable'])
            else:
                destOtfadCfg = getOtfadCfg
            destOtfadCfg = destOtfadCfg ^ getOtfadCfg
            burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_OtfadEnable'], destOtfadCfg)
            if not burnResult:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnOtfadEnablementBit'][self.languageIndex])
                return False
        return True

    def _isDeviceFuseOtfadKeyScrambleAlgoRegionReadyForBurn( self, scrambleAlgo ):
        isReady = True
        isBlank = True
        key = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_KEY'], '', False)
        if key == None:
            isReady = False
        elif key != 0:
            isBlank = False
            if key != scrambleAlgo:
                isReady = False
        return isReady, isBlank

    def burnOtfadKeyScrambleAlgo ( self, scrambleAlgo ):
        isReady, isBlank = self._isDeviceFuseOtfadKeyScrambleAlgoRegionReadyForBurn(scrambleAlgo)
        if isReady:
            if isBlank:
                burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_KEY'], scrambleAlgo)
                if not burnResult:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnOtfadKeyScramble'][self.languageIndex])
                    return False
            return True
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_otfadKeyScrambleHasBeenBurned'][self.languageIndex])
        return False

    def burnOtfadScrambleFields( self ):
        if self.keyStorageRegion == RTyyyy_uidef.kKeyStorageRegion_FlexibleUserKeys:
            userKeyCtrlDict, userKeyCmdDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_UserKeys)
            if userKeyCmdDict['scramble'] != None:
                scrambleAlgo = int(userKeyCmdDict['scramble'][2:len(userKeyCmdDict['scramble'])], 16)
                if not self.burnOtfadKeyScrambleAlgo(scrambleAlgo):
                    return False
                scrambleAlignment = int(userKeyCmdDict['scramble_align'][2:len(userKeyCmdDict['scramble_align'])], 16)
                getOtfadCfg = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_CFG'], '', False)
                if getOtfadCfg != None:
                    destOtfadCfg = getOtfadCfg | (0x1 << self.tgt.efusemapDefnDict['kEfuseShift_OtfadKeyScrambleEnable'])
                    if self.tgt.efusemapDefnDict['kEfuseMask_OtfadKeyScrambleAlign'] != None:
                        destOtfadCfg = (destOtfadCfg & (~self.tgt.efusemapDefnDict['kEfuseMask_OtfadKeyScrambleAlign'])) | (scrambleAlignment << self.tgt.efusemapDefnDict['kEfuseShift_OtfadKeyScrambleAlign'])
                    destOtfadCfg = destOtfadCfg ^ getOtfadCfg
                    burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_OTFAD_CFG'], destOtfadCfg)
                    if not burnResult:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnOtfadScrambleConfigurationField'][self.languageIndex])
                        return False
                return True
            else:
                return True
        else:
            return True

    def burnHwCryptoEnablements( self ):
        if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
            return True
        elif self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
            return self.enableOtfad() and self.burnOtfadScrambleFields()
        else:
            pass

    def flashHabDekToGenerateKeyBlob ( self ):
        if os.path.isfile(self.habDekFilename) and self.habDekDataOffset != None:
            self._RTyyyy_prepareForBootDeviceOperation()
            imageLen = os.path.getsize(self.destAppFilename)
            imageCopies = 0x1
            if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
                imageCopies = self.semcNandImageCopies
            else:
                pass
            # Construct KeyBlob Option
            #---------------------------------------------------------------------------
            # bit [31:28] tag, fixed to 0x0b
            # bit [27:24] type, 0 - Update KeyBlob context, 1 Program Keyblob to SPI NAND
            # bit [23:20] keyblob option block size, must equal to 3 if type =0,
            #             reserved if type = 1
            # bit [19:08] Reserved
            # bit [07:04] DEK size, 0-128bit 1-192bit 2-256 bit, only applicable if type=0
            # bit [03:00] Firmware Index, only applicable if type = 1
            # if type = 0, next words indicate the address that holds dek
            #              the 3rd word
            #----------------------------------------------------------------------------
            keyBlobContextOpt = 0xb0300000
            keyBlobDataOpt = 0xb1000000
            if self.isSbFileEnabledToGen:
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load dekFile > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadDekData))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(keyBlobContextOpt))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadDekData))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext + 4))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(self.habDekDataOffset))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext + 8))) + ";\n")
                self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.writeMemory(self.tgt.ramFreeSpaceStart_LoadDekData, self.habDekFilename)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext, 0x4, keyBlobContextOpt)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext + 4, 0x4, self.tgt.ramFreeSpaceStart_LoadDekData)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadKeyBlobContext + 8, 0x4, self.habDekDataOffset)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadKeyBlobContext)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
            for i in range(imageCopies):
                ramFreeSpace = self.tgt.ramFreeSpaceStart_LoadKeyBlobData + (RTyyyy_rundef.kRamFreeSpaceStep_LoadKeyBlobData * i)
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(keyBlobDataOpt + i))) + " > " + self.convertLongIntHexText(str(hex(ramFreeSpace))) + ";\n")
                else:
                    status, results, cmdStr = self.blhost.fillMemory(ramFreeSpace, 0x4, keyBlobDataOpt + i)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
                ########################################################################
                # Flashloader will not erase keyblob region automatically, so we need to handle it here manually
                imageLoadAddr = 0x0
                if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
                    semcNandOpt, semcNandFcbOpt, imageInfo = uivar.getBootDeviceConfiguration(self.bootDevice)
                    imageLoadAddr = self.bootDeviceMemBase + (imageInfo[i] >> 16) * self.semcNandBlockSize
                elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor or \
                     self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor or \
                     self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd or \
                     self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
                    imageLoadAddr = self.bootDeviceMemBase
                else:
                    pass
                alignedErasedSize = misc.align_up(imageLen, self.comMemEraseUnit)
                needToBeErasedSize = misc.align_up(self.habDekDataOffset + RTyyyy_memdef.kMemBlockSize_HabKeyBlob, self.comMemEraseUnit)
                if alignedErasedSize < needToBeErasedSize:
                    memEraseLen = needToBeErasedSize - alignedErasedSize
                    alignedMemEraseAddr = imageLoadAddr + alignedErasedSize
                    rangeStart, rangeLen = self._getAlignedFlexspiNorEraseRange(alignedMemEraseAddr, memEraseLen)
                    if self.isSbFileEnabledToGen:
                        self._RTyyyy_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(rangeStart))) + ".." + self.convertLongIntHexText(str(hex(rangeStart + rangeLen))) + ";\n")
                    else:
                        status, results, cmdStr = self.blhost.flashEraseRegion(rangeStart, rangeLen, self.bootDeviceMemId)
                        self.printLog(cmdStr)
                        if status != boot.status.kStatus_Success:
                            return False
                ########################################################################
                if self.isSbFileEnabledToGen:
                    self._RTyyyy_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(ramFreeSpace))) + ";\n")
                else:
                    status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, ramFreeSpace)
                    self.printLog(cmdStr)
                    if status != boot.status.kStatus_Success:
                        return False
            if self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor:
                if not self._eraseFlexspiNorForConfigBlockLoading():
                    return False
                if not self._programFlexspiNorConfigBlock():
                    return False
            self.updateImgPictureAfterFlashDek()
            return True
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['certGenError_dekNotGen'][self.languageIndex])
            return False

    def enableHab( self ):
        if self.mcuDeviceHabStatus != RTyyyy_fusedef.kHabStatus_Closed0 and \
           self.mcuDeviceHabStatus != RTyyyy_fusedef.kHabStatus_Closed1:
            secConfig1 = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_SecConfig1'], '', False)
            if secConfig1 != None:
                secConfig1 = (self.tgt.efusemapDefnDict['kEfuseMask_SecConfig1'] | secConfig1) ^ secConfig1
                burnResult = self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseLocation_SecConfig1'], secConfig1)
                if not burnResult:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_failToBurnSecConfig1'][self.languageIndex])
                    return False
        return True

    def RTyyyy_resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
