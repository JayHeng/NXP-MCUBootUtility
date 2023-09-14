#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import MCX_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from _main import Kinetis_main

class secBootMcxUi(Kinetis_main.secBootKinetisMain):

    def __init__(self, parent):
        Kinetis_main.secBootKinetisMain.__init__(self, parent)
        if self.mcuSeries == uidef.kMcuSeries_MCX:
            self.MCX_initUi()

    def MCX_initUi( self ):
        self._MCX_initTargetSetupValue()
        self.MCX_setTargetSetupValue()

        self.secureBootType = None
        self._MCX_initSecureBootSeqValue()
        self._MCX_initSecureBootSeqColor()
        self.setDcdButtonEnablement(False)
        self.setBdcButtonEnablement(False)
        self.setXmcdButtonEnablement(False)

    def _MCX_initTargetSetupValue( self ):
        self.m_choice_bootDevice.Clear()
        self.m_choice_bootDevice.SetItems(MCX_uidef.kBootDevice_Latest)
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

    def MCX_setTargetSetupValue( self ):
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.MCX_createMcuTarget()
        self.refreshBootDeviceList()
        self.bootDevice = self.m_choice_bootDevice.GetString(self.m_choice_bootDevice.GetSelection())
        self.toolCommDict['bootDevice'] = self.m_choice_bootDevice.GetSelection()

    def _MCX_initSecureBootSeqValue( self ):
        if not self.initSecureBootTypeList():
            self.m_choice_secureBootType.Clear()
            self.m_choice_secureBootType.SetItems(MCX_uidef.kSecureBootType_Latest)
        totalSel = self.m_choice_secureBootType.GetCount()
        if self.toolCommDict['secBootType'] < totalSel:
            self.m_choice_secureBootType.SetSelection(self.toolCommDict['secBootType'])
        else:
            self.m_choice_secureBootType.SetSelection(0)

    def _MCX_initSecureBootSeqColor ( self ):
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.MCX_setSecureBootSeqColor()

    def MCX_setSecureBootButtonColor( self, needToPlaySound=True ):
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
        if self.secureBootType == MCX_uidef.kSecureBootType_PlainUnsigned:
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

    def _MCX_getImgName( self ):
        memType = 'ftfx_'
        return memType

    def MCX_setSecureBootSeqColor( self , needToPlaySound=True ):
        self.hasDynamicLableBeenInit = True
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.refreshSecureBootTypeList()
        self.toolCommDict['secBootType'] = self.m_choice_secureBootType.GetSelection()
        self.secureBootType = self.m_choice_secureBootType.GetString(self.m_choice_secureBootType.GetSelection())
        self.resetSecureBootSeqColor()
        if self.secureBootType == MCX_uidef.kSecureBootType_PlainUnsigned:
            self.m_panel_genImage1_browseApp.Enable( True )
            self.m_panel_genImage1_browseApp.SetBackgroundColour( uidef.kBootSeqColor_Active )
            self.m_button_genImage.SetLabel(uilang.kMainLanguageContentDict['button_genImage_u'][self.languageIndex])
            self.m_panel_flashImage1_showImage.Enable( True )
            self.m_panel_flashImage1_showImage.SetBackgroundColour( uidef.kBootSeqColor_Active )
            strMemType = self._MCX_getImgName()
            imgPath = "../img/Kinetis/" + strMemType + "image_unsigned.png"
            self.showImageLayout(imgPath.encode('utf-8'))
            self.m_button_flashImage.SetLabel(uilang.kMainLanguageContentDict['button_flashImage_u'][self.languageIndex])
        else:
            pass
        self.MCX_setSecureBootButtonColor(needToPlaySound)
        self.Refresh()

    def MCX_setLanguage( self ):
        pass
