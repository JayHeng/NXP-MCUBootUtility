#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import json
import sys
import os
import time
import RTyyyy_fusedef
import collections

sys.path.append(os.path.abspath(".."))
from run import RTyyyy_runcore
from run import RTyyyy_rundef
from ui import RTyyyy_uidef
from ui import uicore
from ui import uidef
from ui import uivar
from ui import uilang
from gen import gendef
from operator import itemgetter

class secBootRTyyyyFuse(RTyyyy_runcore.secBootRTyyyyRun):

    def __init__(self, parent):
        RTyyyy_runcore.secBootRTyyyyRun.__init__(self, parent)
        self.needToScanFuse = None
        self.scannedFuseList = [None] * RTyyyy_fusedef.kTotalEfuseWords
        self.toBeBurnnedFuseList = [None] * RTyyyy_fusedef.kTotalEfuseWords
        self.runModeFuseFlagList = [None] * RTyyyy_fusedef.kTotalEfuseWords
        self.toBeRefreshedFuseList = [False] * RTyyyy_fusedef.kTotalEfuseWords
        self.isRunModeFuseFlagRemapped = False
        self.loadedFuseList = [None] * RTyyyy_fusedef.kTotalEfuseWords
        if self.mcuSeries in uidef.kMcuSeries_iMXRTyyyy:
            self.RTyyyy_initFuse()

    def RTyyyy_initFuse( self ):
        self.applyFuseOperToRunMode()
        self.RTyyyy_updateFuseGroupText()

    def _initEntryModeFuseFlag( self ):
        if self.toolRunMode == uidef.kToolRunMode_Entry:
            for i in range(RTyyyy_fusedef.kTotalEfuseWords):
                idx = i + self.tgt.efusemapIndexDict['kEfuseIndex_START']
                if (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion0IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion0IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion0IndexEnd'])) or \
                   (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion1IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion1IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion1IndexEnd'])) or \
                   (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion2IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion2IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion2IndexEnd'])) or \
                   (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion3IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion3IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion3IndexEnd'])) or \
                   (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion4IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion4IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion4IndexEnd'])) or \
                   (self.tgt.efusemapIndexDict['kEfuseEntryModeRegion5IndexStart'] != None and (idx >= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion5IndexStart'] and idx <= self.tgt.efusemapIndexDict['kEfuseEntryModeRegion5IndexEnd'])):
                    self.runModeFuseFlagList[i] = True
                else:
                    self.runModeFuseFlagList[i] = False
        else:
            for i in range(RTyyyy_fusedef.kTotalEfuseWords):
                self.runModeFuseFlagList[i] = True

    def applyFuseOperToRunMode( self ):
        self._initEntryModeFuseFlag()
        self.RTyyyy_updateFuseRegionField()
        self.RTyyyy_updateFuseGroupText()
        self.isRunModeFuseFlagRemapped = False
        self.needToScanFuse = True

    def _remapRunModeFuseFlagList( self ):
        if self.isRunModeFuseFlagRemapped:
            return
        if self.tgt.hasRemappedFuse:
            for i in range(RTyyyy_fusedef.kEfuseRemapLen):
                self.runModeFuseFlagList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i], self.runModeFuseFlagList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i] = \
                self.runModeFuseFlagList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i], self.runModeFuseFlagList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i]
            self.isRunModeFuseFlagRemapped = True
        else:
            pass

    def _swapRemappedScannedFuseIfAppliable( self ):
        if self.tgt.hasRemappedFuse:
            for i in range(RTyyyy_fusedef.kEfuseRemapLen):
                self.scannedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i], self.scannedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i] = \
                self.scannedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i], self.scannedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i]
        else:
            pass

    def RTyyyy_scanAllFuseRegions( self, needSwapAndShow=True, isRefreshOpt=False ):
        self.needToScanFuse = False
        hasRefreshFuse = False
        curFuseGroupStartIndex = self.efuseGroupSel * RTyyyy_fusedef.kGroupEfuseWords
        nxtFuseGroupStartIndex = (self.efuseGroupSel + 1) * RTyyyy_fusedef.kGroupEfuseWords
        self._remapRunModeFuseFlagList()
        for i in range(RTyyyy_fusedef.kGroupEfuseWords):
            idx = curFuseGroupStartIndex + i
            if self.runModeFuseFlagList[idx]:
                if not isRefreshOpt:
                    self.scannedFuseList[idx] = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_START'] + idx, '', False)
                elif self.toBeRefreshedFuseList[idx]:
                    self.scannedFuseList[idx] = self.RTyyyy_readMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_START'] + idx, '', False)
                    self.toBeRefreshedFuseList[idx] = False
                    hasRefreshFuse = True
            else:
                self.scannedFuseList[idx] = None
        if isRefreshOpt and (not hasRefreshFuse):
            return
        if needSwapAndShow:
            self._swapRemappedScannedFuseIfAppliable()
            self.RTyyyy_showScannedFuses(self.scannedFuseList[curFuseGroupStartIndex:nxtFuseGroupStartIndex])

    def _swapRemappedToBeBurnFuseIfAppliable( self ):
        if self.tgt.hasRemappedFuse:
            for i in range(RTyyyy_fusedef.kEfuseRemapLen):
                self.toBeBurnnedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i], self.toBeBurnnedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i] = \
                self.toBeBurnnedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Dest + i], self.toBeBurnnedFuseList[RTyyyy_fusedef.kEfuseRemapIndex_Src + i]
        else:
            pass

    def _burnFuseLockRegion( self, srcFuseValue, destFuseValue, fuseIdxKey='kEfuseIndex_LOCK' ):
        destFuseValue = (destFuseValue | srcFuseValue) ^ srcFuseValue
        if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
            # High-4bits cannot be burned along with low-28bits for fuse lock region, this is design limitation
            lowLock = destFuseValue & RTyyyy_fusedef.kEfuseMask_LockLow
            if lowLock:
                # Don't allow to lock Fuse SRK because SRK will be OP+RP+WP if lock bit is set and then ROM cannot get SRK
                if (lowLock & RTyyyy_fusedef.kEfuseMask_LockSrk):
                    lowLock = lowLock & (~RTyyyy_fusedef.kEfuseMask_LockSrk)
                    self.popupMsgBox(uilang.kMsgLanguageContentDict['burnFuseError_cannotBurnSrkLock'][self.languageIndex])
                self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIdxKey], lowLock, RTyyyy_rundef.kActionFrom_BurnFuse)
            highLock = destFuseValue & RTyyyy_fusedef.kEfuseMask_LockHigh
            if highLock:
                self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIdxKey], highLock, RTyyyy_rundef.kActionFrom_BurnFuse)
            # Some RT doesn't have this design limitation, so we should try again to make sure lock has been really burnned
            destLock = destFuseValue
            if destLock:
                self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIdxKey], destLock, RTyyyy_rundef.kActionFrom_BurnFuse)
        elif self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
            self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict[fuseIdxKey], destFuseValue, RTyyyy_rundef.kActionFrom_BurnFuse)
        else:
            pass

    def RTyyyy_burnAllFuseRegions( self ):
        curFuseGroupStartIndex = self.efuseGroupSel * RTyyyy_fusedef.kGroupEfuseWords
        nxtFuseGroupStartIndex = (self.efuseGroupSel + 1) * RTyyyy_fusedef.kGroupEfuseWords
        self.toBeBurnnedFuseList[curFuseGroupStartIndex:nxtFuseGroupStartIndex] = self.getUserFuses()
        self._swapRemappedToBeBurnFuseIfAppliable()
        self._remapRunModeFuseFlagList()
        if self.needToScanFuse:
            self.RTyyyy_scanAllFuseRegions(False)
        else:
            self._swapRemappedScannedFuseIfAppliable()
        lockOperDict = {'kEfuseIndex_LOCK':None,
                        'kEfuseIndex_LOCK2':None,
                       }
        for i in range(RTyyyy_fusedef.kGroupEfuseWords):
            idx = curFuseGroupStartIndex + i
            if self.runModeFuseFlagList[idx]:
                if self.toBeBurnnedFuseList[idx] != self.scannedFuseList[idx] and \
                   self.toBeBurnnedFuseList[idx] != None and \
                   self.scannedFuseList[idx] != None:
                    if idx == self.tgt.efusemapIndexDict['kEfuseIndex_LOCK']:
                        lockOperDict['kEfuseIndex_LOCK'] = [self.scannedFuseList[idx], self.toBeBurnnedFuseList[idx]]
                    elif (('kEfuseIndex_LOCK2' in self.tgt.efusemapIndexDict) and (idx == self.tgt.efusemapIndexDict['kEfuseIndex_LOCK2'])):
                        lockOperDict['kEfuseIndex_LOCK2'] = [self.scannedFuseList[idx], self.toBeBurnnedFuseList[idx]]
                    else:
                        # We need to do | operation first, in case user set 1 to 0 wrongly
                        # Then we do ^ operation, because only bit 1 in fuse word will take affect, bit 0 will be bypassed by OCOTP controller
                        fuseValue = (self.toBeBurnnedFuseList[idx] | self.scannedFuseList[idx]) ^ self.scannedFuseList[idx]
                        self.RTyyyy_burnMcuDeviceFuseByBlhost(self.tgt.efusemapIndexDict['kEfuseIndex_START'] + idx, fuseValue, RTyyyy_rundef.kActionFrom_BurnFuse)
                    self.toBeRefreshedFuseList[idx] = True
        if lockOperDict['kEfuseIndex_LOCK'] !=None:
            self._burnFuseLockRegion(lockOperDict['kEfuseIndex_LOCK'][0], lockOperDict['kEfuseIndex_LOCK'][1], 'kEfuseIndex_LOCK')
        if lockOperDict['kEfuseIndex_LOCK2'] !=None:
            self._burnFuseLockRegion(lockOperDict['kEfuseIndex_LOCK2'][0], lockOperDict['kEfuseIndex_LOCK2'][1], 'kEfuseIndex_LOCK2')
        self.RTyyyy_scanAllFuseRegions(True, True)

    def RTyyyy_task_doShowSettedEfuse( self ):
        while True:
            if self.mcuSeries == uidef.kMcuSeries_iMXRT10yy:
                efuseDict = uivar.getEfuseSettings()
                if efuseDict['0x400_lock'] != self.toBeBurnnedFuseList[0]:
                    self.toBeBurnnedFuseList[0] = efuseDict['0x400_lock']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_LOCK'], efuseDict['0x400_lock'])
                if efuseDict['0x450_bootCfg0'] != self.toBeBurnnedFuseList[5]:
                    self.toBeBurnnedFuseList[5] = efuseDict['0x450_bootCfg0']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG0'], efuseDict['0x450_bootCfg0'])
                if efuseDict['0x460_bootCfg1'] != self.toBeBurnnedFuseList[6]:
                    self.toBeBurnnedFuseList[6] = efuseDict['0x460_bootCfg1']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG1'], efuseDict['0x460_bootCfg1'])
                if efuseDict['0x470_bootCfg2'] != self.toBeBurnnedFuseList[7]:
                    self.toBeBurnnedFuseList[7] = efuseDict['0x470_bootCfg2']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_BOOT_CFG2'], efuseDict['0x470_bootCfg2'])
                if efuseDict['0x6d0_miscConf0'] != self.toBeBurnnedFuseList[45]:
                    self.toBeBurnnedFuseList[45] = efuseDict['0x6d0_miscConf0']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_MISC_CONF0'], efuseDict['0x6d0_miscConf0'])
                if efuseDict['0x6e0_miscConf1'] != self.toBeBurnnedFuseList[46]:
                    self.toBeBurnnedFuseList[46] = efuseDict['0x6e0_miscConf1']
                    self.showSettedEfuse(self.tgt.efusemapIndexDict['kEfuseIndex_MISC_CONF1'], efuseDict['0x6e0_miscConf1'])
            time.sleep(0.5)

    def saveFuseRegions( self ):
        if os.path.isfile(self.fuseSettingFilename):
            with open(self.fuseSettingFilename, 'r+') as fileObj:
                FuseMapJson = json.load(fileObj)
                FuseMapDict = FuseMapJson["FuseMAP"][0]
                fileObj.close()
            self.saveFuselist = [None] * RTyyyy_fusedef.kTotalEfuseWords
            self.saveFuselist = self.getUserFuses()
            with open(self.fuseSettingFilename, 'w') as fileObj:
                FuseMapDict = collections.OrderedDict(sorted(FuseMapDict.iteritems(), key=itemgetter(0), reverse=False))
                if self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                    if self.tgt.bootHeaderType == gendef.kBootHeaderType_IVT:
                        if self.efuseGroupSel == 0:
                            for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                                new_str = 'Fuse' + str(hex(2048 + i * 16))
                                new_str = new_str[0:6] + '0' + new_str[6:9]
                                if self.saveFuselist[i] == None:
                                    FuseMapDict[new_str] = "None"
                                else:
                                    FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                        elif self.efuseGroupSel == 1:
                            for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                                if i<48:
                                    new_str = 'Fuse' + str(hex(3328 + i * 16))
                                    new_str = new_str[0:6] + '0' + new_str[6:9]
                                else:
                                     new_str = 'Fuse' + str(hex(3328 + i * 16))
                                if self.saveFuselist[i] == None:
                                    FuseMapDict[new_str] = "None"
                                else:
                                    FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                        elif self.efuseGroupSel == 2:
                            for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                                new_str = 'Fuse' + str(hex(4608 + i * 16))
                                if self.saveFuselist[i] == None:
                                    FuseMapDict[new_str] = "None"
                                else:
                                    FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                        elif self.efuseGroupSel == 3:
                            for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                                new_str = 'Fuse' + str(hex(5888 + i * 16))
                                if self.saveFuselist[i] == None:
                                    FuseMapDict[new_str] = "None"
                                else:
                                    FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                        else:
                            pass
                    elif self.tgt.bootHeaderType == gendef.kBootHeaderType_Container:
                        for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                            new_str = 'Fuse-W' + str(self.efuseGroupSel * RTyyyy_fusedef.kGroupEfuseWords + i)
                            if self.saveFuselist[i] == None:
                                FuseMapDict[new_str] = "None"
                            else:
                                FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                else:
                    for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                        new_str = 'Fuse' + str(hex(1024 + i * 16))
                        new_str = new_str[0:6] + '0' + new_str[6:9]
                        if self.saveFuselist[i] == None:
                            FuseMapDict[new_str] = "None"
                        else:
                            FuseMapDict[new_str] = (str(hex(self.saveFuselist[i])))[2:10]
                cfgDict = {
                    "FuseMAP": [FuseMapDict]
                }
                json.dump(cfgDict, fileObj, indent=1)
                fileObj.close()

    def loadFuseRegions( self ):
        if os.path.isfile(self.fuseSettingFilename):
            with open(self.fuseSettingFilename, 'r') as fileObj:
                FuseMapJson = json.load(fileObj)
                FuseMapDict = FuseMapJson["FuseMAP"][0]
                fileObj.close()
                FuseMapDict = collections.OrderedDict(sorted(FuseMapDict.iteritems(), key=itemgetter(0), reverse=False))
            if self.mcuSeries == uidef.kMcuSeries_iMXRT11yy:
                if self.efuseGroupSel == 0:
                    for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                        new_str = 'Fuse' + str(hex(2048 + i * 16))
                        new_str = new_str[0:6] + '0' + new_str[6:9]
                        self.loadedFuseList[i] = FuseMapDict[new_str]
                elif self.efuseGroupSel == 1:
                    for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                        if i < 48:
                            new_str = 'Fuse' + str(hex(3328 + i * 16))
                            new_str = new_str[0:6] + '0' + new_str[6:9]
                        else:
                            new_str = 'Fuse' + str(hex(3328 + i * 16))
                        self.loadedFuseList[i] = FuseMapDict[new_str]
                elif self.efuseGroupSel == 2:
                    for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                        new_str = 'Fuse' + str(hex(4608 + i * 16))
                        self.loadedFuseList[i] = FuseMapDict[new_str]
                elif self.efuseGroupSel == 3:
                    for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                        new_str = 'Fuse' + str(hex(5888 + i * 16))
                        self.loadedFuseList[i] = FuseMapDict[new_str]
                else:
                    pass
            else:
                for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                    new_str = 'Fuse' + str(hex(1024 + i * 16))
                    new_str = new_str[0:6] + '0' + new_str[6:9]
                    self.loadedFuseList[i] = FuseMapDict[new_str]
            for i in range(RTyyyy_fusedef.kGroupEfuseWords):
                if self.loadedFuseList[i] == "None":
                    self.loadedFuseList[i] = None
                else:
                    self.loadedFuseList[i] = int(self.loadedFuseList[i], 16)
        self.RTyyyy_showScannedFuses(self.loadedFuseList)







