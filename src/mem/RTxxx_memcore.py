#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import boot
import memdef
import RTxxx_memdef
sys.path.append(os.path.abspath(".."))
from fuse import RTxxx_otpcore
from gen import RTxxx_gendef
from ui import RTxxx_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from utils import misc

class secBootRTxxxMem(RTxxx_otpcore.secBootRTxxxOtp):

    def __init__(self, parent):
        RTxxx_otpcore.secBootRTxxxOtp.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_initMem()

    def RTxxx_initMem( self ):

        self.needToShowCfgIntr = None
        self.needToShowImgVerIntr = None
        self.needToShowImageIntr = None
        self.needToShowMbrdptIntr = None
        self._RTxxx_initShowIntr()

    def _RTxxx_initShowIntr( self ):
        self.needToShowCfgIntr = True
        self.needToShowImgVerIntr = True
        self.needToShowImageIntr = True
        self.needToShowMbrdptIntr = True

    def _RTxxx_showUsdhcSdMmcMbrdpt( self ):
        memFilename = 'usdhcSdMmcMbrdpt.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        mbrdptAddr = self.bootDeviceMemBase
        status, results, cmdStr = self.blhost.readMemory(mbrdptAddr, RTxxx_memdef.kMemBlockSize_MBRDPT, memFilename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        readoutMemLen = os.path.getsize(memFilepath)
        memLeft = readoutMemLen
        with open(memFilepath, 'rb') as fileObj:
            while memLeft > 0:
                contentToShow, memContent = self.getOneLineContentToShow(mbrdptAddr, memLeft, fileObj)
                memLeft -= len(memContent)
                mbrdptAddr += len(memContent)
                if self.needToShowMbrdptIntr:
                    self.printMem('----------------------------------MBR&DPT---------------------------------------------', RTxxx_uidef.kMemBlockColor_MBRDPT)
                    self.needToShowMbrdptIntr = False
                self.printMem(contentToShow, RTxxx_uidef.kMemBlockColor_MBRDPT)
        try:
            os.remove(memFilepath)
        except:
            pass
        return True

    def RTxxx_readProgrammedMemoryAndShow( self ):
        if not os.path.isfile(self.destAppFilename):
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
            return
        self.clearMem()

        imageMemBase = 0
        readoutMemLen = 0
        imageFileLen = os.path.getsize(self.destAppFilename)
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            imageMemBase = self.bootDeviceMemBase
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd or \
             self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            self._RTxxx_showUsdhcSdMmcMbrdpt()
            imageMemBase = self.bootDeviceMemBase
        else:
            pass
        readoutMemLen += imageFileLen + self.destAppInitialLoadSize

        memFilename = 'bootableImageFromBootDevice.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        status, results, cmdStr = self.blhost.readMemory(imageMemBase, readoutMemLen, memFilename, self.bootDeviceMemId)
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
                if addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset:
                    self.printMem(contentToShow)
                elif addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen:
                    if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
                       self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
                       self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
                        if self.needToShowCfgIntr:
                            self.printMem('------------------------------------FDCB----------------------------------------------', RTxxx_uidef.kMemBlockColor_FDCB)
                            self.needToShowCfgIntr = False
                        self.printMem(contentToShow, RTxxx_uidef.kMemBlockColor_FDCB)
                    else:
                        self.printMem(contentToShow)
                elif addr <= imageMemBase + memdef.kMemBlockOffset_ImageVersion:
                    self.printMem(contentToShow)
                elif addr <= imageMemBase + memdef.kMemBlockOffset_ImageVersion + len(memContent):
                    if self.flexspiNorImage0Version != None:
                        self.printMem('-------------------------------Image Version------------------------------------------', RTxxx_uidef.kMemBlockColor_ImageVersion)
                        self.needToShowCfgIntr = False
                        self.printMem(contentToShow[0:(14 + memdef.kMemBlockSize_ImageVersion * 3)], RTxxx_uidef.kMemBlockColor_ImageVersion, False)
                        self.printMem(contentToShow[(14 + memdef.kMemBlockSize_ImageVersion * 3):len(contentToShow)])
                    else:
                        self.printMem(contentToShow)
                elif addr <= imageMemBase + self.destAppInitialLoadSize:
                    self.printMem(contentToShow)
                elif addr <= imageMemBase + self.destAppInitialLoadSize + self.destAppBinaryBytes:
                    if self.needToShowImageIntr:
                        self.printMem('-----------------------------------Image----------------------------------------------', RTxxx_uidef.kMemBlockColor_Image)
                        self.needToShowImageIntr = False
                    self.printMem(contentToShow, RTxxx_uidef.kMemBlockColor_Image)
                else:
                    pass
            fileObj.close()
        self._RTxxx_initShowIntr()
        self.tryToSaveImageDataFile(memFilepath)
