#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import os
import math
import array
import struct
import shutil
import uidef
import uivar
import uilang
import ui_cfg_lut
import uidef_fdcb
sys.path.append(os.path.abspath(".."))
from win import bootDeviceWin_FDCB
from mem import memdef
from utils import sound

kAccessType_Set = 0
kAccessType_Get = 1

class secBootUiCfgFdcb(bootDeviceWin_FDCB.bootDeviceWin_FDCB):

    def __init__(self, parent):
        bootDeviceWin_FDCB.bootDeviceWin_FDCB.__init__(self, parent)
        self.mcuSeries = None
        self.cfgFdcbBinFilename = None
        self.fdcbBuffer = array.array('c', [chr(0x00)]) * memdef.kMemBlockSize_FDCB

    def setNecessaryInfo( self, mcuSeries, flexspiFreqs, cfgFdcbBinFilename ):
        if flexspiFreqs != None:
            self.m_choice_serialClkFreq.Clear()
            self.m_choice_serialClkFreq.SetItems(flexspiFreqs)
            self.m_choice_serialClkFreq.SetSelection(0)
            self.m_choice_ipcmdSerialClkFreq.Clear()
            self.m_choice_ipcmdSerialClkFreq.SetItems(flexspiFreqs)
            self.m_choice_ipcmdSerialClkFreq.SetSelection(0)
        self.mcuSeries = mcuSeries
        self.cfgFdcbBinFilename = cfgFdcbBinFilename
        self._defnMcuSeriesDifference()
        self._recoverLastSettings()

    def _defnMcuSeriesDifference( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
            self.m_staticText_readSampleClkSrc.SetLabel("readSamplingOption:")
            self.m_staticText_lutCustomSeqEnable.SetLabel("N/A")
            self.m_staticText_commandInterval.SetLabel("N/A")
            self.m_staticText_dataValidTime0time_100ps.SetLabel("coarseTuning:")
            self.m_staticText_dataValidTime0delay_cells.SetLabel("fineTuning:")
            self.m_staticText_dataValidTime1time_100ps.SetLabel("samplePoint:")
            self.m_staticText_dataValidTime1delay_cells.SetLabel("dataHoldTime:")
            self.m_staticText_lutCustomSeq0Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq0Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq1Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq1Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq2Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq2Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq3Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq3Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq4Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq4Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq5Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq5Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq6Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq6Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq7Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq7Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq8Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq8Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq9Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq9Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq10Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq10Id.SetLabel("N/A")
            self.m_staticText_lutCustomSeq11Num.SetLabel("N/A")
            self.m_staticText_lutCustomSeq11Id.SetLabel("N/A")
            self.m_staticText_isDataOrderSwapped.SetLabel("N/A")
            self.m_staticText_serialNorType.SetLabel("N/A")
            self.m_staticText_needExitNoCmdMode.SetLabel("N/A")
            self.m_staticText_halfClkForNonReadCmd.SetLabel("N/A")
            self.m_staticText_needRestoreNoCmdMode.SetLabel("N/A")
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.m_staticText_isNonBlockingMode.SetLabel("N/A")
        else:
            pass

    def _convertPackFmt( self, byteNum ):
        fmt = '<B'
        if byteNum == 4:
            fmt = '<I'
        elif byteNum == 2:
            fmt = '<H'
        #elif byteNum == 1:
        else:
            pass
        return fmt

    def _getMemberFromFdcb( self, buf, offset, byteNum ):
        return struct.unpack_from(self._convertPackFmt(byteNum), buf[offset:offset+byteNum], 0)

    def _setMemberForFdcb( self, offset, byteNum, data ):
        struct.pack_into(self._convertPackFmt(byteNum), self.fdcbBuffer, offset, data)

    def _accessTag( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            tag = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_tag, uidef_fdcb.kFlexspiFdcbLength_tag)
            self.m_textCtrl_tag.Clear()
            self.m_textCtrl_tag.write(str(hex(tag[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_tag, uidef_fdcb.kFlexspiFdcbLength_tag, int(self.m_textCtrl_tag.GetLineText(0), 16))

    def _accessVersion( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            version = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_version, uidef_fdcb.kFlexspiFdcbLength_version)
            self.m_textCtrl_version.Clear()
            self.m_textCtrl_version.write(str(hex(version[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_version, uidef_fdcb.kFlexspiFdcbLength_version, int(self.m_textCtrl_version.GetLineText(0), 16))

    def _accessReadSampleClkSrc( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            readSampleClkSrc = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_readSampleClkSrc, uidef_fdcb.kFlexspiFdcbLength_readSampleClkSrc)
            self.m_choice_readSampleClkSrc.SetSelection(readSampleClkSrc[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_readSampleClkSrc, uidef_fdcb.kFlexspiFdcbLength_readSampleClkSrc, self.m_choice_readSampleClkSrc.GetSelection())

    def _accessCsHoldTime( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            csHoldTime = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_csHoldTime, uidef_fdcb.kFlexspiFdcbLength_csHoldTime)
            self.m_textCtrl_csHoldTime.Clear()
            self.m_textCtrl_csHoldTime.write(str(hex(csHoldTime[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_csHoldTime, uidef_fdcb.kFlexspiFdcbLength_csHoldTime, int(self.m_textCtrl_csHoldTime.GetLineText(0), 16))

    def _accessCsSetupTime( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            csSetupTime = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_csSetupTime, uidef_fdcb.kFlexspiFdcbLength_csSetupTime)
            self.m_textCtrl_csSetupTime.Clear()
            self.m_textCtrl_csSetupTime.write(str(hex(csSetupTime[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_csSetupTime, uidef_fdcb.kFlexspiFdcbLength_csSetupTime, int(self.m_textCtrl_csSetupTime.GetLineText(0), 16))

    def _accessColumnAddressWidth( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            columnAddressWidth = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_columnAddressWidth, uidef_fdcb.kFlexspiFdcbLength_columnAddressWidth)
            if columnAddressWidth[0] == 0:
                self.m_choice_columnAddressWidth.SetSelection(0)
            else:
                self.m_choice_columnAddressWidth.SetSelection(1)
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_columnAddressWidth, uidef_fdcb.kFlexspiFdcbLength_columnAddressWidth, self.m_choice_columnAddressWidth.GetSelection())

    def _accessDeviceModeCfgEnable( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            deviceModeCfgEnable = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_deviceModeCfgEnable, uidef_fdcb.kFlexspiFdcbLength_deviceModeCfgEnable)
            self.m_choice_deviceModeCfgEnable.SetSelection(deviceModeCfgEnable[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceModeCfgEnable, uidef_fdcb.kFlexspiFdcbLength_deviceModeCfgEnable, self.m_choice_deviceModeCfgEnable.GetSelection())

    def _accessDeviceModeType( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            deviceModeType = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_deviceModeType, uidef_fdcb.kFlexspiFdcbLength_deviceModeType)
            self.m_choice_deviceModeType.SetSelection(deviceModeType[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceModeType, uidef_fdcb.kFlexspiFdcbLength_deviceModeType, self.m_choice_deviceModeType.GetSelection())

    def _accessWaitTimeCfgCommands( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            waitTimeCfgCommands = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_waitTimeCfgCommands, uidef_fdcb.kFlexspiFdcbLength_waitTimeCfgCommands)
            self.m_textCtrl_waitTimeCfgCommands.Clear()
            self.m_textCtrl_waitTimeCfgCommands.write(str(hex(waitTimeCfgCommands[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_waitTimeCfgCommands, uidef_fdcb.kFlexspiFdcbLength_waitTimeCfgCommands, int(self.m_textCtrl_waitTimeCfgCommands.GetLineText(0), 16))

    def _accessDeviceModeSeq( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            deviceModeSeqNum = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_deviceModeSeq, 1)
            deviceModeSeqId = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_deviceModeSeq + 1, 1)
            self.m_choice_deviceModeSeqNum.SetSelection(deviceModeSeqNum[0])
            self.m_choice_deviceModeSeqId.SetSelection(deviceModeSeqId[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceModeSeq, 1, self.m_choice_deviceModeSeqNum.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceModeSeq + 1, 1, self.m_choice_deviceModeSeqId.GetSelection())

    def _accessDeviceModeArg( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            deviceModeArg = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_deviceModeArg, uidef_fdcb.kFlexspiFdcbLength_deviceModeArg)
            self.m_textCtrl_deviceModeArg.Clear()
            self.m_textCtrl_deviceModeArg.write(str(hex(deviceModeArg[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceModeArg, uidef_fdcb.kFlexspiFdcbLength_deviceModeArg, int(self.m_textCtrl_deviceModeArg.GetLineText(0), 16))

    def _accessConfigCmdEnable( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            configCmdEnable = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdEnable, uidef_fdcb.kFlexspiFdcbLength_configCmdEnable)
            self.m_choice_configCmdEnable.SetSelection(configCmdEnable[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdEnable, uidef_fdcb.kFlexspiFdcbLength_configCmdEnable, self.m_choice_configCmdEnable.GetSelection())

    def _accessConfigModeType( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            configModeType0 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configModeType, 1)
            configModeType1 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configModeType + 1, 1)
            configModeType2 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configModeType + 2, 1)
            self.m_choice_configModeType0.SetSelection(configModeType0[0])
            self.m_choice_configModeType1.SetSelection(configModeType1[0])
            self.m_choice_configModeType2.SetSelection(configModeType2[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configModeType, 1, self.m_choice_configModeType0.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configModeType + 1, 1, self.m_choice_configModeType1.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configModeType + 2, 1, self.m_choice_configModeType2.GetSelection())

    def _accessConfigCmdSeqs( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            configCmdSeqs0Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs, 1)
            configCmdSeqs0Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 1, 1)
            configCmdSeqs1Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 4, 1)
            configCmdSeqs1Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 5, 1)
            configCmdSeqs2Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 8, 1)
            configCmdSeqs2Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 9, 1)
            self.m_choice_configCmdSeqs0Num.SetSelection(configCmdSeqs0Num[0])
            self.m_choice_configCmdSeqs0Id.SetSelection(configCmdSeqs0Id[0])
            self.m_choice_configCmdSeqs1Num.SetSelection(configCmdSeqs1Num[0])
            self.m_choice_configCmdSeqs1Id.SetSelection(configCmdSeqs1Id[0])
            self.m_choice_configCmdSeqs2Num.SetSelection(configCmdSeqs2Num[0])
            self.m_choice_configCmdSeqs2Id.SetSelection(configCmdSeqs2Id[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs, 1, self.m_choice_configCmdSeqs0Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 1, 1, self.m_choice_configCmdSeqs0Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 4, 1, self.m_choice_configCmdSeqs1Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 5, 1, self.m_choice_configCmdSeqs1Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 8, 1, self.m_choice_configCmdSeqs2Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdSeqs + 9, 1, self.m_choice_configCmdSeqs2Id.GetSelection())

    def _accessConfigCmdArgs( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            configCmdArgs0 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs, 1)
            configCmdArgs1 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs + 1, 1)
            configCmdArgs2 = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs + 2, 1)
            self.m_textCtrl_configCmdArgs0.Clear()
            self.m_textCtrl_configCmdArgs0.write(str(hex(configCmdArgs0[0])))
            self.m_textCtrl_configCmdArgs1.Clear()
            self.m_textCtrl_configCmdArgs1.write(str(hex(configCmdArgs1[0])))
            self.m_textCtrl_configCmdArgs2.Clear()
            self.m_textCtrl_configCmdArgs2.write(str(hex(configCmdArgs2[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs, 1, int(self.m_textCtrl_configCmdArgs0.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs + 1, 1, int(self.m_textCtrl_configCmdArgs1.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_configCmdArgs + 2, 1, int(self.m_textCtrl_configCmdArgs2.GetLineText(0), 16))

    def _accessControllerMiscOption( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            controllerMiscOption = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_controllerMiscOption, uidef_fdcb.kFlexspiFdcbLength_controllerMiscOption)
            self.m_textCtrl_controllerMiscOption.Clear()
            self.m_textCtrl_controllerMiscOption.write(str(hex(controllerMiscOption[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_controllerMiscOption, uidef_fdcb.kFlexspiFdcbLength_controllerMiscOption, int(self.m_textCtrl_controllerMiscOption.GetLineText(0), 16))

    def _accessDeviceType( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            self.m_choice_deviceType.SetSelection(0)
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_deviceType, uidef_fdcb.kFlexspiFdcbLength_deviceType, 1)

    def _accessSflashPadType( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            sflashPadType = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sflashPadType, uidef_fdcb.kFlexspiFdcbLength_sflashPadType)
            sflashPadType = int(math.log(sflashPadType[0], 2))
            self.m_choice_sflashPadType.SetSelection(sflashPadType)
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sflashPadType, uidef_fdcb.kFlexspiFdcbLength_sflashPadType, int(math.pow(2, self.m_choice_sflashPadType.GetSelection())))

    def _accessSerialClkFreq( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            serialClkFreq = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_serialClkFreq, uidef_fdcb.kFlexspiFdcbLength_serialClkFreq)
            self.m_choice_serialClkFreq.SetSelection(serialClkFreq[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_serialClkFreq, uidef_fdcb.kFlexspiFdcbLength_serialClkFreq, self.m_choice_serialClkFreq.GetSelection())

    def _accessLutCustomSeqEnable( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            lutCustomSeqEnable = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeqEnable, uidef_fdcb.kFlexspiFdcbLength_lutCustomSeqEnable)
            self.m_choice_lutCustomSeqEnable.SetSelection(lutCustomSeqEnable[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeqEnable, uidef_fdcb.kFlexspiFdcbLength_lutCustomSeqEnable, self.m_choice_lutCustomSeqEnable.GetSelection())

    def _accessSflashSize( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            sflashA1Size = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sflashA1Size, uidef_fdcb.kFlexspiFdcbLength_sflashA1Size)
            sflashA2Size = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sflashA2Size, uidef_fdcb.kFlexspiFdcbLength_sflashA2Size)
            sflashB1Size = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sflashB1Size, uidef_fdcb.kFlexspiFdcbLength_sflashB1Size)
            sflashB2Size = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sflashB2Size, uidef_fdcb.kFlexspiFdcbLength_sflashB2Size)
            self.m_textCtrl_sflashA1Size.Clear()
            self.m_textCtrl_sflashA1Size.write(str(hex(sflashA1Size[0])))
            self.m_textCtrl_sflashA2Size.Clear()
            self.m_textCtrl_sflashA2Size.write(str(hex(sflashA2Size[0])))
            self.m_textCtrl_sflashB1Size.Clear()
            self.m_textCtrl_sflashB1Size.write(str(hex(sflashB1Size[0])))
            self.m_textCtrl_sflashB2Size.Clear()
            self.m_textCtrl_sflashB2Size.write(str(hex(sflashB2Size[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sflashA1Size, uidef_fdcb.kFlexspiFdcbLength_sflashA1Size, int(self.m_textCtrl_sflashA1Size.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sflashA2Size, uidef_fdcb.kFlexspiFdcbLength_sflashA2Size, int(self.m_textCtrl_sflashA2Size.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sflashB1Size, uidef_fdcb.kFlexspiFdcbLength_sflashB1Size, int(self.m_textCtrl_sflashB1Size.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sflashB2Size, uidef_fdcb.kFlexspiFdcbLength_sflashB2Size, int(self.m_textCtrl_sflashB2Size.GetLineText(0), 16))

    def _accessPadSettingOverride( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            csPadSettingOverride = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_csPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_csPadSettingOverride)
            sclkPadSettingOverride = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sclkPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_sclkPadSettingOverride)
            dataPadSettingOverride = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dataPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_dataPadSettingOverride)
            dqsPadSettingOverride = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dqsPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_dqsPadSettingOverride)
            self.m_textCtrl_csPadSettingOverride.Clear()
            self.m_textCtrl_csPadSettingOverride.write(str(hex(csPadSettingOverride[0])))
            self.m_textCtrl_sclkPadSettingOverride.Clear()
            self.m_textCtrl_sclkPadSettingOverride.write(str(hex(sclkPadSettingOverride[0])))
            self.m_textCtrl_dataPadSettingOverride.Clear()
            self.m_textCtrl_dataPadSettingOverride.write(str(hex(dataPadSettingOverride[0])))
            self.m_textCtrl_dqsPadSettingOverride.Clear()
            self.m_textCtrl_dqsPadSettingOverride.write(str(hex(dqsPadSettingOverride[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_csPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_csPadSettingOverride, int(self.m_textCtrl_csPadSettingOverride.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sclkPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_sclkPadSettingOverride, int(self.m_textCtrl_sclkPadSettingOverride.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dataPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_dataPadSettingOverride, int(self.m_textCtrl_dataPadSettingOverride.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dqsPadSettingOverride, uidef_fdcb.kFlexspiFdcbLength_dqsPadSettingOverride, int(self.m_textCtrl_dqsPadSettingOverride.GetLineText(0), 16))

    def _accessTimeoutInMs( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            timeoutInMs = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_timeoutInMs, uidef_fdcb.kFlexspiFdcbLength_timeoutInMs)
            self.m_textCtrl_timeoutInMs.Clear()
            self.m_textCtrl_timeoutInMs.write(str(hex(timeoutInMs[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_timeoutInMs, uidef_fdcb.kFlexspiFdcbLength_timeoutInMs, int(self.m_textCtrl_timeoutInMs.GetLineText(0), 16))

    def _accessCommandInterval( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            commandInterval = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_commandInterval, uidef_fdcb.kFlexspiFdcbLength_commandInterval)
            self.m_textCtrl_commandInterval.Clear()
            self.m_textCtrl_commandInterval.write(str(hex(commandInterval[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_commandInterval, uidef_fdcb.kFlexspiFdcbLength_commandInterval, int(self.m_textCtrl_commandInterval.GetLineText(0), 16))

    def _accessDataValidTime( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            dataValidTime0time_100ps = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dataValidTime, 1)
            dataValidTime0delay_cells = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 1, 1)
            dataValidTime1time_100ps = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 2, 1)
            dataValidTime1delay_cells = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 3, 1)
            self.m_textCtrl_dataValidTime0time_100ps.Clear()
            self.m_textCtrl_dataValidTime0time_100ps.write(str(hex(dataValidTime0time_100ps[0])))
            self.m_textCtrl_dataValidTime0delay_cells.Clear()
            self.m_textCtrl_dataValidTime0delay_cells.write(str(hex(dataValidTime0delay_cells[0])))
            self.m_textCtrl_dataValidTime1time_100ps.Clear()
            self.m_textCtrl_dataValidTime1time_100ps.write(str(hex(dataValidTime1time_100ps[0])))
            self.m_textCtrl_dataValidTime1delay_cells.Clear()
            self.m_textCtrl_dataValidTime1delay_cells.write(str(hex(dataValidTime1delay_cells[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dataValidTime, 1, int(self.m_textCtrl_dataValidTime0time_100ps.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 1, 1, int(self.m_textCtrl_dataValidTime0delay_cells.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 2, 1, int(self.m_textCtrl_dataValidTime1time_100ps.GetLineText(0), 16))
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_dataValidTime + 3, 1, int(self.m_textCtrl_dataValidTime1delay_cells.GetLineText(0), 16))

    def _accessBusyOffset( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            busyOffset = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_busyOffset, uidef_fdcb.kFlexspiFdcbLength_busyOffset)
            self.m_choice_busyOffset.SetSelection(busyOffset[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_busyOffset, uidef_fdcb.kFlexspiFdcbLength_busyOffset, self.m_choice_busyOffset.GetSelection())

    def _accessBusyBitPolarity( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            busyBitPolarity = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_busyBitPolarity, uidef_fdcb.kFlexspiFdcbLength_busyBitPolarity)
            self.m_choice_busyBitPolarity.SetSelection(busyBitPolarity[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_busyBitPolarity, uidef_fdcb.kFlexspiFdcbLength_busyBitPolarity, self.m_choice_busyBitPolarity.GetSelection())

    def _accessLutCustomSeq( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            lutCustomSeq0Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq, 1)
            lutCustomSeq0Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 1, 1)
            lutCustomSeq1Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 4, 1)
            lutCustomSeq1Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 5, 1)
            lutCustomSeq2Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 8, 1)
            lutCustomSeq2Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 9, 1)
            lutCustomSeq3Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 12, 1)
            lutCustomSeq3Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 13, 1)
            lutCustomSeq4Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 16, 1)
            lutCustomSeq4Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 17, 1)
            lutCustomSeq5Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 20, 1)
            lutCustomSeq5Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 21, 1)
            lutCustomSeq6Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 24, 1)
            lutCustomSeq6Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 25, 1)
            lutCustomSeq7Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 28, 1)
            lutCustomSeq7Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 29, 1)
            lutCustomSeq8Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 32, 1)
            lutCustomSeq8Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 33, 1)
            lutCustomSeq9Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 36, 1)
            lutCustomSeq9Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 37, 1)
            lutCustomSeq10Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 40, 1)
            lutCustomSeq10Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 41, 1)
            lutCustomSeq11Num = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 44, 1)
            lutCustomSeq11Id = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 45, 1)
            self.m_choice_lutCustomSeq0Num.SetSelection(lutCustomSeq0Num[0])
            self.m_choice_lutCustomSeq0Id.SetSelection(lutCustomSeq0Id[0])
            self.m_choice_lutCustomSeq1Num.SetSelection(lutCustomSeq1Num[0])
            self.m_choice_lutCustomSeq1Id.SetSelection(lutCustomSeq1Id[0])
            self.m_choice_lutCustomSeq2Num.SetSelection(lutCustomSeq2Num[0])
            self.m_choice_lutCustomSeq2Id.SetSelection(lutCustomSeq2Id[0])
            self.m_choice_lutCustomSeq3Num.SetSelection(lutCustomSeq3Num[0])
            self.m_choice_lutCustomSeq3Id.SetSelection(lutCustomSeq3Id[0])
            self.m_choice_lutCustomSeq4Num.SetSelection(lutCustomSeq4Num[0])
            self.m_choice_lutCustomSeq4Id.SetSelection(lutCustomSeq4Id[0])
            self.m_choice_lutCustomSeq5Num.SetSelection(lutCustomSeq5Num[0])
            self.m_choice_lutCustomSeq5Id.SetSelection(lutCustomSeq5Id[0])
            self.m_choice_lutCustomSeq6Num.SetSelection(lutCustomSeq6Num[0])
            self.m_choice_lutCustomSeq6Id.SetSelection(lutCustomSeq6Id[0])
            self.m_choice_lutCustomSeq7Num.SetSelection(lutCustomSeq7Num[0])
            self.m_choice_lutCustomSeq7Id.SetSelection(lutCustomSeq7Id[0])
            self.m_choice_lutCustomSeq8Num.SetSelection(lutCustomSeq8Num[0])
            self.m_choice_lutCustomSeq8Id.SetSelection(lutCustomSeq8Id[0])
            self.m_choice_lutCustomSeq9Num.SetSelection(lutCustomSeq9Num[0])
            self.m_choice_lutCustomSeq9Id.SetSelection(lutCustomSeq9Id[0])
            self.m_choice_lutCustomSeq10Num.SetSelection(lutCustomSeq10Num[0])
            self.m_choice_lutCustomSeq10Id.SetSelection(lutCustomSeq10Id[0])
            self.m_choice_lutCustomSeq11Num.SetSelection(lutCustomSeq11Num[0])
            self.m_choice_lutCustomSeq11Id.SetSelection(lutCustomSeq11Id[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq, 1, self.m_choice_lutCustomSeq0Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 1, 1, self.m_choice_lutCustomSeq0Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 4, 1, self.m_choice_lutCustomSeq1Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 5, 1, self.m_choice_lutCustomSeq1Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 8, 1, self.m_choice_lutCustomSeq2Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 9, 1, self.m_choice_lutCustomSeq2Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 12, 1, self.m_choice_lutCustomSeq3Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 13, 1, self.m_choice_lutCustomSeq3Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 16, 1, self.m_choice_lutCustomSeq4Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 17, 1, self.m_choice_lutCustomSeq4Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 20, 1, self.m_choice_lutCustomSeq5Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 21, 1, self.m_choice_lutCustomSeq5Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 24, 1, self.m_choice_lutCustomSeq6Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 25, 1, self.m_choice_lutCustomSeq6Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 28, 1, self.m_choice_lutCustomSeq7Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 29, 1, self.m_choice_lutCustomSeq7Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 32, 1, self.m_choice_lutCustomSeq8Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 33, 1, self.m_choice_lutCustomSeq8Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 36, 1, self.m_choice_lutCustomSeq9Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 37, 1, self.m_choice_lutCustomSeq9Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 40, 1, self.m_choice_lutCustomSeq10Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 41, 1, self.m_choice_lutCustomSeq10Id.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 44, 1, self.m_choice_lutCustomSeq11Num.GetSelection())
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_lutCustomSeq + 45, 1, self.m_choice_lutCustomSeq11Id.GetSelection())

    def _accessPageSize( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            pageSize = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_pageSize, uidef_fdcb.kFlexspiFdcbLength_pageSize)
            self.m_textCtrl_pageSize.Clear()
            self.m_textCtrl_pageSize.write(str(hex(pageSize[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_pageSize, uidef_fdcb.kFlexspiFdcbLength_pageSize, int(self.m_textCtrl_pageSize.GetLineText(0), 16))

    def _accessSectorSize( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            sectorSize = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_sectorSize, uidef_fdcb.kFlexspiFdcbLength_sectorSize)
            self.m_textCtrl_sectorSize.Clear()
            self.m_textCtrl_sectorSize.write(str(hex(sectorSize[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_sectorSize, uidef_fdcb.kFlexspiFdcbLength_sectorSize, int(self.m_textCtrl_sectorSize.GetLineText(0), 16))

    def _accessIpcmdSerialClkFreq( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            ipcmdSerialClkFreq = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_ipcmdSerialClkFreq, uidef_fdcb.kFlexspiFdcbLength_ipcmdSerialClkFreq)
            self.m_choice_ipcmdSerialClkFreq.SetSelection(ipcmdSerialClkFreq[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_ipcmdSerialClkFreq, uidef_fdcb.kFlexspiFdcbLength_ipcmdSerialClkFreq, self.m_choice_ipcmdSerialClkFreq.GetSelection())

    def _accessIsUniformBlockSize( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            isUniformBlockSize = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_isUniformBlockSize, uidef_fdcb.kFlexspiFdcbLength_isUniformBlockSize)
            self.m_choice_isUniformBlockSize.SetSelection(isUniformBlockSize[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_isUniformBlockSize, uidef_fdcb.kFlexspiFdcbLength_isUniformBlockSize, self.m_choice_isUniformBlockSize.GetSelection())

    def _accessIsDataOrderSwapped( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            isDataOrderSwapped = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_isDataOrderSwapped, uidef_fdcb.kFlexspiFdcbLength_isDataOrderSwapped)
            self.m_choice_isDataOrderSwapped.SetSelection(isDataOrderSwapped[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_isDataOrderSwapped, uidef_fdcb.kFlexspiFdcbLength_isDataOrderSwapped, self.m_choice_isDataOrderSwapped.GetSelection())

    def _accessSerialNorType( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            serialNorType = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_serialNorType, uidef_fdcb.kFlexspiFdcbLength_serialNorType)
            self.m_choice_serialNorType.SetSelection(serialNorType[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_serialNorType, uidef_fdcb.kFlexspiFdcbLength_serialNorType, self.m_choice_serialNorType.GetSelection())

    def _accessNeedExitNoCmdMode( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            needExitNoCmdMode = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_needExitNoCmdMode, uidef_fdcb.kFlexspiFdcbLength_needExitNoCmdMode)
            self.m_choice_needExitNoCmdMode.SetSelection(needExitNoCmdMode[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_needExitNoCmdMode, uidef_fdcb.kFlexspiFdcbLength_needExitNoCmdMode, self.m_choice_needExitNoCmdMode.GetSelection())

    def _accessHalfClkForNonReadCmd( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            halfClkForNonReadCmd = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_halfClkForNonReadCmd, uidef_fdcb.kFlexspiFdcbLength_halfClkForNonReadCmd)
            self.m_choice_halfClkForNonReadCmd.SetSelection(halfClkForNonReadCmd[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_halfClkForNonReadCmd, uidef_fdcb.kFlexspiFdcbLength_halfClkForNonReadCmd, self.m_choice_halfClkForNonReadCmd.GetSelection())

    def _accessNeedRestoreNoCmdMode( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            needRestoreNoCmdMode = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_needRestoreNoCmdMode, uidef_fdcb.kFlexspiFdcbLength_needRestoreNoCmdMode)
            self.m_choice_needRestoreNoCmdMode.SetSelection(needRestoreNoCmdMode[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_needRestoreNoCmdMode, uidef_fdcb.kFlexspiFdcbLength_needRestoreNoCmdMode, self.m_choice_needRestoreNoCmdMode.GetSelection())

    def _accessBlockSize( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            blockSize = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_blockSize, uidef_fdcb.kFlexspiFdcbLength_blockSize)
            self.m_textCtrl_blockSize.Clear()
            self.m_textCtrl_blockSize.write(str(hex(blockSize[0])))
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_blockSize, uidef_fdcb.kFlexspiFdcbLength_blockSize, int(self.m_textCtrl_blockSize.GetLineText(0), 16))

    def _accessIsNonBlockingMode( self, accessType=kAccessType_Get, fdcbBuf=None):
        if accessType == kAccessType_Set:
            isNonBlockingMode = self._getMemberFromFdcb(fdcbBuf, uidef_fdcb.kFlexspiFdcbOffset_isNonBlockingMode, uidef_fdcb.kFlexspiFdcbLength_isNonBlockingMode)
            self.m_choice_isNonBlockingMode.SetSelection(isNonBlockingMode[0])
        else:
            self._setMemberForFdcb(uidef_fdcb.kFlexspiFdcbOffset_isNonBlockingMode, uidef_fdcb.kFlexspiFdcbLength_isNonBlockingMode, self.m_choice_isNonBlockingMode.GetSelection())

    def _recoverLutTable( self, fdcbBytes ):
        for i in range(uidef_fdcb.kFlexspiFdcbLength_lookupTable):
            self.fdcbBuffer[uidef_fdcb.kFlexspiFdcbOffset_lookupTable + i] = fdcbBytes[uidef_fdcb.kFlexspiFdcbOffset_lookupTable + i]

    def _recoverLastSettings ( self ):
        if os.path.isfile(self.cfgFdcbBinFilename):
            self.m_filePicker_binFile.SetPath(self.cfgFdcbBinFilename)
            fdcbBuf = None
            with open(self.cfgFdcbBinFilename, 'rb') as fileObj:
                fdcbBuf = fileObj.read()
                fileObj.close()
            self._accessTag(kAccessType_Set, fdcbBuf)
            self._accessVersion(kAccessType_Set, fdcbBuf)
            self._accessReadSampleClkSrc(kAccessType_Set, fdcbBuf)
            self._accessCsHoldTime(kAccessType_Set, fdcbBuf)
            self._accessCsSetupTime(kAccessType_Set, fdcbBuf)
            self._accessColumnAddressWidth(kAccessType_Set, fdcbBuf)
            self._accessDeviceModeCfgEnable(kAccessType_Set, fdcbBuf)
            self._accessDeviceModeType(kAccessType_Set, fdcbBuf)
            self._accessWaitTimeCfgCommands(kAccessType_Set, fdcbBuf)
            self._accessDeviceModeSeq(kAccessType_Set, fdcbBuf)
            self._accessDeviceModeArg(kAccessType_Set, fdcbBuf)
            self._accessConfigCmdEnable(kAccessType_Set, fdcbBuf)
            self._accessConfigModeType(kAccessType_Set, fdcbBuf)
            self._accessConfigCmdSeqs(kAccessType_Set, fdcbBuf)
            self._accessConfigCmdArgs(kAccessType_Set, fdcbBuf)
            self._accessControllerMiscOption(kAccessType_Set, fdcbBuf)
            self._accessDeviceType(kAccessType_Set, fdcbBuf)
            self._accessSflashPadType(kAccessType_Set, fdcbBuf)
            self._accessSerialClkFreq(kAccessType_Set, fdcbBuf)
            self._accessLutCustomSeqEnable(kAccessType_Set, fdcbBuf)
            self._accessSflashSize(kAccessType_Set, fdcbBuf)
            self._accessPadSettingOverride(kAccessType_Set, fdcbBuf)
            self._accessTimeoutInMs(kAccessType_Set, fdcbBuf)
            self._accessCommandInterval(kAccessType_Set, fdcbBuf)
            self._accessDataValidTime(kAccessType_Set, fdcbBuf)
            self._accessBusyOffset(kAccessType_Set, fdcbBuf)
            self._accessBusyBitPolarity(kAccessType_Set, fdcbBuf)
            self._accessLutCustomSeq(kAccessType_Set, fdcbBuf)
            self._accessPageSize(kAccessType_Set, fdcbBuf)
            self._accessSectorSize(kAccessType_Set, fdcbBuf)
            self._accessIpcmdSerialClkFreq(kAccessType_Set, fdcbBuf)
            self._accessIsUniformBlockSize(kAccessType_Set, fdcbBuf)
            self._accessIsDataOrderSwapped(kAccessType_Set, fdcbBuf)
            self._accessSerialNorType(kAccessType_Set, fdcbBuf)
            self._accessNeedExitNoCmdMode(kAccessType_Set, fdcbBuf)
            self._accessHalfClkForNonReadCmd(kAccessType_Set, fdcbBuf)
            self._accessNeedRestoreNoCmdMode(kAccessType_Set, fdcbBuf)
            self._accessBlockSize(kAccessType_Set, fdcbBuf)
            self._accessIsNonBlockingMode(kAccessType_Set, fdcbBuf)
            self._recoverLutTable(fdcbBuf)

    def callbackSetLookupTable( self, event ):
        lutFrame = ui_cfg_lut.secBootUiCfgLut(None)
        lutFrame.SetTitle(u"LUT Configuration")
        lutFrame.setNecessaryInfo(self.cfgFdcbBinFilename)
        lutFrame.Show(True)

    def popupMsgBox( self, msgStr ):
        messageText = (msgStr)
        wx.MessageBox(messageText, "Error", wx.OK | wx.ICON_INFORMATION)

    def callbackSelectFdcbFile( self, event ):
        fdcbPath = self.m_filePicker_binFile.GetPath()
        if os.path.isfile(fdcbPath) and os.path.getsize(fdcbPath) == memdef.kMemBlockSize_FDCB:
            if self.cfgFdcbBinFilename != fdcbPath:
                shutil.copy(fdcbPath, self.cfgFdcbBinFilename)
            self._recoverLastSettings()
            self.m_filePicker_binFile.SetPath(fdcbPath)
        else:
            self.popupMsgBox('FDCB file should be 512 bytes raw binary')
            self.m_filePicker_binFile.SetPath('')

    def callbackOk( self, event ):
        self._accessTag(kAccessType_Get)
        self._accessVersion(kAccessType_Get)
        self._accessReadSampleClkSrc(kAccessType_Get)
        self._accessCsHoldTime(kAccessType_Get)
        self._accessCsSetupTime(kAccessType_Get)
        self._accessColumnAddressWidth(kAccessType_Get)
        self._accessDeviceModeCfgEnable(kAccessType_Get)
        self._accessDeviceModeType(kAccessType_Get)
        self._accessWaitTimeCfgCommands(kAccessType_Get)
        self._accessDeviceModeSeq(kAccessType_Get)
        self._accessDeviceModeArg(kAccessType_Get)
        self._accessConfigCmdEnable(kAccessType_Get)
        self._accessConfigModeType(kAccessType_Get)
        self._accessConfigCmdSeqs(kAccessType_Get)
        self._accessConfigCmdArgs(kAccessType_Get)
        self._accessControllerMiscOption(kAccessType_Get)
        self._accessDeviceType(kAccessType_Get)
        self._accessSflashPadType(kAccessType_Get)
        self._accessSerialClkFreq(kAccessType_Get)
        self._accessLutCustomSeqEnable(kAccessType_Get)
        self._accessSflashSize(kAccessType_Get)
        self._accessPadSettingOverride(kAccessType_Get)
        self._accessTimeoutInMs(kAccessType_Get)
        self._accessCommandInterval(kAccessType_Get)
        self._accessDataValidTime(kAccessType_Get)
        self._accessBusyOffset(kAccessType_Get)
        self._accessBusyBitPolarity(kAccessType_Get)
        self._accessLutCustomSeq(kAccessType_Get)
        self._accessPageSize(kAccessType_Get)
        self._accessSectorSize(kAccessType_Get)
        self._accessIpcmdSerialClkFreq(kAccessType_Get)
        self._accessIsUniformBlockSize(kAccessType_Get)
        self._accessIsDataOrderSwapped(kAccessType_Get)
        self._accessSerialNorType(kAccessType_Get)
        self._accessNeedExitNoCmdMode(kAccessType_Get)
        self._accessHalfClkForNonReadCmd(kAccessType_Get)
        self._accessNeedRestoreNoCmdMode(kAccessType_Get)
        self._accessBlockSize(kAccessType_Get)
        self._accessIsNonBlockingMode(kAccessType_Get)
        with open(self.cfgFdcbBinFilename, 'wb') as fileObj:
            fileObj.write(self.fdcbBuffer)
            fileObj.close()
        uivar.setRuntimeSettings(False)
        self.Show(False)
        runtimeSettings = uivar.getRuntimeSettings()
        sound.playSoundEffect(runtimeSettings[1], runtimeSettings[2], uidef.kSoundEffectFilename_Progress)

    def callbackCancel( self, event ):
        uivar.setRuntimeSettings(False)
        self.Show(False)

    def callbackClose( self, event ):
        uivar.setRuntimeSettings(False)
        self.Show(False)

