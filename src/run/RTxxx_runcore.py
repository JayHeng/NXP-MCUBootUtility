#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import RTxxx_rundef
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gendef
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
    elif device == uidef.kMcuDevice_iMXRT700:
        cpu = "MIMXRT798"
    elif device == uidef.kMcuDevice_RW612:
        cpu = "RW612"
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
        if self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
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
        self.isFlexspiNandBlockAddr = None

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

        self.RTxxx_createMcuTarget()

    def RTxxx_createMcuTarget( self ):
        self.tgt, self.cpuDir = RTxxx_createTarget(self.mcuDevice, self.exeBinRoot)

    def RTxxx_updateFlexspiNorMemBase( self ):
        # Set main flexspi nor XIP region
        if self.flexspiBootInstance == 0:
            self.tgt.flexspiNorMemBase = self.tgt.flexspiNorMemBase0
        elif self.flexspiBootInstance == 1:
            self.tgt.flexspiNorMemBase = self.tgt.flexspiNorMemBase1
        else:
            pass

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
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG0'], '(otp) BOOT_CFG0')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG1'], '(otp) BOOT_CFG1')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG2'], '(otp) BOOT_CFG2')
        self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict['kOtpIndex_BOOT_CFG3'], '(otp) BOOT_CFG3')

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
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        flexspiTag = self.getVal32FromBinFile(filepath, rundef.kFlexspiNorCfgOffset_FlexspiTag)
        xspiTag = self.getVal32FromBinFile(filepath, rundef.kXspiNorCfgOffset_XspiTag)
        if flexspiTag == rundef.kFlexspiNorCfgTag_Flexspi or \
           xspiTag == rundef.kXspiNorCfgTag_Xspi:
            xspiNorCfgOffset_PageByteSize = 0
            xspiNorCfgOffset_SectorByteSize = 0
            xspiNorCfgOffset_BlockByteSize = 0
            if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
                xspiNorCfgOffset_PageByteSize = rundef.kFlexspiNorCfgOffset_PageByteSize
                xspiNorCfgOffset_SectorByteSize = rundef.kFlexspiNorCfgOffset_SectorByteSize
                xspiNorCfgOffset_BlockByteSize = rundef.kFlexspiNorCfgOffset_BlockByteSize
            elif self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
                xspiNorCfgOffset_PageByteSize = rundef.kXspiNorCfgOffset_PageByteSize
                xspiNorCfgOffset_SectorByteSize = rundef.kXspiNorCfgOffset_SectorByteSize
                xspiNorCfgOffset_BlockByteSize = rundef.kXspiNorCfgOffset_BlockByteSize
            pageByteSize = self.getVal32FromBinFile(filepath, xspiNorCfgOffset_PageByteSize)
            sectorByteSize = self.getVal32FromBinFile(filepath, xspiNorCfgOffset_SectorByteSize)
            blockByteSize = self.getVal32FromBinFile(filepath, xspiNorCfgOffset_BlockByteSize)
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
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
                self.printDeviceStatus("--------FlexSPI NOR memory--------")
            elif self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
                self.printDeviceStatus("--------QuadSPI NOR memory--------")
            elif self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
                self.printDeviceStatus("----------XSPI NOR memory---------")
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
            self.getUsdhcSdMmcDeviceInfo()
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            self.printDeviceStatus("--------uSDHC MMC Card info-------")
            self.getUsdhcSdMmcDeviceInfo()
        else:
            pass

    def _RTxxx_prepareForBootDeviceOperation ( self ):
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_FlexspiNor
            self.bootDeviceMemBase = self.tgt.flexspiNorMemBase
        elif self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_QuadspiNor
            self.bootDeviceMemBase = self.tgt.quadspiNorMemBase
        elif self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            self.bootDeviceMemId = rundef.kBootDeviceMemId_XspiNor
            self.bootDeviceMemBase = self.tgt.flexspiNorMemBase
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
        status, results, cmdStr = self.blhost.readMemory(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, filename, self.bootDeviceMemId)
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

    def _eraseXspiNorForConfigBlockLoading( self ):
        status = boot.status.kStatus_Success
        if self.RTxxx_isDeviceEnabledToOperate:
            if not self._isXspiNorConfigBlockRegionBlank():
                if self.bootDeviceMemId == rundef.kBootDeviceMemId_FlexspiNor or \
                   self.bootDeviceMemId == rundef.kBootDeviceMemId_XspiNor:
                    status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, self.bootDeviceMemId)
                elif self.bootDeviceMemId == rundef.kBootDeviceMemId_QuadspiNor:
                    status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.quadspiNorMemBase + self.tgt.xspiNorCfgInfoOffset, self.tgt.xspiNorCfgInfoLen, rundef.kBootDeviceMemId_QuadspiNor)
                else:
                    pass
                self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset))) + ".." + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen))) + ";\n")
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
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCfgBlock, 0x4, rundef.kFlexspiNorCfgInfo_Notify)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(rundef.kFlexspiNorCfgInfo_Notify))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCfgBlock))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCfgBlock)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCfgBlock))) + ";\n")
        if self.isSbFileEnabledToGen:
            return True
        else:
            return (status == boot.status.kStatus_Success)

    def RTxxx_setFlexspiInstance( self ):
        if self.mcuDevice == uidef.kMcuDevice_iMXRT700:
            # In RT700 flashloader, 0xFC900000/0xFC900001 is used to switch XSPI0/1 instance
            #  0xFC900000 -> Primary instance
            #  0xFC900001 -> Secondary instance
            configOpt = rundef.kXspiDevCfgInfo_Instance + self.flexspiBootInstance
            status = boot.status.kStatus_Success
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt, 0x4, configOpt)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(configOpt))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCommOpt)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
        else:
            pass

    def RTxxx_configureBootDevice ( self ):
        self._RTxxx_prepareForBootDeviceOperation()
        flexspiNorDeviceModel = None
        configOptList = []
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            self.getFlexspiBootInstance()
            self.RTxxx_updateFlexspiNorMemBase()
            flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(uidef.kBootDevice_XspiNor)
            configOptList.extend([flexspiNorOpt0, flexspiNorOpt1])
            self.RTxxx_setFlexspiInstance()
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            flexcommSpiNorOpt0, flexcommSpiNorOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([flexcommSpiNorOpt0, flexcommSpiNorOpt1])
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            usdhcSdOpt = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([usdhcSdOpt])
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            usdhcMmcOpt0, usdhcMmcOpt1 = uivar.getBootDeviceConfiguration(self.bootDevice)
            configOptList.extend([usdhcMmcOpt0, usdhcMmcOpt1])
        else:
            pass
        self._RTxxx_prepareForBootDeviceOperation()
        status = boot.status.kStatus_Success
        if flexspiNorDeviceModel == uidef.kFlexspiNorDevice_FDCB:
            if self.RTxxx_isDeviceEnabledToOperate:
                status, results, cmdStr = self.blhost.writeMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt, self.cfgFdcbBinFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " cfgFdcbBinFile > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
            if status != boot.status.kStatus_Success:
                return False
        else:
            for i in range(len(configOptList)):
                if self.RTxxx_isDeviceEnabledToOperate:
                    status, results, cmdStr = self.blhost.fillMemory(self.tgt.ramFreeSpaceStart_LoadCommOpt + 4 * i, 0x4, configOptList[i])
                    self.printLog(cmdStr)
                if self.isSbFileEnabledToGen:
                    self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(configOptList[i]))) + " > " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt + 4 * i))) + ";\n")
                if status != boot.status.kStatus_Success:
                    return False
        if self.RTxxx_isDeviceEnabledToOperate:
            status, results, cmdStr = self.blhost.configureMemory(self.bootDeviceMemId, self.tgt.ramFreeSpaceStart_LoadCommOpt)
            self.printLog(cmdStr)
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    enable " + self.sbEnableBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.ramFreeSpaceStart_LoadCommOpt))) + ";\n")
        if status != boot.status.kStatus_Success:
            return False
        return True

    def _eraseXspiNorForImageLoading( self ):
        imageLen = os.path.getsize(self.destAppFilename)
        imageLen += self.tgt.xspiNorImgHdrOffset
        memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
        status = None
        cmdStr = ''
        if self.isSbFileEnabledToGen:
            self._RTxxx_addFlashActionIntoSbAppBdContent("    erase " + self.sbAccessBootDeviceMagic + " " + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase))) + ".." + self.convertLongIntHexText(str(hex(self.tgt.flexspiNorMemBase + memEraseLen))) + ";\n")
        else:
            if self.bootDeviceMemId == rundef.kBootDeviceMemId_FlexspiNor or \
               self.bootDeviceMemId == rundef.kBootDeviceMemId_XspiNor:
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
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            image0Size = 0
            if not self.isXspiNorErasedForImage:
                if not self._eraseXspiNorForImageLoading():
                    return False
                if self.secureBootType == RTxxx_uidef.kSecureBootType_PlainUnsigned or \
                   self.secureBootType == RTxxx_uidef.kSecureBootType_PlainCrc:
                    if not self._programXspiNorConfigBlock():
                        self.isXspiNorErasedForImage = False
                        self.isFdcbFromSrcApp = False
                        return False
            flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
            if self.tgt.hasFlexspiNorDualImageBoot and ((flexspiNorDualImageInfoList[2] & 0xFFFF) != 0):
                if flexspiNorDualImageInfoList[0] == 0xffffffff:
                    self.flexspiNorImage0Version = flexspiNorDualImageInfoList[0]
                else:
                    self.flexspiNorImage0Version = flexspiNorDualImageInfoList[0] + ((flexspiNorDualImageInfoList[0] ^ 0xFFFF) << 16)
            if self.flexspiNorImage0Version != None and self.flexspiNorImage0Version != rundef.kFlexspiNorContent_Blank32:
                versionLoadAddr = self.bootDeviceMemBase + gendef.kImgVerOffset_NOR
                if self.isSbFileEnabledToGen:
                    self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.convertLongIntHexText(str(hex(self.flexspiNorImage0Version))) + " > " + self.convertLongIntHexText(str(hex(versionLoadAddr))) + ";\n")
                    status = boot.status.kStatus_Success
                else:
                    status, results, cmdStr = self.blhost.fillMemory(versionLoadAddr, 0x4, self.flexspiNorImage0Version)
                    self.printLog(cmdStr)
            imageLoadAddr = self.bootDeviceMemBase + self.tgt.xspiNorImgHdrOffset
            if self.isSbFileEnabledToGen:
                self._RTxxx_addFlashActionIntoSbAppBdContent("    load " + self.sbAccessBootDeviceMagic + " myBinFile > " + self.convertLongIntHexText(str(hex(imageLoadAddr))) + ";\n")
                status = boot.status.kStatus_Success
            else:
                status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename, self.bootDeviceMemId)
                self.printLog(cmdStr)
            image0Size = imageLoadAddr - self.bootDeviceMemBase + os.path.getsize(self.destAppFilename)
            self.isXspiNorErasedForImage = False
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
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            imageLoadAddr = self.bootDeviceMemBase + self.destAppInitialLoadSize
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
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd or \
             self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
            imageLoadAddr = self.bootDeviceMemBase + self.destAppInitialLoadSize
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

    def _burnCommonMcuOtpBits( self, otpIndexStr, otpMaskStr, otpShiftStr, setOtpBits ):
            getOtpWord = self.RTxxx_readMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict[otpIndexStr], '', False)
            getOtpBits = (getOtpWord & self.tgt.otpmapDefnDict[otpMaskStr]) >> self.tgt.otpmapDefnDict[otpShiftStr]
            if setOtpBits != getOtpBits:
                if getOtpBits != 0:
                    return False
                setOtpWord = (getOtpWord & (~self.tgt.otpmapDefnDict[otpMaskStr]) | (setOtpBits << self.tgt.otpmapDefnDict[otpShiftStr]))
                burnResult = self.RTxxx_burnMcuDeviceOtpByBlhost(self.tgt.otpmapIndexDict[otpIndexStr], setOtpWord)
                return burnResult 
            else:
                return True

    def RTxxx_burnBootDeviceOtps( self ):
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            if self.tgt.hasFlexspiNorDualImageBoot:
                flexspiNorOpt0, flexspiNorOpt1, flexspiNorDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
                flexspiNorImage1Offset = (flexspiNorDualImageInfoList[2] & 0xFFFF)
                flexspiNorImage1Size = ((flexspiNorDualImageInfoList[2] >> 16) & 0xFFFF)
                if flexspiNorImage1Offset != 0:
                    if not self._burnCommonMcuOtpBits('kOtpLocation_FlexspiNorDualImageBootCfg3', 'kOtpMask_FlexspiNorImage1Offset', 'kOtpShift_FlexspiNorImage1Offset', flexspiNorImage1Offset):
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnOtpError_failToBurnDualImageBootCfg3'][self.languageIndex])
                        return False
                    if not self._burnCommonMcuOtpBits('kOtpLocation_FlexspiNorDualImageBootCfg2', 'kOtpMask_FlexspiNorImage1Size', 'kOtpShift_FlexspiNorImage1Size', flexspiNorImage1Size):
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['burnOtpError_failToBurnDualImageBootCfg2'][self.languageIndex])
                        return False
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
