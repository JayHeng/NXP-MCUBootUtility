#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import math
import serial.tools.list_ports
import pywinusb.hid
import RTyyyy_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from win import secBootWin
from gen import gendef
from run import rundef
from fuse import RTyyyy_fusedef
from fuse import RTxxx_otpdef
from utils import sound

kRetryDetectTimes = 5

s_isGaugeWorking = False
s_curGauge = 0
s_maxGauge = 0
s_gaugeIntervalSec = 1

class secBootUi(secBootWin.secBootWin):

    def __init__(self, parent):
        secBootWin.secBootWin.__init__(self, parent)
        self.m_bitmap_nxp.SetBitmap(wx.Bitmap( u"../img/logo_nxp.png", wx.BITMAP_TYPE_ANY ))

        self.exeBinRoot = os.getcwd()
        self.exeTopRoot = os.path.dirname(self.exeBinRoot)
        exeMainFile = os.path.join(self.exeTopRoot, 'src', 'main.py')
        if not os.path.isfile(exeMainFile):
            self.exeTopRoot = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        uivar.setRuntimeSettings(None, self.exeTopRoot)
        uivar.initVar(os.path.join(self.exeTopRoot, 'bin', 'nsb_settings.json'))
        toolCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Tool)
        self.toolCommDict = toolCommDict.copy()

        self.fuseSettingFilename = os.path.join(self.exeTopRoot, 'bin', 'fuse_settings.json')

        self.logFolder = os.path.join(self.exeTopRoot, 'gen', 'cmdlog_file')
        self.logFilename = os.path.join(self.exeTopRoot, 'gen', 'cmdlog_file', 'log.txt')

        self.connectStatusColor = None
        self.hasDynamicLableBeenInit = False

        self.languageIndex = 0
        self._initLanguage()
        self.setLanguage()

        self.toolRunMode = None
        self._initToolRunMode()
        self.setToolRunMode()

        self.isDymaticUsbDetection = None
        self._initUsbDetection()
        self.setUsbDetection()

        self.soundEffectType = None
        self._initSoundEffect()
        self.setSoundEffect()

        self.isSbFileEnabledToGen = None
        self._initGenSbFile()
        self.setGenSbFile()

        self.isAutomaticImageReadback = None
        self._initImageReadback()
        self.setImageReadback()

        self.flashloaderResident = None
        self._initFlashloaderResident()
        self.setFlashloaderResident()

        self.updateConnectStatus()

        self.sbEnableBootDeviceMagic = None
        self.sbAccessBootDeviceMagic = None

        self.mcuSeries = None
        self.mcuDevice = None
        self.bootDevice = None
        self.isMcuSeriesChanged = False
        self.isMcuDeviceChanged = False
        self._initTargetSetupValue()
        self.setTargetSetupValue()

        self.efuseGroupSel = None
        self._initEfuseGroup()
        self.setEfuseGroup()

        self.isAutomaticEfuseLocker = None
        self._initEfuseLocker()
        self.setEfuseLocker()

        self.flexspiBootInstance = 0
        self.flexspiBootInstanceFromFuse = uidef.kFlexspiInstance_Max
        self.getFlexspiBootInstance()

        self.isIvtEntryResetHandler = None
        self._initIvtEntryType()
        self.setIvtEntryType()

        self.edgelockFwEn = None
        self._initEdgelockFwOption()
        self.setEdgelockFwOption()

        self.isUartPortSelected = None
        self.isUsbhidPortSelected = None
        self.uartComPort = None
        self.uartBaudrate = None
        self.usbhidVid = None
        self.usbhidPid = None
        self.isUsbhidConnected = False
        self.usbhidToConnect = [None] * 2
        self._initPortSetupValue()

        self.soundEffectFilenameForTask = None

        self.isOneStepConnectMode = None
        self.initOneStepConnectMode()

        self.setBootLogInfo()

    def _initToolRunMode( self ):
        if self.toolCommDict['toolRunMode'] == uidef.kToolRunMode_Entry:
            self.m_menuItem_runModeEntry.Check(True)
            self.m_menuItem_runModeMaster.Check(False)
            self.m_menuItem_runModeOta.Check(False)
        elif self.toolCommDict['toolRunMode'] == uidef.kToolRunMode_Master:
            self.m_menuItem_runModeEntry.Check(False)
            self.m_menuItem_runModeMaster.Check(True)
            self.m_menuItem_runModeOta.Check(False)
        elif self.toolCommDict['toolRunMode'] == uidef.kToolRunMode_SblOta:
            self.m_menuItem_runModeEntry.Check(False)
            self.m_menuItem_runModeMaster.Check(False)
            self.m_menuItem_runModeOta.Check(True)
        else:
            pass

    def setToolRunMode( self ):
        if self.m_menuItem_runModeEntry.IsChecked():
            self.toolRunMode = uidef.kToolRunMode_Entry
        elif self.m_menuItem_runModeMaster.IsChecked():
            self.toolRunMode = uidef.kToolRunMode_Master
        elif self.m_menuItem_runModeOta.IsChecked():
            self.toolRunMode = uidef.kToolRunMode_SblOta
        else:
            pass
        self.toolCommDict['toolRunMode'] = self.toolRunMode

    def _initUsbDetection( self ):
        if self.toolCommDict['isDymaticUsbDetection']:
            self.m_menuItem_usbDetectionDynamic.Check(True)
            self.m_menuItem_usbDetectionStatic.Check(False)
        else:
            self.m_menuItem_usbDetectionDynamic.Check(False)
            self.m_menuItem_usbDetectionStatic.Check(True)

    def setUsbDetection( self ):
        self.isDymaticUsbDetection = self.m_menuItem_usbDetectionDynamic.IsChecked()
        self.toolCommDict['isDymaticUsbDetection'] = self.isDymaticUsbDetection

    def _initSoundEffect( self ):
        if self.toolCommDict['soundEffectType'] == 'quiet':
            self.m_menuItem_soundEffectQuiet.Check(True)
            self.m_menuItem_soundEffectMario.Check(False)
            self.m_menuItem_soundEffectContra.Check(False)
        elif self.toolCommDict['soundEffectType'] == 'mario':
            self.m_menuItem_soundEffectQuiet.Check(False)
            self.m_menuItem_soundEffectMario.Check(True)
            self.m_menuItem_soundEffectContra.Check(False)
        elif self.toolCommDict['soundEffectType'] == 'contra':
            self.m_menuItem_soundEffectQuiet.Check(False)
            self.m_menuItem_soundEffectMario.Check(False)
            self.m_menuItem_soundEffectContra.Check(True)
        else:
            pass

    def setSoundEffect( self ):
        if self.m_menuItem_soundEffectQuiet.IsChecked():
            self.soundEffectType = 'quiet'
        elif self.m_menuItem_soundEffectMario.IsChecked():
            self.soundEffectType = 'mario'
        elif self.m_menuItem_soundEffectContra.IsChecked():
            self.soundEffectType = 'contra'
        else:
            pass
        self.toolCommDict['soundEffectType'] = self.soundEffectType
        uivar.setRuntimeSettings(None, None, self.soundEffectType)

    def playSoundEffect( self, soundFilename ):
        sound.playSoundEffect(self.exeTopRoot, self.soundEffectType, soundFilename)

    def _initGenSbFile( self ):
        if self.toolCommDict['isSbFileEnabledToGen']:
            self.m_menuItem_genSbFileYes.Check(True)
            self.m_menuItem_genSbFileNo.Check(False)
        else:
            self.m_menuItem_genSbFileYes.Check(False)
            self.m_menuItem_genSbFileNo.Check(True)

    def setGenSbFile( self ):
        self.isSbFileEnabledToGen = self.m_menuItem_genSbFileYes.IsChecked()
        self.toolCommDict['isSbFileEnabledToGen'] = self.isSbFileEnabledToGen
        langIndex = 0
        if self.m_menuItem_english.IsChecked():
            langIndex = uilang.kLanguageIndex_English
        else:
            langIndex = uilang.kLanguageIndex_Chinese
        if self.isSbFileEnabledToGen:
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_genSbFileAction'][langIndex])
        else:
            self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction'][langIndex])

    def _initImageReadback( self ):
        if self.toolCommDict['isAutomaticImageReadback']:
            self.m_menuItem_imageReadbackAutomatic.Check(True)
            self.m_menuItem_imageReadbackManual.Check(False)
        else:
            self.m_menuItem_imageReadbackAutomatic.Check(False)
            self.m_menuItem_imageReadbackManual.Check(True)

    def setImageReadback( self ):
        self.isAutomaticImageReadback = self.m_menuItem_imageReadbackAutomatic.IsChecked()
        self.toolCommDict['isAutomaticImageReadback'] = self.isAutomaticImageReadback

    def _initFlashloaderResident( self ):
        if self.toolCommDict['flashloaderResident'] == None:
            self.m_menuItem_flashloaderResidentDefault.Check(True)
            self.m_menuItem_flashloaderResidentItcm.Check(False)
            self.m_menuItem_flashloaderResidentDtcm.Check(False)
            self.m_menuItem_flashloaderResidentOcram.Check(False)
        elif self.toolCommDict['flashloaderResident'] == 'itcm':
            self.m_menuItem_flashloaderResidentDefault.Check(False)
            self.m_menuItem_flashloaderResidentItcm.Check(True)
            self.m_menuItem_flashloaderResidentDtcm.Check(False)
            self.m_menuItem_flashloaderResidentOcram.Check(False)
        elif self.toolCommDict['flashloaderResident'] == 'dtcm':
            self.m_menuItem_flashloaderResidentDefault.Check(False)
            self.m_menuItem_flashloaderResidentItcm.Check(False)
            self.m_menuItem_flashloaderResidentDtcm.Check(True)
            self.m_menuItem_flashloaderResidentOcram.Check(False)
        elif self.toolCommDict['flashloaderResident'] == 'ocram':
            self.m_menuItem_flashloaderResidentDefault.Check(False)
            self.m_menuItem_flashloaderResidentItcm.Check(False)
            self.m_menuItem_flashloaderResidentDtcm.Check(False)
            self.m_menuItem_flashloaderResidentOcram.Check(True)
        else:
            pass

    def setFlashloaderResident( self ):
        if self.m_menuItem_flashloaderResidentDefault.IsChecked():
            self.flashloaderResident = None
        elif self.m_menuItem_flashloaderResidentItcm.IsChecked():
            self.flashloaderResident = 'itcm'
        elif self.m_menuItem_flashloaderResidentDtcm.IsChecked():
            self.flashloaderResident = 'dtcm'
        elif self.m_menuItem_flashloaderResidentOcram.IsChecked():
            self.flashloaderResident = 'ocram'
        else:
            pass
        self.toolCommDict['flashloaderResident'] = self.flashloaderResident

    def _initEfuseGroup( self ):
        if self.toolCommDict['efuseGroupSel'] == 0:
            self.m_menuItem_efuseGroup0.Check(True)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 1:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(True)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 2:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(True)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 3:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(True)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 4:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(True)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 5:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(True)
            self.m_menuItem_efuseGroup6.Check(False)
        elif self.toolCommDict['efuseGroupSel'] == 6:
            self.m_menuItem_efuseGroup0.Check(False)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(True)
        else:
            pass

    def setEfuseGroup( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
            if self.isMcuDeviceChanged:
                self.toolCommDict['efuseGroupSel'] = 1
                self._initEfuseGroup()
                self.isMcuDeviceChanged = False
            if self.m_menuItem_efuseGroup0.IsChecked():
                self.efuseGroupSel = 0
            elif self.m_menuItem_efuseGroup1.IsChecked():
                self.efuseGroupSel = 1
            elif self.m_menuItem_efuseGroup2.IsChecked():
                self.efuseGroupSel = 2
            elif self.m_menuItem_efuseGroup3.IsChecked():
                self.efuseGroupSel = 3
            elif self.m_menuItem_efuseGroup4.IsChecked():
                self.efuseGroupSel = 4
            elif self.m_menuItem_efuseGroup5.IsChecked():
                self.efuseGroupSel = 5
            elif self.m_menuItem_efuseGroup6.IsChecked():
                self.efuseGroupSel = 6
            else:
                pass
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            if self.isMcuDeviceChanged:
                self.toolCommDict['efuseGroupSel'] = 0
                self._initEfuseGroup()
                self.isMcuDeviceChanged = False
            if self.m_menuItem_efuseGroup0.IsChecked():
                self.efuseGroupSel = 0
            elif self.m_menuItem_efuseGroup1.IsChecked():
                self.efuseGroupSel = 1
            elif self.m_menuItem_efuseGroup2.IsChecked():
                self.efuseGroupSel = 2
            elif self.m_menuItem_efuseGroup3.IsChecked():
                self.efuseGroupSel = 3
            else:
                pass
            if self.mcuDevice == uidef.kMcuDevice_iMXRT118x:
                if self.m_menuItem_efuseGroup4.IsChecked():
                    self.efuseGroupSel = 4
                elif self.m_menuItem_efuseGroup5.IsChecked():
                    self.efuseGroupSel = 5
                elif self.m_menuItem_efuseGroup6.IsChecked():
                    self.efuseGroupSel = 6
                else:
                    pass
        else:
            self.efuseGroupSel = 0
            self.m_menuItem_efuseGroup0.Check(True)
            self.m_menuItem_efuseGroup1.Check(False)
            self.m_menuItem_efuseGroup2.Check(False)
            self.m_menuItem_efuseGroup3.Check(False)
            self.m_menuItem_efuseGroup4.Check(False)
            self.m_menuItem_efuseGroup5.Check(False)
            self.m_menuItem_efuseGroup6.Check(False)
        self.toolCommDict['efuseGroupSel'] = self.efuseGroupSel

    def _initEfuseLocker( self ):
        if self.toolCommDict['isAutomaticEfuseLocker']:
            self.m_menuItem_efuseLockerAutomatic.Check(True)
            self.m_menuItem_efuseLockerManual.Check(False)
        else:
            self.m_menuItem_efuseLockerAutomatic.Check(False)
            self.m_menuItem_efuseLockerManual.Check(True)

    def setEfuseLocker( self ):
        if self.m_menuItem_efuseLockerAutomatic.IsChecked():
            self.isAutomaticEfuseLocker = True
        elif self.m_menuItem_efuseLockerManual.IsChecked():
            self.isAutomaticEfuseLocker = False
        else:
            pass
        self.toolCommDict['isAutomaticEfuseLocker'] = self.isAutomaticEfuseLocker

    def getFlexspiBootInstance( self ):
        if self.mcuSeries == uidef.kMcuSeries_iMXRT11yy or \
           self.mcuDevice == uidef.kMcuDevice_iMXRT1060X or \
           self.mcuDevice == uidef.kMcuDevice_iMXRT700:
            if self.flexspiBootInstanceFromFuse == uidef.kFlexspiInstance_Max:
                toolCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Tool)
                self.flexspiBootInstance = toolCommDict['flexspiBootInstance']
            else:
                self.flexspiBootInstance = self.flexspiBootInstanceFromFuse
                self.toolCommDict['flexspiBootInstance'] = self.flexspiBootInstance
                uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)
        else:
            self.flexspiBootInstance = 0
            self.toolCommDict['flexspiBootInstance'] = self.flexspiBootInstance
            uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)

    def _initIvtEntryType( self ):
        if self.toolCommDict['isIvtEntryResetHandler']:
            self.m_menuItem_ivtEntryResetHandler.Check(True)
            self.m_menuItem_ivtEntryVectorTable.Check(False)
        else:
            self.m_menuItem_ivtEntryResetHandler.Check(False)
            self.m_menuItem_ivtEntryVectorTable.Check(True)

    def setIvtEntryType( self ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            if self.m_menuItem_ivtEntryResetHandler.IsChecked():
                self.isIvtEntryResetHandler = True
            elif self.m_menuItem_ivtEntryVectorTable.IsChecked():
                self.isIvtEntryResetHandler = False
            else:
                pass
        else:
            self.isIvtEntryResetHandler = True
            self.m_menuItem_ivtEntryResetHandler.Check(True)
            self.m_menuItem_ivtEntryVectorTable.Check(False)
        self.toolCommDict['isIvtEntryResetHandler'] = self.isIvtEntryResetHandler

    def _initEdgelockFwOption( self ):
        if self.toolCommDict['edgelockFwEn']:
            self.m_menuItem_edgelockFwDis.Check(False)
            self.m_menuItem_edgelockFwEn.Check(True)
        else:
            self.m_menuItem_edgelockFwDis.Check(True)
            self.m_menuItem_edgelockFwEn.Check(False)

    def setEdgelockFwOption( self ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            if self.m_menuItem_edgelockFwEn.IsChecked():
                self.edgelockFwEn = True
            elif self.m_menuItem_edgelockFwDis.IsChecked():
                self.edgelockFwEn = False
            else:
                pass
        else:
            self.edgelockFwEn = False
            self.m_menuItem_edgelockFwDis.Check(True)
            self.m_menuItem_edgelockFwEn.Check(False)
        self.toolCommDict['edgelockFwEn'] = self.edgelockFwEn

    def checkIfSubWinHasBeenOpened( self ):
        runtimeSettings = uivar.getRuntimeSettings()
        if not runtimeSettings[0]:
            uivar.setRuntimeSettings(True)
            return False
        else:
            return True

    def _refreshMcuDeviceList( self, mcuSeries ):
        self.m_choice_mcuDevice.Clear()
        if mcuSeries == uidef.kMcuSeries_MCX:
            self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_MCX_Latest)
        elif mcuSeries == uidef.kMcuSeries_Kinetis:
            self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_Kinetis_Latest)
        elif mcuSeries == uidef.kMcuSeries_LPC:
            self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_LPC_Latest)
        elif mcuSeries == uidef.kMcuSeries_iMXRT:
            self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_iMXRT_Latest)
        elif mcuSeries == uidef.kMcuSeries_Wireless:
            self.m_choice_mcuDevice.SetItems(uidef.kMcuDevice_Wireless_Latest)
        else:
            pass

    def _detectImxrtSeries( self ):
        mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        mcuSeries = uidef.kMcuSeries_iMXRT10yy
        if mcuDevice in uidef.kMcuDevice_iMXRT11yy:
            mcuSeries = uidef.kMcuSeries_iMXRT11yy
        elif mcuDevice in uidef.kMcuDevice_iMXRTxxx:
            mcuSeries = uidef.kMcuSeries_iMXRTxxx
        elif mcuDevice in uidef.kMcuDevice_iMXRT10yy:
            mcuSeries = uidef.kMcuSeries_iMXRT10yy
        else:
            pass
        if self.mcuSeries != None and self.mcuSeries != mcuSeries:
            self.isMcuSeriesChanged = True
        self.mcuSeries = mcuSeries

    def _detectWirelessSeries( self ):
        mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        mcuSeries = uidef.kMcuSeries_iMXRTxxx
        if mcuDevice in uidef.kMcuDevice_iMXRTxxx_sub:
            mcuSeries = uidef.kMcuSeries_iMXRTxxx_sub
        elif mcuDevice in uidef.kMcuDevice_Kinetis_sub:
            mcuSeries = uidef.kMcuSeries_Kinetis_sub
        else:
            pass
        if self.mcuSeries != None and self.mcuSeries != mcuSeries:
            self.isMcuSeriesChanged = True
        self.mcuSeries = mcuSeries

    def _initTargetSetupValue( self ):
        self.m_choice_mcuSeries.Clear()
        self.m_choice_mcuSeries.SetItems(uidef.kMcuSeries_Latest)
        self.m_choice_mcuSeries.SetSelection(self.toolCommDict['mcuSeries'])

        mcuSeries = self.m_choice_mcuSeries.GetString(self.m_choice_mcuSeries.GetSelection())
        self._refreshMcuDeviceList(mcuSeries)
        self.m_choice_mcuDevice.SetSelection(self.toolCommDict['mcuDevice'])
        if mcuSeries == uidef.kMcuSeries_iMXRT:
            self._detectImxrtSeries()
        elif mcuSeries == uidef.kMcuSeries_Wireless:
            self._detectWirelessSeries()
        else:
            self.mcuSeries = mcuSeries

    def setFlexspiNorDeviceForEvkBoard( self ):
        try:
            flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS25LP064A
            flexspiNorOpt1 = 0x0
            flexspiDeviceModel = self.tgt.flexspiNorDevice
            if  type(flexspiDeviceModel) == long:
                flexspiNorOpt0 = self.tgt.flexspiNorDevice
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_SipWinbond_W25Q32:
                flexspiNorOpt0 = 0xC0000007
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Winbond_W25Q128JV:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Winbond_W25Q128JV
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Winbond_W35T51NW:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Winbond_W35T51NW
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_MXIC_MX25L12845G:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25L12845G
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_MXIC_MX25UM51245G:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51245G
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G_OPI:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G_OPI
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G_2nd:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G_2nd
                flexspiNorOpt1 = uidef.kFlexspiNorOpt1_MXIC_MX25UM51345G_2nd
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_GigaDevice_GD25Q64C:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25Q64C
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_GigaDevice_GD25LB256E:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LB256E
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_GigaDevice_GD25LT256E:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LT256E
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_GigaDevice_GD25LX256E:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LX256E
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_ISSI_IS25LP064A:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS25LP064A
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_ISSI_IS25LX256:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS25LX256
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_ISSI_IS26KS512S:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS26KS512S
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Micron_MT25QL128A:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT25QL128A
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Micron_MT35X_RW303:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT35X_RW303
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Micron_MT35X_RW304:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT35X_RW304
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Adesto_AT25SF128A:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Adesto_AT25SF128A
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Adesto_ATXP032:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Adesto_ATXP032
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Cypress_S25FL064L:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S25FL064L
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Cypress_S25FL128S:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S25FL128S
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Cypress_S28HS512T:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S28HS512T
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Cypress_S26KS512S:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S26KS512S
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Microchip_SST26VF064B:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Microchip_SST26VF064B
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_FudanMicro_FM25Q64:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_FudanMicro_FM25Q64
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_BoyaMicro_BY25Q16BS:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_BoyaMicro_BY25Q16BS
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_XMC_XM25QH64B:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_XMC_XM25QH64B
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_XTXtech_X25Q64D:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_XTXtech_X25Q64D
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_Puya_P25Q64LE:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Puya_P25Q64LE
            elif flexspiDeviceModel == uidef.kFlexspiNorDevice_AMIC_A25LQ64:
                flexspiNorOpt0 = uidef.kFlexspiNorOpt0_AMIC_A25LQ64
            else:
                pass
            uivar.setBootDeviceConfiguration(uidef.kBootDevice_XspiNor, flexspiNorOpt0, flexspiNorOpt1, flexspiDeviceModel)
        except:
            pass

    def refreshBootDeviceList( self ):
        if self.tgt.availableBootDevices != None:
            self.m_choice_bootDevice.Clear()
            self.m_choice_bootDevice.SetItems(self.tgt.availableBootDevices)
            retSel = self.m_choice_bootDevice.FindString(self.bootDevice)
            if retSel != wx.NOT_FOUND:
                self.m_choice_bootDevice.SetSelection(retSel)
            else:
                self.m_choice_bootDevice.SetSelection(0)

    def setTargetSetupValue( self ):
        mcuSeries = self.m_choice_mcuSeries.GetString(self.m_choice_mcuSeries.GetSelection())
        if mcuSeries != self.mcuSeries:
            self.toolCommDict['mcuSeries'] = self.m_choice_mcuSeries.GetSelection()
            # from Wireless to Wireless
            if mcuSeries == uidef.kMcuSeries_Wireless and (self.mcuSeries == uidef.kMcuSeries_Kinetis_sub or self.mcuSeries == uidef.kMcuSeries_iMXRTxxx_sub):
                self._detectWirelessSeries()
            # from i.MXRT/LPC/MCX/Kinetis to Wireless
            elif mcuSeries == uidef.kMcuSeries_Wireless:
                self._refreshMcuDeviceList(mcuSeries)
                self.m_choice_mcuDevice.SetSelection(0)
                self._detectWirelessSeries()
            # from Wireless to i.MXRT/LPC/MCX/Kinetis
            elif self.mcuSeries == uidef.kMcuSeries_Kinetis_sub or self.mcuSeries == uidef.kMcuSeries_iMXRTxxx_sub:
                self._refreshMcuDeviceList(mcuSeries)
                self.m_choice_mcuDevice.SetSelection(0)
                if mcuSeries == uidef.kMcuSeries_iMXRT:
                    self._detectImxrtSeries()
                else:
                    self.mcuSeries = mcuSeries
                    self.isMcuSeriesChanged = True
            # from i.MXRT/LPC/MCX     to Kinetis
            # from i.MXRT/Kinetis/MCX to LPC
            # from i.MXRT/LPC/Kinetis to MCX
            elif mcuSeries == uidef.kMcuSeries_MCX or \
                 mcuSeries == uidef.kMcuSeries_Kinetis or \
                 mcuSeries == uidef.kMcuSeries_LPC:
                self.mcuSeries = mcuSeries
                self.isMcuSeriesChanged = True
                self._refreshMcuDeviceList(mcuSeries)
                self.m_choice_mcuDevice.SetSelection(0)
            # from MCX/Kinetis/LPC to i.MXRT
            elif self.mcuSeries == uidef.kMcuSeries_MCX or \
                 self.mcuSeries == uidef.kMcuSeries_Kinetis or \
                 self.mcuSeries == uidef.kMcuSeries_LPC:
                self._refreshMcuDeviceList(mcuSeries)
                self.m_choice_mcuDevice.SetSelection(0)
                self._detectImxrtSeries()
            # from i.MXRT to i.MXRT
            else:
                self._detectImxrtSeries()
        # Case: MCX     -> MCX
        # Case: Kinetis -> Kinetis
        # Case: LPC     -> LPC
        else:
            pass

        mcuDevice = self.m_choice_mcuDevice.GetString(self.m_choice_mcuDevice.GetSelection())
        if mcuDevice != self.mcuDevice:
            self.mcuDevice = mcuDevice
            self.isMcuDeviceChanged = True
        else:
            self.isMcuDeviceChanged = False
        self.toolCommDict['mcuDevice'] = self.m_choice_mcuDevice.GetSelection()

    def setBdcButtonEnablement( self, isEnabled ):
        self.m_button_bootDeviceConfiguration.Enable( isEnabled )

    def setDcdButtonEnablement( self, isEnabled ):
        self.m_button_deviceConfigurationData.Enable( isEnabled )

    def setXmcdButtonEnablement( self, isEnabled ):
        self.m_button_externalMemConfigurationData.Enable( isEnabled )

    def task_doPlaySound( self ):
        while True:
            if self.soundEffectFilenameForTask != None:
                self.playSoundEffect(self.soundEffectFilenameForTask)
                self.soundEffectFilenameForTask = None
            time.sleep(1)

    def _initPortSetupValue( self ):
        if self.toolCommDict['isUsbhidPortSelected']:
            self.m_radioBtn_uart.SetValue(False)
            self.m_radioBtn_usbhid.SetValue(True)
        else:
            self.m_radioBtn_uart.SetValue(True)
            self.m_radioBtn_usbhid.SetValue(False)
        usbIdList = []
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            usbIdList = self.RTyyyy_getUsbid()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            usbIdList = self.RTxxx_getUsbid()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            usbIdList = self.LPC_getUsbid()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            usbIdList = self.Kinetis_getUsbid()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            usbIdList = self.MCX_getUsbid()
        else:
            pass
        self.setPortSetupValue(uidef.kConnectStage_Rom, usbIdList)

    def task_doDetectUsbhid( self ):
        while True:
            if self.isUsbhidPortSelected:
                self._retryToDetectUsbhidDevice(False)
            time.sleep(1)

    def _retryToDetectUsbhidDevice( self, needToRetry = True ):
        usbVid = [None]
        usbPid = [None]
        self.isUsbhidConnected = False
        retryCnt = 1
        if needToRetry:
            retryCnt = kRetryDetectTimes
        while retryCnt > 0:
            # Auto detect USB-HID device
            hidFilter = pywinusb.hid.HidDeviceFilter(vendor_id = int(self.usbhidToConnect[0], 16), product_id = int(self.usbhidToConnect[1], 16))
            hidDevice = hidFilter.get_devices()
            if (not self.isDymaticUsbDetection) or (len(hidDevice) > 0):
                self.isUsbhidConnected = True
                usbVid[0] = self.usbhidToConnect[0]
                usbPid[0] = self.usbhidToConnect[1]
                break
            retryCnt = retryCnt - 1
            if retryCnt != 0:
                time.sleep(2)
            else:
                usbVid[0] = 'N/A - Not Found'
                usbPid[0] = usbVid[0]
        if self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection()) != usbVid[0] or \
           self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection()) != usbPid[0]:
            self.m_choice_portVid.Clear()
            self.m_choice_portVid.SetItems(usbVid)
            self.m_choice_portVid.SetSelection(0)
            self.m_choice_baudPid.Clear()
            self.m_choice_baudPid.SetItems(usbPid)
            self.m_choice_baudPid.SetSelection(0)

    def adjustPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[] ):
        self.hasDynamicLableBeenInit = True
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        if self.isUartPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_comPort'][self.languageIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_baudrate'][self.languageIndex])
            # Auto detect available ports
            comports = list(serial.tools.list_ports.comports())
            ports = [None] * len(comports)
            for i in range(len(comports)):
                comport = list(comports[i])
                ports[i] = comport[0]
            lastPort = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            lastBaud = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
            self.m_choice_portVid.Clear()
            self.m_choice_portVid.SetItems(ports)
            if lastPort in ports:
                self.m_choice_portVid.SetSelection(self.m_choice_portVid.FindString(lastPort))
            else:
                self.m_choice_portVid.SetSelection(0)
            baudItems = ['115200']
            if connectStage == uidef.kConnectStage_Rom:
                baudItems = rundef.kUartSpeed_Sdphost
            elif connectStage == uidef.kConnectStage_Flashloader:
                baudItems = rundef.kUartSpeed_Blhost
            else:
                pass
            self.m_choice_baudPid.Clear()
            self.m_choice_baudPid.SetItems(baudItems)
            if lastBaud in baudItems:
                self.m_choice_baudPid.SetSelection(self.m_choice_baudPid.FindString(lastBaud))
            else:
                self.m_choice_baudPid.SetSelection(0)
        elif self.isUsbhidPortSelected:
            self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_vid'][self.languageIndex])
            self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_pid'][self.languageIndex])
            if connectStage == uidef.kConnectStage_Rom:
                self.usbhidToConnect[0] = usbIdList[0]
                self.usbhidToConnect[1] = usbIdList[1]
                self._retryToDetectUsbhidDevice(False)
            elif connectStage == uidef.kConnectStage_Flashloader:
                self.usbhidToConnect[0] = usbIdList[2]
                self.usbhidToConnect[1] = usbIdList[3]
                self._retryToDetectUsbhidDevice(False)
            else:
                pass
        else:
            pass

    def setPortSetupValue( self, connectStage=uidef.kConnectStage_Rom, usbIdList=[], retryToDetectUsb=False, showError=False ):
        self.adjustPortSetupValue(connectStage, usbIdList)
        self.updatePortSetupValue(retryToDetectUsb, showError)

    def updatePortSetupValue( self, retryToDetectUsb=False, showError=False ):
        status = True
        self.isUartPortSelected = self.m_radioBtn_uart.GetValue()
        self.isUsbhidPortSelected = self.m_radioBtn_usbhid.GetValue()
        if self.isUartPortSelected:
            self.uartComPort = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
            self.uartBaudrate = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
        elif self.isUsbhidPortSelected:
            if self.isUsbhidConnected:
                self.usbhidVid = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
                self.usbhidPid = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
            else:
                self._retryToDetectUsbhidDevice(retryToDetectUsb)
                if not self.isUsbhidConnected:
                    status = False
                    if showError:
                        if self.languageIndex == uilang.kLanguageIndex_English:
                            self.popupMsgBox('Cannnot find USB-HID device (vid=%s, pid=%s), Please connect USB cable to your board first!' %(self.usbhidToConnect[0], self.usbhidToConnect[1]))
                        elif self.languageIndex == uilang.kLanguageIndex_Chinese:
                            self.popupMsgBox(u"找不到USB-HID设备 (vid=%s, pid=%s), 请先将USB线连接到板子！" %(self.usbhidToConnect[0], self.usbhidToConnect[1]))
                        else:
                            pass
                else:
                    self.usbhidVid = self.m_choice_portVid.GetString(self.m_choice_portVid.GetSelection())
                    self.usbhidPid = self.m_choice_baudPid.GetString(self.m_choice_baudPid.GetSelection())
        else:
            pass
        self.toolCommDict['isUsbhidPortSelected'] = self.isUsbhidPortSelected
        return status

    def updateConnectStatus( self, color='black' ):
        self.connectStatusColor = color
        if color == 'black':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_black'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_black.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'yellow':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_yellow'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_yellow.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'yellow_ota':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_yellow_ota'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_yellow.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'green':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_green'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_green.png", wx.BITMAP_TYPE_ANY ))
        elif color == 'blue':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_blue'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_blue.png", wx.BITMAP_TYPE_ANY ))
            self.playSoundEffect(uidef.kSoundEffectFilename_Progress)
        elif color == 'red':
            self.m_button_connect.SetLabel(uilang.kMainLanguageContentDict['button_connect_red'][self.languageIndex])
            self.m_bitmap_connectLed.SetBitmap(wx.Bitmap( u"../img/led_red.png", wx.BITMAP_TYPE_ANY ))
        else:
            pass

    def initOneStepConnectMode( self ):
        self.m_checkBox_oneStepConnect.SetValue(self.toolCommDict['isOneStepChecked'])
        self.getOneStepConnectMode()

    def getOneStepConnectMode( self ):
        self.isOneStepConnectMode = self.m_checkBox_oneStepConnect.GetValue()
        self.toolCommDict['isOneStepChecked'] = self.isOneStepConnectMode

    def enableOneStepForEntryMode( self ):
        if self.toolRunMode == uidef.kToolRunMode_Entry:
            self.m_checkBox_oneStepConnect.SetValue(True)
            self.toolCommDict['isOneStepChecked'] = True

    def showPageInMainBootSeqWin(self, pageIndex ):
        if pageIndex != self.m_notebook_imageSeq.GetSelection():
            self.m_notebook_imageSeq.SetSelection(pageIndex)

    def initSecureBootTypeList( self ):
        if self.tgt.availableSecureBootTypes != None:
            self.m_choice_secureBootType.Clear()
            self.m_choice_secureBootType.SetItems(self.tgt.availableSecureBootTypes)
            return True
        else:
            return False

    def refreshSecureBootTypeList( self ):
        if self.initSecureBootTypeList():
            retSel = self.m_choice_secureBootType.FindString(self.secureBootType)
            if retSel != wx.NOT_FOUND:
                self.m_choice_secureBootType.SetSelection(retSel)
            else:
                self.m_choice_secureBootType.SetSelection(0)

    def invalidateStepButtonColor( self, stepName, excuteResult ):
        invalidColor = None
        allInOneSoundEffect = None
        stepSoundEffect = None
        if excuteResult:
            invalidColor = uidef.kBootSeqColor_Invalid
            allInOneSoundEffect = uidef.kSoundEffectFilename_Success
            stepSoundEffect = uidef.kSoundEffectFilename_Progress
        else:
            invalidColor = uidef.kBootSeqColor_Failed
            allInOneSoundEffect = uidef.kSoundEffectFilename_Failure
        if stepName == uidef.kSecureBootSeqStep_AllInOne:
            self.m_button_allInOneAction.SetBackgroundColour( invalidColor )
            self.soundEffectFilenameForTask = allInOneSoundEffect
        else:
            if stepName == uidef.kSecureBootSeqStep_GenCert:
                self.m_button_genCert.SetBackgroundColour( invalidColor )
            elif stepName == uidef.kSecureBootSeqStep_GenImage:
                self.m_button_genImage.SetBackgroundColour( invalidColor )
                if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                    if excuteResult and (not(self.secureBootType in RTyyyy_uidef.kSecureBootType_HwCrypto)):
                        self.showPageInMainBootSeqWin(uidef.kPageIndex_ImageLoadingSequence)
                elif self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
                    self.showPageInMainBootSeqWin(uidef.kPageIndex_ImageLoadingSequence)
            elif stepName == uidef.kSecureBootSeqStep_PrepHwCrypto:
                self.m_button_prepHwCrypto.SetBackgroundColour( invalidColor )
                if excuteResult:
                    self.showPageInMainBootSeqWin(uidef.kPageIndex_ImageLoadingSequence)
            elif stepName == uidef.kSecureBootSeqStep_ProgSrk:
                self.m_button_progSrk.SetBackgroundColour( invalidColor )
            elif stepName == uidef.kSecureBootSeqStep_OperHwCrypto:
                self.m_button_operHwCrypto.SetBackgroundColour( invalidColor )
            elif stepName == uidef.kSecureBootSeqStep_FlashImage:
                self.m_button_flashImage.SetBackgroundColour( invalidColor )
            elif stepName == uidef.kSecureBootSeqStep_ProgDek:
                self.m_button_progDek.SetBackgroundColour( invalidColor )
            else:
                pass
            if stepSoundEffect != None:
                self.playSoundEffect(stepSoundEffect)
        self.Refresh()

    def resetSecureBootSeqColor( self ):
        self.resetCertificateColor()
        self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage1_browseApp.Enable( False )
        self.m_panel_genImage2_habCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage2_habCryptoAlgo.Enable( False )
        self.m_panel_genImage3_enableCertForHwCrypto.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_genImage3_enableCertForHwCrypto.Enable( False )
        self.m_button_genImage.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_genImage.Enable( False )
        self.resetKeyStorageRegionColor()
        self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_flashImage1_showImage.Enable( False )
        self.m_button_flashImage.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_flashImage.Enable( False )
        self.m_panel_progDek1_showHabDek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progDek1_showHabDek.Enable( False )
        self.m_textCtrl_habDek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_textCtrl_habDek128bit.Enable( False )
        self.m_button_progDek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_progDek.Enable( False )
        self.Refresh()

    def resetKeyStorageRegionColor( self ):
        self.m_panel_prepHwCrypto1_hwCryptoKeyRegion.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepHwCrypto1_hwCryptoKeyRegion.Enable( False )
        self.m_panel_prepHwCrypto2_hwCryptoAlgo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_prepHwCrypto2_hwCryptoAlgo.Enable( False )
        self.m_button_prepHwCrypto.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_prepHwCrypto.Enable( False )
        self.m_panel_operHwCrypto1_hwCryptoKeyInfo.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operHwCrypto1_hwCryptoKeyInfo.Enable( False )
        self.m_panel_operHwCrypto2_showGp4Dek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operHwCrypto2_showGp4Dek.Enable( False )
        self.m_textCtrl_gp4Dek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_textCtrl_gp4Dek128bit.Enable( False )
        self.m_panel_operHwCrypto3_showSwgp2Dek.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_operHwCrypto3_showSwgp2Dek.Enable( False )
        self.m_textCtrl_swgp2Dek128bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_textCtrl_swgp2Dek128bit.Enable( False )
        self.m_button_operHwCrypto.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_operHwCrypto.Enable( False )
        self.Refresh()

    def resetCertificateColor( self ):
        self.m_panel_doAuth1_certInput.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_textCtrl_serial.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_textCtrl_keyPass.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_panel_doAuth1_certInput.Enable( False )
        self.m_panel_doAuth2_certFmt.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_doAuth2_certFmt.Enable( False )
        self.m_button_genCert.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_genCert.Enable( False )
        self.m_panel_progSrk1_showSrk.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_panel_progSrk1_showSrk.Enable( False )
        self.m_textCtrl_srk256bit.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_textCtrl_srk256bit.Enable( False )
        self.m_button_progSrk.SetBackgroundColour( uidef.kBootSeqColor_Invalid )
        self.m_button_progSrk.Enable( False )
        self.Refresh()

    def popupMsgBox( self, msgStr, msgType="Error" ):
        messageText = (msgStr.encode('utf-8'))
        wx.MessageBox(messageText, msgType, wx.OK | wx.ICON_INFORMATION)

    def printLog( self, logStr ):
        try:
            self.m_textCtrl_cmdLog.write(logStr + "\n")
        except:
            pass

    def clearCmdLog( self ):
        self.m_textCtrl_cmdLog.Clear()

    def saveCmdLog( self ):
        self.m_textCtrl_cmdLog.SaveFile(self.logFilename)
        msgText = (('Command Log is saved in file: ' + self.logFilename + ' \n').encode('utf-8'))
        wx.MessageBox(msgText, "Log Info", wx.OK | wx.ICON_INFORMATION)

    def task_doIncreaseGauge( self ):
        while True:
            self._increaseGauge()
            global s_gaugeIntervalSec
            time.sleep(s_gaugeIntervalSec)

    def _increaseGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        if s_isGaugeWorking:
            gaugePercentage = s_curGauge * 1.0 / s_maxGauge
            if gaugePercentage <= 0.9:
                s_gaugeIntervalSec = int(gaugePercentage  / 0.1) * 0.5 + 0.5
                self.m_gauge_action.SetValue(s_curGauge)
                s_curGauge += 1
            self.updateCostTime()

    def initGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        s_isGaugeWorking = True
        s_curGauge = 0
        s_gaugeIntervalSec = 0.5
        s_maxGauge = self.m_gauge_action.GetRange()
        self.m_gauge_action.SetValue(s_curGauge)

    def deinitGauge( self ):
        global s_isGaugeWorking
        global s_curGauge
        global s_maxGauge
        global s_gaugeIntervalSec
        s_isGaugeWorking = False
        s_curGauge = s_maxGauge
        s_gaugeIntervalSec = 1
        self.m_gauge_action.SetValue(s_maxGauge)

    def printDeviceStatus( self, statusStr ):
        self.m_textCtrl_deviceStatus.write(statusStr + "\n")

    def clearDeviceStatus( self ):
        self.m_textCtrl_deviceStatus.Clear()

    def getUserAppFilePath( self ):
        appPath = self.m_filePicker_appPath.GetPath()
        self.toolCommDict['appFilename'] = appPath.encode("utf-8")
        return appPath.encode('utf-8').encode("gbk")

    def _setUserBinaryBaseField( self ):
        txt = self.m_choice_appFormat.GetString(self.m_choice_appFormat.GetSelection())
        if txt == uidef.kAppImageFormat_AutoDetect or txt == uidef.kAppImageFormat_RawBinary:
            self.m_textCtrl_appBaseAddr.Enable(True)
        else:
            self.m_textCtrl_appBaseAddr.Enable(False)

    def getUserAppFileFormat( self ):
        self.toolCommDict['appFormat'] = self.m_choice_appFormat.GetSelection()
        self._setUserBinaryBaseField()
        return self.m_choice_appFormat.GetString(self.m_choice_appFormat.GetSelection())

    def getUserBinaryBaseAddress( self ):
        self.toolCommDict['appBinBaseAddr'] = self.m_textCtrl_appBaseAddr.GetLineText(0)
        return self.getVal32FromHexText(self.m_textCtrl_appBaseAddr.GetLineText(0))

    def convertLongIntHexText( self, hexText ):
        lastStr = hexText[len(hexText) - 1]
        if lastStr == 'l' or lastStr == 'L':
            return hexText[0:len(hexText) - 1]
        else:
            return hexText

    def getVal32FromHexText( self, hexText ):
        status = False
        val32 = None
        if len(hexText) > 2 and hexText[0:2] == '0x':
            try:
                val32 = int(hexText[2:len(hexText)], 16)
                status = True
            except:
                pass
        if not status:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['inputError_illegalFormat'][self.languageIndex])
        return status, val32

    def resetFuseOtpRegionField( self ):
        color = wx.SYS_COLOUR_WINDOW
        self.m_textCtrl_fuse400.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse410.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse420.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse430.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse440.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse450.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse460.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse470.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse480.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse490.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4c0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4d0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4e0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse4f0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse500.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse510.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse520.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse530.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse540.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse550.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse560.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse570.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse580.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse590.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5c0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5d0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5e0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse5f0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse600.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse610.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse620.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse630.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse640.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse650.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse660.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse670.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse680.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse690.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6c0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6d0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6e0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse6f0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse700.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse710.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse720.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse730.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse740.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse750.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse760.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse770.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse780.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse790.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7c0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7d0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7e0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse7f0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse800.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse810.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse820.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse830.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse840.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse850.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse860.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse870.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse880.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse890.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8c0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8d0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8e0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.m_textCtrl_fuse8f0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
        self.Refresh()

    def getFormattedFuseValue( self, fuseValue, direction='LSB'):
        formattedVal32 = ''
        for i in range(8):
            loc = 0
            if direction =='LSB':
                loc = 32 - (i + 1) * 4
            elif direction =='MSB':
                loc = i * 4
            else:
                pass
            halfbyteStr = str(hex((fuseValue & (0xF << loc))>> loc))
            formattedVal32 += halfbyteStr[2]
        return formattedVal32

    def getFormattedHexValue( self, val32 ):
        return ('0x' + self.getFormattedFuseValue(val32))

    def getFormattedUpperHexValue( self, val32 ):
        return ('0x' + self.getFormattedFuseValue(val32).upper())

    def parseReadFuseValue( self, fuseValue ):
        if fuseValue != None:
            return self.getFormattedHexValue(fuseValue)
        else:
            return '--------'

    def clearUserFuses( self ):
        self.m_textCtrl_fuse400.Clear()
        self.m_textCtrl_fuse410.Clear()
        self.m_textCtrl_fuse420.Clear()
        self.m_textCtrl_fuse430.Clear()
        self.m_textCtrl_fuse440.Clear()
        self.m_textCtrl_fuse450.Clear()
        self.m_textCtrl_fuse460.Clear()
        self.m_textCtrl_fuse470.Clear()
        self.m_textCtrl_fuse480.Clear()
        self.m_textCtrl_fuse490.Clear()
        self.m_textCtrl_fuse4a0.Clear()
        self.m_textCtrl_fuse4b0.Clear()
        self.m_textCtrl_fuse4c0.Clear()
        self.m_textCtrl_fuse4d0.Clear()
        self.m_textCtrl_fuse4e0.Clear()
        self.m_textCtrl_fuse4f0.Clear()
        self.m_textCtrl_fuse500.Clear()
        self.m_textCtrl_fuse510.Clear()
        self.m_textCtrl_fuse520.Clear()
        self.m_textCtrl_fuse530.Clear()
        self.m_textCtrl_fuse540.Clear()
        self.m_textCtrl_fuse550.Clear()
        self.m_textCtrl_fuse560.Clear()
        self.m_textCtrl_fuse570.Clear()
        self.m_textCtrl_fuse580.Clear()
        self.m_textCtrl_fuse590.Clear()
        self.m_textCtrl_fuse5a0.Clear()
        self.m_textCtrl_fuse5b0.Clear()
        self.m_textCtrl_fuse5c0.Clear()
        self.m_textCtrl_fuse5d0.Clear()
        self.m_textCtrl_fuse5e0.Clear()
        self.m_textCtrl_fuse5f0.Clear()
        self.m_textCtrl_fuse600.Clear()
        self.m_textCtrl_fuse610.Clear()
        self.m_textCtrl_fuse620.Clear()
        self.m_textCtrl_fuse630.Clear()
        self.m_textCtrl_fuse640.Clear()
        self.m_textCtrl_fuse650.Clear()
        self.m_textCtrl_fuse660.Clear()
        self.m_textCtrl_fuse670.Clear()
        self.m_textCtrl_fuse680.Clear()
        self.m_textCtrl_fuse690.Clear()
        self.m_textCtrl_fuse6a0.Clear()
        self.m_textCtrl_fuse6b0.Clear()
        self.m_textCtrl_fuse6c0.Clear()
        self.m_textCtrl_fuse6d0.Clear()
        self.m_textCtrl_fuse6e0.Clear()
        self.m_textCtrl_fuse6f0.Clear()
        self.m_textCtrl_fuse700.Clear()
        self.m_textCtrl_fuse710.Clear()
        self.m_textCtrl_fuse720.Clear()
        self.m_textCtrl_fuse730.Clear()
        self.m_textCtrl_fuse740.Clear()
        self.m_textCtrl_fuse750.Clear()
        self.m_textCtrl_fuse760.Clear()
        self.m_textCtrl_fuse770.Clear()
        self.m_textCtrl_fuse780.Clear()
        self.m_textCtrl_fuse790.Clear()
        self.m_textCtrl_fuse7a0.Clear()
        self.m_textCtrl_fuse7b0.Clear()
        self.m_textCtrl_fuse7c0.Clear()
        self.m_textCtrl_fuse7d0.Clear()
        self.m_textCtrl_fuse7e0.Clear()
        self.m_textCtrl_fuse7f0.Clear()
        self.m_textCtrl_fuse800.Clear()
        self.m_textCtrl_fuse810.Clear()
        self.m_textCtrl_fuse820.Clear()
        self.m_textCtrl_fuse830.Clear()
        self.m_textCtrl_fuse840.Clear()
        self.m_textCtrl_fuse850.Clear()
        self.m_textCtrl_fuse860.Clear()
        self.m_textCtrl_fuse870.Clear()
        self.m_textCtrl_fuse880.Clear()
        self.m_textCtrl_fuse890.Clear()
        self.m_textCtrl_fuse8a0.Clear()
        self.m_textCtrl_fuse8b0.Clear()
        self.m_textCtrl_fuse8c0.Clear()
        self.m_textCtrl_fuse8d0.Clear()
        self.m_textCtrl_fuse8e0.Clear()
        self.m_textCtrl_fuse8f0.Clear()

    def parseUserFuseValue( self, fuseText ):
        if len(fuseText) >= 3 and fuseText[0:2] == '0x':
            return int(fuseText[2:len(fuseText)], 16)
        else:
            return None

    def getUserFuses( self ):
        userFuseList = [None] * RTyyyy_fusedef.kGroupEfuseWords
        userFuseList[0] = self.parseUserFuseValue(self.m_textCtrl_fuse400.GetLineText(0))
        userFuseList[1] = self.parseUserFuseValue(self.m_textCtrl_fuse410.GetLineText(0))
        userFuseList[2] = self.parseUserFuseValue(self.m_textCtrl_fuse420.GetLineText(0))
        userFuseList[3] = self.parseUserFuseValue(self.m_textCtrl_fuse430.GetLineText(0))
        userFuseList[4] = self.parseUserFuseValue(self.m_textCtrl_fuse440.GetLineText(0))
        userFuseList[5] = self.parseUserFuseValue(self.m_textCtrl_fuse450.GetLineText(0))
        userFuseList[6] = self.parseUserFuseValue(self.m_textCtrl_fuse460.GetLineText(0))
        userFuseList[7] = self.parseUserFuseValue(self.m_textCtrl_fuse470.GetLineText(0))
        userFuseList[8] = self.parseUserFuseValue(self.m_textCtrl_fuse480.GetLineText(0))
        userFuseList[9] = self.parseUserFuseValue(self.m_textCtrl_fuse490.GetLineText(0))
        userFuseList[10] = self.parseUserFuseValue(self.m_textCtrl_fuse4a0.GetLineText(0))
        userFuseList[11] = self.parseUserFuseValue(self.m_textCtrl_fuse4b0.GetLineText(0))
        userFuseList[12] = self.parseUserFuseValue(self.m_textCtrl_fuse4c0.GetLineText(0))
        userFuseList[13] = self.parseUserFuseValue(self.m_textCtrl_fuse4d0.GetLineText(0))
        userFuseList[14] = self.parseUserFuseValue(self.m_textCtrl_fuse4e0.GetLineText(0))
        userFuseList[15] = self.parseUserFuseValue(self.m_textCtrl_fuse4f0.GetLineText(0))

        userFuseList[16] = self.parseUserFuseValue(self.m_textCtrl_fuse500.GetLineText(0))
        userFuseList[17] = self.parseUserFuseValue(self.m_textCtrl_fuse510.GetLineText(0))
        userFuseList[18] = self.parseUserFuseValue(self.m_textCtrl_fuse520.GetLineText(0))
        userFuseList[19] = self.parseUserFuseValue(self.m_textCtrl_fuse530.GetLineText(0))
        userFuseList[20] = self.parseUserFuseValue(self.m_textCtrl_fuse540.GetLineText(0))
        userFuseList[21] = self.parseUserFuseValue(self.m_textCtrl_fuse550.GetLineText(0))
        userFuseList[22] = self.parseUserFuseValue(self.m_textCtrl_fuse560.GetLineText(0))
        userFuseList[23] = self.parseUserFuseValue(self.m_textCtrl_fuse570.GetLineText(0))
        userFuseList[24] = self.parseUserFuseValue(self.m_textCtrl_fuse580.GetLineText(0))
        userFuseList[25] = self.parseUserFuseValue(self.m_textCtrl_fuse590.GetLineText(0))
        userFuseList[26] = self.parseUserFuseValue(self.m_textCtrl_fuse5a0.GetLineText(0))
        userFuseList[27] = self.parseUserFuseValue(self.m_textCtrl_fuse5b0.GetLineText(0))
        userFuseList[28] = self.parseUserFuseValue(self.m_textCtrl_fuse5c0.GetLineText(0))
        userFuseList[29] = self.parseUserFuseValue(self.m_textCtrl_fuse5d0.GetLineText(0))
        userFuseList[30] = self.parseUserFuseValue(self.m_textCtrl_fuse5e0.GetLineText(0))
        userFuseList[31] = self.parseUserFuseValue(self.m_textCtrl_fuse5f0.GetLineText(0))

        userFuseList[32] = self.parseUserFuseValue(self.m_textCtrl_fuse600.GetLineText(0))
        userFuseList[33] = self.parseUserFuseValue(self.m_textCtrl_fuse610.GetLineText(0))
        userFuseList[34] = self.parseUserFuseValue(self.m_textCtrl_fuse620.GetLineText(0))
        userFuseList[35] = self.parseUserFuseValue(self.m_textCtrl_fuse630.GetLineText(0))
        userFuseList[36] = self.parseUserFuseValue(self.m_textCtrl_fuse640.GetLineText(0))
        userFuseList[37] = self.parseUserFuseValue(self.m_textCtrl_fuse650.GetLineText(0))
        userFuseList[38] = self.parseUserFuseValue(self.m_textCtrl_fuse660.GetLineText(0))
        userFuseList[39] = self.parseUserFuseValue(self.m_textCtrl_fuse670.GetLineText(0))
        userFuseList[40] = self.parseUserFuseValue(self.m_textCtrl_fuse680.GetLineText(0))
        userFuseList[41] = self.parseUserFuseValue(self.m_textCtrl_fuse690.GetLineText(0))
        userFuseList[42] = self.parseUserFuseValue(self.m_textCtrl_fuse6a0.GetLineText(0))
        userFuseList[43] = self.parseUserFuseValue(self.m_textCtrl_fuse6b0.GetLineText(0))
        userFuseList[44] = self.parseUserFuseValue(self.m_textCtrl_fuse6c0.GetLineText(0))
        userFuseList[45] = self.parseUserFuseValue(self.m_textCtrl_fuse6d0.GetLineText(0))
        userFuseList[46] = self.parseUserFuseValue(self.m_textCtrl_fuse6e0.GetLineText(0))
        userFuseList[47] = self.parseUserFuseValue(self.m_textCtrl_fuse6f0.GetLineText(0))

        userFuseList[48] = self.parseUserFuseValue(self.m_textCtrl_fuse700.GetLineText(0))
        userFuseList[49] = self.parseUserFuseValue(self.m_textCtrl_fuse710.GetLineText(0))
        userFuseList[50] = self.parseUserFuseValue(self.m_textCtrl_fuse720.GetLineText(0))
        userFuseList[51] = self.parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        userFuseList[52] = self.parseUserFuseValue(self.m_textCtrl_fuse730.GetLineText(0))
        userFuseList[53] = self.parseUserFuseValue(self.m_textCtrl_fuse750.GetLineText(0))
        userFuseList[54] = self.parseUserFuseValue(self.m_textCtrl_fuse760.GetLineText(0))
        userFuseList[55] = self.parseUserFuseValue(self.m_textCtrl_fuse770.GetLineText(0))
        userFuseList[56] = self.parseUserFuseValue(self.m_textCtrl_fuse780.GetLineText(0))
        userFuseList[57] = self.parseUserFuseValue(self.m_textCtrl_fuse790.GetLineText(0))
        userFuseList[58] = self.parseUserFuseValue(self.m_textCtrl_fuse7a0.GetLineText(0))
        userFuseList[59] = self.parseUserFuseValue(self.m_textCtrl_fuse7b0.GetLineText(0))
        userFuseList[60] = self.parseUserFuseValue(self.m_textCtrl_fuse7c0.GetLineText(0))
        userFuseList[61] = self.parseUserFuseValue(self.m_textCtrl_fuse7d0.GetLineText(0))
        userFuseList[62] = self.parseUserFuseValue(self.m_textCtrl_fuse7e0.GetLineText(0))
        userFuseList[63] = self.parseUserFuseValue(self.m_textCtrl_fuse7f0.GetLineText(0))

        userFuseList[64] = self.parseUserFuseValue(self.m_textCtrl_fuse800.GetLineText(0))
        userFuseList[65] = self.parseUserFuseValue(self.m_textCtrl_fuse810.GetLineText(0))
        userFuseList[66] = self.parseUserFuseValue(self.m_textCtrl_fuse820.GetLineText(0))
        userFuseList[67] = self.parseUserFuseValue(self.m_textCtrl_fuse830.GetLineText(0))
        userFuseList[68] = self.parseUserFuseValue(self.m_textCtrl_fuse840.GetLineText(0))
        userFuseList[69] = self.parseUserFuseValue(self.m_textCtrl_fuse850.GetLineText(0))
        userFuseList[70] = self.parseUserFuseValue(self.m_textCtrl_fuse860.GetLineText(0))
        userFuseList[71] = self.parseUserFuseValue(self.m_textCtrl_fuse870.GetLineText(0))
        userFuseList[72] = self.parseUserFuseValue(self.m_textCtrl_fuse880.GetLineText(0))
        userFuseList[73] = self.parseUserFuseValue(self.m_textCtrl_fuse890.GetLineText(0))
        userFuseList[74] = self.parseUserFuseValue(self.m_textCtrl_fuse8a0.GetLineText(0))
        userFuseList[75] = self.parseUserFuseValue(self.m_textCtrl_fuse8b0.GetLineText(0))
        userFuseList[76] = self.parseUserFuseValue(self.m_textCtrl_fuse8c0.GetLineText(0))
        userFuseList[77] = self.parseUserFuseValue(self.m_textCtrl_fuse8d0.GetLineText(0))
        userFuseList[78] = self.parseUserFuseValue(self.m_textCtrl_fuse8e0.GetLineText(0))
        userFuseList[79] = self.parseUserFuseValue(self.m_textCtrl_fuse8f0.GetLineText(0))

        return userFuseList

    def setInitialFuseGroupText( self, eFuseGroupSel, styleStr='N/A'):
        if styleStr == 'W':
            labelPreStr = 'W'
            labelStart = eFuseGroupSel * RTyyyy_fusedef.kGroupEfuseWords
            self.m_button_fuse400.SetLabel(labelPreStr+str(labelStart+0))
            self.m_staticText_fuse410.SetLabel(labelPreStr+str(labelStart+1))
            self.m_staticText_fuse420.SetLabel(labelPreStr+str(labelStart+2))
            self.m_staticText_fuse430.SetLabel(labelPreStr+str(labelStart+3))
            self.m_staticText_fuse440.SetLabel(labelPreStr+str(labelStart+4))
            self.m_button_fuse450.SetLabel(labelPreStr+str(labelStart+5))
            self.m_button_fuse460.SetLabel(labelPreStr+str(labelStart+6))
            self.m_button_fuse470.SetLabel(labelPreStr+str(labelStart+7))
            self.m_staticText_fuse480.SetLabel(labelPreStr+str(labelStart+8))
            self.m_staticText_fuse490.SetLabel(labelPreStr+str(labelStart+9))
            self.m_staticText_fuse4a0.SetLabel(labelPreStr+str(labelStart+10))
            self.m_staticText_fuse4b0.SetLabel(labelPreStr+str(labelStart+11))
            self.m_staticText_fuse4c0.SetLabel(labelPreStr+str(labelStart+12))
            self.m_staticText_fuse4d0.SetLabel(labelPreStr+str(labelStart+13))
            self.m_staticText_fuse4e0.SetLabel(labelPreStr+str(labelStart+14))
            self.m_staticText_fuse4f0.SetLabel(labelPreStr+str(labelStart+15))
            self.m_staticText_fuse500.SetLabel(labelPreStr+str(labelStart+16))
            self.m_staticText_fuse510.SetLabel(labelPreStr+str(labelStart+17))
            self.m_staticText_fuse520.SetLabel(labelPreStr+str(labelStart+18))
            self.m_staticText_fuse530.SetLabel(labelPreStr+str(labelStart+19))
            self.m_staticText_fuse540.SetLabel(labelPreStr+str(labelStart+20))
            self.m_staticText_fuse550.SetLabel(labelPreStr+str(labelStart+21))
            self.m_staticText_fuse560.SetLabel(labelPreStr+str(labelStart+22))
            self.m_staticText_fuse570.SetLabel(labelPreStr+str(labelStart+23))
            self.m_staticText_fuse580.SetLabel(labelPreStr+str(labelStart+24))
            self.m_staticText_fuse590.SetLabel(labelPreStr+str(labelStart+25))
            self.m_staticText_fuse5a0.SetLabel(labelPreStr+str(labelStart+26))
            self.m_staticText_fuse5b0.SetLabel(labelPreStr+str(labelStart+27))
            self.m_staticText_fuse5c0.SetLabel(labelPreStr+str(labelStart+28))
            self.m_staticText_fuse5d0.SetLabel(labelPreStr+str(labelStart+29))
            self.m_staticText_fuse5e0.SetLabel(labelPreStr+str(labelStart+30))
            self.m_staticText_fuse5f0.SetLabel(labelPreStr+str(labelStart+31))
            self.m_staticText_fuse600.SetLabel(labelPreStr+str(labelStart+32))
            self.m_staticText_fuse610.SetLabel(labelPreStr+str(labelStart+33))
            self.m_staticText_fuse620.SetLabel(labelPreStr+str(labelStart+34))
            self.m_staticText_fuse630.SetLabel(labelPreStr+str(labelStart+35))
            self.m_staticText_fuse640.SetLabel(labelPreStr+str(labelStart+36))
            self.m_staticText_fuse650.SetLabel(labelPreStr+str(labelStart+37))
            self.m_staticText_fuse660.SetLabel(labelPreStr+str(labelStart+38))
            self.m_staticText_fuse670.SetLabel(labelPreStr+str(labelStart+39))
            self.m_staticText_fuse680.SetLabel(labelPreStr+str(labelStart+40))
            self.m_staticText_fuse690.SetLabel(labelPreStr+str(labelStart+41))
            self.m_staticText_fuse6a0.SetLabel(labelPreStr+str(labelStart+42))
            self.m_staticText_fuse6b0.SetLabel(labelPreStr+str(labelStart+43))
            self.m_staticText_fuse6c0.SetLabel(labelPreStr+str(labelStart+44))
            self.m_button_fuse6d0.SetLabel(labelPreStr+str(labelStart+45))
            self.m_button_fuse6e0.SetLabel(labelPreStr+str(labelStart+46))
            self.m_staticText_fuse6f0.SetLabel(labelPreStr+str(labelStart+47))
            self.m_staticText_fuse700.SetLabel(labelPreStr+str(labelStart+48))
            self.m_staticText_fuse710.SetLabel(labelPreStr+str(labelStart+49))
            self.m_staticText_fuse720.SetLabel(labelPreStr+str(labelStart+50))
            self.m_staticText_fuse730.SetLabel(labelPreStr+str(labelStart+51))
            self.m_staticText_fuse740.SetLabel(labelPreStr+str(labelStart+52))
            self.m_staticText_fuse750.SetLabel(labelPreStr+str(labelStart+53))
            self.m_staticText_fuse760.SetLabel(labelPreStr+str(labelStart+54))
            self.m_staticText_fuse770.SetLabel(labelPreStr+str(labelStart+55))
            self.m_staticText_fuse780.SetLabel(labelPreStr+str(labelStart+56))
            self.m_staticText_fuse790.SetLabel(labelPreStr+str(labelStart+57))
            self.m_staticText_fuse7a0.SetLabel(labelPreStr+str(labelStart+58))
            self.m_staticText_fuse7b0.SetLabel(labelPreStr+str(labelStart+59))
            self.m_staticText_fuse7c0.SetLabel(labelPreStr+str(labelStart+60))
            self.m_staticText_fuse7d0.SetLabel(labelPreStr+str(labelStart+61))
            self.m_staticText_fuse7e0.SetLabel(labelPreStr+str(labelStart+62))
            self.m_staticText_fuse7f0.SetLabel(labelPreStr+str(labelStart+63))
            self.m_staticText_fuse800.SetLabel(labelPreStr+str(labelStart+64))
            self.m_staticText_fuse810.SetLabel(labelPreStr+str(labelStart+65))
            self.m_staticText_fuse820.SetLabel(labelPreStr+str(labelStart+66))
            self.m_staticText_fuse830.SetLabel(labelPreStr+str(labelStart+67))
            self.m_staticText_fuse840.SetLabel(labelPreStr+str(labelStart+68))
            self.m_staticText_fuse850.SetLabel(labelPreStr+str(labelStart+69))
            self.m_staticText_fuse860.SetLabel(labelPreStr+str(labelStart+70))
            self.m_staticText_fuse870.SetLabel(labelPreStr+str(labelStart+71))
            self.m_staticText_fuse880.SetLabel(labelPreStr+str(labelStart+72))
            self.m_staticText_fuse890.SetLabel(labelPreStr+str(labelStart+73))
            self.m_staticText_fuse8a0.SetLabel(labelPreStr+str(labelStart+74))
            self.m_staticText_fuse8b0.SetLabel(labelPreStr+str(labelStart+75))
            self.m_staticText_fuse8c0.SetLabel(labelPreStr+str(labelStart+76))
            self.m_staticText_fuse8d0.SetLabel(labelPreStr+str(labelStart+77))
            self.m_staticText_fuse8e0.SetLabel(labelPreStr+str(labelStart+78))
            self.m_staticText_fuse8f0.SetLabel(labelPreStr+str(labelStart+79))
        else:
            self.m_button_fuse400.SetLabel(styleStr)
            self.m_staticText_fuse410.SetLabel(styleStr)
            self.m_staticText_fuse420.SetLabel(styleStr)
            self.m_staticText_fuse430.SetLabel(styleStr)
            self.m_staticText_fuse440.SetLabel(styleStr)
            self.m_button_fuse450.SetLabel(styleStr)
            self.m_button_fuse460.SetLabel(styleStr)
            self.m_button_fuse470.SetLabel(styleStr)
            self.m_staticText_fuse480.SetLabel(styleStr)
            self.m_staticText_fuse490.SetLabel(styleStr)
            self.m_staticText_fuse4a0.SetLabel(styleStr)
            self.m_staticText_fuse4b0.SetLabel(styleStr)
            self.m_staticText_fuse4c0.SetLabel(styleStr)
            self.m_staticText_fuse4d0.SetLabel(styleStr)
            self.m_staticText_fuse4e0.SetLabel(styleStr)
            self.m_staticText_fuse4f0.SetLabel(styleStr)
            self.m_staticText_fuse500.SetLabel(styleStr)
            self.m_staticText_fuse510.SetLabel(styleStr)
            self.m_staticText_fuse520.SetLabel(styleStr)
            self.m_staticText_fuse530.SetLabel(styleStr)
            self.m_staticText_fuse540.SetLabel(styleStr)
            self.m_staticText_fuse550.SetLabel(styleStr)
            self.m_staticText_fuse560.SetLabel(styleStr)
            self.m_staticText_fuse570.SetLabel(styleStr)
            self.m_staticText_fuse580.SetLabel(styleStr)
            self.m_staticText_fuse590.SetLabel(styleStr)
            self.m_staticText_fuse5a0.SetLabel(styleStr)
            self.m_staticText_fuse5b0.SetLabel(styleStr)
            self.m_staticText_fuse5c0.SetLabel(styleStr)
            self.m_staticText_fuse5d0.SetLabel(styleStr)
            self.m_staticText_fuse5e0.SetLabel(styleStr)
            self.m_staticText_fuse5f0.SetLabel(styleStr)
            self.m_staticText_fuse600.SetLabel(styleStr)
            self.m_staticText_fuse610.SetLabel(styleStr)
            self.m_staticText_fuse620.SetLabel(styleStr)
            self.m_staticText_fuse630.SetLabel(styleStr)
            self.m_staticText_fuse640.SetLabel(styleStr)
            self.m_staticText_fuse650.SetLabel(styleStr)
            self.m_staticText_fuse660.SetLabel(styleStr)
            self.m_staticText_fuse670.SetLabel(styleStr)
            self.m_staticText_fuse680.SetLabel(styleStr)
            self.m_staticText_fuse690.SetLabel(styleStr)
            self.m_staticText_fuse6a0.SetLabel(styleStr)
            self.m_staticText_fuse6b0.SetLabel(styleStr)
            self.m_staticText_fuse6c0.SetLabel(styleStr)
            self.m_button_fuse6d0.SetLabel(styleStr)
            self.m_button_fuse6e0.SetLabel(styleStr)
            self.m_staticText_fuse6f0.SetLabel(styleStr)
            self.m_staticText_fuse700.SetLabel(styleStr)
            self.m_staticText_fuse710.SetLabel(styleStr)
            self.m_staticText_fuse720.SetLabel(styleStr)
            self.m_staticText_fuse730.SetLabel(styleStr)
            self.m_staticText_fuse740.SetLabel(styleStr)
            self.m_staticText_fuse750.SetLabel(styleStr)
            self.m_staticText_fuse760.SetLabel(styleStr)
            self.m_staticText_fuse770.SetLabel(styleStr)
            self.m_staticText_fuse780.SetLabel(styleStr)
            self.m_staticText_fuse790.SetLabel(styleStr)
            self.m_staticText_fuse7a0.SetLabel(styleStr)
            self.m_staticText_fuse7b0.SetLabel(styleStr)
            self.m_staticText_fuse7c0.SetLabel(styleStr)
            self.m_staticText_fuse7d0.SetLabel(styleStr)
            self.m_staticText_fuse7e0.SetLabel(styleStr)
            self.m_staticText_fuse7f0.SetLabel(styleStr)
            self.m_staticText_fuse800.SetLabel(styleStr)
            self.m_staticText_fuse810.SetLabel(styleStr)
            self.m_staticText_fuse820.SetLabel(styleStr)
            self.m_staticText_fuse830.SetLabel(styleStr)
            self.m_staticText_fuse840.SetLabel(styleStr)
            self.m_staticText_fuse850.SetLabel(styleStr)
            self.m_staticText_fuse860.SetLabel(styleStr)
            self.m_staticText_fuse870.SetLabel(styleStr)
            self.m_staticText_fuse880.SetLabel(styleStr)
            self.m_staticText_fuse890.SetLabel(styleStr)
            self.m_staticText_fuse8a0.SetLabel(styleStr)
            self.m_staticText_fuse8b0.SetLabel(styleStr)
            self.m_staticText_fuse8c0.SetLabel(styleStr)
            self.m_staticText_fuse8d0.SetLabel(styleStr)
            self.m_staticText_fuse8e0.SetLabel(styleStr)
            self.m_staticText_fuse8f0.SetLabel(styleStr)

    def getComMemStartAddress( self ):
        return self.getVal32FromHexText(self.m_textCtrl_memStart.GetLineText(0))

    def getComMemByteLength( self ):
        return self.getVal32FromHexText(self.m_textCtrl_memLength.GetLineText(0))

    def getComMemBinFile( self ):
        memBinFile = self.m_filePicker_memBinFile.GetPath()
        return memBinFile.encode('utf-8').encode("gbk")

    def needToSaveReadbackImageData( self ):
        return self.m_checkBox_saveImageData.GetValue()

    def getImageDataFolderToSave( self ):
        savedBinFolder = self.m_dirPicker_savedBinFolder.GetPath()
        return savedBinFolder.encode('utf-8').encode("gbk")

    def setImageDataFilePath( self, filePath ):
        self.m_filePicker_savedBinFile.SetPath(filePath)

    def printMem( self , memStr, strColor=uidef.kMemBlockColor_Padding, feedEol = True ):
        self.m_textCtrl_bootDeviceMem.SetDefaultStyle(wx.TextAttr(strColor, uidef.kMemBlockColor_Background))
        if feedEol:
            self.m_textCtrl_bootDeviceMem.AppendText(memStr + "\n")
        else:
            self.m_textCtrl_bootDeviceMem.AppendText(memStr)

    def clearMem( self ):
        self.m_textCtrl_bootDeviceMem.Clear()

    def showImageLayout( self , imgPath ):
        self.m_bitmap_bootableImage.SetBitmap(wx.Bitmap( imgPath, wx.BITMAP_TYPE_ANY ))

    def getBootLogBinFile( self ):
        logBinFile = self.m_filePicker_bootLogBinFile.GetPath()
        return logBinFile.encode('utf-8').encode("gbk")

    def needToSaveBootLogContext( self ):
        return self.m_checkBox_saveBootLog.GetValue()

    def getBootLogFolderToSave( self ):
        savedLogFolder = self.m_dirPicker_savedBootLogFolder.GetPath()
        return savedLogFolder.encode('utf-8').encode("gbk")

    def printBootLog( self , logStr, feedEol = True ):
        if feedEol:
            self.m_textCtrl_bootLogContext.AppendText(logStr + "\n")
        else:
            self.m_textCtrl_bootLogContext.AppendText(logStr)

    def clearBootLog( self ):
        self.m_textCtrl_bootLogContext.Clear()

    def _initLanguage( self ):
        if self.toolCommDict['isEnglishLanguage']:
            self.m_menuItem_english.Check(True)
            self.m_menuItem_chinese.Check(False)
        else:
            self.m_menuItem_english.Check(False)
            self.m_menuItem_chinese.Check(True)

    def _getLastLangIndex( self ):
        label = self.m_staticText_mcuSeries.GetLabel()
        labelList = uilang.kMainLanguageContentDict['sText_mcuSeries'][:]
        for index in range(len(labelList)):
            if label == labelList[index]:
                return index
        return 0

    def setLanguage( self ):
        isEnglishLanguage = self.m_menuItem_english.IsChecked()
        self.toolCommDict['isEnglishLanguage'] = isEnglishLanguage
        lastIndex = self._getLastLangIndex()
        langIndex = 0
        if isEnglishLanguage:
            langIndex = uilang.kLanguageIndex_English
        else:
            langIndex = uilang.kLanguageIndex_Chinese
        self.languageIndex = langIndex
        uivar.setRuntimeSettings(None, None, None, self.languageIndex)
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_File, uilang.kMainLanguageContentDict['menu_file'][langIndex])
        self.m_menuItem_exit.SetItemLabel(uilang.kMainLanguageContentDict['mItem_exit'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Edit, uilang.kMainLanguageContentDict['menu_edit'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_View, uilang.kMainLanguageContentDict['menu_view'][langIndex])
        # Hard way to set label for submenu
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Tools, uilang.kMainLanguageContentDict['menu_tools'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_runMode'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_runMode'][langIndex])
        self.m_menuItem_runModeEntry.SetItemLabel(uilang.kMainLanguageContentDict['mItem_runModeEntry'][langIndex])
        self.m_menuItem_runModeMaster.SetItemLabel(uilang.kMainLanguageContentDict['mItem_runModeMaster'][langIndex])
        self.m_menuItem_runModeOta.SetItemLabel(uilang.kMainLanguageContentDict['mItem_runModeOta'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_usbDetection'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_usbDetection'][langIndex])
        self.m_menuItem_usbDetectionDynamic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionDynamic'][langIndex])
        self.m_menuItem_usbDetectionStatic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_usbDetectionStatic'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_genSbFile'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_genSbFile'][langIndex])
        self.m_menuItem_genSbFileYes.SetItemLabel(uilang.kMainLanguageContentDict['mItem_genSbFileYes'][langIndex])
        self.m_menuItem_genSbFileNo.SetItemLabel(uilang.kMainLanguageContentDict['mItem_genSbFileNo'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_imageReadback'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_imageReadback'][langIndex])
        self.m_menuItem_imageReadbackAutomatic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_imageReadbackAutomatic'][langIndex])
        self.m_menuItem_imageReadbackManual.SetItemLabel(uilang.kMainLanguageContentDict['mItem_imageReadbackManual'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_flashloaderResident'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_flashloaderResident'][langIndex])
        self.m_menuItem_flashloaderResidentDefault.SetItemLabel(uilang.kMainLanguageContentDict['mItem_flashloaderResidentDefault'][langIndex])
        self.m_menuItem_flashloaderResidentItcm.SetItemLabel(uilang.kMainLanguageContentDict['mItem_flashloaderResidentItcm'][langIndex])
        self.m_menuItem_flashloaderResidentDtcm.SetItemLabel(uilang.kMainLanguageContentDict['mItem_flashloaderResidentDtcm'][langIndex])
        self.m_menuItem_flashloaderResidentOcram.SetItemLabel(uilang.kMainLanguageContentDict['mItem_flashloaderResidentOcram'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_efuseGroup'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_efuseGroup'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_efuseLocker'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_efuseLocker'][langIndex])
        self.m_menuItem_efuseLockerAutomatic.SetItemLabel(uilang.kMainLanguageContentDict['mItem_efuseLockerAutomatic'][langIndex])
        self.m_menuItem_efuseLockerManual.SetItemLabel(uilang.kMainLanguageContentDict['mItem_efuseLockerManual'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_ivtEntryType'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_ivtEntryType'][langIndex])
        self.m_menuItem_ivtEntryResetHandler.SetItemLabel(uilang.kMainLanguageContentDict['mItem_ivtEntryReset'][langIndex])
        self.m_menuItem_ivtEntryVectorTable.SetItemLabel(uilang.kMainLanguageContentDict['mItem_ivtEntryVector'][langIndex])
        self.m_menu_tools.SetLabel(self.m_menu_tools.FindItem(uilang.kMainLanguageContentDict['subMenu_edgelockFwOpt'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_edgelockFwOpt'][langIndex])
        self.m_menuItem_edgelockFwEn.SetItemLabel(uilang.kMainLanguageContentDict['mItem_edgelockFwEn'][langIndex])
        self.m_menuItem_edgelockFwDis.SetItemLabel(uilang.kMainLanguageContentDict['mItem_edgelockFwDis'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Window, uilang.kMainLanguageContentDict['menu_window'][langIndex])
        self.m_menu_window.SetLabel(self.m_menu_window.FindItem(uilang.kMainLanguageContentDict['subMenu_soundEffect'][lastIndex]), uilang.kMainLanguageContentDict['subMenu_soundEffect'][langIndex])
        self.m_menuItem_soundEffectContra.SetItemLabel(uilang.kMainLanguageContentDict['mItem_soundEffectContra'][langIndex])
        self.m_menuItem_soundEffectMario.SetItemLabel(uilang.kMainLanguageContentDict['mItem_soundEffectMario'][langIndex])
        self.m_menuItem_soundEffectQuiet.SetItemLabel(uilang.kMainLanguageContentDict['mItem_soundEffectQuiet'][langIndex])
        self.m_menubar.SetMenuLabel(uilang.kMenuPosition_Help, uilang.kMainLanguageContentDict['menu_help'][langIndex])
        self.m_menuItem_homePage.SetItemLabel(uilang.kMainLanguageContentDict['mItem_homePage'][langIndex])
        self.m_menuItem_aboutAuthor.SetItemLabel(uilang.kMainLanguageContentDict['mItem_aboutAuthor'][langIndex])
        self.m_menuItem_contributors.SetItemLabel(uilang.kMainLanguageContentDict['mItem_contributors'][langIndex])
        self.m_menuItem_specialThanks.SetItemLabel(uilang.kMainLanguageContentDict['mItem_specialThanks'][langIndex])
        self.m_menuItem_revisionHistory.SetItemLabel(uilang.kMainLanguageContentDict['mItem_revisionHistory'][langIndex])

        self.m_notebook_targetSetup.SetPageText(0, uilang.kMainLanguageContentDict['panel_targetSetup'][langIndex])
        self.m_staticText_mcuSeries.SetLabel(uilang.kMainLanguageContentDict['sText_mcuSeries'][langIndex])
        self.m_staticText_mcuDevice.SetLabel(uilang.kMainLanguageContentDict['sText_mcuDevice'][langIndex])
        self.m_staticText_bootDevice.SetLabel(uilang.kMainLanguageContentDict['sText_bootDevice'][langIndex])
        self.m_button_bootDeviceConfiguration.SetLabel(uilang.kMainLanguageContentDict['button_bootDeviceConfiguration'][langIndex])
        self.m_button_deviceConfigurationData.SetLabel(uilang.kMainLanguageContentDict['button_deviceConfigurationData'][langIndex])
        self.m_button_externalMemConfigurationData.SetLabel(uilang.kMainLanguageContentDict['button_externalMemConfigurationData'][langIndex])

        self.m_notebook_portSetup.SetPageText(0, uilang.kMainLanguageContentDict['panel_portSetup'][langIndex])
        self.m_radioBtn_uart.SetLabel(uilang.kMainLanguageContentDict['radioBtn_uart'][langIndex])
        self.m_radioBtn_usbhid.SetLabel(uilang.kMainLanguageContentDict['radioBtn_usbhid'][langIndex])
        if self.hasDynamicLableBeenInit:
            if self.isUartPortSelected:
                self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_comPort'][langIndex])
                self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_baudrate'][langIndex])
            elif self.isUsbhidPortSelected:
                self.m_staticText_portVid.SetLabel(uilang.kMainLanguageContentDict['sText_vid'][langIndex])
                self.m_staticText_baudPid.SetLabel(uilang.kMainLanguageContentDict['sText_pid'][langIndex])
            else:
                pass
        self.m_checkBox_oneStepConnect.SetLabel(uilang.kMainLanguageContentDict['checkBox_oneStepConnect'][langIndex])
        if self.connectStatusColor != None:
            self.updateConnectStatus(self.connectStatusColor)

        self.m_notebook_deviceStatus.SetPageText(0, uilang.kMainLanguageContentDict['panel_deviceStatus'][langIndex])

        self.m_staticText_secureBootType.SetLabel(uilang.kMainLanguageContentDict['sText_secureBootType'][langIndex])
        self.m_button_allInOneAction.SetLabel(uilang.kMainLanguageContentDict['button_allInOneAction'][langIndex])

        self.m_notebook_cmdLog.SetPageText(0, uilang.kMainLanguageContentDict['panel_cmdLog'][langIndex])
        self.m_button_clearCmdLog.SetLabel(uilang.kMainLanguageContentDict['button_clearCmdLog'][langIndex])
        self.m_button_saveCmdLog.SetLabel(uilang.kMainLanguageContentDict['button_SaveCmdLog'][langIndex])

    def setCostTime( self, costTimeSec ):
        minValueStr = '00'
        secValueStr = '00'
        millisecValueStr = '000'
        if costTimeSec != 0:
            costTimeSecMod = math.modf(costTimeSec)
            minValue = int(costTimeSecMod[1] / 60)
            if minValue < 10:
                minValueStr = '0' + str(minValue)
            elif minValue <= 59:
                minValueStr = str(minValue)
            else:
                minValueStr = 'xx'
            secValue = int(costTimeSecMod[1]) % 60
            if secValue < 10:
                secValueStr = '0' + str(secValue)
            else:
                secValueStr = str(secValue)
            millisecValue = int(costTimeSecMod[0] * 1000)
            if millisecValue < 10:
                millisecValueStr = '00' + str(millisecValue)
            elif millisecValue < 100:
                millisecValueStr = '0' + str(millisecValue)
            else:
                millisecValueStr = str(millisecValue)
        self.m_staticText_costTime.SetLabel(' ' + minValueStr + ':' + secValueStr + '.' + millisecValueStr)

    def updateCostTime( self ):
        curTime = time.time()
        self.setCostTime(curTime - self.lastTime)

    def setBootLogInfo( self ):
        self.m_textCtrl_logStart.Enable( False )
        self.m_textCtrl_logStart.Clear()
        self.m_textCtrl_logLength.Enable( False )
        self.m_textCtrl_logLength.Clear()
        if self.tgt.bootLogStart != None:
            self.m_textCtrl_logStart.write(str(hex(self.tgt.bootLogStart)))
            self.m_textCtrl_logLength.write(str(self.tgt.bootLogLength))
