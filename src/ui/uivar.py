#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import uidef
import RTyyyy_uidef
import RTxxx_uidef

g_exeTopRoot = None
g_soundEffectType = None
g_languageIndex = None
g_hasSubWinBeenOpened = False
g_efuseDict = {'0x400_lock':0x00000000,
               '0x450_bootCfg0':0x00000000,
               '0x460_bootCfg1':0x00000000,
               '0x470_bootCfg2':0x00000000,
               '0x6d0_miscConf0':0x00000000,
               '0x6e0_miscConf1':0x00000000
               }

g_cfgFilename = None
g_toolCommDict = {'toolRunMode':None,
                  'isDymaticUsbDetection':None,
                  'soundEffectType':None,
                  'isSbFileEnabledToGen':None,
                  'isAutomaticImageReadback':None,
                  'flashloaderResident':None,
                  'efuseGroupSel':None,
                  'isAutomaticEfuseLocker':None,
                  'flexspiBootInstance':None,
                  'isIvtEntryResetHandler':None,
                  'edgelockFwEn':None,
                  'isEnglishLanguage':None,
                  'secBootType':None,
                  'mcuSeries':None,
                  'mcuDevice':None,
                  'bootDevice':None,
                  'isUsbhidPortSelected':None,
                  'isOneStepChecked':None,
                  'certSerial':None,
                  'certKeyPass':None,
                  'appFilename':None,
                  'appFormat':None,
                  'appBinBaseAddr':None,
                  'keyStoreRegion':None,
                  'certOptForHwCrypto':None
                 }

g_flexspiNorOpt0 = None
g_flexspiNorOpt1 = None
g_flexspiNorDeviceModel = None
g_isFdcbKept = None
g_flexspiNorDualImageInfoList = [None] * 3

g_flexspiNandOpt0 = None
g_flexspiNandOpt1 = None
g_flexspiNandFcbOpt = None
g_flexspiNandImageInfoList = [None] * 8
g_flexspiNandDeviceModel = None

g_semcNorOpt = None
g_semcNorSetting = None
g_semcNorDeviceModel = None

g_semcNandOpt = None
g_semcNandFcbOpt = None
g_semcNandImageInfoList = [None] * 8

g_usdhcSdOpt = None

g_usdhcMmcOpt0 = None
g_usdhcMmcOpt1 = None

g_lpspiNorOpt0 = None
g_lpspiNorOpt1 = None

g_flexcommSpiNorOpt0 = None
g_flexcommSpiNorOpt1 = None

g_dcdCtrlDict = {'isDcdEnabled':None,
                 'dcdFileType':None}
g_dcdSettingsDict = {'dcdSource':None,
                     'userBinFile':None,
                     'userCfgFile':None,
                     'dcdPurpose':None,
                     'sdramBase':None,
                     'deviceModel':None,
                     'dcdDesc':None}

g_xmcdSettingsDict = {'isXmcdEnabled':None,
                      'xmcdSource':None,
                      'userBinFile':None,
                      'xmcdHeader':None,
                      'xmcdOption0':None,
                      'xmcdOption1':None,
                      'xmcdOption2':None}

g_certSettingsDict = {'cstVersion':None,
                      'useExistingCaKey':None,
                      'useEllipticCurveCrypto':None,
                      'pkiTreeKeyLen':None,
                      'pkiTreeKeyCn':None,
                      'pkiTreeDuration':None,
                      'SRKs':None,
                      'caFlagSet':None}

g_signSettingsDict = {'isPartSigned':None,
                      'signedStart0':None,
                      'signedSize0':None,
                      'signedStart1':None,
                      'signedSize1':None,
                      'signedStart2':None,
                      'signedSize2':None}

g_otpmkKeyCommDict = {'secureBootType':None,
                      'opt':None,
                      'regionStartList':[None] * 4,
                      'regionLengthList':[None] * 4}

