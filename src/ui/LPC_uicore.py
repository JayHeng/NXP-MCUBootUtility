#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import LPC_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from _main import RTxxx_main

class secBootLpcUi(RTxxx_main.secBootRTxxxMain):

    def __init__(self, parent):
        RTxxx_main.secBootRTxxxMain.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_LPC:
            self.LPC_initUi()

    def LPC_initUi( self ):
        self._LPC_initTargetSetupValue()
        self.LPC_setTargetSetupValue()

        self.secureBootType = None
        self._LPC_initSecureBootSeqValue()
        self._LPC_initSecureBootSeqColor()
        self.setDcdButtonEnablement(False)
        self.setBdcButtonEnablement(False)
        self.setXmcdButtonEnablement(False)

    def _LPC_initTargetSetupValue( self ):
        self.m_choice_bootDevice.Clear()
        self.m_choice_bootDevice.SetItems(LPC_uidef.kBootDevice_Latest)
        totalSel = self.m_choice_bootDevice.GetCount()
        if self.toolCommDict['bootDevice'] < totalSel:
            self.m_choice_bootDevice.SetSelection(self.toolCommDict['bootDevice'])
        else:
            self.m_choice_bootDevice.SetSelection(0)
        if self.toolCommDict['appFilename'] != None:
            self.m_filePicker_appPath.SetPath(self.toolCommDict['appFilename'])
        self.m_choice_appFormat.SetSelection(self.toolCommDict['appFormat'])
        self._setUserBinaryBaseField()
        self.m_textCtrl_appBaseAddr.Clear()
        self.m_textCtrl_appBaseAddr.write(self.toolCommDict['appBinBaseAddr'])

    def LPC_setTargetSetupValue( self ):
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.LPC_createMcuTarget()
        self.refreshBootDeviceList()
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.toolCommDict['bootDevice'] = self.m_choice_bootDevice.GetSelection()

    def _LPC_initSecureBootSeqValue( self ):
        if not self.initSecureBootTypeList():
            self.m_choice_secureBootType.Clear()
            self.m_choice_secureBootType.SetItems(LPC_uidef.kSecureBootType_Latest)
        totalSel = self.m_choice_secureBootType.GetCount()
        if self.toolCommDict['secBootType'] < totalSel:
            self.m_choice_secureBootType.SetSelection(self.toolCommDict['secBootType'])
        else:
            self.m_choice_secureBootType.SetSelection(0)

    def _LPC_initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.LPC_setSecureBootSeqColor()

    def LPC_setSecureBootButtonColor( self, needToPlaySound=True ):
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
        if self.secureBootType == LPC_uidef.kSecureBootType_PlainUnsigned:
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

    def _LPC_getImgName( self ):
        memType = 'c040hd_'
        return memType

    def LPC_setSecureBootSeqColor( self , needToPlaySound=True ):
        self.hasDynamicLableBeenInit = True
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.refreshSecureBootTypeList()
        self.toolCommDict['secBootType'] = self.m_choice_secureBootType.GetSelection()
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.resetSecureBootSeqColor()
        if self.secureBootType == LPC_uidef.kSecureBootType_PlainUnsigned:
            self.m_panel_genImage1_browseApp.Enable( True )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel(uilang.kMainLanguageContentDict['button_genImage_u'][self.languageIndex])
            self.m_panel_flashImage1_showImage.Enable( True )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            strMemType = self._LPC_getImgName()
            imgPath = "../img/LPC/" + strMemType + "image_unsigned.png"
            self.showImageLayout(imgPath.encode('utf-8'))
            self.m_button_flashImage.SetLabel(uilang.kMainLanguageContentDict['button_flashImage_u'][self.languageIndex])
        else:
            pass
        self.LPC_setSecureBootButtonColor(needToPlaySound)
        self.Refresh()

    def LPC_setLanguage( self ):
        pass
