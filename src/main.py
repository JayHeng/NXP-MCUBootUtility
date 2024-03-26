#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
import threading
import inspect
import ctypes
from _main import MCX_main
from _main import Kinetis_main
from _main import LPC_main
from _main import RTxxx_main
from _main import RTyyyy_main
from ui import RTyyyy_uidef
from ui import RTxxx_uidef
from ui import LPC_uidef
from ui import Kinetis_uidef
from ui import MCX_uidef
from ui import uidef
from ui import uivar
from ui import uilang
from ui import ui_cfg_flexspinor
from ui import ui_cfg_flexspinand
from ui import ui_cfg_semcnor
from ui import ui_cfg_semcnand
from ui import ui_cfg_usdhcsd
from ui import ui_cfg_usdhcmmc
from ui import ui_cfg_recoveryspinor

g_main_win = None
g_task_detectUsbhid = None
g_task_playSound = None
g_task_increaseGauge = None
g_task_accessMem = None
g_RTyyyy_task_allInOneAction = None
g_RTxxx_task_allInOneAction = None
g_LPC_task_allInOneAction = None
g_Kinetis_task_allInOneAction = None
g_MCX_task_allInOneAction = None
g_RTyyyy_task_showSettedEfuse = None

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class secBootMain(MCX_main.secBootMcxMain):

    def __init__(self, parent):
        MCX_main.secBootMcxMain.__init__(self, parent)

        self.isAccessMemTaskPending = False
        self.accessMemType = ''
        self.lastTime = None
        self._previousToolRunMode = None

    def _startGaugeTimer( self ):
        self.lastTime = time.time()
        self.initGauge()

    def _stopGaugeTimer( self ):
        self.deinitGauge()
        self.updateCostTime()

    def _setupMcuTargets( self ):
        self.setTargetSetupValue()
        self._switchEfuseGroup()
        self._setUartUsbPort()
        if self._isRunModeRelatedToOta():
            self.isMcuSeriesChanged = True
        if self.isMcuSeriesChanged:
            if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
                self.RTyyyy_callbackSetMcuSeries()
            elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
                self.RTxxx_callbackSetMcuSeries()
            elif self.mcuSeries == uidef.kMcuSeries_LPC:
                self.LPC_callbackSetMcuSeries()
            elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
                self.Kinetis_callbackSetMcuSeries()
            elif self.mcuSeries == uidef.kMcuSeries_MCX:
                self.MCX_callbackSetMcuSeries()
            else:
                pass
            self.isMcuSeriesChanged = False
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackSetMcuDevice()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackSetMcuDevice()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackSetMcuDevice()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackSetMcuDevice()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackSetMcuDevice()
        else:
            pass

    def callbackSetMcuSeries( self, event ):
        self._setupMcuTargets()

    def callbackSetMcuDevice( self, event ):
        self._setupMcuTargets()

    def callbackSetBootDevice( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackSetBootDevice()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackSetBootDevice()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackSetBootDevice()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackSetBootDevice()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackSetBootDevice()
        else:
            pass

    def _hasMultipleFlexspiInstance( self ):
        return self.tgt.flexspiNorMemBase0 != None and self.tgt.flexspiNorMemBase1 != None

    def callbackBootDeviceConfiguration( self, event ):
        if self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            if self.tgt.isSipFlexspiNorDevice:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['bootDeviceInfo_hasOnchipSerialNor'][self.languageIndex])
                return
        if self.checkIfSubWinHasBeenOpened():
            return
        if self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor or \
           self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            flexspiNorFrame = ui_cfg_flexspinor.secBootUiCfgFlexspiNor(None)
            if self.bootDevice == RTxxx_uidef.kBootDevice_QuadspiNor:
                flexspiNorFrame.SetTitle(uilang.kSubLanguageContentDict['quadspinor_title'][self.languageIndex])
            else:
                flexspiNorFrame.SetTitle(uilang.kSubLanguageContentDict['flexspinor_title'][self.languageIndex])
            flexspiNorFrame.setNecessaryInfo(self.mcuSeries, self.tgt.flexspiFreqs, self.cfgFdcbBinFilename, self.tgt.hasFlexspiNorDualImageBoot, self._hasMultipleFlexspiInstance())
            flexspiNorFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_FlexspiNand:
            flexspiNandFrame = ui_cfg_flexspinand.secBootUiFlexspiNand(None)
            flexspiNandFrame.SetTitle(uilang.kSubLanguageContentDict['flexspinand_title'][self.languageIndex])
            flexspiNandFrame.setNecessaryInfo(self._hasMultipleFlexspiInstance())
            flexspiNandFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNor:
            semcNorFrame = ui_cfg_semcnor.secBootUiSemcNor(None)
            semcNorFrame.SetTitle(u"SEMC NOR Device Configuration")
            semcNorFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_SemcNand:
            semcNandFrame = ui_cfg_semcnand.secBootUiCfgSemcNand(None)
            semcNandFrame.SetTitle(uilang.kSubLanguageContentDict['semcnand_title'][self.languageIndex])
            semcNandFrame.setNecessaryInfo(self.tgt.isSwEccSetAsDefaultInNandOpt)
            semcNandFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcSd or \
             self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            usdhcSdFrame = ui_cfg_usdhcsd.secBootUiUsdhcSd(None)
            usdhcSdFrame.SetTitle(uilang.kSubLanguageContentDict['usdhcsd_title'][self.languageIndex])
            usdhcSdFrame.setNecessaryInfo(self.tgt.hasMultiUsdhcBootInstance)
            usdhcSdFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_UsdhcMmc or \
             self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            usdhcMmcFrame = ui_cfg_usdhcmmc.secBootUiUsdhcMmc(None)
            usdhcMmcFrame.SetTitle(uilang.kSubLanguageContentDict['usdhcmmc_title'][self.languageIndex])
            usdhcMmcFrame.setNecessaryInfo(self.tgt.hasMultiUsdhcBootInstance)
            usdhcMmcFrame.Show(True)
        elif self.bootDevice == RTyyyy_uidef.kBootDevice_LpspiNor or \
             self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            recoverySpiNorFrame = ui_cfg_recoveryspinor.secBootUiCfgRecoverySpiNor(None)
            if self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
                recoverySpiNorFrame.SetTitle(uilang.kSubLanguageContentDict['flexcommspinor_title'][self.languageIndex])
            else:
                recoverySpiNorFrame.SetTitle(uilang.kSubLanguageContentDict['lpspinor_title'][self.languageIndex])
            recoverySpiNorFrame.setNecessaryInfo(self.mcuSeries)
            recoverySpiNorFrame.Show(True)
        else:
            pass

    def _setUartUsbPort( self ):
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
        retryToDetectUsb = False
        showError = True
        self.setPortSetupValue(self.connectStage, usbIdList, retryToDetectUsb, showError)

    def callbackSetUartPort( self, event ):
        self._setUartUsbPort()

    def callbackSetUsbhidPort( self, event ):
        self._setUartUsbPort()

    def callbackSetOneStep( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self.getOneStepConnectMode()
        else:
            self.initOneStepConnectMode()
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_cannotSetOneStep'][self.languageIndex])

    def callbackConnectToDevice( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackConnectToDevice()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackConnectToDevice()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackConnectToDevice()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackConnectToDevice()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackConnectToDevice()
        else:
            pass

    def callbackSetSecureBootType( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackSetSecureBootType()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackSetSecureBootType()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackSetSecureBootType()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackSetSecureBootType()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackSetSecureBootType()
        else:
            pass

    def callbackAllInOneAction( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackAllInOneAction()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackAllInOneAction()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackAllInOneAction()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackAllInOneAction()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackAllInOneAction()
        else:
            pass

    def callbackChangedAppFile( self, event ):
        self.getUserAppFilePath()
        self.setCostTime(0)
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_setSecureBootButtonColor()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_setSecureBootButtonColor()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_setSecureBootButtonColor()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_setSecureBootButtonColor()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_setSecureBootButtonColor()
        else:
            pass

    def callbackSetAppFormat( self, event ):
        self.getUserAppFileFormat()

    def callbackGenImage( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackGenImage()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackGenImage()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackGenImage()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackGenImage()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackGenImage()
        else:
            pass

    def callbackFlashImage( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackFlashImage()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackFlashImage()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackFlashImage()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackFlashImage()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackFlashImage()
        else:
            pass

    def task_doAccessMem( self ):
        while True:
            if self.isAccessMemTaskPending:
                if self.accessMemType == 'ScanFuse':
                    if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
                        self.RTyyyy_scanAllFuseRegions()
                        if self.isSbFileEnabledToGen:
                            self.RTyyyy_initSbEfuseBdfileContent()
                    elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
                        self.RTxxx_scanAllOtpRegions()
                    else:
                        pass
                elif self.accessMemType == 'BurnFuse':
                    if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
                        self.RTyyyy_burnAllFuseRegions()
                        if self.isSbFileEnabledToGen:
                            self.RTyyyy_genSbEfuseImage()
                    elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
                        self.RTxxx_burnAllOtpRegions()
                    else:
                        pass
                elif self.accessMemType == 'SaveFuse':
                    self.saveFuseRegions()
                elif self.accessMemType == 'LoadFuse':
                    self.loadFuseRegions()
                elif self.accessMemType == 'ReadMem':
                    if self.connectStage == uidef.kConnectStage_ExternalMemory:
                        self.readRamMemory()
                    elif self.connectStage == uidef.kConnectStage_Reset:
                        self.readBootDeviceMemory()
                    else:
                        pass
                elif self.accessMemType == 'EraseMem':
                    self.eraseBootDeviceMemory()
                elif self.accessMemType == 'MassEraseMem':
                    self.massEraseBootDeviceMemory()
                elif self.accessMemType == 'WriteMem':
                    if self.connectStage == uidef.kConnectStage_ExternalMemory:
                        self.writeRamMemory()
                    elif self.connectStage == uidef.kConnectStage_Reset:
                        self.writeBootDeviceMemory()
                    else:
                        pass
                elif self.accessMemType == 'EccWriteMem':
                    if self.connectStage == uidef.kConnectStage_Reset:
                        self.eccWriteBootDeviceMemory()
                    else:
                        pass
                else:
                    pass
                self.isAccessMemTaskPending = False
                self._stopGaugeTimer()
            time.sleep(1)

    def callbackScanFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'ScanFuse'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackBurnFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'BurnFuse'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackSaveFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'SaveFuse'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackLoadFuse( self, event ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'LoadFuse'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackViewMem( self, event ):
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_callbackViewMem()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_callbackViewMem()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_callbackViewMem()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_callbackViewMem()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_callbackViewMem()
        else:
            pass

    def callbackClearMem( self, event ):
        self.clearMem()

    def _doReadMem( self ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'ReadMem'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackReadMem( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doReadMem()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def _doEraseMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'EraseMem'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotCfgBootDevice'][self.languageIndex])

    def callbackEraseMem( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doEraseMem()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def _doMassEraseMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'MassEraseMem'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotCfgBootDevice'][self.languageIndex])

    def callbackMassEraseMem( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doMassEraseMem()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def _doWriteMem( self ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'WriteMem'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackWriteMem( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doWriteMem()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def _doEccWriteMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            self._startGaugeTimer()
            self.isAccessMemTaskPending = True
            self.accessMemType = 'EccWriteMem'
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotCfgBootDevice'][self.languageIndex])

    def callbackEccWriteMem( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doEccWriteMem()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def _doExecuteApp( self ):
        if self.connectStage == uidef.kConnectStage_ExternalMemory or \
           self.connectStage == uidef.kConnectStage_Reset:
            self.executeAppInFlexram()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_hasnotEnterFl'][self.languageIndex])

    def callbackExecuteApp( self, event ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._doExecuteApp()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['operMemError_notAvailUnderEntry'][self.languageIndex])

    def callbackClearLog( self, event ):
        self.clearLog()

    def callbackSaveLog( self, event ):
        self.saveLog()

    def _stopTask( self, thread ):
        _async_raise(thread.ident, SystemExit)

    def _deinitToolToExit( self ):
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)
        uivar.deinitVar()
        #exit(0)
        self._stopTask(g_task_detectUsbhid)
        self._stopTask(g_task_playSound)
        self._stopTask(g_task_increaseGauge)
        self._stopTask(g_task_accessMem)
        self._stopTask(g_RTyyyy_task_allInOneAction)
        self._stopTask(g_RTxxx_task_allInOneAction)
        self._stopTask(g_LPC_task_allInOneAction)
        self._stopTask(g_Kinetis_task_allInOneAction)
        self._stopTask(g_MCX_task_allInOneAction)
        self._stopTask(g_RTyyyy_task_showSettedEfuse)
        global g_main_win
        g_main_win.Show(False)
        try:
            self.Destroy()
        except:
            pass

    def callbackExit( self, event ):
        self._deinitToolToExit()

    def callbackClose( self, event ):
        self._deinitToolToExit()

    def _isRunModeRelatedToOta( self ):
        normalRunModeList = [uidef.kToolRunMode_Entry, uidef.kToolRunMode_Master]
        return (not ((self._previousToolRunMode in normalRunModeList) and (self.toolRunMode in normalRunModeList)))

    def _switchToolRunMode( self ):
        if self._isRunModeRelatedToOta():
            self._setupMcuTargets()
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_switchToolRunMode()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_switchToolRunMode()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_switchToolRunMode()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_switchToolRunMode()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_switchToolRunMode()
        else:
            pass
        self.enableOneStepForEntryMode()

    def callbackSetRunModeAsEntry( self, event ):
        self._previousToolRunMode = self.toolRunMode
        self.setToolRunMode()
        self._switchToolRunMode()

    def callbackSetRunModeAsMaster( self, event ):
        self._previousToolRunMode = self.toolRunMode
        self.setToolRunMode()
        self._switchToolRunMode()

    def callbackSetRunModeAsOta( self, event ):
        self._previousToolRunMode = self.toolRunMode
        self.setToolRunMode()
        self._switchToolRunMode()

    def callbackSetUsbDetectionAsDynamic( self, event ):
        self.setUsbDetection()

    def callbackSetUsbDetectionAsStatic( self, event ):
        self.setUsbDetection()

    def callbackSetSoundEffectAsContra( self, event ):
        self.setSoundEffect()

    def callbackSetSoundEffectAsMario( self, event ):
        self.setSoundEffect()

    def callbackSetSoundEffectAsQuiet( self, event ):
        self.setSoundEffect()

    def callbackSetGenSbFileAsYes( self, event ):
        self.setGenSbFile()

    def callbackSetGenSbFileAsNo( self, event ):
        self.setGenSbFile()

    def callbackSetImageReadbackAsAutomatic( self, event ):
        self.setImageReadback()

    def callbackSetImageReadbackAsManual( self, event ):
        self.setImageReadback()

    def callbackSetFlashloaderResidentToDefault( self, event ):
        self.setFlashloaderResident()

    def callbackSetFlashloaderResidentToItcm( self, event ):
        self.setFlashloaderResident()

    def callbackSetFlashloaderResidentToDtcm( self, event ):
        self.setFlashloaderResident()

    def callbackSetFlashloaderResidentToOcram( self, event ):
        self.setFlashloaderResident()

    def _switchEfuseGroup( self ):
        self.setEfuseGroup()
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_updateFuseRegionField()
            self.RTyyyy_updateFuseGroupText()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_updateOtpRegionField()
            self.RTxxx_updateOtpGroupText()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            pass
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            pass
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            pass
        else:
            pass

    def callbackSetEfuseGroupTo0( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo1( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo2( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo3( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo4( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo5( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseGroupTo6( self, event ):
        self._switchEfuseGroup()

    def callbackSetEfuseLockerAsAutomatic( self, event ):
        self.setEfuseLocker()

    def callbackSetEfuseLockerAsManual( self, event ):
        self.setEfuseLocker()

    def callbackSetIvtEntryToResetHandler( self, event ):
        self.setIvtEntryType()

    def callbackSetIvtEntryToVectorTable( self, event ):
        self.setIvtEntryType()

    def callbackDisableEdgelockFw( self, event ):
        self.setEdgelockFwOption()

    def callbackEnableEdgelockFw( self, event ):
        self.setEdgelockFwOption()

    def _doSetLanguage( self ):
        self.setLanguage()
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_setLanguage()
        elif self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_setLanguage()
        elif self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_setLanguage()
        elif self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self.Kinetis_setLanguage()
        elif self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_setLanguage()
        else:
            pass

    def callbackSetLanguageAsEnglish( self, event ):
        self._doSetLanguage()

    def callbackSetLanguageAsChinese( self, event ):
        self._doSetLanguage()

    def callbackShowHomePage( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['homePage_info'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['homePage_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowAboutAuthor( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['aboutAuthor_author'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_email2'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['aboutAuthor_blog'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['aboutAuthor_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowContributors( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['contributors_info'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['contributors_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowSpecialThanks( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['specialThanks_info'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['specialThanks_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

    def callbackShowRevisionHistory( self, event ):
        msgText = ((uilang.kMsgLanguageContentDict['revisionHistory_v1_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v1_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v1_2_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v1_3_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v1_4_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_2_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_3_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_3_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v2_4_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_1_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_2_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_3_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_3_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_4_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v3_5_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v4_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v4_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v4_1_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_2_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_2_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_3_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_3_1'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v5_3_2'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v6_0_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v6_1_0'][self.languageIndex]) +
                   (uilang.kMsgLanguageContentDict['revisionHistory_v6_2_0'][self.languageIndex]))
        wx.MessageBox(msgText, uilang.kMsgLanguageContentDict['revisionHistory_title'][self.languageIndex], wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()

    g_main_win = secBootMain(None)
    g_main_win.SetTitle(u"NXP MCU Boot Utility v6.2.0")
    g_main_win.Show()

    g_task_detectUsbhid = threading.Thread(target=g_main_win.task_doDetectUsbhid)
    g_task_detectUsbhid.setDaemon(True)
    g_task_detectUsbhid.start()
    g_task_playSound = threading.Thread(target=g_main_win.task_doPlaySound)
    g_task_playSound.setDaemon(True)
    g_task_playSound.start()
    g_task_increaseGauge = threading.Thread(target=g_main_win.task_doIncreaseGauge)
    g_task_increaseGauge.setDaemon(True)
    g_task_increaseGauge.start()
    g_task_accessMem = threading.Thread(target=g_main_win.task_doAccessMem)
    g_task_accessMem.setDaemon(True)
    g_task_accessMem.start()

    g_RTyyyy_task_allInOneAction = threading.Thread(target=g_main_win.RTyyyy_task_doAllInOneAction)
    g_RTyyyy_task_allInOneAction.setDaemon(True)
    g_RTyyyy_task_allInOneAction.start()
    g_RTxxx_task_allInOneAction = threading.Thread(target=g_main_win.RTxxx_task_doAllInOneAction)
    g_RTxxx_task_allInOneAction.setDaemon(True)
    g_RTxxx_task_allInOneAction.start()
    g_LPC_task_allInOneAction = threading.Thread(target=g_main_win.LPC_task_doAllInOneAction)
    g_LPC_task_allInOneAction.setDaemon(True)
    g_LPC_task_allInOneAction.start()
    g_Kinetis_task_allInOneAction = threading.Thread(target=g_main_win.Kinetis_task_doAllInOneAction)
    g_Kinetis_task_allInOneAction.setDaemon(True)
    g_Kinetis_task_allInOneAction.start()
    g_MCX_task_allInOneAction = threading.Thread(target=g_main_win.MCX_task_doAllInOneAction)
    g_MCX_task_allInOneAction.setDaemon(True)
    g_MCX_task_allInOneAction.start()

    g_RTyyyy_task_showSettedEfuse = threading.Thread(target=g_main_win.RTyyyy_task_doShowSettedEfuse)
    g_RTyyyy_task_showSettedEfuse.setDaemon(True)
    g_RTyyyy_task_showSettedEfuse.start()

    app.MainLoop()