g_userKeyCtrlDict = {'mcu_device':None,
                     # For BEE
                     'engine_sel':None,
                     'engine0_key_src':None,
                     'engine0_fac_cnt':None,
                     'engine1_key_src':None,
                     'engine1_fac_cnt':None,
                     # For OTFAD
                     'total_regions':None,
                     'kek_src':None,
                     }
g_userKeyCmdDict = {'base_addr':None,
                    'hw_eng':None,
                    # For BEE
                    'engine0_key':None,
                    'engine0_arg':None,
                    'engine0_lock':None,
                    'engine1_key':None,
                    'engine1_arg':None,
                    'engine1_lock':None,
                    'use_zero_key':None,
                    'is_boot_image':None,
                    # For OTFAD
                    'kek':None,
                    'otfad_arg':None,
                    'scramble':None,
                    'scramble_align':None,
                    'otfad_ctx_lock':None,
                    }

def initVar(cfgFilename):
    global g_hasSubWinBeenOpened

    global g_cfgFilename

    global g_toolCommDict

    global g_flexspiNorOpt0
    global g_flexspiNorOpt1
    global g_flexspiNorDeviceModel
    global g_isFdcbKept
    global g_flexspiNorDualImageInfoList

    global g_flexspiNandOpt0
    global g_flexspiNandOpt1
    global g_flexspiNandFcbOpt
    global g_flexspiNandImageInfoList
    global g_flexspiNandDeviceModel

    global g_semcNandOpt
    global g_semcNandFcbOpt
    global g_semcNandImageInfoList

    global g_lpspiNorOpt0
    global g_lpspiNorOpt1

    global g_flexcommSpiNorOpt0
    global g_flexcommSpiNorOpt1

    global g_semcNorOpt
    global g_semcNorSetting
    global g_semcNorDeviceModel

    global g_usdhcSdOpt

    global g_usdhcMmcOpt0
    global g_usdhcMmcOpt1

    global g_dcdCtrlDict
    global g_dcdSettingsDict

    global g_xmcdSettingsDict

    global g_certSettingsDict
    global g_signSettingsDict

    global g_otpmkKeyCommDict

    global g_userKeyCtrlDict
    global g_userKeyCmdDict

    g_hasSubWinBeenOpened = False
    g_cfgFilename = cfgFilename
    if os.path.isfile(cfgFilename):
        cfgDict = None
        with open(cfgFilename, 'r') as fileObj:
            cfgDict = json.load(fileObj)
            fileObj.close()

        g_toolCommDict = cfgDict["cfgToolCommon"][0]

        g_flexspiNorOpt0 = cfgDict["cfgFlexspiNor"][0]
        g_flexspiNorOpt1 = cfgDict["cfgFlexspiNor"][1]
        g_flexspiNorDeviceModel = cfgDict["cfgFlexspiNor"][2]
        g_isFdcbKept = cfgDict["cfgFlexspiNor"][3]
        g_flexspiNorDualImageInfoList = cfgDict["cfgFlexspiNor"][4]

        g_flexspiNandOpt0 = cfgDict["cfgFlexspiNand"][0]
        g_flexspiNandOpt1 = cfgDict["cfgFlexspiNand"][1]
        g_flexspiNandFcbOpt = cfgDict["cfgFlexspiNand"][2]
        g_flexspiNandImageInfoList = cfgDict["cfgFlexspiNand"][3]
        g_flexspiNandDeviceModel = cfgDict["cfgFlexspiNand"][4]

        g_semcNandOpt = cfgDict["cfgSemcNand"][0]
        g_semcNandFcbOpt = cfgDict["cfgSemcNand"][1]
        g_semcNandImageInfoList = cfgDict["cfgSemcNand"][2]

        g_lpspiNorOpt0 = cfgDict["cfgLpspiNor"][0]
        g_lpspiNorOpt1 = cfgDict["cfgLpspiNor"][1]

        g_flexcommSpiNorOpt0 = cfgDict["cfgFlexcommSpiNor"][0]
        g_flexcommSpiNorOpt1 = cfgDict["cfgFlexcommSpiNor"][1]

        g_semcNorOpt = cfgDict["cfgSemcNor"][0]
        g_semcNorSetting = cfgDict["cfgSemcNor"][1]
        g_semcNorDeviceModel = cfgDict["cfgSemcNor"][2]

        g_usdhcSdOpt = cfgDict["cfgUsdhcSd"][0]

        g_usdhcMmcOpt0 = cfgDict["cfgUsdhcMmc"][0]
        g_usdhcMmcOpt1 = cfgDict["cfgUsdhcMmc"][1]

        g_dcdCtrlDict = cfgDict["cfgDcd"][0]
        g_dcdSettingsDict = cfgDict["cfgDcd"][1]

        g_xmcdSettingsDict = cfgDict["cfgXmcd"][0]

        g_certSettingsDict = cfgDict["cfgCertificate"][0]
        g_signSettingsDict = cfgDict["cfgSignature"][0]

        g_otpmkKeyCommDict = cfgDict["cfgSnvsKey"][0]

        g_userKeyCtrlDict = cfgDict["cfgUserKey"][0]
        g_userKeyCmdDict = cfgDict["cfgUserKey"][1]
    else:
        g_toolCommDict = {'toolRunMode':uidef.kToolRunMode_Master,
                          'isDymaticUsbDetection':True,
                          'soundEffectType':'quiet',
                          'isSbFileEnabledToGen':False,
                          'isAutomaticImageReadback':False,
                          'flashloaderResident':None,
                          'efuseGroupSel':0,
                          'isAutomaticEfuseLocker':True,
                          'flexspiBootInstance':0,
                          'isIvtEntryResetHandler':False,
                          'edgelockFwEn':False,
                          'isEnglishLanguage':True,
                          'secBootType':0,
                          'mcuSeries':0,
                          'mcuDevice':0,
                          'bootDevice':0,
                          'isUsbhidPortSelected':True,
                          'isOneStepChecked':True,
                          'certSerial':'12345678',
                          'certKeyPass':'test',
                          'appFilename':None,
                          'appFormat':0,
                          'appBinBaseAddr':'Eg: 0x00003000',
                          'keyStoreRegion':1,
                          'certOptForHwCrypto':0
                         }

        g_flexspiNorOpt0 = 0xc0000007
        g_flexspiNorOpt1 = 0x00000000
        g_flexspiNorDeviceModel = uidef.kFlexspiNorDevice_None
        g_isFdcbKept = False
        g_flexspiNorDualImageInfoList[0] = 0xFFFFFFFF
        g_flexspiNorDualImageInfoList[1] = 0xFFFFFFFF
        g_flexspiNorDualImageInfoList[2] = 0x0

        g_flexspiNandOpt0 = 0xC0010023
        g_flexspiNandOpt1 = 0x0000002C
        g_flexspiNandFcbOpt = 0xc2000104
        g_flexspiNandImageInfoList = [None] * 8
        g_flexspiNandImageInfoList[0] = 0x00040004
        g_flexspiNandDeviceModel = uidef.kFlexspiNandDevice_None

        g_semcNandOpt = 0xD0010101
        g_semcNandFcbOpt = 0x00010101
        g_semcNandImageInfoList = [None] * 8
        g_semcNandImageInfoList[0] = 0x00020001

        g_lpspiNorOpt0 = 0xc1100500
        g_lpspiNorOpt1 = 0x00000000

        g_flexcommSpiNorOpt0 = 0xc0000000
        g_flexcommSpiNorOpt1 = 0x00000000

        g_semcNorOpt = 0xD0000600
        g_semcNorSetting = 0x00010601
        g_semcNorDeviceModel = uidef.kSemcNorDevice_None

        g_usdhcSdOpt = 0xD0000000

        g_usdhcMmcOpt0 = 0xC0000000
        g_usdhcMmcOpt1 = 0x00000000

        g_dcdCtrlDict['isDcdEnabled'] = False
        g_dcdCtrlDict['dcdFileType'] = None
        g_dcdSettingsDict['dcdSource'] = 'Disable DCD'
        g_dcdSettingsDict['userBinFile'] = 'N/A'
        g_dcdSettingsDict['userCfgFile'] = 'N/A'
        g_dcdSettingsDict['dcdPurpose'] = 'SDRAM'
        g_dcdSettingsDict['sdramBase'] = '0x80000000'
        g_dcdSettingsDict['deviceModel'] = 'No'
        g_dcdSettingsDict['dcdDesc'] = None

        g_xmcdSettingsDict['isXmcdEnabled'] = False
        g_xmcdSettingsDict['xmcdSource'] = 'Disable XMCD'
        g_xmcdSettingsDict['userBinFile'] = 'N/A'
        g_xmcdSettingsDict['xmcdHeader'] = 0xC0010008
        g_xmcdSettingsDict['xmcdOption0'] = 0xC0000700
        g_xmcdSettingsDict['xmcdOption1'] = 0x0
        g_xmcdSettingsDict['xmcdOption2'] = 0x0

        g_certSettingsDict['cstVersion'] = RTyyyy_uidef.kCstVersion_v3_0_1
        g_certSettingsDict['useExistingCaKey'] = 'n'
        g_certSettingsDict['useEllipticCurveCrypto'] = 'n'
        g_certSettingsDict['pkiTreeKeyLen'] = 2048
        g_certSettingsDict['pkiTreeDuration'] = 10
        g_certSettingsDict['SRKs'] = 4
        g_certSettingsDict['caFlagSet'] = 'y'

        g_signSettingsDict['isPartSigned'] = False
        g_signSettingsDict['signedStart0'] = 0x0
        g_signSettingsDict['signedSize0'] = 0x0
        g_signSettingsDict['signedStart1'] = 0x0
        g_signSettingsDict['signedSize1'] = 0x0
        g_signSettingsDict['signedStart2'] = 0x0
        g_signSettingsDict['signedSize2'] = 0x0

        g_otpmkKeyCommDict['opt'] = 0xe0100000
        g_otpmkKeyCommDict['regionStartList'] = [None] * 4
        g_otpmkKeyCommDict['regionLengthList'] = [None] * 4

        g_userKeyCtrlDict['engine_sel'] = RTyyyy_uidef.kUserEngineSel_Engine0
        g_userKeyCtrlDict['engine0_key_src'] = RTyyyy_uidef.kUserKeySource_SW_GP2
        g_userKeyCtrlDict['engine0_fac_cnt'] = 1
        g_userKeyCtrlDict['engine1_key_src'] = RTyyyy_uidef.kUserKeySource_SW_GP2
        g_userKeyCtrlDict['engine1_fac_cnt'] = 1
        g_userKeyCtrlDict['total_regions'] = 1
        g_userKeyCtrlDict['kek_src'] = RTyyyy_uidef.kUserKeySource_SW_GP2
        g_userKeyCmdDict['base_addr'] = '0x60000000'
        g_userKeyCmdDict['hw_eng'] = 'bee'
        g_userKeyCmdDict['engine0_key'] = '0123456789abcdeffedcba9876543210'
        g_userKeyCmdDict['engine0_arg'] = '1,[0x60001000,0x1000,0]'
        g_userKeyCmdDict['engine0_lock'] = '0'
        g_userKeyCmdDict['engine1_key'] = '0123456789abcdeffedcba9876543210'
        g_userKeyCmdDict['engine1_arg'] = '1,[0x60002000,0x1000,0]'
        g_userKeyCmdDict['engine1_lock'] = '0'
        g_userKeyCmdDict['use_zero_key'] = '1'
        g_userKeyCmdDict['is_boot_image'] = '1'
        g_userKeyCmdDict['kek'] = '0123456789abcdeffedcba9876543210'
        g_userKeyCmdDict['otfad_arg'] = '[0123456789abcdeffedcba9876543210,0020406001030507,0x60001000,0x1000]'
        g_userKeyCmdDict['scramble'] = '0x33aa55cc'
        g_userKeyCmdDict['scramble_align'] = '0x1b'
        g_userKeyCmdDict['otfad_ctx_lock'] = '0,0,0,0'

