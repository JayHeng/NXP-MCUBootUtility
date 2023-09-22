#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import json
import subprocess
import bincopy
import gendef
import LPC_gendef
sys.path.append(os.path.abspath(".."))
from ui import LPC_uicore
from ui import LPC_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from run import rundef
from run import LPC_rundef
from mem import memdef
from mem import LPC_memdef
from utils import elf

class secBootLpcGen(LPC_uicore.secBootLpcUi):

    def __init__(self, parent):
        LPC_uicore.secBootLpcUi.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_initGen()

    def LPC_initGen( self ):
        self.srcAppFilename = None
        self.destAppFilename = os.path.join(self.exeTopRoot, 'gen', 'bootable_image', 'bt_application.bin')

        self.isConvertedAppUsed = False

        self.destAppVectorAddress = 0
        self.destAppVectorOffset = None
        self.destAppBinaryBytes = 0
        self.isXipApp = False

    def _LPC_generatePlainImageBinary( self, binaryArray, appName, startAddress, lengthInByte ):
        destBinAppFilename = os.path.join(self.userFileFolder, appName + gendef.kAppImageFileExtensionList_Bin[0])
        self.srcAppFilename = destBinAppFilename
        with open(self.srcAppFilename, 'wb') as fileObj:
            fileObj.write(binaryArray)
            fileObj.close()
        self.isConvertedAppUsed = True

    def _LPC_getImageInfo( self, srcAppFilename ):
        startAddress = None
        entryPointAddress = None
        lengthInByte = 0
        if os.path.isfile(srcAppFilename):
            appPath, appFilename = os.path.split(srcAppFilename)
            appName, appType = os.path.splitext(appFilename)
            srcAppFilename, appType = self.convertImageFormatToSrec(srcAppFilename, appName, appType)
            isConvSuccessed = False
            if appType.lower() in gendef.kAppImageFileExtensionList_S19:
                try:
                    srecObj = bincopy.BinFile(str(srcAppFilename))
                    startAddress = srecObj.minimum_address
                    entryPointAddress = self.getVal32FromByteArray(srecObj.as_binary(startAddress + 0x4, startAddress  + 0x8))
                    lengthInByte = len(srecObj.as_binary())
                    self._LPC_generatePlainImageBinary(srecObj.as_binary(), appName, startAddress, lengthInByte)
                    isConvSuccessed = True
                except:
                    pass
            else:
                pass
            if not isConvSuccessed:
                startAddress = None
                entryPointAddress = None
                lengthInByte = 0
                self.popupMsgBox(uilang.kMsgLanguageContentDict['genImgError_formatNotValid'][self.languageIndex] + srcAppFilename.encode('utf-8'))
        return startAddress, entryPointAddress, lengthInByte

    def _LPC_isValidNonXipAppImage( self, imageStartAddr ):
        if self.isInTheRangeOfSram(imageStartAddr, 1):
            return True
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['srcImgError_invalidNonXipRange2'][self.languageIndex])
            return False

    def _LPC_isValidAppImage( self, imageStartAddr ):
        if self.isXipApp:
            return True
        else:
            return self._LPC_isValidNonXipAppImage(imageStartAddr)

    def LPC_createFinalBtAppfile( self ):
        self.srcAppFilename = self.getUserAppFilePath()
        imageStartAddr, imageEntryAddr, imageLength = self._LPC_getImageInfo(self.srcAppFilename)
        if imageStartAddr == None or imageEntryAddr == None:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['srcImgError_notFound'][self.languageIndex])
            return False
        self.isXipApp = False
        self.destAppVectorAddress = imageStartAddr
        if self.bootDevice == LPC_uidef.kBootDevice_InternalNor:
            if ((imageStartAddr >= self.tgt.c040hdNorMemBase) and (imageStartAddr < self.tgt.c040hdNorMemBase + LPC_rundef.kBootDeviceMemXipSize_C040hdNor)):
                if (imageStartAddr + imageLength <= self.tgt.c040hdNorMemBase + LPC_rundef.kBootDeviceMemXipSize_C040hdNor):
                    self.isXipApp = True
                    self.destAppVectorOffset = imageStartAddr - self.tgt.c040hdNorMemBase
                else:
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['srcImgError_xipSizeTooLarge'][self.languageIndex] + u"0x%s !" %(LPC_rundef.kBootDeviceMemXipSize_C040hdNor))
                    return False
            else:
                pass
        else:
            pass
        if not self._LPC_isValidAppImage(imageStartAddr):
            return False
        self.destAppBinaryBytes = imageLength
        return True

    def LPC_genBootableImage( self ):
        if self.secureBootType != LPC_uidef.kSecureBootType_PlainUnsigned:
            return False
        else:
            shutil.copy(self.srcAppFilename, self.destAppFilename)
            return True
