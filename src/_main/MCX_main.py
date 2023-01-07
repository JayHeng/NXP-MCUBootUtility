#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
sys.path.append(os.path.abspath(".."))
from mem import MCX_memcore
from ui import MCX_uidef
from ui import uidef
from ui import uivar
from ui import uilang

kRetryPingTimes = 5

class secBootMcxMain(MCX_memcore.secBootMcxMem):

    def __init__(self, parent):
        MCX_memcore.secBootMcxMem.__init__(self, parent)
        self.MCX_isAllInOneActionTaskPending = False
        if self.mcuSeries == uidef.kMcuSeries_MCX:
            self._MCX_initMain()

    def _MCX_initMain( self ):
        self.connectStage = uidef.kConnectStage_Rom
        self.updateConnectStatus('black')
        self.isBootableAppAllowedToView = False
        self.lastTime = None
        self.isAccessMemTaskPending = False
        self.accessMemType = ''
        self.isThereBoardConnection = False

    def _MCX_startGaugeTimer( self ):
        if not self.MCX_isAllInOneActionTaskPending:
            self.lastTime = time.time()
            self.initGauge()

    def _MCX_stopGaugeTimer( self ):
        if not self.MCX_isAllInOneActionTaskPending:
            self.deinitGauge()
            self.updateCostTime()

    def MCX_callbackSetMcuSeries( self ):
        self.MCX_initUi()
        self.MCX_initGen()
        self.MCX_initRun()
        self.MCX_initMem()
        self._MCX_initMain()
        self.MCX_setTargetSetupValue()

    def MCX_callbackSetMcuDevice( self ):
        self.MCX_setTargetSetupValue()
        needToPlaySound = False
        self.MCX_setSecureBootSeqColor(needToPlaySound)

    def MCX_callbackSetBootDevice( self ):
        self.MCX_setTargetSetupValue()
        needToPlaySound = False
        self.MCX_setSecureBootSeqColor(needToPlaySound)

    def _MCX_retryToPingBootloader( self ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            pingStatus = self.MCX_pingRom()
            if pingStatus:
                break
            pingCnt = pingCnt - 1
            if self.isUsbhidPortSelected:
                time.sleep(2)
        return pingStatus

    def _MCX_connectFailureHandler( self ):
        self.connectStage = uidef.kConnectStage_Rom
        self.updateConnectStatus('red')
        usbIdList = self.MCX_getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList, False, False)
        self.isBootableAppAllowedToView = False

    def _MCX_connectStateMachine( self, showError=True ):
        connectSteps = MCX_uidef.kConnectStep_Normal
        #self.getOneStepConnectMode()
        retryToDetectUsb = True
        while connectSteps:
            if not self.updatePortSetupValue(retryToDetectUsb, showError):
                if self.connectStage == uidef.kConnectStage_Rom:
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspMode'][self.languageIndex])
                self._MCX_connectFailureHandler()
                return
            if self.connectStage == uidef.kConnectStage_Rom:
                self.MCX_connectToDevice(self.connectStage)
                if self._MCX_retryToPingBootloader():
                    self.MCX_getMcuDeviceInfoViaRom()
                    self.MCX_getBootDeviceInfoViaRom()
                    self.updateConnectStatus('blue')
                    self.connectStage = uidef.kConnectStage_Reset
                else:
                    self.updateConnectStatus('red')
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspMode'][self.languageIndex])
                    return
            elif self.connectStage == uidef.kConnectStage_Reset:
                self.MCX_resetMcuDevice()
                self.isBootableAppAllowedToView = False
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
                usbIdList = self.MCX_getUsbid()
                self.setPortSetupValue(self.connectStage, usbIdList, True, True)
                self.MCX_connectToDevice(self.connectStage)
            else:
                pass
            connectSteps -= 1

    def MCX_callbackConnectToDevice( self ):
        self._MCX_startGaugeTimer()
        self.printLog("'Connect to xxx' button is clicked")
        if not self.isSbFileEnabledToGen:
            self._MCX_connectStateMachine(True)
        else:
            if not self.isThereBoardConnection:
                if self.connectStage == uidef.kConnectStage_Rom:
                    self.initSbAppBdfilesContent()
                else:
                    # It means there is board connection
                    self.isThereBoardConnection = True
                self._MCX_connectStateMachine(False)
                if not self.isThereBoardConnection:
                    if self.connectStage == uidef.kConnectStage_Rom:
                        # It means there is no board connection, but we need to set it as True for SB generation
                        self.isThereBoardConnection = True
                        self.MCX_isDeviceEnabledToOperate = False
                        self.connectStage = uidef.kConnectStage_Reset
                        self.updateConnectStatus('blue')
                else:
                    self.isThereBoardConnection = False
            else:
                self.isThereBoardConnection = False
                self.MCX_isDeviceEnabledToOperate = True
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
        self._MCX_stopGaugeTimer()

    def MCX_callbackSetSecureBootType( self ):
        self.setCostTime(0)
        self.MCX_setSecureBootSeqColor()

    def MCX_task_doAllInOneAction( self ):
        while True:
            if self.MCX_isAllInOneActionTaskPending:
                self._MCX_doAllInOneAction()
                self.MCX_isAllInOneActionTaskPending = False
                self._MCX_stopGaugeTimer()
            time.sleep(1)

    def _MCX_doAllInOneAction( self ):
        allInOneSeqCnt = 1
        status = False
        while allInOneSeqCnt:
            status = self._MCX_doGenImage()
            if not status:
                break
            status = self._MCX_doFlashImage()
            if not status:
                break
            allInOneSeqCnt -= 1
        if status and self.isAutomaticImageReadback:
            self.showPageInMainBootSeqWin(uidef.kPageIndex_BootDeviceMemory)
            self._MCX_doViewMem()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_AllInOne, status)

    def MCX_callbackAllInOneAction( self ):
        self._MCX_startGaugeTimer()
        self.MCX_isAllInOneActionTaskPending = True

    def _MCX_doGenImage( self ):
        status = False
        self._MCX_startGaugeTimer()
        self.printLog("'Generate Bootable Image' button is clicked")
        if self.MCX_createFinalBtAppfile():
            if self.MCX_genBootableImage():
                status = True
        self._MCX_stopGaugeTimer()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_GenImage, status)
        return status

    def MCX_callbackGenImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._MCX_doGenImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _MCX_doFlashImage( self ):
        status = False
        if self.connectStage == uidef.kConnectStage_Reset:
            self._MCX_startGaugeTimer()
            self.printLog("'Load Bootable Image' button is clicked")
            if not self.MCX_flashBootableImage():
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_failToFlashImage'][self.languageIndex])
            else:
                self.isBootableAppAllowedToView = True
                status = True
            self._MCX_stopGaugeTimer()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_FlashImage, status)
        return status

    def MCX_callbackFlashImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._MCX_doFlashImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _MCX_doViewMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            if self.isBootableAppAllowedToView:
                self._MCX_startGaugeTimer()
                self.MCX_readProgrammedMemoryAndShow()
                self._MCX_stopGaugeTimer()
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotFlashImage'][self.languageIndex])
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])

    def MCX_callbackViewMem( self ):
        self._MCX_doViewMem()

    def MCX_switchToolRunMode( self ):
        pass

