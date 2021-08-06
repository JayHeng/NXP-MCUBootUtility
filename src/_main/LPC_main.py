#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
sys.path.append(os.path.abspath(".."))
from mem import LPC_memcore
from ui import LPC_uidef
from ui import uidef
from ui import uivar
from ui import uilang

kRetryPingTimes = 5

class secBootLpcMain(LPC_memcore.secBootLpcMem):

    def __init__(self, parent):
        LPC_memcore.secBootLpcMem.__init__(self, parent)
        self.LPC_isAllInOneActionTaskPending = False
        if self.mcuSeries == uidef.kMcuSeries_LPC:
            self._LPC_initMain()

    def _LPC_initMain( self ):
        if self.toolRunMode != uidef.kToolRunMode_SblOta:
            self.connectStage = uidef.kConnectStage_Rom
            self.updateConnectStatus('black')
        else:
            self.connectStage = uidef.kConnectStage_Flashloader
            self.updateConnectStatus('yellow_ota')
        usbIdList = self.LPC_getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList, False, False)

        self.isBootableAppAllowedToView = False
        self.lastTime = None
        self.isAccessMemTaskPending = False
        self.accessMemType = ''
        self.isThereBoardConnection = False

    def _LPC_startGaugeTimer( self ):
        if not self.LPC_isAllInOneActionTaskPending:
            self.lastTime = time.time()
            self.initGauge()

    def _LPC_stopGaugeTimer( self ):
        if not self.LPC_isAllInOneActionTaskPending:
            self.deinitGauge()
            self.updateCostTime()

    def LPC_callbackSetMcuSeries( self ):
        self.LPC_initUi()
        self.LPC_initGen()
        self.LPC_initRun()
        self.LPC_initMem()
        self._LPC_initMain()
        self.LPC_setTargetSetupValue()

    def LPC_callbackSetMcuDevice( self ):
        self.LPC_setTargetSetupValue()
        needToPlaySound = False
        self.LPC_setSecureBootSeqColor(needToPlaySound)

    def LPC_callbackSetBootDevice( self ):
        self.LPC_setTargetSetupValue()
        needToPlaySound = False
        self.LPC_setSecureBootSeqColor(needToPlaySound)

    def _LPC_retryToPingBootloader( self ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            pingStatus = self.LPC_pingRom()
            if pingStatus:
                break
            pingCnt = pingCnt - 1
            if self.isUsbhidPortSelected:
                time.sleep(2)
        return pingStatus

    def _LPC_connectFailureHandler( self ):
        if self.toolRunMode != uidef.kToolRunMode_SblOta:
            self.connectStage = uidef.kConnectStage_Rom
        else:
            self.connectStage = uidef.kConnectStage_Flashloader
        self.updateConnectStatus('red')
        usbIdList = self.LPC_getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList, False, False)
        self.isBootableAppAllowedToView = False

    def _LPC_connectStateMachine( self, showError=True ):
        connectSteps = LPC_uidef.kConnectStep_Normal
        #self.getOneStepConnectMode()
        retryToDetectUsb = True
        while connectSteps:
            if not self.updatePortSetupValue(retryToDetectUsb, showError):
                if self.connectStage == uidef.kConnectStage_Rom:
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspBoot'][self.languageIndex])
                self._LPC_connectFailureHandler()
                return
            if self.connectStage == uidef.kConnectStage_Rom:
                self.LPC_connectToDevice(self.connectStage)
                if self._LPC_retryToPingBootloader():
                    self.LPC_getMcuDeviceInfoViaRom()
                    self.LPC_getBootDeviceInfoViaRom()
                    self.updateConnectStatus('blue')
                    self.connectStage = uidef.kConnectStage_Reset
                else:
                    self.updateConnectStatus('red')
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspBoot'][self.languageIndex])
                    return
            elif self.connectStage == uidef.kConnectStage_Flashloader:
                # It is only for SBL OTA mode
                self.LPC_connectToDevice(self.connectStage)
                if self._LPC_retryToPingBootloader():
                    self.LPC_getBootDeviceInfoViaRom()
                    self.connectStage = uidef.kConnectStage_Reset
                    self.updateConnectStatus('blue')
                else:
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_failToPingSblIsp'][self.languageIndex])
                    self._LPC_connectFailureHandler()
                    return
            elif self.connectStage == uidef.kConnectStage_Reset:
                self.LPC_resetMcuDevice()
                self.isBootableAppAllowedToView = False
                if self.toolRunMode != uidef.kToolRunMode_SblOta:
                    self.connectStage = uidef.kConnectStage_Rom
                    self.updateConnectStatus('black')
                else:
                    self.connectStage = uidef.kConnectStage_Flashloader
                    self.updateConnectStatus('yellow_ota')
                usbIdList = self.LPC_getUsbid()
                self.setPortSetupValue(self.connectStage, usbIdList, True, True)
                self.LPC_connectToDevice(self.connectStage)
            else:
                pass
            connectSteps -= 1

    def LPC_callbackConnectToDevice( self ):
        self._LPC_startGaugeTimer()
        self.printLog("'Connect to xxx' button is clicked")
        if not self.isSbFileEnabledToGen:
            self._LPC_connectStateMachine(True)
        else:
            if not self.isThereBoardConnection:
                if self.connectStage == uidef.kConnectStage_Rom:
                    self.initSbAppBdfilesContent()
                else:
                    # It means there is board connection
                    self.isThereBoardConnection = True
                self._LPC_connectStateMachine(False)
                if not self.isThereBoardConnection:
                    if self.connectStage == uidef.kConnectStage_Rom:
                        # It means there is no board connection, but we need to set it as True for SB generation
                        self.isThereBoardConnection = True
                        self.LPC_isDeviceEnabledToOperate = False
                        self.connectStage = uidef.kConnectStage_Reset
                        self.updateConnectStatus('blue')
                else:
                    self.isThereBoardConnection = False
            else:
                self.isThereBoardConnection = False
                self.LPC_isDeviceEnabledToOperate = True
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
        self._LPC_stopGaugeTimer()

    def LPC_callbackSetSecureBootType( self ):
        self.setCostTime(0)
        self.LPC_setSecureBootSeqColor()

    def LPC_task_doAllInOneAction( self ):
        while True:
            if self.LPC_isAllInOneActionTaskPending:
                self._LPC_doAllInOneAction()
                self.LPC_isAllInOneActionTaskPending = False
                self._LPC_stopGaugeTimer()
            time.sleep(1)

    def _LPC_doAllInOneAction( self ):
        allInOneSeqCnt = 1
        status = False
        while allInOneSeqCnt:
            status = self._LPC_doGenImage()
            if not status:
                break
            status = self._LPC_doFlashImage()
            if not status:
                break
            allInOneSeqCnt -= 1
        if status and self.isAutomaticImageReadback:
            self.showPageInMainBootSeqWin(uidef.kPageIndex_BootDeviceMemory)
            self._LPC_doViewMem()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_AllInOne, status)

    def LPC_callbackAllInOneAction( self ):
        self._LPC_startGaugeTimer()
        self.LPC_isAllInOneActionTaskPending = True

    def _LPC_doGenImage( self ):
        status = False
        self._LPC_startGaugeTimer()
        self.printLog("'Generate Bootable Image' button is clicked")
        if self.LPC_createFinalBtAppfile():
            if self.LPC_genBootableImage():
                status = True
        self._LPC_stopGaugeTimer()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_GenImage, status)
        return status

    def LPC_callbackGenImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._LPC_doGenImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _LPC_doFlashImage( self ):
        status = False
        if self.connectStage == uidef.kConnectStage_Reset:
            self._LPC_startGaugeTimer()
            self.printLog("'Load Bootable Image' button is clicked")
            if not self.LPC_flashBootableImage():
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_failToFlashImage'][self.languageIndex])
            else:
                self.isBootableAppAllowedToView = True
                status = True
            self._LPC_stopGaugeTimer()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspBoot'][self.languageIndex])
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_FlashImage, status)
        return status

    def LPC_callbackFlashImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._LPC_doFlashImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _LPC_doViewMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            if self.isBootableAppAllowedToView:
                self._LPC_startGaugeTimer()
                self.LPC_readProgrammedMemoryAndShow()
                self._LPC_stopGaugeTimer()
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotFlashImage'][self.languageIndex])
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckIspBoot'][self.languageIndex])

    def LPC_callbackViewMem( self ):
        self._LPC_doViewMem()

    def LPC_switchToolRunMode( self ):
        pass

