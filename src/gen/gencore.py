#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import bincopy
import array
import gendef
sys.path.append(os.path.abspath(".."))
from ui import uicore
from ui import uidef
from ui import uivar
from ui import uilang
from mem import memdef
from run import rundef

class secBootGen(uicore.secBootUi):

    def __init__(self, parent):
        uicore.secBootUi.__init__(self, parent)

        self.srcAppFilename = None

        self.userFileFolder = os.path.join(self.exeTopRoot, 'gen', 'user_file')
        self.mdkAxfConvToolPath = os.path.join(self.exeTopRoot, 'tools', 'ide_utils', 'keil_mdk', 'fromelf.exe')
        self.iarElfConvToolPath = os.path.join(self.exeTopRoot, 'tools', 'ide_utils', 'iar_ewarm', 'ielftool.exe')
        self.mcuxAxfConvToolPath = os.path.join(self.exeTopRoot, 'tools', 'ide_utils', 'mcuxpresso', 'arm-none-eabi-objcopy.exe')
        self.appFmtBatFilename = os.path.join(self.exeTopRoot, 'gen', 'user_file', 'imx_format_conv.bat')
        self.isConvertedAppUsed = False

        self.fdcbBinFilename = os.path.join(self.exeTopRoot, 'gen', 'bootable_image', 'bt_fdcb.bin')
        self.cfgFdcbBinFilename = os.path.join(self.exeTopRoot, 'gen', 'fdcb_file', 'cfg_fdcb.bin')
        self.isFdcbFromSrcApp = False
        self.flexspiNorImage0Version = None
        self.flexspiNorImage1Version = None

    def isInTheRangeOfFlexram( self, start, length ):
        if ((start >= self.tgt.memoryRange['itcm'].start) and (start + length <= self.tgt.memoryRange['itcm'].start + self.tgt.memoryRange['itcm'].length)) or \
           ((start >= self.tgt.memoryRange['dtcm'].start) and (start + length <= self.tgt.memoryRange['dtcm'].start + self.tgt.memoryRange['dtcm'].length)) or \
           ((start >= self.tgt.memoryRange['ocram'].start) and (start + length <= self.tgt.memoryRange['ocram'].start + self.tgt.memoryRange['ocram'].length)) or \
           (('itcm_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['itcm_ns'].start) and (start + length <= self.tgt.memoryRange['itcm_ns'].start + self.tgt.memoryRange['itcm_ns'].length))) or \
           (('dtcm_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['dtcm_ns'].start) and (start + length <= self.tgt.memoryRange['dtcm_ns'].start + self.tgt.memoryRange['dtcm_ns'].length))) or \
           (('ocram_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['ocram_ns'].start) and (start + length <= self.tgt.memoryRange['ocram_ns'].start + self.tgt.memoryRange['ocram_ns'].length))) or \
           (('itcm_sec' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['itcm_sec'].start) and (start + length <= self.tgt.memoryRange['itcm_sec'].start + self.tgt.memoryRange['itcm_sec'].length))) or \
           (('dtcm_sec' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['dtcm_sec'].start) and (start + length <= self.tgt.memoryRange['dtcm_sec'].start + self.tgt.memoryRange['dtcm_sec'].length))) or \
           (('itcm_sec_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['itcm_sec_ns'].start) and (start + length <= self.tgt.memoryRange['itcm_sec_ns'].start + self.tgt.memoryRange['itcm_sec_ns'].length))) or \
           (('dtcm_sec_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['dtcm_sec_ns'].start) and (start + length <= self.tgt.memoryRange['dtcm_sec_ns'].start + self.tgt.memoryRange['dtcm_sec_ns'].length))):
            return True
        else:
            return False

    def isInTheRangeOfFlexspiRam( self, start, length ):
        if (('flexspi1_ram' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi1_ram'].start) and (start + length <= self.tgt.memoryRange['flexspi1_ram'].start + self.tgt.memoryRange['flexspi1_ram'].length))) or \
           (('flexspi1_ram_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi1_ram_ns'].start) and (start + length <= self.tgt.memoryRange['flexspi1_ram_ns'].start + self.tgt.memoryRange['flexspi1_ram_ns'].length))) or \
           (('flexspi1_ram_a' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi1_ram_a'].start) and (start + length <= self.tgt.memoryRange['flexspi1_ram_a'].start + self.tgt.memoryRange['flexspi1_ram_a'].length))) or \
           (('flexspi1_ram_a_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi1_ram_a_ns'].start) and (start + length <= self.tgt.memoryRange['flexspi1_ram_a_ns'].start + self.tgt.memoryRange['flexspi1_ram_a_ns'].length))) or \
           (('flexspi2_ram' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi2_ram'].start) and (start + length <= self.tgt.memoryRange['flexspi2_ram'].start + self.tgt.memoryRange['flexspi2_ram'].length))) or \
           (('flexspi2_ram_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi2_ram_ns'].start) and (start + length <= self.tgt.memoryRange['flexspi2_ram_ns'].start + self.tgt.memoryRange['flexspi2_ram_ns'].length))) or \
           (('flexspi2_ram_a' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi2_ram_a'].start) and (start + length <= self.tgt.memoryRange['flexspi2_ram_a'].start + self.tgt.memoryRange['flexspi2_ram_a'].length))) or \
           (('flexspi2_ram_a_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['flexspi2_ram_a_ns'].start) and (start + length <= self.tgt.memoryRange['flexspi2_ram_a_ns'].start + self.tgt.memoryRange['flexspi2_ram_a_ns'].length))):
            return True
        else:
            return False

    def isInTheRangeOfSram( self, start, length ):
        if (('sram' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['sram'].start) and (start + length <= self.tgt.memoryRange['sram'].start + self.tgt.memoryRange['sram'].length))) or \
           (('sramx' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['sramx'].start) and (start + length <= self.tgt.memoryRange['sramx'].start + self.tgt.memoryRange['sramx'].length))) or \
           (('sramc' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['sramc'].start) and (start + length <= self.tgt.memoryRange['sramc'].start + self.tgt.memoryRange['sramc'].length))) or \
           (('srams' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['srams'].start) and (start + length <= self.tgt.memoryRange['srams'].start + self.tgt.memoryRange['srams'].length))) or \
           (('sramc_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['sramc_ns'].start) and (start + length <= self.tgt.memoryRange['sramc_ns'].start + self.tgt.memoryRange['sramc_ns'].length))) or \
           (('srams_ns' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['srams_ns'].start) and (start + length <= self.tgt.memoryRange['srams_ns'].start + self.tgt.memoryRange['srams_ns'].length))):
            return True
        else:
            return False

    def isInTheRangeOfSemcSdram( self, start, length ):
        if (('semc0_sdram' in self.tgt.memoryRange) and ((start >= self.tgt.memoryRange['semc0_sdram'].start) and (start + length <= self.tgt.memoryRange['semc0_sdram'].start + self.tgt.memoryRange['semc0_sdram'].length))):
            return True
        else:
            return False

    def _convertElfOrAxfToSrec( self, appFilename, destSrecAppFilename, appFormat):
        batContent = ''
        # below are conv results:
        # ----------------------------------------------------------------
        # |                       |    IAR     |    MDK     |    MCUX    |
        # ----------------------------------------------------------------
        # |      ielftool         |    Yes     |    Yes     |    No      |   // Start address is always 0x0000_0000
        # ----------------------------------------------------------------
        # | arm-none-eabi-objcopy |    Yes     |    No      |    Yes     |   // Error content in last three lines
        # ----------------------------------------------------------------
        # |      fromelf          |    No      |    Yes     |    No      |   // A folder will be generated for IAR, All contents are error for MCUX
        # ----------------------------------------------------------------
        ideutilToolPath = None
        if appFormat == uidef.kAppImageFormat_ElfFromIar or appFormat == uidef.kAppImageFormat_AxfFromMdk:
            batContent = "\"" + self.iarElfConvToolPath + "\" --srec-s3only \"" + appFilename +"\" \"" + destSrecAppFilename + "\""
            ideutilToolPath = self.iarElfConvToolPath
        elif appFormat == uidef.kAppImageFormat_AxfFromMcux or appFormat == uidef.kAppImageFormat_ElfFromGcc:
            batContent = "\"" + self.mcuxAxfConvToolPath + "\" -O srec \"" + appFilename +"\" \"" + destSrecAppFilename + "\""
            ideutilToolPath = self.mcuxAxfConvToolPath
        #elif appFormat == uidef.kAppImageFormat_AxfFromMdk:
        #    batContent = "\"" + self.mdkAxfConvToolPath + "\" --m32 \"" + appFilename +"\" --output \"" + destSrecAppFilename + "\""
        else:
            pass
        with open(self.appFmtBatFilename, 'wb') as fileObj:
            fileObj.write(batContent)
            fileObj.close()
        try:
            os.system(self.appFmtBatFilename)
            #curdir = os.getcwd()
            #os.chdir(os.path.split(ideutilToolPath)[0])
            #process = subprocess.Popen(self.appFmtBatFilename, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #os.chdir(curdir)
        except:
            pass
        if os.path.isfile(destSrecAppFilename):
            self.srcAppFilename = destSrecAppFilename
            appType = gendef.kAppImageFileExtensionList_S19[0]
            self.isConvertedAppUsed = True
            self.printLog('User image file has been converted to S-Records successfully')
            return self.srcAppFilename, appType
        else:
            appType = gendef.kAppImageFileExtensionList_Elf[0]
            return appFilename, appType

    def _getSrecDataWithoutS6Frame( self, srecData ):
        s6FrameStartLoc = srecData.find('S6')
        if s6FrameStartLoc != -1:
            newSrecData = srecData[0:s6FrameStartLoc]
            s6FrameEndLoc = srecData.find('\n', s6FrameStartLoc)
            if s6FrameEndLoc != -1:
                if len(srecData) > s6FrameEndLoc:
                    newSrecData += srecData[s6FrameEndLoc + 1:len(srecData)]
                else:
                    newSrecData += '\n'
            else:
                newSrecData += '\n'
            return newSrecData
        else:
            return srecData

    def _convertHexOrBinToSrec( self, appFilename, destSrecAppFilename, appType):
        status = True
        fmtObj = None
        if appType.lower() in gendef.kAppImageFileExtensionList_Hex:
            fmtObj = bincopy.BinFile(str(appFilename))
        elif appType.lower() in gendef.kAppImageFileExtensionList_Bin:
            fmtObj = bincopy.BinFile()
            status, baseAddr = self.getUserBinaryBaseAddress()
            if status:
                fmtObj.add_binary_file(str(appFilename), baseAddr)
            else:
                appType = None
        if status:
            self.srcAppFilename = destSrecAppFilename
            with open(self.srcAppFilename, 'wb') as fileObj:
                # Prototype: as_srec(number_of_data_bytes=32, address_length_bits=32)
                #    Format the binary file as Motorola S-Records records and return them as a string.
                #    number_of_data_bytes is the number of data bytes in each record.
                #    address_length_bits is the number of address bits in each record.
                fileObj.write(self._getSrecDataWithoutS6Frame(fmtObj.as_srec(16, 32)))
                fileObj.close()
            appFilename = self.srcAppFilename
            appType = gendef.kAppImageFileExtensionList_S19[0]
            self.isConvertedAppUsed = True
        return appFilename, appType

    def convertImageFormatToSrec( self, appFilename, appName, appType, ideType = None):
        appFormat = self.getUserAppFileFormat()
        destSrecAppFilename = os.path.join(self.userFileFolder, appName + gendef.kAppImageFileExtensionList_S19[0])
        if appFormat == uidef.kAppImageFormat_AutoDetect:
            if appType.lower() in gendef.kAppImageFileExtensionList_S19:
                return appFilename, appType
            elif (appType.lower() in gendef.kAppImageFileExtensionList_Hex) or (appType.lower() in gendef.kAppImageFileExtensionList_Bin):
                return self._convertHexOrBinToSrec(appFilename, destSrecAppFilename, appType)
            else:
                if ideType == None:
                    appFilename, appType = self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_ElfFromIar)
                    if appType.lower() in gendef.kAppImageFileExtensionList_S19:
                        return appFilename, appType
                    appFilename, appType = self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_AxfFromMcux)
                    if appType.lower() in gendef.kAppImageFileExtensionList_S19:
                        return appFilename, appType
                    return self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_AxfFromMdk)
                elif ideType == gendef.kIdeType_MCUX:
                    return self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_AxfFromMcux)
                elif ideType == gendef.kIdeType_IAR:
                    return self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_ElfFromIar)
                elif ideType == gendef.kIdeType_MDK:
                    return self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, uidef.kAppImageFormat_AxfFromMdk)
                else:
                    pass
        elif appFormat == uidef.kAppImageFormat_AxfFromMdk or \
             appFormat == uidef.kAppImageFormat_ElfFromIar or \
             appFormat == uidef.kAppImageFormat_AxfFromMcux or \
             appFormat == uidef.kAppImageFormat_ElfFromGcc:
            return self._convertElfOrAxfToSrec(appFilename, destSrecAppFilename, appFormat)
        elif appFormat == uidef.kAppImageFormat_IntelHex:
            return self._convertHexOrBinToSrec(appFilename, destSrecAppFilename, gendef.kAppImageFileExtensionList_Hex[0])
        elif appFormat == uidef.kAppImageFormat_RawBinary:
            return self._convertHexOrBinToSrec(appFilename, destSrecAppFilename, gendef.kAppImageFileExtensionList_Bin[0])
        elif appFormat == uidef.kAppImageFormat_MotoSrec:
            return appFilename, gendef.kAppImageFileExtensionList_S19[0]
        else:
            pass

    def getReg32FromBinFile( self, filename, offset=0):
        return hex(self.getVal32FromBinFile(filename, offset))

    def getVal8FromBinFile( self, filename, offset=0):
        var8Vaule = 0
        if os.path.isfile(filename):
            var8Vaule = array.array('c', [chr(0xff)]) * 1
            with open(filename, 'rb') as fileObj:
                fileObj.seek(offset)
                var8Vaule = fileObj.read(1)
                fileObj.close()
            var8Vaule = ord(var8Vaule[0])
        return var8Vaule

    def getVal32FromBinFile( self, filename, offset=0):
        var32Vaule = 0
        if os.path.isfile(filename):
            var32Vaule = array.array('c', [chr(0xff)]) * 4
            with open(filename, 'rb') as fileObj:
                fileObj.seek(offset)
                var32Vaule = fileObj.read(4)
                fileObj.close()
            var32Vaule = (ord(var32Vaule[3])<<24) + (ord(var32Vaule[2])<<16) + (ord(var32Vaule[1])<<8) + ord(var32Vaule[0])
        return var32Vaule

    def getVal16FromByteArray( self, binarray, offset=0):
        val16Vaule = (binarray[1+offset]<<8) + binarray[0+offset]
        return val16Vaule

    def getVal32FromByteArray( self, binarray, offset=0):
        val32Vaule = ((binarray[3+offset]<<24) + (binarray[2+offset]<<16) + (binarray[1+offset]<<8) + binarray[0+offset])
        return val32Vaule

    def fillVal32IntoBinFile( self, filename, val32):
        with open(filename, 'ab') as fileObj:
            byteStr = ''
            for i in range(4):
                byteStr = chr((val32 & (0xFF << (i * 8))) >> (i * 8))
                fileObj.write(byteStr)
            fileObj.close()

    def extractFdcbDataFromSrcApp(self, initialLoadAppBytes, fdcbOffset ):
        flexspiNorOpt0, flexspiNorOpt1, flexspiDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(uidef.kBootDevice_XspiNor)
        self.isFdcbFromSrcApp = isFdcbKept
        if self.isFdcbFromSrcApp:
            with open(self.fdcbBinFilename, 'wb') as fileObj:
                fileObj.write(initialLoadAppBytes[fdcbOffset:fdcbOffset+memdef.kMemBlockSize_FDCB])
                fileObj.close()

    def getImageVersionValueFromSrcApp(self, initialLoadAppBytes, fdcbOffset ):
        var32Vaule = 0
        idxStart = fdcbOffset + gendef.kImgVerOffset_NOR - self.tgt.xspiNorCfgInfoOffset
        #for i in range(memdef.kMemBlockSize_ImageVersion):
        #    var32Vaule = var32Vaule + initialLoadAppBytes[idxStart + i] << (8 * i)
        #    self.printLog('----------------' + str(initialLoadAppBytes[idxStart + i]))
        #    self.printLog('----------------' + str(hex(var32Vaule)))
        var32Vaule = (initialLoadAppBytes[idxStart + 3] << 24) + (initialLoadAppBytes[idxStart + 2] << 16) + (initialLoadAppBytes[idxStart + 1] << 8) + initialLoadAppBytes[idxStart]
        if var32Vaule == 0:
            var32Vaule = rundef.kFlexspiNorContent_Blank32
        return var32Vaule

    def adjustTgtFlexspiMemBaseAccordingToApp( self, imageStartAddr ):
        flexspiNorMemBase  = None
        flexspiNorMemBaseNs = None
        flexspiNorMemBaseAliased = None
        flexspiNorMemBaseAliasedNs = None
        flexspiNorMemMaxSize = None
        flexspiNorMemAliasedMaxSize = None
        if self.flexspiBootInstance == 0:
            flexspiNorMemBase  = self.tgt.flexspiNorMemBase0
            flexspiNorMemBaseNs = self.tgt.flexspiNorMemBase0Ns
            flexspiNorMemBaseAliased = self.tgt.flexspiNorMemBase0Aliased
            flexspiNorMemBaseAliasedNs = self.tgt.flexspiNorMemBase0AliasedNs
            flexspiNorMemMaxSize = self.tgt.flexspiNorMem0MaxSize
            flexspiNorMemAliasedMaxSize = self.tgt.flexspiNorMem0AliasedMaxSize
        elif self.flexspiBootInstance == 1:
            flexspiNorMemBase  = self.tgt.flexspiNorMemBase1
            flexspiNorMemBaseNs = self.tgt.flexspiNorMemBase1Ns
            flexspiNorMemBaseAliased = self.tgt.flexspiNorMemBase1Aliased
            flexspiNorMemBaseAliasedNs = self.tgt.flexspiNorMemBase1AliasedNs
            flexspiNorMemMaxSize = self.tgt.flexspiNorMem1MaxSize
            flexspiNorMemAliasedMaxSize = self.tgt.flexspiNorMem1AliasedMaxSize
        else:
            pass
        if flexspiNorMemBase != None:
            if ((imageStartAddr >= flexspiNorMemBase) and (imageStartAddr < flexspiNorMemBase + flexspiNorMemMaxSize)):
                self.tgt.flexspiNorMemBase = flexspiNorMemBase
                self.tgt.flexspiNorMemMaxSize = flexspiNorMemMaxSize
                return
        if flexspiNorMemBaseNs != None:
            if ((imageStartAddr >= flexspiNorMemBaseNs) and (imageStartAddr < flexspiNorMemBaseNs + flexspiNorMemMaxSize)):
                self.tgt.flexspiNorMemBase = flexspiNorMemBaseNs
                self.tgt.flexspiNorMemMaxSize = flexspiNorMemMaxSize
                return
        if flexspiNorMemBaseAliased != None:
            if ((imageStartAddr >= flexspiNorMemBaseAliased) and (imageStartAddr < flexspiNorMemBaseAliased + flexspiNorMemAliasedMaxSize)):
                self.tgt.flexspiNorMemBase = flexspiNorMemBaseAliased
                self.tgt.flexspiNorMemMaxSize = flexspiNorMemAliasedMaxSize
                return
        if flexspiNorMemBaseAliasedNs != None:
            if ((imageStartAddr >= flexspiNorMemBaseAliasedNs) and (imageStartAddr < flexspiNorMemBaseAliasedNs + flexspiNorMemAliasedMaxSize)):
                self.tgt.flexspiNorMemBase = flexspiNorMemBaseAliasedNs
                self.tgt.flexspiNorMemMaxSize = flexspiNorMemAliasedMaxSize
                return

    def genPaddingByteArrayStr( self, num, pattern=0xFF ):
        paddingBytes = [pattern] * num
        paddingBytesStr = ''
        for i in range(num):
            paddingBytesStr += chr(paddingBytes[i])
        return paddingBytesStr

    def bincopyFileToFile( self, destBinFile, srcBinFile, offset ):
        destFileObj = open(destBinFile,'rb')
        destFileData = destFileObj.read()
        destFileObj.close()
        srcFileObj = open(srcBinFile,'rb')
        srcFileData = srcFileObj.read()
        srcFileObj.close()
        if offset >= 0:
            finalFileData = destFileData[0:offset] + srcFileData + destFileData[offset+len(srcFileData):]
        else:
            offset = -offset
            finalFileData = srcFileData + self.genPaddingByteArrayStr(offset - len(srcFileData), 0xFF) + destFileData
        with open(destBinFile, 'wb') as fileObj:
            fileObj.write(finalFileData)
            fileObj.close()

