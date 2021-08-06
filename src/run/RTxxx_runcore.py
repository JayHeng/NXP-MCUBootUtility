#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import RTxxx_rundef
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import RTxxx_gencore
from gen import RTxxx_gendef
from ui import RTxxx_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from mem import RTxxx_memdef
from boot import bltest
from boot import target
from utils import misc

def RTxxx_createTarget(device, exeBinRoot):
    # Build path to target directory and config file.
    cpu = "MIMXRT685"
    if device == uidef.kMcuDevice_iMXRT500:
        cpu = "MIMXRT595"
    elif device == uidef.kMcuDevice_iMXRT600:
        cpu = "MIMXRT685"
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

class secBootRTxxxRun(RTxxx_gencore.secBootRTxxxGen):

    def __init__(self, parent):
        RTxxx_gencore.secBootRTxxxGen.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
            self.RTxxx_initRun()

    def RTxxx_initRun( self ):
        self.blhost = None
        self.tgt = None
        self.cpuDir = None
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost2_3', 'win', 'vectors')

        self.RTxxx_isDeviceEnabledToOperate = True
        self.bootDeviceMemId = None
        self.bootDeviceMemBase = None
        self.isXspiNorErasedForImage = False

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

        self.RTxxx_createMcuTarget()

    def RTxxx_createMcuTarget( self ):
        self.tgt, self.cpuDir = RTxxx_createTarget(self.mcuDevice, self.exeBinRoot)

    def RTxxx_getUsbid( self ):
        self.RTxxx_createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def RTxxx_connectToDevice( self , connectStage):
        if connectStage == uidef.kConnectStage_Rom or connectStage == uidef.kConnectStage_Flashloader:
            # Create the target object.
            self.RTxxx_createMcuTarget()
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
                if connectStage == uidef.kConnectStage_Rom:
                    usbVid = self.tgt.romUsbVid
                    usbPid = self.tgt.romUsbPid
                elif connectStage == uidef.kConnectStage_Flashloader:
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

    def RTxxx_pingRom( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def RTxxx_readMcuDeviceOtpByBlhost( self, otpIndex, otpName, needToShow=True):
        if not self.RTxxx_isDeviceEnabledToOperate and self.isSbFileEnabledToGen:
            return RTxxx_fusedef.kOtpValue_Blank
        status, results, cmdStr = self.blhost.efuseReadOnce(otpIndex)
        self.printLog(cmdStr)
        if (status == boot.status.kStatus_Success):
            if needToShow:
                self.printDeviceStatus(otpName + " = " + self.convertLongIntHexText(str(hex(results[1]))))
            return results[1]
        else:
            if needToShow:
                self.printDeviceStatus(otpName + " = --------")
            return None

    def _RTxxx_readMcuDeviceOtpBootCfg( self ):
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG0'], '(0x60) BOOT_CFG0')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG1'], '(0x61) BOOT_CFG1')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG2'], '(0x62) BOOT_CFG2')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG3'], '(0x63) BOOT_CFG3')

    def RTxxx_getMcuDeviceInfoViaRom( self ):
        self.printDeviceStatus("----------MCU ROM info-----------")
        self.getMcuDeviceBootloaderVersion()
        self.printDeviceStatus("--------MCU device otpmap--------")
        self._RTxxx_readMcuDeviceOtpBootCfg()

    def _getXspiNorDeviceInfo ( self, useDefault=False ):
        if not self.RTxxx_isDeviceEnabledToOperate and self.isSbFileEnabledToGen:
            return True
        filename = 'xspiNorCfg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset, rundef.kXspiNorCfgInfo_Length, filename, self.bootDeviceMemId)
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

    def _getFlexcommSpiNorDeviceInfo ( self ):
        pageByteSize = 0
        sectorByteSize = 0
        totalByteSize = 0
        flexcommSpiNorOpt0, flexcommSpiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
        val = (flexcommSpiNorOpt0 & 0x0000000F) >> 0
        if val <= 2:
            pageByteSize = int(math.pow(2, val + 8))
        else:
            pageByteSize = int(math.pow(2, val + 2))
        val = (flexcommSpiNorOpt0 & 0x000000F0) >> 4
        if val <= 1:
            sectorByteSize = int(math.pow(2, val + 12))
        else:
            sectorByteSize = int(math.pow(2, val + 13))
        val = (flexcommSpiNorOpt0 & 0x00000F00) >> 8
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

    def RTxxx_getBootDeviceInfoViaRom ( self ):
        if self.toolRunMode == uidef.kToolRunMode_SblOta:
            self._RTxxx_prepareForBootDeviceOperation()
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
            if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
                self.printDeviceStatus("--------FlexSPI NOR memory--------")
            elif self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
                self.printDeviceStatus("--------QuadSPI NOR memory--------")
            else:
                pass
            if not self._getXspiNorDeviceInfo(False):
                if not self._eraseXspiNorForConfigBlockLoading():
                    return False
                if not self._programXspiNorConfigBlock():
                    return False
                self._getXspiNorDeviceInfo(True)
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            self.printDeviceStatus("--Flexcomm SPI NOR memory--")
            self._getFlexcommSpiNorDeviceInfo()
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            self.printDeviceStatus("--------uSDHC SD Card info--------")
            pass
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            self.printDeviceStatus("--------uSDHC MMC Card info-------")
            pass
        else:
            pass

    def _RTxxx_prepareForBootDeviceOperation ( self ):
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNor
            self.bootDeviceMemBase = self.tgt.flexspiNorMemBase
        elif self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_QuadspiNor
            self.bootDeviceMemBase = self.tgt.quadspiNorMemBase
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_UsdhcSd
            self.bootDeviceMemBase = RTxxx_rundef.kBootDeviceMemBase_UsdhcSd
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_UsdhcMmc
            self.bootDeviceMemBase = RTxxx_rundef.kBootDeviceMemBase_UsdhcMmc
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_SpiNor
            self.bootDeviceMemBase = RTxxx_rundef.kBootDeviceMemBase_FlexcommSpiNor
        else:
            pass

    def _RTxxx_addFlashActionIntoSbAppBdContent(self, actionContent ):
        self.sbAppBdContent += actionContent

    def _isXspiNorConfigBlockRegionBlank( self ):
        filename = 'xspiNorCfg.dat'
        filepath = os.path.join(self.blhostVectorsDir, filename)
        status, results, cmdStr = self.blhost.readMemory(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, rundef.kFlexspiNorCfgInfo_Length, filename, rundef.kBootDeviceMemId_FlexspiNor)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        for offset in range(rundef.kFlexspiNorCfgInfo_Length):
            value = self.getVal8FromBinFile(filepath, offset)
            if value != rundef.kFlexspiNorContent_Blank8:
                return False
        try:
            os.remove(filepath)
        except:
            pass
        return True

    def _eraseXspiNorForConfigBlockLoading( self ):
        status = boot.status.kStatus_Success
        if self.RTxxx_isDeviceEnabledToOperate:
            if not self._isXspiNorConfigBlockRegionBlank():
                if self.bootDeviceMemId == rundef.kBootDeviceMemId_FlexspiNor:
                    status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, rundef.kXspiNorCfgInfo_Length, rundef.kBootDeviceMemId_FlexspiNor)
                elif self.bootDeviceMemId == rundef.kBootDeviceMemId_QuadspiNor:
                    status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.quadspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, rundef.kXspiNorCfgInfo_Length, rundef.kBootDeviceMemId_QuadspiNor)
                else:
                    pass
                self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset))) + ".." + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset + rundef.kFlexspiNorCfgInfo_Length))) + ";\n")
        return (status == boot.status.kStatus_Success)

    def _programXspiNorConfigBlock ( self ):
        status = boot.status.kStatus_Success
        # 0xf000000f is the tag to notify Flashloader to program FlexSPI/QuadSPI NOR config block to the start of device
        if self.isFdcbFromSrcApp:
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.writeMemory(self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset, self.fdcbBinFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
        else:
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.fillMemory(RTxxx_rundef.kRamFreeSpaceStart_LoadCfgBlock, 0x4, rundef.kFlexspiNorCfgInfo_Notify)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(rundef.kFlexspiNorCfgInfo_Notify))) + " > " + self.convertLongIntHexText(str(hex(RTxxx_rundef.kRamFreeSpaceStart_LoadCfgBlock))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, RTxxx_rundef.kRamFreeSpaceStart_LoadCfgBlock)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(RTxxx_rundef.kRamFreeSpaceStart_LoadCfgBlock))) + ";\n")
        if self.isSbFileEnabledToGen:
            return True
        else:
            return (status == boot.status.kStatus_Success)

    def RTxxx_configureBootDevice ( self ):
        self._RTxxx_prepareForBootDeviceOperation()
        flexspiNorDeviceModel = None
        configOptList = []
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
            flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept = uivar.getBootDeviceConfiguration(uidef.kBootDevice_XspiNor)
            configOptList.extend([flexspiNorOpt0, flexspiNorOpt1])
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            flexcommSpiNorOpt0, flexcommSpiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([flexcommSpiNorOpt0, flexcommSpiNorOpt1])
        else:
            pass
        status = boot.status.kStatus_Success
        if flexspiNorDeviceModel == uidef.kFlexspiNorDevice_FDCB:
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.writeMemory(RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt, self.cfgFdcbBinFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " cfgFdcbBinFile > " + self.convertLongIntHexText(str(hex(RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
        else:
            for i in range(len(configOptList)):
                if self.RTxxx_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.fillMemory(RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt + 4 * i, 0x4, configOptList[i])
                    self.printLog(cmdStr)
                if self.isSbFileEnabledToGen:
                    self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(configOptList[i]))) + " > " + self.convertLongIntHexText(str(hex(RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt + 4 * i))) + ";\n")
                if status != boot.status.kStatus_Success:
                    return False
        if self.RTxxx_isDeviceEnabledToOperate:
            status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt)
            self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(RTxxx_rundef.kRamFreeSpaceStart_LoadCommOpt))) + ";\n")
        if status != boot.status.kStatus_Success:
            return False
        return True

    def _eraseXspiNorForImageLoading( self ):
        imageLen = os.path.getsize(self.destAppFilename)
        imageLen += RTxxx_gendef.kBootImageOffset_NOR_SD_EEPROM
        memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
        status = None
        cmdStr = ''
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase))) + ".." + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + memEraseLen))) + ";\n")
        else:
            if self.bootDeviceMemId == rundef.kBootDeviceMemId_FlexspiNor:
                status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.flexspiNorMemBase, memEraseLen, self.bootDeviceMemId)
            elif self.bootDeviceMemId == rundef.kBootDeviceMemId_QuadspiNor:
                status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.quadspiNorMemBase, memEraseLen, self.bootDeviceMemId)
            else:
                pass
            self.printLog(cmdStr)
            if status != boot.status.kStatus_Success:
                return False
        self.isXspiNorErasedForImage = True
        return True

    def RTxxx_burnMcuDeviceOtpByBlhost( self, otpIndex, otpValue, actionFrom=RTxxx_rundef.kActionFrom_AllInOne):
        status = boot.status.kStatus_Success
        if self.isSbFileEnabledToGen:
            if actionFrom == RTxxx_rundef.kActionFrom_AllInOne:
                sbAppBdContent = "    load ifr 0x" + self.getFormattedFuseValue(otpValue) + " > " + self.convertLongIntHexText(str(hex(otpIndex))) + ";\n"
                self.sbAppBdContent += sbAppBdContent
                self.isOtpOperationInSbApp = True
            elif actionFrom == RTxxx_rundef.kActionFrom_BurnOtp:
                self.sbUserEfuseBdContent += "    load ifr 0x" + self.getFormattedFuseValue(otpValue) + " > " + self.convertLongIntHexText(str(hex(otpIndex))) + ";\n"
            else:
                pass
        else:
            status, results, cmdStr = self.blhost.efuseProgramOnce(otpIndex, self.getFormattedFuseValue(otpValue))
            self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def RTxxx_flashBootableImage ( self ):
        self._RTxxx_prepareForBootDeviceOperation()
        imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
            if not self.isXspiNorErasedForImage:
                if not self._eraseXspiNorForImageLoading():
                    return False
                if self.secureBootType == RTxxx_uidef.kSecureBootType_PlainUnsigned or \
                   self.secureBootType == RTxxx_uidef.kSecureBootType_PlainCrc:
                    if not self._programXspiNorConfigBlock():
                        self.isXspiNorErasedForImage = False
                        self.isFdcbFromSrcApp = False
                        return False
            imageLoadAddr = self.bootDeviceMemBase + RTxxx_gendef.kBootImageOffset_NOR_SD_EEPROM
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
                status = boot.status.kStatus_Success
            else:
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
            self.isXspiNorErasedForImage = False
            self.isFdcbFromSrcApp = False
            if status != boot.status.kStatus_Success:
                return False
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            imageLoadAddr = self.bootDeviceMemBase + RTxxx_gendef.kBootImageOffset_NOR_SD_EEPROM
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ".." + self.convertLongIntHexText(str(hex(imageLoadAddr + memEraseLen))) + ";\n")
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
            else:
                status, results, cmdStr = self.blhost.flashEraseRegion(imageLoadAddr, memEraseLen, self.bootDeviceMemId)
                self.printLog(cmdStr)
                if status != boot.status.kStatus_Success:
                    return False
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
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

    def _getMcuDeviceFlexcommSpiCfg( self ):
        flexcommSpi = self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpLocation_FlexcommSpiCfg'], '', False)
        return flexcommSpi

    def RTxxx_burnBootDeviceOtps( self ):
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
            pass
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            setFlexcommSpiCfg = 0
            flexcommSpiNorOpt0, flexcommSpiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            # Set Spi Index
            spiIndex = ((flexcommSpiNorOpt0 & 0x00F00000) >> 20)
            setFlexcommSpiCfg = (setFlexcommSpiCfg & (~self.tgt.otpmapDefnDict['kOtpMask_RedundantSpiPort']) | (spiIndex << self.tgt.otpmapDefnDict['kOtpShift_RedundantSpiPort']))
            getFlexcommSpiCfg = self._getMcuDeviceFlexcommSpiCfg()
            if getFlexcommSpiCfg != None:
                destFlexcommSpiCfg = setFlexcommSpiCfg | getFlexcommSpiCfg
                if (destFlexcommSpiCfg & self.tgt.otpmapDefnDict['kOtpMask_RedundantSpiPort']) != setFlexcommSpiCfg:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnOtpError_bootCfg0HasBeenBurned'][self.languageIndex])
                    return False
                else:
                    # We do ^ operation here, because only bit 1 in fuse word will take affect, bit 0 will be bypassed by OCOTP controller
                    destFlexcommSpiCfg = destFlexcommSpiCfg ^ getFlexcommSpiCfg
                    burnResult = self.RTxxx_burnMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpLocation_FlexcommSpiCfg'], destFlexcommSpiCfg)
                    if not burnResult:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnOtpError_failToBurnBootCfg0'][self.languageIndex])
                        return False
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            pass
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            pass
        else:
            pass
        return True

    def RTxxx_resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
