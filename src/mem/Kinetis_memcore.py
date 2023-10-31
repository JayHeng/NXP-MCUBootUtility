#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import boot
import memdef
import Kinetis_memdef
sys.path.append(os.path.abspath(".."))
from run import Kinetis_runcore
from gen import Kinetis_gendef
from ui import Kinetis_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from utils import misc

class secBootKinetisMem(Kinetis_runcore.secBootKinetisRun):

    def __init__(self, parent):
        Kinetis_runcore.secBootKinetisRun.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_initMem()

    def Kinetis_initMem( self ):

        self.needToShowBcaIntr = None
        self.needToShowFcfIntr = None
        self.needToShowImageIntr = None
        self._Kinetis_initShowIntr()

    def _Kinetis_initShowIntr( self ):
        self.needToShowBcaIntr = True
        self.needToShowFcfIntr = True
        self.needToShowImageIntr = True

    def Kinetis_readProgrammedMemoryAndShow( self ):
        if not os.path.isfile(self.destAppFilename):
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
            return
        self.clearMem()

        imageMemBase = 0
        readoutMemLen = 0
        imageFileLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
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
                if addr <= imageMemBase + Kinetis_memdef.kMemBlockOffset_BCA:
                    if self.needToShowImageIntr:
                        self.printMem('-----------------------------------Image----------------------------------------------', Kinetis_uidef.kMemBlockColor_Image)
                        self.needToShowImageIntr = False
                    self.printMem(contentToShow, Kinetis_uidef.kMemBlockColor_Image)
                elif addr <= imageMemBase + Kinetis_memdef.kMemBlockOffset_BCA + Kinetis_memdef.kMemBlockSize_BCA:
                    if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
                        if self.needToShowBcaIntr:
                            self.printMem('-------------------------------------BCA----------------------------------------------', Kinetis_uidef.kMemBlockColor_BCA)
                            self.needToShowBcaIntr = False
                        self.printMem(contentToShow, Kinetis_uidef.kMemBlockColor_BCA)
                    else:
                        self.printMem(contentToShow)
                elif addr <= imageMemBase + Kinetis_memdef.kMemBlockOffset_FCF + Kinetis_memdef.kMemBlockSize_FCF:
                    if self.bootDevice == Kinetis_uidef.kBootDevice_InternalNor:
                        if self.needToShowFcfIntr:
                            self.printMem('-------------------------------------FCF----------------------------------------------', Kinetis_uidef.kMemBlockColor_FCF)
                            self.needToShowFcfIntr = False
                        self.printMem(contentToShow, Kinetis_uidef.kMemBlockColor_FCF)
                    else:
                        self.printMem(contentToShow)
                elif addr <= imageMemBase + self.destAppBinaryBytes:
                    self.printMem(contentToShow, Kinetis_uidef.kMemBlockColor_Image)
                else:
                    pass

            fileObj.close()
        self._Kinetis_initShowIntr()
        self.tryToSaveImageDataFile(memFilepath)