def deinitVar(cfgFilename=None):
    global g_cfgFilename
    if cfgFilename == None and g_cfgFilename != None:
        cfgFilename = g_cfgFilename
    with open(cfgFilename, 'w') as fileObj:
        global g_toolCommDict
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        global g_flexspiNorDeviceModel
        global g_isFdcbKept
        global g_flexspiNorDualImageInfoList
        global g_flexspiNandOpt0
        global g_flexspiNandOpt1
        global g_flexspiNandFcbOpt
        global g_flexspiNandImageInfoList
        global g_flexspiNandDeviceModel
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfoList
        global g_lpspiNorOpt0
        global g_lpspiNorOpt1
        global g_flexcommSpiNorOpt0
        global g_flexcommSpiNorOpt1
        global g_usdhcSdOpt
        global g_usdhcMmcOpt0
        global g_usdhcMmcOpt1
        global g_dcdCtrlDict
        global g_dcdSettingsDict
        global g_xmcdSettingsDict
        global g_certSettingsDict
        global g_signSettingsDict
        global g_otpmkKeyCommDict
        global g_userKeyCtrlDict
        global g_userKeyCmdDict
        cfgDict = {
            "cfgToolCommon": [g_toolCommDict],
            "cfgFlexspiNor": [g_flexspiNorOpt0, g_flexspiNorOpt1, g_flexspiNorDeviceModel, g_isFdcbKept, g_flexspiNorDualImageInfoList],
            "cfgFlexspiNand": [g_flexspiNandOpt0, g_flexspiNandOpt1, g_flexspiNandFcbOpt, g_flexspiNandImageInfoList, g_flexspiNandDeviceModel],
            "cfgSemcNor": [g_semcNorOpt, g_semcNorSetting, g_semcNorDeviceModel],
            "cfgSemcNand": [g_semcNandOpt, g_semcNandFcbOpt, g_semcNandImageInfoList],
            "cfgLpspiNor": [g_lpspiNorOpt0, g_lpspiNorOpt1],
            "cfgFlexcommSpiNor": [g_flexcommSpiNorOpt0, g_flexcommSpiNorOpt1],
            "cfgUsdhcSd": [g_usdhcSdOpt],
            "cfgUsdhcMmc": [g_usdhcMmcOpt0, g_usdhcMmcOpt1],
            "cfgDcd": [g_dcdCtrlDict, g_dcdSettingsDict],
            "cfgXmcd": [g_xmcdSettingsDict],
            "cfgCertificate": [g_certSettingsDict],
            "cfgSignature": [g_signSettingsDict],
            "cfgSnvsKey": [g_otpmkKeyCommDict],
            "cfgUserKey": [g_userKeyCtrlDict, g_userKeyCmdDict]
        }
        json.dump(cfgDict, fileObj, indent=1)
        fileObj.close()

