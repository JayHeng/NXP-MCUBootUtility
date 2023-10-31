#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import math
import Kinetis_rundef
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import Kinetis_gencore
from gen import Kinetis_gendef
from ui import Kinetis_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from mem import Kinetis_memdef
from boot import bltest
from boot import target
from utils import misc

def Kinetis_createTarget(device, exeBinRoot):
    # Build path to target directory and config file.
    cpu = "MKxx"
    if device in uidef.kMcuDevice_Kinetis or device in uidef.kMcuDevice_Kinetis_sub:
        cpu = "MKxx"
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

class secBootKinetisRun(Kinetis_gencore.secBootKinetisGen):

    def __init__(self, parent):
        Kinetis_gencore.secBootKinetisGen.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_initRun()

    def Kinetis_initRun( self ):
        self.blhost = None
        self.tgt = None
        self.cpuDir = None
        self.blhostVectorsDir = os.path.join(self.exeTopRoot, 'tools', 'blhost2_3', 'win', 'vectors')

        self.Kinetis_isDeviceEnabledToOperate = True
        self.bootDeviceMemId = 0
        self.bootDeviceMemBase = None

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

        self.Kinetis_createMcuTarget()

    def Kinetis_createMcuTarget( self ):
        self.tgt, self.cpuDir = Kinetis_createTarget(self.mcuDevice, self.exeBinRoot)

    def Kinetis_getUsbid( self ):
        self.Kinetis_createMcuTarget()
        return [self.tgt.romUsbVid, self.tgt.romUsbPid, self.tgt.flashloaderUsbVid, self.tgt.flashloaderUsbPid]

    def Kinetis_connectToDevice( self , connectStage):
        if connectStage == uidef.kConnectStage_Rom:
            # Create the target object.
            self.Kinetis_createMcuTarget()
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

    def Kinetis_pingRom( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def _Kinetis_getMcuDeviceIds( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_SystemDeviceIdent)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("SIM->SDID = " + self.convertLongIntHexText(str(hex(results[0]))))
        else:
            pass
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_UniqueDeviceIdent)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus("SIM->UIDL  = " + self.convertLongIntHexText(str(hex(results[0]))))
            self.printDeviceStatus("SIM->UIDML = " + self.convertLongIntHexText(str(hex(results[1]))))
            self.printDeviceStatus("SIM->UIDMH = " + self.convertLongIntHexText(str(hex(results[2]))))
            try:
                self.printDeviceStatus("SIM->UIDH  = " + self.convertLongIntHexText(str(hex(results[3]))))
            except:
                pass
        else:
            pass

    def Kinetis_getMcuDeviceInfoViaRom( self ):
        self.printDeviceStatus("----------MCU ROM info-----------")
        self.getMcuDeviceBootloaderVersion()
        self._Kinetis_getMcuDeviceIds()

    def _Kinetis_getFtfxFlashProperties( self ):
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

    def Kinetis_getBootDeviceInfoViaRom ( self ):
        if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
            self.printDeviceStatus("-------On-chip NOR memory------")
            self._Kinetis_getFtfxFlashProperties()
        else:
            pass

    def _Kinetis_prepareForBootDeviceOperation ( self ):
        if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
            self.bootDeviceMemBase = self.tgt.ftfxNorMemBase
        else:
            pass

    def _eraseFtfxNorForImageLoading( self ):
        imageLen = os.path.getsize(self.destAppFilename)
        memEraseLen = misc.align_up(imageLen, self.comMemEraseUnit)
        status, results, cmdStr = self.blhost.flashEraseRegion(self.tgt.ftfxNorMemBase, memEraseLen)
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)

    def Kinetis_flashBootableImage ( self ):
        self._Kinetis_prepareForBootDeviceOperation()
        imageLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
            if not self._eraseFtfxNorForImageLoading():
                return False
            if self.secureBootType == Kinetis_uidef.kSecureBootType_PlainUnsigned:
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

    def Kinetis_resetMcuDevice( self ):
        status, results, cmdStr = self.blhost.reset()
        self.printLog(cmdStr)
        return (status == boot.status.kStatus_Success)
