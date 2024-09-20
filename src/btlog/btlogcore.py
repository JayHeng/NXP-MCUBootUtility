#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import btlogdef
import boot
sys.path.append(os.path.abspath(".."))
from mem import memcore
from ui import uidef
from ui import uivar
from ui import uilang
from utils import misc

class secBootLog(memcore.secBootMem):

    def __init__(self, parent):
        memcore.secBootMem.__init__(self, parent)
        self.lastBootDataValue = None
        self.btlogFilename = os.path.join(self.exeTopRoot, 'gen', 'btlog_file', 'btlog.bin')
        self.userBtlogFile = None

    def _invalidLogDataFile( self ):
        if self.languageIndex == uilang.kLanguageIndex_English:
            self.popupMsgBox('Invalid boot log data file!')
        elif self.languageIndex == uilang.kLanguageIndex_Chinese:
            self.popupMsgBox(u"无效的启动日志文件！")
        else:
            pass

    def _failToGetLogDataFromRam( self ):
        if self.languageIndex == uilang.kLanguageIndex_English:
            self.popupMsgBox('Cannot read boot log data from RAM(Make sure it is Flashloader stage)!')
        elif self.languageIndex == uilang.kLanguageIndex_Chinese:
            self.popupMsgBox(u"无法从RAM里读取启动日志(请确保处于Flashloader阶段)！")
        else:
            pass

    def _decodeBootLogEntry( self, entryValue ):
        contextStr = ' 0x'+'{:0>8x}'.format(entryValue) + ':  '
        state = (entryValue >> 24) & 0xFF
        subState = (entryValue >> 16) & 0xFF
        status = (entryValue >> 8) & 0xFF
        entries = entryValue & 0xFF
        try:
            contextStr += btlogdef.btlogStateDict_RTmix['0x'+'{:0>2x}'.format(state)]
            contextStr += btlogdef.btlogSubStateDict_RTmix['0x'+'{:0>2x}'.format(subState)]
            contextStr += btlogdef.btlogStatusDict_RTmix['0x'+'{:0>2x}'.format(status)]
            return True, contextStr, entries, state, subState
        except:
            return False, contextStr, entries, state, subState

    def _decodeBootDataEntry( self, stateType, subStatueType, entryValue, entryIdx):
        contextStr = ', '
        if stateType == btlogdef.kBootLogStateType_HardwareInit:
            if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
                contextStr += 'TRNG->TOTSAM'
                return True, contextStr
        elif stateType == btlogdef.kBootLogStateType_MasterBoot:
            try:
                contextStr += 'boot type -> '
                contextStr += btlogdef.btDataStateDict_BootDevice0_RTmix['0x'+'{:0>2x}'.format(entryValue)]
                return True, contextStr
            except:
                return False, contextStr
        elif stateType == btlogdef.kBootLogStateType_BootDevice:
            if entryIdx == 0:
                if self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                    if subStatueType == btlogdef.kBootLogSubStateType_Init:
                        self.lastBootDataValue = entryValue
                        try:
                            contextStr += 'boot type -> '
                            contextStr += btlogdef.btDataStateDict_BootDevice0_RTmix['0x'+'{:0>2x}'.format(entryValue)]
                            return True, contextStr
                        except:
                            return False, contextStr
                    elif subStatueType == btlogdef.kBootLogSubStateType_Call:
                        contextStr += 'image index -> ' + str(entryValue)
                        return True, contextStr
                elif self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
                    try:
                        contextStr += 'boot periph -> '
                        contextStr += btlogdef.btDataStateDict_BootDevice1_8_RTmix['0x'+'{:0>4x}'.format(entryValue)]
                        return True, contextStr
                    except:
                        return False, contextStr
            elif entryIdx == 1:
                try:
                    contextStr += 'boot periph -> '
                    if self.lastBootDataValue == 0x1:
                        contextStr += btlogdef.btDataStateDict_BootDevice1_1_RTmix['0x'+'{:0>2x}'.format(entryValue)]
                    elif self.lastBootDataValue == 0x2:
                        contextStr += btlogdef.btDataStateDict_BootDevice1_2_RTmix['0x'+'{:0>2x}'.format(entryValue)]
                    elif self.lastBootDataValue == 0x4:
                        contextStr += btlogdef.btDataStateDict_BootDevice1_4_RTmix['0x'+'{:0>2x}'.format(entryValue)]
                    elif self.lastBootDataValue == 0x8:
                        contextStr += btlogdef.btDataStateDict_BootDevice1_8_RTmix['0x'+'{:0>4x}'.format(entryValue)]
                    return True, contextStr
                except:
                    return False, contextStr
            elif entryIdx == 2:
                contextStr += 'periph instance -> ' + str(entryValue)
                return True, contextStr
        elif stateType == btlogdef.kBootLogStateType_AuthImage:
            contextStr += 'cost time {0}us'.format(entryValue)
            return True, contextStr
        elif stateType == btlogdef.kBootLogStateType_JumpToImage:
            if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx:
                contextStr += 'image vector table address / tzm preset result / image type return'
            elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                contextStr += 'image entry address'
            return True, contextStr
        else:
            return False, None

    def _getBootLogFromRam( self ):
        status, results, cmdStr = self.blhost.readMemory(self.tgt.bootLogStart, self.tgt.bootLogLength, self.btlogFilename)
        self.printLog(cmdStr)
        return status == boot.status.kStatus_Success

    def viewRtBootLog( self ):
        logBinFile = None
        self.userBtlogFile = self.getBootLogBinFile()
        if os.path.isfile(self.userBtlogFile):
            logBinFile = self.userBtlogFile
        else:
            if self._getBootLogFromRam():
                logBinFile = self.btlogFilename
            else:
                self._failToGetLogDataFromRam()
                return
        logFilelen = os.path.getsize(logBinFile)
        #####################################################
        if self.mcuSeries == uidef.kMcuSeries_iMXRTxxx or \
           self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            logEntries = 0
            if logFilelen >= 4:
                logEntries = self.getVal32FromBinFile(logBinFile, 0)
            else:
                self._invalidLogDataFile()
                return
            if logFilelen < logEntries * 4 + 4:
                self._invalidLogDataFile()
                return
            self.printBootLog(btlogdef.btlogIntro2)
            self.printBootLog(btlogdef.btlogIntro0)
            self.printBootLog(btlogdef.btlogIntro2)
            dataEntries = 0
            maxDataEntries = 0
            lastEntryState = 0
            lastEntrySubState = 0
            for entryIdx in range(logEntries - 1):
                entryValue = self.getVal32FromBinFile(logBinFile, 4 + entryIdx * 4)
                if dataEntries == 0:
                    ret, context, dataEntries, lastEntryState, lastEntrySubState = self._decodeBootLogEntry(entryValue)
                    if ret:
                        maxDataEntries = dataEntries
                        self.printBootLog(context)
                    else:
                        if entryIdx == 0:
                            self._invalidLogDataFile()
                        return
                else:
                    self.printBootLog('    data[{0}] = '.format(maxDataEntries-dataEntries) + '0x'+'{:0>8x}'.format(entryValue), False)
                    ret, context = self._decodeBootDataEntry(lastEntryState, lastEntrySubState, entryValue, maxDataEntries-dataEntries)
                    if ret:
                        self.printBootLog(context)
                    else:
                        self.printBootLog('')
                    dataEntries -= 1
        #####################################################
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            logEntries = logFilelen / 4
            if logFilelen % 4:
                self._invalidLogDataFile()
                return
            self.printBootLog(btlogdef.btlogIntro2)
            self.printBootLog(btlogdef.btlogIntro1)
            self.printBootLog(btlogdef.btlogIntro2)
            for entryIdx in range(logEntries):
                entryValue = self.getVal32FromBinFile(logBinFile, entryIdx * 4)
                context = ' 0x'+'{:0>8x}'.format(entryValue) + ':  '
                try:
                    context += btlogdef.btlogDict_RT10yy['0x'+'{:0>8x}'.format(entryValue)]
                    self.printBootLog(context)
                except:
                    if entryIdx == 0:
                        self._invalidLogDataFile()
                    return
        else:
            pass

