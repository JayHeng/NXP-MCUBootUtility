#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import MCX_rundef
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import MCX_gencore
from gen import MCX_gendef
from ui import MCX_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from mem import MCX_memdef
from boot import bltest
from boot import target
from utils import misc

def MCX_createTarget(device, exeBinRoot):
    # Build path to target directory and config file.
    cpu = "MCXN947"
    if device in uidef.kMcuDevice_MCX:
        cpu = "MCXN947"
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

class secBootMcxRun(MCX_gencore.secBootMcxGen):

    def __init__(self, parent):
        MCX_gencore.secBootMcxGen.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_initRun()

    def MCX_initRun( self ):
        self.blhost = None
        self.tgt = None
        self.cpuDir = None
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost2_6', 'win', 'vectors')

        self.MCX_isDeviceEnabledToOperate = True
        self.bootDeviceMemId = 0
        self.bootDeviceMemBase = None

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

        self.MCX_createMcuTarget()

    def MCX_createMcuTarget( self ):
        self.tgt, self.cpuDir = MCX_createTarget(self.mcuDevice, self.exeBinRoot)

    def MCX_getUsbid( self ):
        self.MCX_createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def MCX_connectToDevice( self , connectStage):
        if connectStage == uidef.kConnectStage_Rom:
            # Create the target object.
            self.MCX_createMcuTarget()
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
                usbVid = self.tgt.romUsbVid
                usbPid = self.tgt.romUsbPid
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

    def MCX_pingRom( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def _MCX_getMcuDeviceIds( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_SystemDeviceIdent)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("SYSCON->DEVICE_ID0 = " + self.convertLongIntHexText(str(hex(results[0]))))
        else:
            pass
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_UniqueDeviceIdent)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("UUID0 = " + self.convertLongIntHexText(str(hex(results[0]))))
            self.printDeviceStatus("UUID1 = " + self.convertLongIntHexText(str(hex(results[1]))))
            self.printDeviceStatus("UUID2 = " + self.convertLongIntHexText(str(hex(results[2]))))
            self.printDeviceStatus("UUID3 = " + self.convertLongIntHexText(str(hex(results[3]))))
        else:
            pass

    def MCX_getMcuDeviceInfoViaRom( self ):
        self.printDeviceStatus("----------MCU ROM info-----------")
        self.getMcuDeviceBootloaderVersion()
        self._MCX_getMcuDeviceIds()

    def _MCX_getFtfxFlashProperties( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_FlashSectorSize)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("Sector Size = " + self.showAsOptimalMemoryUnit(results[0]))
            self.comMemEraseUnit = results[0]
        else:
            pass
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_FlashSizeInBytes)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("Total Size = " + self.showAsOptimalMemoryUnit(results[0]))
        else:
            pass

    def MCX_getBootDeviceInfoViaRom ( self ):
        if self.bootDevice == MCX_uidef.kBootDevice_InternalNor:
            self.printDeviceStatus("-------On-chip NOR memory------")
            self._MCX_getFtfxFlashProperties()
        else:
            pass

    def _MCX_prepareForBootDeviceOperation ( self ):
        if self.bootDevice == MCX_uidef.kBootDevice_InternalNor:
            self.bootDeviceMemBase = self.tgt.c040hdNorMemBase
        else:
            pass

    def _eraseFtfxNorForImageLoading( self ):
        imageLen = os.path.getsize(self.destAppFilename)
        memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
        status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.c040hdNorMemBase, memEraseLen)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def MCX_flashBootableImage ( self ):
        self._MCX_prepareForBootDeviceOperation()
        imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == MCX_uidef.kBootDevice_InternalNor:
            if not self._eraseFtfxNorForImageLoading():
                return False
            if self.secureBootType == MCX_uidef.kSecureBootType_PlainUnsigned:
                pass
            imageLoadAddr = self.bootDeviceMemBase
            status, results, cmdStr = self.blhost.writeMemory(imageLoadAddr, self.destAppFilename)
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

    def MCX_resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
