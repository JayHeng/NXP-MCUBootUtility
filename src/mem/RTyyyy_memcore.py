#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import boot
import memdef
import RTyyyy_memdef
sys.path.append(os.path.abspath(".."))
from fuse import RTyyyy_fusecore
from run import RTyyyy_rundef
from ui import RTyyyy_uidef
from gen import gendef
from gen import RTyyyy_gendef
from ui import uidef
from ui import uiheader
from ui import uivar
from ui import uilang
from utils import misc

class secBootRTyyyyMem(RTyyyy_fusecore.secBootRTyyyyFuse):

    def __init__(self, parent):
        RTyyyy_fusecore.secBootRTyyyyFuse.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_initMem()

    def RTyyyy_initMem( self ):

        self.needToShowHwCryptoKeyBlobIntr = None
        self.needToShowCfgIntr = None
        self.needToShowEkib0Intr = None
        self.needToShowEprdb0Intr = None
        self.needToShowEkib1Intr = None
        self.needToShowEprdb1Intr = None
        self.needToShowImgVerIntr = None
        self.needToShowIvtIntr = None
        self.needToShowBootDataIntr = None
        self.needToShowDcdIntr = None
        self.needToShowXmcdIntr = None
        self.needToShowImageIntr = None
        self.needToShowCsfIntr = None
        self.needToShowHabKeyBlobIntr = None
        self.needToShowNfcbIntr = None
        self.needToShowDbbtIntr = None
        self.needToShowMbrdptIntr = None

        self.needToShowContainerHdrIntr = None
        self.needToShowImageEntryIntr = None
        self.needToShowEdgelockContainerIntr = None
        self.needToShowEdgelockFwIntr = None
        self._RTyyyy_initShowIntr()

    def _RTyyyy_initShowIntr( self ):
        self.needToShowHwCryptoKeyBlobIntr = True
        self.needToShowCfgIntr = True
        self.needToShowEkib0Intr = True
        self.needToShowEprdb0Intr = True
        self.needToShowEkib1Intr = True
        self.needToShowEprdb1Intr = True
        self.needToShowImgVerIntr = True
        self.needToShowIvtIntr = True
        self.needToShowBootDataIntr = True
        self.needToShowDcdIntr = True
        self.needToShowXmcdIntr = True
        self.needToShowImageIntr = True
        self.needToShowCsfIntr = True
        self.needToShowHabKeyBlobIntr = True
        self.needToShowNfcbIntr = True
        self.needToShowDbbtIntr = True
        self.needToShowMbrdptIntr = True
        self.needToShowContainerHdrIntr = True
        self.needToShowImageEntryIntr = True
        self.needToShowEdgelockContainerIntr = True
        self.needToShowEdgelockFwIntr = True

    def _getCsfBlockInfo( self ):
        self.destAppCsfAddress = self.getVal32FromBinFile(self.destAppFilename, self.destAppIvtOffset + RTyyyy_memdef.kMemberOffsetInIvt_Csf)

    def _getInfoFromIvt( self ):
        self._getCsfBlockInfo()

    def _getDcdInfo( self ):
        dcdCtrlDict, dcdSettingsDict = uivar.getBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_Dcd)
        if dcdCtrlDict['isDcdEnabled']:
            self.destAppDcdLength = os.path.getsize(self.dcdBinFilename)
        else:
            pass

    def _showNandFcb( self, ipTypeStr, fingerprintOffset, fingerprintValue, ipTagOffset, ipTagValue, dbbtOffset ):
        memFilename = ipTypeStr + 'NandFcb.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        nfcbAddr = self.bootDeviceMemBase
        dbbtAddr = 0
        status, results, cmdStr = self.blhost.readMemory(nfcbAddr, RTyyyy_memdef.kMemBlockSize_NFCB, memFilename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False, 0
        readoutMemLen = os.path.getsize(memFilepath)
        memLeft = readoutMemLen
        with open(memFilepath, 'rb') as fileObj:
            while memLeft > 0:
                contentToShow, memContent = self.getOneLineContentToShow(nfcbAddr, memLeft, fileObj)
                memLeft -= len(memContent)
                nfcbAddr += len(memContent)
                if self.needToShowNfcbIntr:
                    self.printMem('------------------------------------NFCB----------------------------------------------', RTyyyy_uidef.kMemBlockColor_NFCB)
                    self.needToShowNfcbIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_NFCB)
        fingerprint = self.getVal32FromBinFile(memFilepath, fingerprintOffset)
        ipTag = self.getVal32FromBinFile(memFilepath, ipTagOffset)
        if fingerprint == fingerprintValue and ipTag == ipTagValue:
            dbbtStartPage = self.getVal32FromBinFile(memFilepath, dbbtOffset)
            dbbtAddr = self.bootDeviceMemBase + dbbtStartPage * self.comMemReadUnit
        else:
            return False, 0
        try:
            os.remove(memFilepath)
        except:
            pass
        return True, dbbtAddr

    def _showNandDbbt( self, ipTypeStr, dbbtAddr ):
        memFilename = ipTypeStr + 'NandDbbt.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        if ((self.isFlexspiNandBlockAddr != None) and self.isFlexspiNandBlockAddr):
            dbbtBlockIndex = dbbtAddr / self.flexspiNandBlockSize
            status, results, cmdStr = self.blhost.readMemory(dbbtBlockIndex, RTyyyy_memdef.kMemBlockSize_DBBT, memFilename, self.bootDeviceMemId)
        else:
            status, results, cmdStr = self.blhost.readMemory(dbbtAddr, RTyyyy_memdef.kMemBlockSize_DBBT, memFilename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        readoutMemLen = os.path.getsize(memFilepath)
        memLeft = readoutMemLen
        with open(memFilepath, 'rb') as fileObj:
            while memLeft > 0:
                contentToShow, memContent = self.getOneLineContentToShow(dbbtAddr, memLeft, fileObj)
                memLeft -= len(memContent)
                dbbtAddr += len(memContent)
                if self.needToShowDbbtIntr:
                    self.printMem('------------------------------------DBBT----------------------------------------------', RTyyyy_uidef.kMemBlockColor_DBBT)
                    self.needToShowDbbtIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_DBBT)
        try:
            os.remove(memFilepath)
        except:
            pass
        return True

    def _RTyyyy_showUsdhcSdMmcMbrdpt( self ):
        memFilename = 'usdhcSdMmcMbrdpt.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        mbrdptAddr = self.bootDeviceMemBase
        status, results, cmdStr = self.blhost.readMemory(mbrdptAddr, RTyyyy_memdef.kMemBlockSize_MBRDPT, memFilename, self.bootDeviceMemId)
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
                    self.printMem('----------------------------------MBR&DPT---------------------------------------------', RTyyyy_uidef.kMemBlockColor_MBRDPT)
                    self.needToShowMbrdptIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_MBRDPT)
        try:
            os.remove(memFilepath)
        except:
            pass
        return True

    def _showOneLineContentForIvtType( self, addr, imageMemBase, contentToShow, memContent ):
        if (self.isXipableDevice and addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset):
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_OtfadCrypto:
                keyBlobStart = imageMemBase + RTyyyy_memdef.kMemBlockOffset_HwCryptoKeyBlob
                if addr > keyBlobStart and addr <= keyBlobStart + RTyyyy_memdef.kMemBlockSize_HwCryptoKeyBlob:
                    if self.needToShowHwCryptoKeyBlobIntr:
                        self.printMem('-----------------------------OTFAD DEK KeyBlob----------------------------------------', RTyyyy_uidef.kMemBlockColor_HwCryptoKeyBlob)
                        self.needToShowHwCryptoKeyBlobIntr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_HwCryptoKeyBlob)
                else:
                    self.printMem(contentToShow)
            else:
                self.printMem(contentToShow)
        elif (self.isXipableDevice and addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen):
            if not self.isSdmmcCard:
                if self.needToShowCfgIntr:
                    self.printMem('------------------------------------FDCB----------------------------------------------', RTyyyy_uidef.kMemBlockColor_FDCB)
                    self.needToShowCfgIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_FDCB)
            else:
                if addr >= self.bootDeviceMemBase + RTyyyy_memdef.kMemBlockSize_MBRDPT:
                    self.printMem(contentToShow)
        elif (self.isXipableDevice and addr <= imageMemBase + memdef.kMemBlockOffset_ImageVersion):
            self.printMem(contentToShow)
        elif (self.isXipableDevice and addr <= imageMemBase + memdef.kMemBlockOffset_ImageVersion + len(memContent)):
            if self.flexspiNorImage0Version != None:
                self.printMem('-------------------------------Image Version------------------------------------------', RTyyyy_uidef.kMemBlockColor_ImageVersion)
                self.needToShowCfgIntr = False
                self.printMem(contentToShow[0:(14 + memdef.kMemBlockSize_ImageVersion * 3)], RTyyyy_uidef.kMemBlockColor_ImageVersion, False)
                self.printMem(contentToShow[(14 + memdef.kMemBlockSize_ImageVersion * 3):len(contentToShow)])
            else:
                self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppIvtOffset:
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_BeeCrypto:
                ekib0Start = imageMemBase + RTyyyy_memdef.kMemBlockOffset_EKIB0
                eprdb0Start = imageMemBase + RTyyyy_memdef.kMemBlockOffset_EPRDB0
                ekib1Start = imageMemBase + RTyyyy_memdef.kMemBlockOffset_EKIB1
                eprdb1Start = imageMemBase + RTyyyy_memdef.kMemBlockOffset_EPRDB1
                if addr > ekib0Start and addr <= ekib0Start + RTyyyy_memdef.kMemBlockSize_EKIB:
                    if self.needToShowEkib0Intr:
                        self.printMem('-----------------------------------EKIB0----------------------------------------------', RTyyyy_uidef.kMemBlockColor_EKIB)
                        self.needToShowEkib0Intr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EKIB)
                elif addr > eprdb0Start and addr <= eprdb0Start + RTyyyy_memdef.kMemBlockSize_EPRDB:
                    if self.needToShowEprdb0Intr:
                        self.printMem('-----------------------------------EPRDB0---------------------------------------------', RTyyyy_uidef.kMemBlockColor_EPRDB)
                        self.needToShowEprdb0Intr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EPRDB)
                elif addr > ekib1Start and addr <= ekib1Start + RTyyyy_memdef.kMemBlockSize_EKIB:
                    if self.needToShowEkib1Intr:
                        self.printMem('-----------------------------------EKIB1----------------------------------------------', RTyyyy_uidef.kMemBlockColor_EKIB)
                        self.needToShowEkib1Intr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EKIB)
                elif addr > eprdb1Start and addr <= eprdb1Start + RTyyyy_memdef.kMemBlockSize_EPRDB:
                    if self.needToShowEprdb1Intr:
                        self.printMem('-----------------------------------EPRDB1---------------------------------------------', RTyyyy_uidef.kMemBlockColor_EPRDB)
                        self.needToShowEprdb1Intr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EPRDB)
                else:
                    self.printMem(contentToShow)
            else:
                self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockSize_IVT:
            if self.needToShowIvtIntr:
                self.printMem('------------------------------------IVT-----------------------------------------------', RTyyyy_uidef.kMemBlockColor_IVT)
                self.needToShowIvtIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_IVT)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockSize_IVT + RTyyyy_memdef.kMemBlockSize_BootData:
            if self.needToShowBootDataIntr:
                self.printMem('---------------------------------Boot Data--------------------------------------------', RTyyyy_uidef.kMemBlockColor_BootData)
                self.needToShowBootDataIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_BootData)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockOffsetToIvt_DCD:
            self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockOffsetToIvt_DCD + misc.align_up(self.destAppDcdLength, 16):
            if self.needToShowDcdIntr:
                self.printMem('------------------------------------DCD-----------------------------------------------', RTyyyy_uidef.kMemBlockColor_DCD)
                self.needToShowDcdIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_DCD)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockOffsetToIvt_XMCD:
            self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppIvtOffset + RTyyyy_memdef.kMemBlockOffsetToIvt_XMCD + misc.align_up(self.destAppXmcdLength, 16):
            if self.needToShowXmcdIntr:
                self.printMem('-----------------------------------XMCD-----------------------------------------------', RTyyyy_uidef.kMemBlockColor_XMCD)
                self.needToShowXmcdIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_XMCD)
        elif addr <= imageMemBase + self.destAppVectorOffset:
            self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppVectorOffset + self.destAppBinaryBytes:
            if self.needToShowImageIntr:
                self.printMem('-----------------------------------Image----------------------------------------------', RTyyyy_uidef.kMemBlockColor_Image)
                self.needToShowImageIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_Image)
        else:
            hasShowed = False
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_HabAuth or self.secureBootType == RTyyyy_uidef.kSecureBootType_HabCrypto or \
               ((self.secureBootType in RTyyyy_uidef.kSecureBootType_HwCrypto) and self.isCertEnabledForHwCrypto):
                csfStart = imageMemBase + (self.destAppCsfAddress - self.destAppVectorAddress) + self.destAppInitialLoadSize
                if addr > csfStart and addr <= csfStart + RTyyyy_memdef.kMemBlockSize_CSF:
                    if self.needToShowCsfIntr:
                        self.printMem('------------------------------------CSF-----------------------------------------------', RTyyyy_uidef.kMemBlockColor_CSF)
                        self.needToShowCsfIntr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_CSF)
                    hasShowed = True
            if self.secureBootType == RTyyyy_uidef.kSecureBootType_HabCrypto and self.habDekDataOffset != None:
                keyBlobStart = imageMemBase + (self.destAppVectorOffset - self.destAppInitialLoadSize) + self.habDekDataOffset
                if addr > keyBlobStart and addr <= keyBlobStart + RTyyyy_memdef.kMemBlockSize_HabKeyBlob:
                    if self.needToShowHabKeyBlobIntr:
                        self.printMem('------------------------------HAB DEK KeyBlob-----------------------------------------', RTyyyy_uidef.kMemBlockColor_HabKeyBlob)
                        self.needToShowHabKeyBlobIntr = False
                    self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_HabKeyBlob)
                    hasShowed = True
            if not hasShowed:
                if not self.isSdmmcCard:
                    self.printMem(contentToShow)
                else:
                    if addr >= self.bootDeviceMemBase + RTyyyy_memdef.kMemBlockSize_MBRDPT:
                        self.printMem(contentToShow)

    def _showOneLineContentForContainerType( self, addr, imageMemBase, contentToShow, memContent ):
        if (self.isXipableDevice and addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset):
            self.printMem(contentToShow)
        elif (self.isXipableDevice and addr <= imageMemBase + self.tgt.xspiNorCfgInfoOffset + self.tgt.xspiNorCfgInfoLen) or (addr <= imageMemBase + self.tgt.xspiNorCfgInfoLen):
            if not self.isSdmmcCard:
                if self.needToShowCfgIntr:
                    self.printMem('------------------------------------FDCB----------------------------------------------', RTyyyy_uidef.kMemBlockColor_FDCB)
                    self.needToShowCfgIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_FDCB)
            else:
                if addr >= self.bootDeviceMemBase + RTyyyy_memdef.kMemBlockSize_MBRDPT:
                    self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppXmcdOffset:
            self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppXmcdOffset + misc.align_up(self.destAppXmcdLength, 16):
            if self.needToShowXmcdIntr:
                self.printMem('-----------------------------------XMCD-----------------------------------------------', RTyyyy_uidef.kMemBlockColor_XMCD)
                self.needToShowXmcdIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_XMCD)
        elif addr <= imageMemBase + self.destAppContainerOffset - RTyyyy_gendef.kContainerSize_Edgelock:
            self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppContainerOffset:
            if self.hasEdgelockFw:
                if self.needToShowEdgelockContainerIntr:
                    self.printMem('----------------------------Container (Edgelock)--------------------------------------', RTyyyy_uidef.kMemBlockColor_EdgeContainer)
                    self.needToShowEdgelockContainerIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EdgeContainer)
            else:
                self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppContainerOffset + uiheader.kContainerBlockSize_CntHdr:
            if self.needToShowContainerHdrIntr:
                self.printMem('-------------------------Container Header (User App)----------------------------------', RTyyyy_uidef.kMemBlockColor_ContainerHdr)
                self.needToShowContainerHdrIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_ContainerHdr)
        elif addr <= imageMemBase + self.destAppContainerOffset + uiheader.kContainerBlockSize_CntHdr + uiheader.kContainerBlockSize_ImgEntry:
            if self.needToShowImageEntryIntr:
                self.printMem('------------------------Image Array Entry (User App)----------------------------------', RTyyyy_uidef.kMemBlockColor_ImageEntry)
                self.needToShowImageEntryIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_ImageEntry)
        elif addr <= imageMemBase + self.destAppVectorOffset:
            if self.hasEdgelockFw and (addr > imageMemBase + self.destAppInitialLoadSize - RTyyyy_memdef.kMemBlockSize_Edgelock) and (addr <= imageMemBase + self.destAppInitialLoadSize):
                if self.needToShowEdgelockFwIntr:
                    self.printMem('----------------------------Firmware (Edgelock)---------------------------------------', RTyyyy_uidef.kMemBlockColor_EdgeFw)
                    self.needToShowEdgelockFwIntr = False
                self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_EdgeFw)
            else:
                self.printMem(contentToShow)
        elif addr <= imageMemBase + self.destAppVectorOffset + self.destAppBinaryBytes:
            if self.needToShowImageIntr:
                self.printMem('-----------------------------Image (User App)-----------------------------------------', RTyyyy_uidef.kMemBlockColor_Image)
                self.needToShowImageIntr = False
            self.printMem(contentToShow, RTyyyy_uidef.kMemBlockColor_Image)
        else:
            pass

    def RTyyyy_readProgrammedMemoryAndShow( self ):
        imageFileLen = 0
        if self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
            if not os.path.isfile(self.destAppContainerFilename):
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
                return
            imageFileLen = RTyyyy_gendef.kContainerOffset_NOR + os.path.getsize(self.destAppContainerFilename)
        elif self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
            if not os.path.isfile(self.destAppFilename):
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotProgImage'][self.languageIndex])
                return
            self._getInfoFromIvt()
            self._getDcdInfo()
            imageFileLen = os.path.getsize(self.destAppFilename)
        self.clearMem()
        imageMemBase = 0
        self.isFlexspiNandBlockAddr = None
        nandBlockIndex = 0
        readoutMemLen = 0
        if self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            semcNandOpt, semcNandFcbOpt, semcNandImageInfoList = uivar.getBootDeviceConfiguration(self.bootDevice)
            status, dbbtAddr = self._showNandFcb('semc', RTyyyy_rundef.kSemcNandFcbOffset_Fingerprint, RTyyyy_rundef.kSemcNandFcbTag_Fingerprint, RTyyyy_rundef.kSemcNandFcbOffset_SemcTag, RTyyyy_rundef.kSemcNandFcbTag_Semc, RTyyyy_rundef.kSemcNandFcbOffset_DBBTSerachAreaStartPage)
            if status:
                self._showNandDbbt('semc', dbbtAddr)
            # Only Readout first image
            imageMemBase = self.bootDeviceMemBase + (semcNandImageInfoList[0] >> 16) * self.semcNandBlockSize
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            flexspiNandOpt0, flexspiNandOpt1, flexspiNandFcbOpt, flexspiNandImageInfoList, flexspiNandDeviceModel = uivar.getBootDeviceConfiguration(self.bootDevice)
            self.isFlexspiNandBlockAddr = (flexspiNandFcbOpt & 0x00000F00) >> 8
            status, dbbtAddr = self._showNandFcb('flexspi', RTyyyy_rundef.kFlexspiNandFcbOffset_Fingerprint, RTyyyy_rundef.kFlexspiNandFcbTag_Fingerprint, RTyyyy_rundef.kFlexspiNandFcbOffset_FlexspiTag, RTyyyy_rundef.kFlexspiNandFcbTag_Flexspi, RTyyyy_rundef.kFlexspiNandFcbOffset_DBBTSerachStartPage)
            if status:
                self._showNandDbbt('flexspi', dbbtAddr)
            # Only Readout first image
            nandBlockIndex = (flexspiNandImageInfoList[0] >> 16)
            imageMemBase = self.bootDeviceMemBase + nandBlockIndex * self.flexspiNandBlockSize
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor or \
             self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor or \
             self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor:
            imageMemBase = self.bootDeviceMemBase
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd or \
             self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc:
            self._RTyyyy_showUsdhcSdMmcMbrdpt()
            imageMemBase = self.bootDeviceMemBase
        else:
            pass
        if self.habDekDataOffset != None and (self.habDekDataOffset + RTyyyy_memdef.kMemBlockSize_HabKeyBlob > imageFileLen):
            readoutMemLen += self.habDekDataOffset + RTyyyy_memdef.kMemBlockSize_HabKeyBlob
        else:
            readoutMemLen += imageFileLen

        memFilename = 'bootableImageFromBootDevice.dat'
        memFilepath = os.path.join(self.blhostVectorsDir, memFilename)
        if ((self.isFlexspiNandBlockAddr != None) and self.isFlexspiNandBlockAddr):
            status, results, cmdStr = self.blhost.readMemory(nandBlockIndex, readoutMemLen, memFilename, self.bootDeviceMemId)
        else:
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
                if self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                    self._showOneLineContentForContainerType(addr, imageMemBase, contentToShow, memContent)
                elif self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                    self._showOneLineContentForIvtType(addr, imageMemBase, contentToShow, memContent)
            fileObj.close()
        self._RTyyyy_initShowIntr()
        self.tryToSaveImageDataFile(memFilepath)