def getBootDeviceConfiguration( group ):
    if group == uidef.kBootDevice_XspiNor or \
       group == RTyyyy_uidef.kBootDevice_FlexspiNor or \
       group == RTxxx_uidef.kBootDevice_FlexspiNor or \
       group == RTxxx_uidef.kBootDevice_QuadspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        global g_flexspiNorDeviceModel
        global g_isFdcbKept
        return g_flexspiNorOpt0, g_flexspiNorOpt1, g_flexspiNorDeviceModel, g_isFdcbKept, g_flexspiNorDualImageInfoList
    elif group == RTyyyy_uidef.kBootDevice_FlexspiNand:
        global g_flexspiNandOpt0
        global g_flexspiNandOpt1
        global g_flexspiNandFcbOpt
        global g_flexspiNandImageInfoList
        global g_flexspiNandDeviceModel
        return g_flexspiNandOpt0, g_flexspiNandOpt1, g_flexspiNandFcbOpt, g_flexspiNandImageInfoList, g_flexspiNandDeviceModel
    elif group == RTyyyy_uidef.kBootDevice_SemcNor:
        global g_semcNorOpt
        global g_semcNorSetting
        global g_semcNorDeviceModel
        return g_semcNorOpt, g_semcNorSetting, g_semcNorDeviceModel
    elif group == RTyyyy_uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfoList
        return g_semcNandOpt, g_semcNandFcbOpt, g_semcNandImageInfoList
    elif group == RTyyyy_uidef.kBootDevice_UsdhcSd or \
         group == RTxxx_uidef.kBootDevice_UsdhcSd:
        global g_usdhcSdOpt
        return g_usdhcSdOpt
    elif group == RTyyyy_uidef.kBootDevice_UsdhcMmc or \
         group == RTxxx_uidef.kBootDevice_UsdhcMmc:
        global g_usdhcMmcOpt0
        global g_usdhcMmcOpt1
        return g_usdhcMmcOpt0, g_usdhcMmcOpt1
    elif group == RTyyyy_uidef.kBootDevice_LpspiNor:
        global g_lpspiNorOpt0
        global g_lpspiNorOpt1
        return g_lpspiNorOpt0, g_lpspiNorOpt1
    elif group == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
        global g_flexcommSpiNorOpt0
        global g_flexcommSpiNorOpt1
        return g_flexcommSpiNorOpt0, g_flexcommSpiNorOpt1
    elif group == RTyyyy_uidef.kBootDevice_Dcd:
        global g_dcdCtrlDict
        global g_dcdSettingsDict
        return g_dcdCtrlDict, g_dcdSettingsDict
    elif group == RTyyyy_uidef.kBootDevice_Xmcd:
        global g_xmcdSettingsDict
        return g_xmcdSettingsDict
    else:
        pass

