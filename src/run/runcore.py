#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gencore
from ui import uidef
from ui import uivar
from ui import uilang

##
# @brief
class secBootRun(gencore.secBootGen):

    def __init__(self, parent):
        gencore.secBootGen.__init__(self, parent)

        self.blhost = None
        self.tgt = None
        self.cpuDir = None
        self.blhostVectorsDir = None

        self.bootDeviceMemId = None
        self.bootDeviceMemBase = None

        self.comMemWriteUnit = 0x1
        self.comMemEraseUnit = 0x1
        self.comMemReadUnit = 0x1

    def showAsOptimalMemoryUnit( self, memSizeBytes ):
        strMemSize = ''
        if memSizeBytes >= 0x40000000:
            strMemSize = str(memSizeBytes * 1.0 / 0x40000000) + ' GB'
        elif memSizeBytes >= 0x100000:
            strMemSize = str(memSizeBytes * 1.0 / 0x100000) + ' MB'
        elif memSizeBytes >= 0x400:
            strMemSize = str(memSizeBytes * 1.0 / 0x400) + ' KB'
        else:
            strMemSize = str(memSizeBytes) + ' Bytes'
        return strMemSize

    def _formatBootloaderVersion( self, version):
        identifier0 = chr((version & 0xff000000) >> 24)
        identifier1 = str((version & 0xff0000) >> 16)
        identifier2 = str((version & 0xff00) >> 8)
        identifier3 = str(version & 0xff)
        return identifier0 + identifier1 + '.' + identifier2 + '.' + identifier3

    def getMcuDeviceBootloaderVersion( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_CurrentVersion)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus('Current Version  = ' + self._formatBootloaderVersion(results[0]))
        else:
            pass
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_TargetVersion)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus('Target Version   = ' + self._formatBootloaderVersion(results[0]))
        else:
            pass

