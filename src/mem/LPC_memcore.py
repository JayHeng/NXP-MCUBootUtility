#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import boot
import memdef
import LPC_memdef
sys.path.append(os.path.abspath(".."))
from run import LPC_runcore
from gen import LPC_gendef
from ui import LPC_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from utils import misc

class secBootLpcMem(LPC_runcore.secBootLpcRun):

    def __init__(self, parent):
        LPC_runcore.secBootLpcRun.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_initMem()

    def LPC_initMem( self ):
        self.needToShowImageIntr = None
        self._LPC_initShowIntr()

    def _LPC_initShowIntr( self ):
        self.needToShowImageIntr = True

    def LPC_readProgrammedMemoryAndShow( self ):
        if not os.path.isfile(self.destAppFilename):
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
            return
        self.clearMem()

        imageMemBase = 0
        readoutMemLen = 0
        imageFileLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == LPC_uidef.kBootDevice_InternalNor:
            imageMemBase = self.bootDeviceMemBase
        else:
            pass
        readoutMemLen += imageFileLen

        memFilename = 'bootableImageFromBootDevice.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        status, results, cmdStr = self.blhost.readMemory(imageMemBase, readoutMemLen, memFilename)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False

        readoutMemLen = os.path.getsize(memFilepath)
        memLeft = readoutMemLen
        addr = imageMemBase
        with open(memFilepath, 'rb') as fileObj:
            while memLeft > 0:
                contentToShow, memContent = self.getOneLineContentToShow(addr, memLeft, fileObj)
                memLeft -= len(memContent)
                addr += len(memContent)
                if addr <= imageMemBase + self.destAppBinaryBytes:
                    if self.needToShowImageIntr:
                        self.printMem('-----------------------------------Image----------------------------------------------', LPC_uidef.kMemBlockColor_Image)
                        self.needToShowImageIntr = False
                    self.printMem(contentToShow, LPC_uidef.kMemBlockColor_Image)
                else:
                    pass

            fileObj.close()
        self._LPC_initShowIntr()
        self.tryToSaveImageDataFile(memFilepath)