def setBootDeviceConfiguration( group, *args ):
    if group == uidef.kBootDevice_XspiNor or \
       group == RTyyyy_uidef.kBootDevice_FlexspiNor or \
       group == RTxxx_uidef.kBootDevice_FlexspiNor or \
       group == RTxxx_uidef.kBootDevice_QuadspiNor:
        global g_flexspiNorOpt0
        global g_flexspiNorOpt1
        global g_flexspiNorDeviceModel
        global g_isFdcbKept
        global g_flexspiNorDualImageInfoList
        g_flexspiNorOpt0 = args[0]
        g_flexspiNorOpt1 = args[1]
        g_flexspiNorDeviceModel = args[2]
        g_isFdcbKept = args[3]
        g_flexspiNorDualImageInfoList = args[4]
    elif group == RTyyyy_uidef.kBootDevice_FlexspiNand:
        global g_flexspiNandOpt0
        global g_flexspiNandOpt1
        global g_flexspiNandFcbOpt
        global g_flexspiNandImageInfoList
        global g_flexspiNandDeviceModel
        g_flexspiNandOpt0 = args[0]
        g_flexspiNandOpt1 = args[1]
        g_flexspiNandFcbOpt = args[2]
        g_flexspiNandImageInfoList = args[3]
        g_flexspiNandDeviceModel = args[4]
    elif group == RTyyyy_uidef.kBootDevice_SemcNor:
        global g_semcNorOpt
        global g_semcNorSetting
        global g_semcNorDeviceModel
        g_semcNorOpt = args[0]
        g_semcNorSetting = args[1]
        g_semcNorDeviceModel = args[2]
    elif group == RTyyyy_uidef.kBootDevice_SemcNand:
        global g_semcNandOpt
        global g_semcNandFcbOpt
        global g_semcNandImageInfoList
        g_semcNandOpt = args[0]
        g_semcNandFcbOpt = args[1]
        g_semcNandImageInfoList = args[2]
    elif group == RTyyyy_uidef.kBootDevice_UsdhcSd or \
         group == RTxxx_uidef.kBootDevice_UsdhcSd:
        global g_usdhcSdOpt
        g_usdhcSdOpt = args[0]
    elif group == RTyyyy_uidef.kBootDevice_UsdhcMmc or \
         group == RTxxx_uidef.kBootDevice_UsdhcMmc:
        global g_usdhcMmcOpt0
        global g_usdhcMmcOpt1
        g_usdhcMmcOpt0 = args[0]
        g_usdhcMmcOpt1 = args[1]
    elif group == RTyyyy_uidef.kBootDevice_LpspiNor:
        global g_lpspiNorOpt0
        global g_lpspiNorOpt1
        g_lpspiNorOpt0 = args[0]
        g_lpspiNorOpt1 = args[1]
    elif group == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
        global g_flexcommSpiNorOpt0
        global g_flexcommSpiNorOpt1
        g_flexcommSpiNorOpt0 = args[0]
        g_flexcommSpiNorOpt1 = args[1]
    elif group == RTyyyy_uidef.kBootDevice_Dcd:
        global g_dcdCtrlDict
        global g_dcdSettingsDict
        g_dcdCtrlDict = args[0]
        g_dcdSettingsDict = args[1]
    elif group == RTyyyy_uidef.kBootDevice_Xmcd:
        global g_xmcdSettingsDict
        g_xmcdSettingsDict = args[0]
    else:
        pass

