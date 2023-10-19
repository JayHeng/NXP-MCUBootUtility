#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import os
import shutil
import RTyyyy_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from win import bootDeviceWin_XMCD
from gen import RTyyyy_gendef
from run import RTyyyy_rundef
from utils import sound

class secBootUiCfgXmcd(bootDeviceWin_XMCD.bootDeviceWin_XMCD):

    def __init__(self, parent):
        bootDeviceWin_XMCD.bootDeviceWin_XMCD.__init__(self, parent)
        self._setLanguage()
        xmcdSettingsDict = uivar.getBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_Xmcd)
        self.xmcdSettingsDict = xmcdSettingsDict.copy()
        self.destBinFilename = None
        self.xmcdSource = self.xmcdSettingsDict['xmcdSource']
        self.userBinFile = self.xmcdSettingsDict['userBinFile']
        self.xmcdHeader = self.xmcdSettingsDict['xmcdHeader']
        self.xmcdOption0 = self.xmcdSettingsDict['xmcdOption0']
        self.xmcdOption1 = self.xmcdSettingsDict['xmcdOption1']
        self.xmcdOption2 = self.xmcdSettingsDict['xmcdOption2']

    def _setLanguage( self ):
        runtimeSettings = uivar.getRuntimeSettings()
        langIndex = runtimeSettings[3]
        self.m_staticText_xmcdSource.SetLabel(uilang.kSubLanguageContentDict['sText_xmcdSource'][langIndex])
        self.m_staticText_memoryInterface.SetLabel(uilang.kSubLanguageContentDict['sText_memoryInterface'][langIndex])
        self.m_staticText_interfaceInstance.SetLabel(uilang.kSubLanguageContentDict['sText_interfaceInstance'][langIndex])
        self.m_staticText_cfgBlockType.SetLabel(uilang.kSubLanguageContentDict['sText_configBlockType'][langIndex])
        self.m_notebook_flexspiRamOpt0.SetPageText(0, uilang.kSubLanguageContentDict['panel_flexspiRamOpt0'][langIndex])
        self.m_staticText_deviceType.SetLabel(uilang.kSubLanguageContentDict['sText_deviceType'][langIndex])
        self.m_staticText_miscMode.SetLabel(uilang.kSubLanguageContentDict['sText_miscMode'][langIndex])
        self.m_staticText_maxFrequency.SetLabel(uilang.kSubLanguageContentDict['sText_maxFrequency'][langIndex])
        self.m_staticText_deviceSizeInMB.SetLabel(uilang.kSubLanguageContentDict['sText_deviceSizeInMB'][langIndex])
        self.m_notebook_flexspiRamOpt1.SetPageText(0, uilang.kSubLanguageContentDict['panel_flexspiRamOpt1'][langIndex])
        self.m_staticText_ramConnection.SetLabel(uilang.kSubLanguageContentDict['sText_ramConnection'][langIndex])
        self.m_staticText_dqsPinmuxGroup.SetLabel(uilang.kSubLanguageContentDict['sText_dqsPinmuxGroup'][langIndex])
        self.m_staticText_dataPinmuxGroup.SetLabel(uilang.kSubLanguageContentDict['sText_dataPinmuxGroup'][langIndex])
        self.m_staticText_writeDummyCycles.SetLabel(uilang.kSubLanguageContentDict['sText_writeDummyCycles'][langIndex])
        self.m_staticText_readDummyCycles.SetLabel(uilang.kSubLanguageContentDict['sText_readDummyCycles'][langIndex])
        self.m_notebook_semcSdramOpt.SetPageText(0, uilang.kSubLanguageContentDict['panel_semcSdramOpt'][langIndex])
        self.m_staticText_clkFreq.SetLabel(uilang.kSubLanguageContentDict['sText_clkFreq'][langIndex])
        self.m_staticText_deviceSizeInKB.SetLabel(uilang.kSubLanguageContentDict['sText_deviceSizeInKB'][langIndex])
        self.m_staticText_portSize.SetLabel(uilang.kSubLanguageContentDict['sText_ioPortSize'][langIndex])
        self.m_staticText_xmcdBinFile.SetLabel(uilang.kSubLanguageContentDict['sText_xmcdBinFile'][langIndex])
        self.m_button_ok.SetLabel(uilang.kSubLanguageContentDict['button_xmcd_ok'][langIndex])
        self.m_button_cancel.SetLabel(uilang.kSubLanguageContentDict['button_xmcd_cancel'][langIndex])

    def setNecessaryInfo( self, binFilename, mcuDevice ):
        if mcuDevice == uidef.kMcuDevice_iMXRT117x or mcuDevice == uidef.kMcuDevice_iMXRT116x:
            #miscMode = ['1.8V', '3.3V']
            pass
        elif mcuDevice == uidef.kMcuDevice_iMXRT118x:
            miscMode = ['Differential clock driven', 'Single-ended clock driven']
            self.m_choice_miscMode.Clear()
            self.m_choice_miscMode.SetItems(miscMode)
            self.m_choice_miscMode.SetSelection(0)
        self.destBinFilename = binFilename
        self._recoverLastSettings()

    def _recoverLastSettings ( self ):
        self.m_choice_xmcdSource.SetSelection(self.m_choice_xmcdSource.FindString(self.xmcdSettingsDict['xmcdSource']))
        self._getXmcdSource()
        if self.xmcdSource == 'Use XMCD option':
            memInterface = (self.xmcdHeader & 0x00F00000) >> 20
            self.m_choice_memoryInterface.SetSelection(memInterface)
            self._getMemoryInterface()
            interfaceInstance = (self.xmcdHeader & 0x000F0000) >> 16
            if interfaceInstance == 0:
                interfaceInstance = 1
            self.m_choice_interfaceInstance.SetSelection(interfaceInstance - 1)
            self.m_choice_cfgBlockType.SetSelection((self.xmcdHeader & 0x0000F000) >> 12)
            if memInterface == 0:   # FlexSPI
                self.m_choice_deviceType.SetSelection((self.xmcdOption0 & 0x00F00000) >> 20)
                self.m_choice_miscMode.SetSelection((self.xmcdOption0 & 0x0000F000) >> 12)
                self.m_choice_maxFrequency.SetSelection(((self.xmcdOption0 & 0x00000F00) >> 8) -1)
                self.m_textCtrl_deviceSizeInMB.Clear()
                self.m_textCtrl_deviceSizeInMB.write(str((self.xmcdOption0 & 0x000000FF) >> 0))
                self.m_choice_ramConnection.SetSelection((self.xmcdOption1 & 0xF0000000) >> 28)
                self.m_choice_dqsPinmuxGroup.SetSelection((self.xmcdOption1 & 0x00F00000) >> 20)
                self.m_choice_dataPinmuxGroup.SetSelection((self.xmcdOption1 & 0x000F0000) >> 16)
                self.m_textCtrl_writeDummyCycles.Clear()
                self.m_textCtrl_writeDummyCycles.write(str((self.xmcdOption1 & 0x000000F0) >> 4))
                self.m_textCtrl_readDummyCycles.Clear()
                self.m_textCtrl_readDummyCycles.write(str((self.xmcdOption1 & 0x0000000F) >> 0))
            elif memInterface == 1: # SEMC
                self.m_textCtrl_clkFreq.Clear()
                self.m_textCtrl_clkFreq.write(str((self.xmcdOption0 & 0xFF000000) >> 24))
                self.m_textCtrl_deviceSizeInKB.Clear()
                self.m_textCtrl_deviceSizeInKB.write(str(self.xmcdOption1))
                self.m_choice_portSize.SetSelection((self.xmcdOption2 & 0x000000FF) >> 0)
            else:
                pass
        elif self.xmcdSource == 'Use XMCD bin file':
            self.m_filePicker_xmcdBinFile.SetPath(self.userBinFile)
        else:
            pass

    def _getXmcdSource( self ):
        txt = self.m_choice_xmcdSource.GetString(self.m_choice_xmcdSource.GetSelection())
        self.xmcdSource = txt
        if txt == 'Disable XMCD':
            self.xmcdSettingsDict['isXmcdEnabled'] = False
            self.m_panel_flexspiRamOpt0.Enable( False )
            self.m_panel_flexspiRamOpt1.Enable( False )
            self.m_panel_semcSdramOpt.Enable( False )
            self.m_filePicker_xmcdBinFile.Enable( False )
            self.m_choice_memoryInterface.Enable( False )
            self.m_choice_interfaceInstance.Enable( False )
            self.m_choice_cfgBlockType.Enable( False )
        elif txt == 'Use XMCD option':
            self.xmcdSettingsDict['isXmcdEnabled'] = True
            self.m_choice_memoryInterface.Enable( True )
            self.m_choice_interfaceInstance.Enable( True )
            self.m_choice_cfgBlockType.Enable( False )
            self.m_panel_flexspiRamOpt0.Enable( True )
            self.m_panel_flexspiRamOpt1.Enable( True )
            self.m_panel_semcSdramOpt.Enable( True )
            self.m_filePicker_xmcdBinFile.Enable( False )
        elif txt == 'Use XMCD bin file':
            self.m_choice_memoryInterface.Enable( False )
            self.m_choice_interfaceInstance.Enable( False )
            self.m_choice_cfgBlockType.Enable( False )
            self.xmcdSettingsDict['isXmcdEnabled'] = True
            self.m_panel_flexspiRamOpt0.Enable( False )
            self.m_panel_flexspiRamOpt1.Enable( False )
            self.m_panel_semcSdramOpt.Enable( False )
            self.m_filePicker_xmcdBinFile.Enable( True )
        else:
            pass

    def _getMemoryInterface( self ):
        val = self.m_choice_memoryInterface.GetSelection()
        self.xmcdHeader = (self.xmcdHeader & 0xFF0FFFFF) | (val << 20)
        txt = self.m_choice_memoryInterface.GetString(val)
        if txt == 'FlexSPI':
            self.m_choice_interfaceInstance.Enable( True )
            self.m_panel_flexspiRamOpt0.Enable( True )
            self.m_panel_flexspiRamOpt1.Enable( True )
            self.m_panel_semcSdramOpt.Enable( False )
            self.xmcdOption0 = self.xmcdOption0 & 0xFFF0FFFF
            self.xmcdOption1 = self.xmcdOption1 & 0xF0FFF0FF
            self.xmcdOption2 = 0
            self.xmcdOption0 = (self.xmcdOption0 & 0x0FFFFFFF) | (0xC << 28)
        elif txt == 'SEMC':
            self.m_choice_interfaceInstance.SetSelection(0)
            self.m_choice_interfaceInstance.Enable( False )
            self.m_panel_flexspiRamOpt0.Enable( False )
            self.m_panel_flexspiRamOpt1.Enable( False )
            self.m_panel_semcSdramOpt.Enable( True )
            self.xmcdOption0 = (self.xmcdOption0 & 0xFF00FFFF) | (0x0 << 16)
            self.xmcdOption0 = (self.xmcdOption0 & 0xFFFF0000) | (0x01A1 << 0)
        else:
            pass

    def _getInterfaceInstance( self ):
        val = self.m_choice_interfaceInstance.GetSelection() + 1
        self.xmcdHeader = (self.xmcdHeader & 0xFFF0FFFF) | (val << 16)

    def _getCfgBlockType( self ):
        val = self.m_choice_cfgBlockType.GetSelection()
        self.xmcdHeader = (self.xmcdHeader & 0xFFFF0FFF) | (val << 12)

    def _getDeviceType( self ):
        val = self.m_choice_deviceType.GetSelection()
        self.xmcdOption0 = (self.xmcdOption0 & 0xFF0FFFFF) | (val << 20)

    def _getMiscMode( self ):
        val = self.m_choice_miscMode.GetSelection()
        self.xmcdOption0 = (self.xmcdOption0 & 0xFFFF0FFF) | (val << 12)

    def _getMaxFrequency( self ):
        val = self.m_choice_maxFrequency.GetSelection() + 1
        self.xmcdOption0 = (self.xmcdOption0 & 0xFFFFF0FF) | (val << 8)

    def _getDeviceSizeMB( self ):
        val = int(self.m_textCtrl_deviceSizeInMB.GetLineText(0))
        if val > 255:
            self.popupMsgBox('Device size should not be more than 255MB')
            return False
        self.xmcdOption0 = (self.xmcdOption0 & 0xFFFFFF00) | (val << 0)
        return True

    def _getRamConnection( self ):
        val = self.m_choice_ramConnection.GetSelection()
        self.xmcdOption1 = (self.xmcdOption1 & 0x0FFFFFFF) | (val << 28)

    def _getDqsPinmuxGroup( self ):
        val = self.m_choice_dqsPinmuxGroup.GetSelection()
        self.xmcdOption1 = (self.xmcdOption1 & 0xFF0FFFFF) | (val << 20)

    def _getDataPinmuxGroup( self ):
        val = self.m_choice_dataPinmuxGroup.GetSelection()
        self.xmcdOption1 = (self.xmcdOption1 & 0xFFF0FFFF) | (val << 16)

    def _getWriteDummyCycles( self ):
        val = int(self.m_textCtrl_writeDummyCycles.GetLineText(0))
        if val > 15:
            self.popupMsgBox('Write dummy cycle should not be more than 15')
            return False
        self.xmcdOption1 = (self.xmcdOption1 & 0xFFFFFF0F) | (val << 4)
        return True

    def _getReadDummyCycles( self ):
        val = int(self.m_textCtrl_readDummyCycles.GetLineText(0))
        if val > 15:
            self.popupMsgBox('Read dummy cycle should not be more than 15')
            return False
        self.xmcdOption1 = (self.xmcdOption1 & 0xFFFFFFF0) | (val << 0)
        return True

    def _getClkFreq( self ):
        val = int(self.m_textCtrl_clkFreq.GetLineText(0))
        if val > 255:
            self.popupMsgBox('Clk freq should not be more than 255MHz')
            return False
        self.xmcdOption0 = (self.xmcdOption0 & 0x00FFFFFF) | (val << 24)
        return True

    def _getDeviceSizeKB( self ):
        val = int(self.m_textCtrl_deviceSizeInKB.GetLineText(0))
        self.xmcdOption1 = val

    def _getPortSize( self ):
        val = self.m_choice_portSize.GetSelection()
        self.xmcdOption2 = (self.xmcdOption2 & 0xFFFFFF00) | (val << 0)

    def _calcOptionSize( self ):
        optionSize = 0
        if self.xmcdOption1 != 0:
            optionSize = 1
        self.xmcdOption0 = (self.xmcdOption0 & 0xF0FFFFFF) | (optionSize << 24)

    def _calcCfgBlockSize( self ):
        size = 0
        memInterface = (self.xmcdHeader & 0x00F00000) >> 20
        if memInterface == 0:   # FlexSPI
            if self.xmcdOption1 != 0:
                size = 12
            else:
                size = 8
        elif memInterface == 1: # SEMC
            size = 13
        else:
            pass
        self.xmcdHeader = (self.xmcdHeader & 0xFFFFF000) | (size << 0)

    def _getXmcdBinFile( self ):
        status = True
        xmcdBinFile = self.m_filePicker_xmcdBinFile.GetPath().encode('utf-8').encode("gbk")
        if os.path.isfile(xmcdBinFile):
            shutil.copy(xmcdBinFile, self.destBinFilename)
            self.userBinFile = xmcdBinFile.decode("gbk")
        else:
            status = False
            self.userBinFile = 'N/A'
            self.popupMsgBox('You should specify a xmcd bin file')
        return status

    def callbackSetXmcdSource( self, event ):
        self._getXmcdSource()
        if self.xmcdSource == 'Use XMCD option':
            self._getMemoryInterface()

    def callbackSetMemoryInterface( self, event ):
        self._getMemoryInterface()

    def _fillDataIntoBinFile( self, filename, val32, valBytes):
        with open(filename, 'ab') as fileObj:
            byteStr = ''
            for i in range(valBytes):
                byteStr = chr((val32 & (0xFF << (i * 8))) >> (i * 8))
                fileObj.write(byteStr)
            fileObj.close()

    def callbackOk( self, event ):
        self._getXmcdSource()
        if self.xmcdSource == 'Use XMCD option':
            self._getMemoryInterface()
            self._getInterfaceInstance()
            self._getCfgBlockType()
            memInterface = (self.xmcdHeader & 0x00F00000) >> 20
            if memInterface == 0:   # FlexSPI
                self._getDeviceType()
                self._getMiscMode()
                self._getMaxFrequency()
                if not self._getDeviceSizeMB():
                    return
                self._getRamConnection()
                self._getDqsPinmuxGroup()
                self._getDataPinmuxGroup()
                if not self._getWriteDummyCycles():
                    return
                if not self._getReadDummyCycles():
                    return
                self._calcOptionSize()
                self._calcCfgBlockSize()
            elif memInterface == 1: # SEMC
                if not self._getClkFreq():
                    return
                self._getDeviceSizeKB()
                self._getPortSize()
                self._calcCfgBlockSize()
            else:
                pass
            blockSize = self.xmcdHeader & 0x00000FFF
            with open(self.destBinFilename, 'wb') as fileObj:
                fileObj.close()
            if blockSize >= 8:
                self._fillDataIntoBinFile(self.destBinFilename, self.xmcdHeader, 4)
                self._fillDataIntoBinFile(self.destBinFilename, self.xmcdOption0, 4)
            if blockSize >= 12:
                self._fillDataIntoBinFile(self.destBinFilename, self.xmcdOption1, 4)
            if blockSize == 13:
                self._fillDataIntoBinFile(self.destBinFilename, self.xmcdOption2, 1)
        elif self.xmcdSource == 'Use XMCD bin file':
            if not self._getXmcdBinFile():
                return
        else:
            pass
        self.xmcdSettingsDict['xmcdSource'] = self.xmcdSource
        self.xmcdSettingsDict['userBinFile'] = self.userBinFile
        self.xmcdSettingsDict['xmcdHeader'] = self.xmcdHeader
        self.xmcdSettingsDict['xmcdOption0'] = self.xmcdOption0
        self.xmcdSettingsDict['xmcdOption1'] = self.xmcdOption1
        self.xmcdSettingsDict['xmcdOption2'] = self.xmcdOption2
        uivar.setBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_Xmcd, self.xmcdSettingsDict)
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

