#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import array
import rundef
import boot
sys.path.append(os.path.abspath(".."))
from gen import gencore
from ui import uidef
from ui import uivar
from ui import uilang
from mem import memdef

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

        self.isFlexspiNandBlockAddr = None

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

    def getMcuDeviceBootloaderUniqueId( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_UniqueDeviceIdent)
        self.printLog(cmdStr)
        if status == boot.status.kStatus_Success:
            self.printDeviceStatus('Unique ID[31:00] = ' + self.convertLongIntHexText(str(hex(results[0]))))
            self.printDeviceStatus('Unique ID[63:32] = ' + self.convertLongIntHexText(str(hex(results[1]))))
            try:
                self.printDeviceStatus('Unique ID[95:64] = ' + self.convertLongIntHexText(str(hex(results[2]))))
                self.printDeviceStatus('Unique ID[127:96] = ' + self.convertLongIntHexText(str(hex(results[3]))))
            except:
                pass
        else:
            pass

    def getUsdhcSdMmcDeviceInfo ( self ):
        status, results, cmdStr = self.blhost.getProperty(boot.properties.kPropertyTag_ExternalMemoryAttribles, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if (status == boot.status.kStatus_Success):
            #typedef struct
            #{
            #    uint32_t availableAttributesFlag; //!< Available Atrributes, bit map
            #    uint32_t startAddress;            //!< start Address of external memory
            #    uint32_t flashSizeInKB;           //!< flash size of external memory
            #    uint32_t pageSize;                //!< page size of external memory
            #    uint32_t sectorSize;              //!< sector size of external memory
            #    uint32_t blockSize;               //!< block size of external memory
            #} external_memory_property_store_t;
            blockByteSize = results[5]
            totalSizeKB = results[2]
            self.printDeviceStatus("Block Size  = " + self.showAsOptimalMemoryUnit(blockByteSize))
            strTotalSizeGB = ("%.2f" % (totalSizeKB / 1024.0 / 1024))
            self.printDeviceStatus("Total Size  = " + self.convertLongIntHexText(strTotalSizeGB) + ' GB')
            self.comMemWriteUnit = blockByteSize
            self.comMemEraseUnit = blockByteSize
            self.comMemReadUnit = blockByteSize
        else:
            self.printDeviceStatus("Block Size  = --------")
            self.printDeviceStatus("Total Size  = --------")
            return False
        return True

    def flash2ndBootableImageIntoFlexspiNor( self, image1Start, image1Size, image1Version, image0Version ):
        status, results, cmdStr = self.blhost.flashEraseRegion(image1Start, image1Size, rundef.kBootDeviceMemId_FlexspiNor)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        image0Filename = 'bootableImage0.bin'
        image0Filepath = os.path.join(self.blhostVectorsDir, image0Filename)
        image1Filename = 'bootableImage1.bin'
        image1Filepath = os.path.join(self.blhostVectorsDir, image1Filename)
        status, results, cmdStr = self.blhost.readMemory(self.bootDeviceMemBase, image1Size, image0Filename, self.bootDeviceMemId)
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        if image0Version != image1Version:
            readoutBin = None
            image0FileObj = open(image0Filepath, 'rb')
            image1FileObj = open(image1Filepath, 'wb')
            readoutBin = image0FileObj.read(memdef.kMemBlockOffset_ImageVersion)
            image1FileObj.write(readoutBin)
            thisBin = image0FileObj.read(4)
            thisBin = chr(image1Version & 0xFF)
            thisBin += chr((image1Version >> 8) & 0xFF)
            thisBin += chr((image1Version >> 16) & 0xFF)
            thisBin += chr((image1Version >> 24) & 0xFF)
            image1FileObj.write(thisBin)
            image1Size = image1Size - memdef.kMemBlockOffset_ImageVersion - 4
            while image1Size > 0:
                if image1Size > memdef.kMemBlockOffset_ImageVersion:
                    readoutBin = image0FileObj.read(memdef.kMemBlockOffset_ImageVersion)
                else:
                    readoutBin = image0FileObj.read(image1Size)
                image1Size -= len(readoutBin)
                image1FileObj.write(readoutBin)
            image0FileObj.close()
            image1FileObj.close()
        else:
            image1Filepath = image0Filepath
        status, results, cmdStr = self.blhost.writeMemory(image1Start, image1Filepath, rundef.kBootDeviceMemId_FlexspiNor)
        try:
            os.remove(image0Filepath)
            os.remove(image1Filepath)
        except:
            pass
        self.printLog(cmdStr)
        if status != boot.status.kStatus_Success:
            return False
        return True