def getAdvancedSettings( group ):
    if group == uidef.kAdvancedSettings_Tool:
        global g_toolCommDict
        return g_toolCommDict
    elif group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        return g_certSettingsDict
    elif group == uidef.kAdvancedSettings_Sign:
        global g_signSettingsDict
        return g_signSettingsDict
    elif group == uidef.kAdvancedSettings_OtpmkKey:
        global g_otpmkKeyCommDict
        return g_otpmkKeyCommDict
    elif group == uidef.kAdvancedSettings_UserKeys:
        global g_userKeyCtrlDict
        global g_userKeyCmdDict
        return g_userKeyCtrlDict, g_userKeyCmdDict
    else:
        pass

def setAdvancedSettings( group, *args ):
    if group == uidef.kAdvancedSettings_Tool:
        global g_toolCommDict
        g_toolCommDict = args[0]
    elif group == uidef.kAdvancedSettings_Cert:
        global g_certSettingsDict
        g_certSettingsDict = args[0]
    elif group == uidef.kAdvancedSettings_Sign:
        global g_signSettingsDict
        g_signSettingsDict = args[0]
    elif group == uidef.kAdvancedSettings_OtpmkKey:
        global g_otpmkKeyCommDict
        g_otpmkKeyCommDict = args[0]
    elif group == uidef.kAdvancedSettings_UserKeys:
        global g_userKeyCtrlDict
        global g_userKeyCmdDict
        g_userKeyCtrlDict = args[0]
        g_userKeyCmdDict = args[1]
    else:
        pass

def getRuntimeSettings( ):
    global g_hasSubWinBeenOpened
    global g_exeTopRoot
    global g_soundEffectType
    global g_languageIndex
    return g_hasSubWinBeenOpened, g_exeTopRoot, g_soundEffectType, g_languageIndex

def setRuntimeSettings( *args ):
    global g_hasSubWinBeenOpened
    if args[0] != None:
        g_hasSubWinBeenOpened = args[0]
    try:
        global g_exeTopRoot
        if args[1] != None:
            g_exeTopRoot = args[1]
    except:
        pass
    try:
        global g_soundEffectType
        if args[2] != None:
            g_soundEffectType = args[2]
    except:
        pass
    try:
        global g_languageIndex
        if args[3] != None:
            g_languageIndex = args[3]
    except:
        pass

def getEfuseSettings( ):
    global g_efuseDict
    return g_efuseDict

def setEfuseSettings( *args ):
    global g_efuseDict
    g_efuseDict = args[0]
