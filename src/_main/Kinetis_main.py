#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time
sys.path.append(os.path.abspath(".."))
from mem import Kinetis_memcore
from ui import Kinetis_uidef
from ui import uidef
from ui import uivar
from ui import uilang

kRetryPingTimes = 5

class secBootKinetisMain(Kinetis_memcore.secBootKinetisMem):

    def __init__(self, parent):
        Kinetis_memcore.secBootKinetisMem.__init__(self, parent)
        self.Kinetis_isAllInOneActionTaskPending = False
        if self.mcuSeries in uidef.kMcuSeries_Kinetis_f:
            self._Kinetis_initMain()

    def _Kinetis_initMain( self ):
        self.connectStage = uidef.kConnectStage_Rom
        self.updateConnectStatus('black')
        self.isBootableAppAllowedToView = False
        self.lastTime = None
        self.isAccessMemTaskPending = False
        self.accessMemType = ''
        self.isThereBoardConnection = False

    def _Kinetis_startGaugeTimer( self ):
        if not self.Kinetis_isAllInOneActionTaskPending:
            self.lastTime = time.time()
            self.initGauge()

    def _Kinetis_stopGaugeTimer( self ):
        if not self.Kinetis_isAllInOneActionTaskPending:
            self.deinitGauge()
            self.updateCostTime()

    def Kinetis_callbackSetMcuSeries( self ):
        self.Kinetis_initUi()
        self.Kinetis_initGen()
        self.Kinetis_initRun()
        self.Kinetis_initMem()
        self._Kinetis_initMain()
        self.Kinetis_setTargetSetupValue()

    def Kinetis_callbackSetMcuDevice( self ):
        self.Kinetis_setTargetSetupValue()
        needToPlaySound = False
        self.Kinetis_setSecureBootSeqColor(needToPlaySound)

    def Kinetis_callbackSetBootDevice( self ):
        self.Kinetis_setTargetSetupValue()
        needToPlaySound = False
        self.Kinetis_setSecureBootSeqColor(needToPlaySound)

    def _Kinetis_retryToPingBootloader( self ):
        pingStatus = False
        pingCnt = kRetryPingTimes
        while (not pingStatus) and pingCnt > 0:
            pingStatus = self.Kinetis_pingRom()
            if pingStatus:
                break
            pingCnt = pingCnt - 1
            if self.isUsbhidPortSelected:
                time.sleep(2)
        return pingStatus

    def _Kinetis_connectFailureHandler( self ):
        self.connectStage = uidef.kConnectStage_Rom
        self.updateConnectStatus('red')
        usbIdList = self.Kinetis_getUsbid()
        self.setPortSetupValue(self.connectStage, usbIdList, False, False)
        self.isBootableAppAllowedToView = False

    def _Kinetis_connectStateMachine( self, showError=True ):
        connectSteps = Kinetis_uidef.kConnectStep_Normal
        #self.getOneStepConnectMode()
        retryToDetectUsb = True
        while connectSteps:
            if not self.updatePortSetupValue(retryToDetectUsb, showError):
                if self.connectStage == uidef.kConnectStage_Rom:
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])
                self._Kinetis_connectFailureHandler()
                return
            if self.connectStage == uidef.kConnectStage_Rom:
                self.Kinetis_connectToDevice(self.connectStage)
                if self._Kinetis_retryToPingBootloader():
                    self.Kinetis_getMcuDeviceInfoViaRom()
                    self.Kinetis_getBootDeviceInfoViaRom()
                    self.updateConnectStatus('blue')
                    self.connectStage = uidef.kConnectStage_Reset
                else:
                    self.updateConnectStatus('red')
                    if showError:
                        self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])
                    return
            elif self.connectStage == uidef.kConnectStage_Reset:
                self.Kinetis_resetMcuDevice()
                self.isBootableAppAllowedToView = False
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
                usbIdList = self.Kinetis_getUsbid()
                self.setPortSetupValue(self.connectStage, usbIdList, True, True)
                self.Kinetis_connectToDevice(self.connectStage)
            else:
                pass
            connectSteps -= 1

    def Kinetis_callbackConnectToDevice( self ):
        self._Kinetis_startGaugeTimer()
        self.printLog("'Connect to xxx' button is clicked")
        if not self.isSbFileEnabledToGen:
            self._Kinetis_connectStateMachine(True)
        else:
            if not self.isThereBoardConnection:
                if self.connectStage == uidef.kConnectStage_Rom:
                    self.initSbAppBdfilesContent()
                else:
                    # It means there is board connection
                    self.isThereBoardConnection = True
                self._Kinetis_connectStateMachine(False)
                if not self.isThereBoardConnection:
                    if self.connectStage == uidef.kConnectStage_Rom:
                        # It means there is no board connection, but we need to set it as True for SB generation
                        self.isThereBoardConnection = True
                        self.Kinetis_isDeviceEnabledToOperate = False
                        self.connectStage = uidef.kConnectStage_Reset
                        self.updateConnectStatus('blue')
                else:
                    self.isThereBoardConnection = False
            else:
                self.isThereBoardConnection = False
                self.Kinetis_isDeviceEnabledToOperate = True
                self.connectStage = uidef.kConnectStage_Rom
                self.updateConnectStatus('black')
        self._Kinetis_stopGaugeTimer()

    def Kinetis_callbackSetSecureBootType( self ):
        self.setCostTime(0)
        self.Kinetis_setSecureBootSeqColor()

    def Kinetis_task_doAllInOneAction( self ):
        while True:
            if self.Kinetis_isAllInOneActionTaskPending:
                self._Kinetis_doAllInOneAction()
                self.Kinetis_isAllInOneActionTaskPending = False
                self._Kinetis_stopGaugeTimer()
            time.sleep(1)

    def _Kinetis_doAllInOneAction( self ):
        allInOneSeqCnt = 1
        status = False
        while allInOneSeqCnt:
            status = self._Kinetis_doGenImage()
            if not status:
                break
            status = self._Kinetis_doFlashImage()
            if not status:
                break
            allInOneSeqCnt -= 1
        if status and self.isAutomaticImageReadback:
            self.showPageInMainBootSeqWin(uidef.kPageIndex_BootDeviceMemory)
            self._Kinetis_doViewMem()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_AllInOne, status)

    def Kinetis_callbackAllInOneAction( self ):
        self._Kinetis_startGaugeTimer()
        self.Kinetis_isAllInOneActionTaskPending = True

    def _Kinetis_doGenImage( self ):
        status = False
        self._Kinetis_startGaugeTimer()
        self.printLog("'Generate Bootable Image' button is clicked")
        if self.Kinetis_createFinalBtAppfile():
            if self.Kinetis_genBootableImage():
                status = True
        self._Kinetis_stopGaugeTimer()
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_GenImage, status)
        return status

    def Kinetis_callbackGenImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._Kinetis_doGenImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _Kinetis_doFlashImage( self ):
        status = False
        if self.connectStage == uidef.kConnectStage_Reset:
            self._Kinetis_startGaugeTimer()
            self.printLog("'Load Bootable Image' button is clicked")
            if not self.Kinetis_flashBootableImage():
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_failToFlashImage'][self.languageIndex])
            else:
                self.isBootableAppAllowedToView = True
                status = True
            self._Kinetis_stopGaugeTimer()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])
        self.invalidateStepButtonColor(uidef.kSecureBootSeqStep_FlashImage, status)
        return status

    def Kinetis_callbackFlashImage( self ):
        if self.toolRunMode != uidef.kToolRunMode_Entry:
            self._Kinetis_doFlashImage()
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['separActnError_notAvailUnderEntry'][self.languageIndex])

    def _Kinetis_doViewMem( self ):
        if self.connectStage == uidef.kConnectStage_Reset:
            if self.isBootableAppAllowedToView:
                self._Kinetis_startGaugeTimer()
                self.Kinetis_readProgrammedMemoryAndShow()
                self._Kinetis_stopGaugeTimer()
            else:
                self.popupMsgBox(uilang.kMsgLanguageContentDict['operImgError_hasnotFlashImage'][self.languageIndex])
        else:
            self.popupMsgBox(uilang.kMsgLanguageContentDict['connectError_doubleCheckFopt'][self.languageIndex])

    def Kinetis_callbackViewMem( self ):
        self._Kinetis_doViewMem()

    def Kinetis_switchToolRunMode( self ):
        pass

