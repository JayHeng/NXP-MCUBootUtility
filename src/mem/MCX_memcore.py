#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import boot
import memdef
import MCX_memdef
sys.path.append(os.path.abspath(".."))
from run import MCX_runcore
from gen import MCX_gendef
from ui import MCX_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from utils import misc

class secBootMcxMem(MCX_runcore.secBootMcxRun):

    def __init__(self, parent):
        MCX_runcore.secBootMcxRun.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_initMem()

    def MCX_initMem( self ):

        self.needToShowBcaIntr = None
        self.needToShowFcfIntr = None
        self.needToShowImageIntr = None
        self._MCX_initShowIntr()

    def _MCX_initShowIntr( self ):
        self.needToShowBcaIntr = True
        self.needToShowFcfIntr = True
        self.needToShowImageIntr = True

    def MCX_readProgrammedMemoryAndShow( self ):
        if not os.path.isfile(self.destAppFilename):
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
            return
        self.clearMem()

        imageMemBase = 0
        readoutMemLen = 0
        imageFileLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == MCX_uidef.kBootDevice_InternalNor:
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
                        self.printMem('-----------------------------------Image----------------------------------------------', MCX_uidef.kMemBlockColor_Image)
                        self.needToShowImageIntr = False
                    self.printMem(contentToShow, MCX_uidef.kMemBlockColor_Image)
                else:
                    pass

            fileObj.close()
        self._MCX_initShowIntr()
        self.tryToSaveImageDataFile(memFilepath)
