#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import RTxxx_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from _main import RTyyyy_main

class secBootRTxxxUi(RTyyyy_main.secBootRTyyyyMain):

    def __init__(self, parent):
        RTyyyy_main.secBootRTyyyyMain.__init__(self, parent)
        if self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            self.RTxxx_initUi()

    def RTxxx_initUi( self ):
        self.isXipableDevice = False
        self.isNandDevice = False
        self.isSdmmcCard = False
        self._RTxxx_initTargetSetupValue()
        self.RTxxx_setTargetSetupValue()

        self.secureBootType = None
        self._RTxxx_initSecureBootSeqValue()
        self._RTxxx_initSecureBootSeqColor()
        self.setDcdButtonEnablement(False)
        self.setBdcButtonEnablement(True)
        self.setXmcdButtonEnablement(False)

    def _RTxxx_initTargetSetupValue( self ):
        self.m_choice_bootDevice.Clear()
        self.m_choice_bootDevice.SetItems(RTxxx_uidef.kBootDevice_Latest)
        totalSel = self.m_choice_bootDevice.GetCount()
        if self.toolCommDict['bootDevice'] < totalSel:
            self.m_choice_bootDevice.SetSelection(self.toolCommDict['bootDevice'])
        else:
            self.m_choice_bootDevice.SetSelection(0)

    def RTxxx_setTargetSetupValue( self ):
        self.showPageInMainBootSeqWin(uidef.kPageIndex_ImageGenerationSequence)
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.RTxxx_createMcuTarget()
        self.refreshBootDeviceList()
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.toolCommDict['bootDevice'] = self.m_choice_bootDevice.GetSelection()
        if self.bootDevice == RTxxx_uidef.kBootDevice_FlexspiNor:
            self.isXipableDevice = True
            self.isNandDevice = False
            self.isSdmmcCard = False
            self.sbEnableBootDeviceMagic = '@0x9'
            self.sbAccessBootDeviceMagic = ''
            self.setFlexspiNorDeviceForEvkBoard()
        elif self.bootDevice == RTxxx_uidef.kBootDevice_XspiNor:
            self.isXipableDevice = True
            self.isNandDevice = False
            self.isSdmmcCard = False
            self.sbEnableBootDeviceMagic = '@0xb'
            self.sbAccessBootDeviceMagic = ''
            self.setFlexspiNorDeviceForEvkBoard()
        elif self.bootDevice == RTxxx_uidef.kBootDevice_FlexcommSpiNor:
            self.isXipableDevice = False
            self.isNandDevice = False
            self.isSdmmcCard = False
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcSd:
            self.isXipableDevice = False
            self.isNandDevice = True
            self.isSdmmcCard = True
        elif self.bootDevice == RTxxx_uidef.kBootDevice_UsdhcMmc:
            self.isXipableDevice = False
            self.isNandDevice = True
            self.isSdmmcCard = True
        else:
            pass

    def _RTxxx_initSecureBootSeqValue( self ):
        if not self.initSecureBootTypeList():
            self.m_choice_secureBootType.Clear()
            self.m_choice_secureBootType.SetItems(RTxxx_uidef.kSecureBootType_Latest)
        totalSel = self.m_choice_secureBootType.GetCount()
        if self.toolCommDict['secBootType'] < totalSel:
            self.m_choice_secureBootType.SetSelection(self.toolCommDict['secBootType'])
        else:
            self.m_choice_secureBootType.SetSelection(0)
        if self.toolCommDict['appFilename'] != None:
            self.m_filePicker_appPath.SetPath(self.toolCommDict['appFilename'])
        self.m_choice_appFormat.SetSelection(self.toolCommDict['appFormat'])
        self._setUserBinaryBaseField()
        self.m_textCtrl_appBaseAddr.Clear()
        self.m_textCtrl_appBaseAddr.write(self.toolCommDict['appBinBaseAddr'])

    def _RTxxx_initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.RTxxx_setSecureBootSeqColor()

    def RTxxx_setSecureBootButtonColor( self, needToPlaySound=True ):
        activeColor = None
        optionalColor = None
        setEnable = None
        if self.toolRunMode == uidef.kToolRunMode_Entry:
            activeColor = uidef.kBootSeqColor_Invalid
            optionalColor = uidef.kBootSeqColor_Invalid
            setEnable = False
        else:
            activeColor = uidef.kBootSeqColor_Active
            optionalColor = uidef.kBootSeqColor_Optional
            setEnable = True
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        if self.secureBootType == RTxxx_uidef.kSecureBootType_PlainUnsigned or \
           self.secureBootType == RTxxx_uidef.kSecureBootType_PlainCrc:
            self.m_button_genImage.Enable( setEnable )
            self.m_button_genImage.SetBackgroundColour( activeColor )
            self.m_button_flashImage.Enable( setEnable )
            self.m_button_flashImage.SetBackgroundColour( activeColor )
        else:
            pass
        self.m_button_allInOneAction.Enable( True )
        self.m_button_allInOneAction.SetBackgroundColour( uidef.kBootSeqColor_Active )
        self.Refresh()
        if needToPlaySound:
            self.soundEffectFilenameForTask = uidef.kSoundEffectFilename_Restart

    def _RTxxx_getImgName( self ):
        memType = ''
        if self.isNandDevice:
            if self.isSdmmcCard:
                memType = 'sdmmc_'
        else:
            memType = 'nor_'
        return memType

    def RTxxx_setSecureBootSeqColor( self , needToPlaySound=True ):
        self.hasDynamicLableBeenInit = True
        self.showPageInMainBootSeqWin(uidef.kPageIndex_ImageGenerationSequence)
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.refreshSecureBootTypeList()
        self.toolCommDict['secBootType'] = self.m_choice_secureBootType.GetSelection()
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.resetSecureBootSeqColor()
        if self.secureBootType == RTxxx_uidef.kSecureBootType_PlainUnsigned:
            self.m_panel_genImage1_browseApp.Enable( True )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel(uilang.kMainLanguageContentDict['button_genImage_u'][self.languageIndex])
            self.m_panel_flashImage1_showImage.Enable( True )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            strMemType = self._RTxxx_getImgName()
            imgPath = "../img/RTxxx/" + strMemType + "image_unsigned.png"
            self.showImageLayout(imgPath.encode('utf-8'))
            self.m_button_flashImage.SetLabel(uilang.kMainLanguageContentDict['button_flashImage_u'][self.languageIndex])
        elif self.secureBootType == RTxxx_uidef.kSecureBootType_PlainCrc:
            self.m_panel_genImage1_browseApp.Enable( True )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel(uilang.kMainLanguageContentDict['button_genImage_c'][self.languageIndex])
            self.m_panel_flashImage1_showImage.Enable( True )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            strMemType = self._RTxxx_getImgName()
            imgPath = "../img/RTxxx/" + strMemType + "image_crc.png"
            self.showImageLayout(imgPath.encode('utf-8'))
            self.m_button_flashImage.SetLabel(uilang.kMainLanguageContentDict['button_flashImage_c'][self.languageIndex])
        else:
            pass
        self.RTxxx_setSecureBootButtonColor(needToPlaySound)
        self.Refresh()

    def RTxxx_updateOtpGroupText( self ):
        self.clearUserFuses()
        if self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
            if self.mcuDevice == uidef.kMcuDevice_iMXRT700:
                if self.efuseGroupSel == 0:
                    self.setInitialFuseGroupText(None, 'N/A')
                    self.m_button_fuse400.SetLabel('Lock0')
                    self.m_staticText_fuse410.SetLabel('Lock1')
                    self.m_staticText_fuse420.SetLabel('Lock2')
                    self.m_staticText_fuse430.SetLabel('Lock3')
                    self.m_staticText_fuse440.SetLabel('Lock4')
                    self.m_button_fuse450.SetLabel('Lock5')
                elif self.efuseGroupSel == 1:
                    self.setInitialFuseGroupText(self.efuseGroupSel, 'W')
                    self.m_staticText_fuse480.SetLabel('ROTKH')
                    self.m_staticText_fuse490.SetLabel('ROTKH')
                    self.m_staticText_fuse4a0.SetLabel('ROTKH')
                    self.m_staticText_fuse4b0.SetLabel('ROTKH')
                    self.m_staticText_fuse4c0.SetLabel('ROTKH')
                    self.m_staticText_fuse4d0.SetLabel('ROTKH')
                    self.m_staticText_fuse4e0.SetLabel('ROTKH')
                    self.m_staticText_fuse4f0.SetLabel('ROTKH')
                    self.m_staticText_fuse500.SetLabel('ROTKH')
                    self.m_staticText_fuse510.SetLabel('ROTKH')
                    self.m_staticText_fuse520.SetLabel('ROTKH')
                    self.m_staticText_fuse530.SetLabel('ROTKH')
                    self.m_staticText_fuse540.SetLabel('MK_SK')
                    self.m_staticText_fuse550.SetLabel('MK_SK')
                    self.m_staticText_fuse560.SetLabel('MK_SK')
                    self.m_staticText_fuse570.SetLabel('MK_SK')
                    self.m_staticText_fuse580.SetLabel('MK_SK')
                    self.m_staticText_fuse590.SetLabel('MK_SK')
                    self.m_staticText_fuse5a0.SetLabel('MK_SK')
                    self.m_staticText_fuse5b0.SetLabel('MK_SK')
                    self.m_staticText_fuse5c0.SetLabel('MK_SK')
                    self.m_staticText_fuse5d0.SetLabel('MK_SK')
                    self.m_staticText_fuse5e0.SetLabel('MK_SK')
                    self.m_staticText_fuse5f0.SetLabel('MK_SK')
                    self.m_staticText_fuse600.SetLabel('NsFwV')
                    self.m_staticText_fuse610.SetLabel('NsFwV')
                    self.m_staticText_fuse620.SetLabel('NsFwV')
                    self.m_staticText_fuse630.SetLabel('NsFwV')
                    self.m_staticText_fuse640.SetLabel('NsFwV')
                    self.m_staticText_fuse650.SetLabel('NsFwV')
                    self.m_staticText_fuse660.SetLabel('NsFwV')
                    self.m_staticText_fuse670.SetLabel('NsFwV')
                    self.m_staticText_fuse680.SetLabel('NsFwV')
                    self.m_staticText_fuse690.SetLabel('NsFwV')
                    self.m_staticText_fuse6a0.SetLabel('NsFwV')
                    self.m_staticText_fuse6b0.SetLabel('NsFwV')
                    self.m_staticText_fuse6c0.SetLabel('NsFwV')
                    self.m_button_fuse6d0.SetLabel('NsFwV')
                    self.m_button_fuse6e0.SetLabel('NsFwV')
                    self.m_staticText_fuse6f0.SetLabel('NsFwV')
                    self.m_staticText_fuse700.SetLabel('SeFwV')
                    self.m_staticText_fuse710.SetLabel('SeFwV')
                    self.m_staticText_fuse720.SetLabel('SeFwV')
                    self.m_staticText_fuse730.SetLabel('SeFwV')
                    self.m_staticText_fuse740.SetLabel('ImgKe')
                    self.m_staticText_fuse750.SetLabel('DCFG_C')
                    self.m_staticText_fuse780.SetLabel('Cfg0')
                    self.m_textCtrl_fuse780.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse790.SetLabel('Cfg1')
                    self.m_textCtrl_fuse790.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse7a0.SetLabel('Cfg2')
                    self.m_textCtrl_fuse7a0.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse7b0.SetLabel('Cfg3')
                    self.m_textCtrl_fuse7b0.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse7c0.SetLabel('Cfg4')
                    self.m_textCtrl_fuse7c0.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse7d0.SetLabel('Cfg5')
                    self.m_textCtrl_fuse7d0.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse7e0.SetLabel('Cfg6')
                    self.m_textCtrl_fuse7e0.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse800.SetLabel('Xip0C0')
                    self.m_staticText_fuse810.SetLabel('Xip0C1')
                    self.m_staticText_fuse820.SetLabel('Xip0C2')
                    self.m_staticText_fuse830.SetLabel('Xip0C3')
                    self.m_staticText_fuse840.SetLabel('Xip1C0')
                    self.m_staticText_fuse850.SetLabel('Xip1C1')
                    self.m_staticText_fuse860.SetLabel('Xip1C2')
                    self.m_staticText_fuse870.SetLabel('Xip1C3')
                    self.m_staticText_fuse880.SetLabel('XspiC0')
                    self.m_staticText_fuse890.SetLabel('XspiC1')
                    self.m_staticText_fuse8a0.SetLabel('XspiC2')
                    self.m_staticText_fuse8b0.SetLabel('XspiC3')
                    self.m_staticText_fuse8c0.SetLabel('XspiC4')
                    self.m_staticText_fuse8d0.SetLabel('XspiC5')
                    self.m_staticText_fuse8e0.SetLabel('SDHCC')
                    self.m_staticText_fuse8f0.SetLabel('SDHCC')
                elif self.efuseGroupSel == 2:
                    self.setInitialFuseGroupText(self.efuseGroupSel, 'W')
                    self.m_button_fuse400.SetLabel('Cfg8')
                    self.m_staticText_fuse420.SetLabel('Cfg10')
                    self.m_staticText_fuse430.SetLabel('Cfg11')
                    self.m_staticText_fuse440.SetLabel('Cfg12')
                    self.m_button_fuse450.SetLabel('Cfg13')
                    self.m_button_fuse460.SetLabel('Cfg14')
                    self.m_button_fuse470.SetLabel('Cfg15')
                    self.m_staticText_fuse480.SetLabel('Cfg16')
                    self.m_staticText_fuse490.SetLabel('Cfg17')
                    self.m_staticText_fuse4a0.SetLabel('Cfg18')
                    self.m_staticText_fuse4b0.SetLabel('Cfg19')
                    self.m_staticText_fuse4c0.SetLabel('Cfg20')
                    self.m_staticText_fuse4d0.SetLabel('Cfg21')
                    self.m_staticText_fuse4e0.SetLabel('Cfg22')
                    self.m_staticText_fuse4f0.SetLabel('Cfg23')
                    self.m_staticText_fuse500.SetLabel('Cfg24')
                    self.m_staticText_fuse510.SetLabel('Cfg25')
                    self.m_staticText_fuse520.SetLabel('Cfg26')
                    self.m_staticText_fuse530.SetLabel('Cfg27')
                    self.m_staticText_fuse540.SetLabel('Cfg28')
                    self.m_staticText_fuse550.SetLabel('Cfg29')
                    self.m_staticText_fuse560.SetLabel('Cfg30')
                    self.m_staticText_fuse570.SetLabel('Cfg31')
                else:
                    self.setInitialFuseGroupText(self.efuseGroupSel, 'N/A')
            else:
                if self.efuseGroupSel == 0:
                    self.setInitialFuseGroupText(self.efuseGroupSel, 'W')
                elif self.efuseGroupSel == 1:
                    self.setInitialFuseGroupText(self.efuseGroupSel, 'W')
                    self.m_staticText_fuse500.SetLabel('Cfg0')
                    self.m_textCtrl_fuse500.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse510.SetLabel('Cfg1')
                    self.m_textCtrl_fuse510.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse520.SetLabel('Cfg2')
                    self.m_textCtrl_fuse520.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse530.SetLabel('Cfg3')
                    self.m_textCtrl_fuse530.SetBackgroundColour( uidef.kFuseFieldColor_BootCfg )
                    self.m_staticText_fuse550.SetLabel('SCfg5')
                    self.m_staticText_fuse570.SetLabel('SCfg7')
                    self.m_staticText_fuse590.SetLabel('UsbId')
                    self.m_staticText_fuse600.SetLabel('OTPMK')
                    self.m_staticText_fuse610.SetLabel('OTPMK')
                    self.m_staticText_fuse620.SetLabel('OTPMK')
                    self.m_staticText_fuse630.SetLabel('OTPMK')
                    self.m_staticText_fuse640.SetLabel('OTPMK')
                    self.m_staticText_fuse650.SetLabel('OTPMK')
                    self.m_staticText_fuse660.SetLabel('OTPMK')
                    self.m_staticText_fuse670.SetLabel('OTPMK')
                    self.m_staticText_fuse680.SetLabel('RKTH')
                    self.m_staticText_fuse690.SetLabel('RKTH')
                    self.m_staticText_fuse6a0.SetLabel('RKTH')
                    self.m_staticText_fuse6b0.SetLabel('RKTH')
                    self.m_staticText_fuse6c0.SetLabel('RKTH')
                    self.m_button_fuse6d0.SetLabel('RKTH')
                    self.m_button_fuse6e0.SetLabel('RKTH')
                    self.m_staticText_fuse6f0.SetLabel('RKTH')
                    self.m_staticText_fuse700.SetLabel('NtFwV')
                    self.m_staticText_fuse710.SetLabel('NtFwV')
                    self.m_staticText_fuse720.SetLabel('NtFwV')
                    self.m_staticText_fuse730.SetLabel('NtFwV')
                    self.m_staticText_fuse740.SetLabel('NtFwV')
                    self.m_staticText_fuse750.SetLabel('NtFwV')
                    self.m_staticText_fuse760.SetLabel('NtFwV')
                    self.m_staticText_fuse770.SetLabel('NtFwV')
                    self.m_staticText_fuse780.SetLabel('NtFwV')
                    self.m_staticText_fuse790.SetLabel('NtFwV')
                    self.m_staticText_fuse7a0.SetLabel('NtFwV')
                    self.m_staticText_fuse7b0.SetLabel('NtFwV')
                    self.m_staticText_fuse7c0.SetLabel('NtFwV')
                    self.m_staticText_fuse7d0.SetLabel('NtFwV')
                    self.m_staticText_fuse7e0.SetLabel('NtFwV')
                    self.m_staticText_fuse7f0.SetLabel('NtFwV')
                    self.m_staticText_fuse800.SetLabel('TzFwV')
                    self.m_staticText_fuse810.SetLabel('TzFwV')
                    self.m_staticText_fuse820.SetLabel('TzFwV')
                    self.m_staticText_fuse830.SetLabel('TzFwV')
                    self.m_staticText_fuse840.SetLabel('UsRed')
                    self.m_staticText_fuse850.SetLabel('UsRed')
                    self.m_staticText_fuse860.SetLabel('UsRed')
                    self.m_staticText_fuse870.SetLabel('UsRed')
                    self.m_staticText_fuse880.SetLabel('UsEcc')
                    self.m_staticText_fuse890.SetLabel('UsEcc')
                    self.m_staticText_fuse8a0.SetLabel('UsEcc')
                    self.m_staticText_fuse8b0.SetLabel('UsEcc')
                    self.m_staticText_fuse8c0.SetLabel('UsEcc')
                    self.m_staticText_fuse8d0.SetLabel('UsEcc')
                    self.m_staticText_fuse8e0.SetLabel('UsEcc')
                    self.m_staticText_fuse8f0.SetLabel('UsEcc')
                elif self.efuseGroupSel == 2 or self.efuseGroupSel == 3:
                    self.setInitialFuseGroupText(None, 'RomP')
                elif self.efuseGroupSel == 4:
                    self.setInitialFuseGroupText(None, 'N/A')
                    self.m_button_fuse400.SetLabel('RomP')
                    self.m_staticText_fuse410.SetLabel('RomP')
                    self.m_staticText_fuse420.SetLabel('RomP')
                    self.m_staticText_fuse430.SetLabel('RomP')
                    self.m_staticText_fuse440.SetLabel('RomP')
                    self.m_button_fuse450.SetLabel('RomP')
                    self.m_button_fuse460.SetLabel('RomP')
                    self.m_button_fuse470.SetLabel('RomP')
                    self.m_staticText_fuse480.SetLabel('RomP')
                    self.m_staticText_fuse490.SetLabel('RomP')
                    self.m_staticText_fuse4a0.SetLabel('RomP')
                    self.m_staticText_fuse4b0.SetLabel('RomP')
                    self.m_staticText_fuse4c0.SetLabel('RomP')
                    self.m_staticText_fuse4d0.SetLabel('RomP')
                    self.m_staticText_fuse4e0.SetLabel('RomP')
                    self.m_staticText_fuse4f0.SetLabel('RomP')
                    self.m_staticText_fuse500.SetLabel('SBKEK')
                    self.m_staticText_fuse510.SetLabel('SBKEK')
                    self.m_staticText_fuse520.SetLabel('SBKEK')
                    self.m_staticText_fuse530.SetLabel('SBKEK')
                    self.m_staticText_fuse540.SetLabel('SBKEK')
                    self.m_staticText_fuse550.SetLabel('SBKEK')
                    self.m_staticText_fuse560.SetLabel('SBKEK')
                    self.m_staticText_fuse570.SetLabel('SBKEK')
                    self.m_staticText_fuse580.SetLabel('CERT')
                    self.m_staticText_fuse590.SetLabel('CERT')
                    self.m_staticText_fuse5a0.SetLabel('CERT')
                    self.m_staticText_fuse5b0.SetLabel('CERT')
                    self.m_staticText_fuse5c0.SetLabel('CERT')
                    self.m_staticText_fuse5d0.SetLabel('CERT')
                    self.m_staticText_fuse5e0.SetLabel('CERT')
                    self.m_staticText_fuse5f0.SetLabel('CERT')
                    self.m_staticText_fuse600.SetLabel('CERT')
                    self.m_staticText_fuse610.SetLabel('CERT')
                    self.m_staticText_fuse620.SetLabel('CERT')
                    self.m_staticText_fuse630.SetLabel('CERT')
                    self.m_staticText_fuse640.SetLabel('CERT')
                    self.m_staticText_fuse650.SetLabel('CERT')
                    self.m_staticText_fuse660.SetLabel('CERT')
                    self.m_staticText_fuse670.SetLabel('CERT')
                elif self.efuseGroupSel == 5:
                    self.setInitialFuseGroupText(None, 'N/A')
                elif self.efuseGroupSel == 6:
                    self.setInitialFuseGroupText(None, 'N/A')
                    self.m_staticText_fuse480.SetLabel('CRC0')
                    self.m_staticText_fuse490.SetLabel('CRC1')
                    self.m_staticText_fuse4a0.SetLabel('CRC2')
                    self.m_staticText_fuse4b0.SetLabel('CRC3')
                    self.m_staticText_fuse4c0.SetLabel('CRC4')
                    self.m_staticText_fuse4d0.SetLabel('CRC5')
                    self.m_staticText_fuse4e0.SetLabel('CRC6')
                    self.m_staticText_fuse4f0.SetLabel('CRC7')
                else:
                    pass
        else:
            pass
        self.Refresh()

    def RTxxx_updateOtpRegionField( self ):
        self.resetFuseOtpRegionField()
        color = None
        if self.toolRunMode == uidef.kToolRunMode_Entry:
            color = wx.SYS_COLOUR_GRAYTEXT
            if self.mcuSeries in uidef.kMcuSeries_iMXRTxxx_f:
                if self.efuseGroupSel == 0:
                    self.m_textCtrl_fuse400.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse410.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse420.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse430.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )

                    self.m_textCtrl_fuse450.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse460.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse470.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )

                    self.m_textCtrl_fuse4a0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse4b0.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )

                    self.m_textCtrl_fuse640.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse650.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )
                    self.m_textCtrl_fuse660.SetBackgroundColour( wx.SystemSettings.GetColour( color ) )

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
                elif self.efuseGroupSel == 1:
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
                elif self.efuseGroupSel == 2:
                    pass
                elif self.efuseGroupSel == 3:
                    pass
                elif self.efuseGroupSel == 4:
                    pass
                elif self.efuseGroupSel == 5:
                    pass
                elif self.efuseGroupSel == 6:
                    pass
                else:
                    pass
            else:
                pass
        self.Refresh()

    def RTxxx_showScannedOtps( self , scannedFuseList ):
        self.clearUserFuses()

        self.m_textCtrl_fuse400.write(self.parseReadFuseValue(scannedFuseList[0]))
        self.m_textCtrl_fuse410.write(self.parseReadFuseValue(scannedFuseList[1]))
        self.m_textCtrl_fuse420.write(self.parseReadFuseValue(scannedFuseList[2]))
        self.m_textCtrl_fuse430.write(self.parseReadFuseValue(scannedFuseList[3]))
        self.m_textCtrl_fuse440.write(self.parseReadFuseValue(scannedFuseList[4]))
        self.m_textCtrl_fuse450.write(self.parseReadFuseValue(scannedFuseList[5]))
        self.m_textCtrl_fuse460.write(self.parseReadFuseValue(scannedFuseList[6]))
        self.m_textCtrl_fuse470.write(self.parseReadFuseValue(scannedFuseList[7]))
        self.m_textCtrl_fuse480.write(self.parseReadFuseValue(scannedFuseList[8]))
        self.m_textCtrl_fuse490.write(self.parseReadFuseValue(scannedFuseList[9]))
        self.m_textCtrl_fuse4a0.write(self.parseReadFuseValue(scannedFuseList[10]))
        self.m_textCtrl_fuse4b0.write(self.parseReadFuseValue(scannedFuseList[11]))
        self.m_textCtrl_fuse4c0.write(self.parseReadFuseValue(scannedFuseList[12]))
        self.m_textCtrl_fuse4d0.write(self.parseReadFuseValue(scannedFuseList[13]))
        self.m_textCtrl_fuse4e0.write(self.parseReadFuseValue(scannedFuseList[14]))
        self.m_textCtrl_fuse4f0.write(self.parseReadFuseValue(scannedFuseList[15]))

        self.m_textCtrl_fuse500.write(self.parseReadFuseValue(scannedFuseList[16]))
        self.m_textCtrl_fuse510.write(self.parseReadFuseValue(scannedFuseList[17]))
        self.m_textCtrl_fuse520.write(self.parseReadFuseValue(scannedFuseList[18]))
        self.m_textCtrl_fuse530.write(self.parseReadFuseValue(scannedFuseList[19]))
        self.m_textCtrl_fuse540.write(self.parseReadFuseValue(scannedFuseList[20]))
        self.m_textCtrl_fuse550.write(self.parseReadFuseValue(scannedFuseList[21]))
        self.m_textCtrl_fuse560.write(self.parseReadFuseValue(scannedFuseList[22]))
        self.m_textCtrl_fuse570.write(self.parseReadFuseValue(scannedFuseList[23]))
        self.m_textCtrl_fuse580.write(self.parseReadFuseValue(scannedFuseList[24]))
        self.m_textCtrl_fuse590.write(self.parseReadFuseValue(scannedFuseList[25]))
        self.m_textCtrl_fuse5a0.write(self.parseReadFuseValue(scannedFuseList[26]))
        self.m_textCtrl_fuse5b0.write(self.parseReadFuseValue(scannedFuseList[27]))
        self.m_textCtrl_fuse5c0.write(self.parseReadFuseValue(scannedFuseList[28]))
        self.m_textCtrl_fuse5d0.write(self.parseReadFuseValue(scannedFuseList[29]))
        self.m_textCtrl_fuse5e0.write(self.parseReadFuseValue(scannedFuseList[30]))
        self.m_textCtrl_fuse5f0.write(self.parseReadFuseValue(scannedFuseList[31]))

        self.m_textCtrl_fuse600.write(self.parseReadFuseValue(scannedFuseList[32]))
        self.m_textCtrl_fuse610.write(self.parseReadFuseValue(scannedFuseList[33]))
        self.m_textCtrl_fuse620.write(self.parseReadFuseValue(scannedFuseList[34]))
        self.m_textCtrl_fuse630.write(self.parseReadFuseValue(scannedFuseList[35]))
        self.m_textCtrl_fuse640.write(self.parseReadFuseValue(scannedFuseList[36]))
        self.m_textCtrl_fuse650.write(self.parseReadFuseValue(scannedFuseList[37]))
        self.m_textCtrl_fuse660.write(self.parseReadFuseValue(scannedFuseList[38]))
        self.m_textCtrl_fuse670.write(self.parseReadFuseValue(scannedFuseList[39]))
        self.m_textCtrl_fuse680.write(self.parseReadFuseValue(scannedFuseList[40]))
        self.m_textCtrl_fuse690.write(self.parseReadFuseValue(scannedFuseList[41]))
        self.m_textCtrl_fuse6a0.write(self.parseReadFuseValue(scannedFuseList[42]))
        self.m_textCtrl_fuse6b0.write(self.parseReadFuseValue(scannedFuseList[43]))
        self.m_textCtrl_fuse6c0.write(self.parseReadFuseValue(scannedFuseList[44]))
        self.m_textCtrl_fuse6d0.write(self.parseReadFuseValue(scannedFuseList[45]))
        self.m_textCtrl_fuse6e0.write(self.parseReadFuseValue(scannedFuseList[46]))
        self.m_textCtrl_fuse6f0.write(self.parseReadFuseValue(scannedFuseList[47]))

        self.m_textCtrl_fuse700.write(self.parseReadFuseValue(scannedFuseList[48]))
        self.m_textCtrl_fuse710.write(self.parseReadFuseValue(scannedFuseList[49]))
        self.m_textCtrl_fuse720.write(self.parseReadFuseValue(scannedFuseList[50]))
        self.m_textCtrl_fuse730.write(self.parseReadFuseValue(scannedFuseList[51]))
        self.m_textCtrl_fuse740.write(self.parseReadFuseValue(scannedFuseList[52]))
        self.m_textCtrl_fuse750.write(self.parseReadFuseValue(scannedFuseList[53]))
        self.m_textCtrl_fuse760.write(self.parseReadFuseValue(scannedFuseList[54]))
        self.m_textCtrl_fuse770.write(self.parseReadFuseValue(scannedFuseList[55]))
        self.m_textCtrl_fuse780.write(self.parseReadFuseValue(scannedFuseList[56]))
        self.m_textCtrl_fuse790.write(self.parseReadFuseValue(scannedFuseList[57]))
        self.m_textCtrl_fuse7a0.write(self.parseReadFuseValue(scannedFuseList[58]))
        self.m_textCtrl_fuse7b0.write(self.parseReadFuseValue(scannedFuseList[59]))
        self.m_textCtrl_fuse7c0.write(self.parseReadFuseValue(scannedFuseList[60]))
        self.m_textCtrl_fuse7d0.write(self.parseReadFuseValue(scannedFuseList[61]))
        self.m_textCtrl_fuse7e0.write(self.parseReadFuseValue(scannedFuseList[62]))
        self.m_textCtrl_fuse7f0.write(self.parseReadFuseValue(scannedFuseList[63]))

        self.m_textCtrl_fuse800.write(self.parseReadFuseValue(scannedFuseList[64]))
        self.m_textCtrl_fuse810.write(self.parseReadFuseValue(scannedFuseList[65]))
        self.m_textCtrl_fuse820.write(self.parseReadFuseValue(scannedFuseList[66]))
        self.m_textCtrl_fuse830.write(self.parseReadFuseValue(scannedFuseList[67]))
        self.m_textCtrl_fuse840.write(self.parseReadFuseValue(scannedFuseList[68]))
        self.m_textCtrl_fuse850.write(self.parseReadFuseValue(scannedFuseList[69]))
        self.m_textCtrl_fuse860.write(self.parseReadFuseValue(scannedFuseList[70]))
        self.m_textCtrl_fuse870.write(self.parseReadFuseValue(scannedFuseList[71]))
        self.m_textCtrl_fuse880.write(self.parseReadFuseValue(scannedFuseList[72]))
        self.m_textCtrl_fuse890.write(self.parseReadFuseValue(scannedFuseList[73]))
        self.m_textCtrl_fuse8a0.write(self.parseReadFuseValue(scannedFuseList[74]))
        self.m_textCtrl_fuse8b0.write(self.parseReadFuseValue(scannedFuseList[75]))
        self.m_textCtrl_fuse8c0.write(self.parseReadFuseValue(scannedFuseList[76]))
        self.m_textCtrl_fuse8d0.write(self.parseReadFuseValue(scannedFuseList[77]))
        self.m_textCtrl_fuse8e0.write(self.parseReadFuseValue(scannedFuseList[78]))
        self.m_textCtrl_fuse8f0.write(self.parseReadFuseValue(scannedFuseList[79]))

    def RTxxx_setLanguage( self ):
        pass
