#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import os
import RTyyyy_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from win import advSettingsWin_Sign
from utils import sound

class secBootUiSettingsSign(advSettingsWin_Sign.advSettingsWin_Sign):

    def __init__(self, parent):
        advSettingsWin_Sign.advSettingsWin_Sign.__init__(self, parent)
        self._setLanguage()
        signSettingsDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Sign)
        self.signSettingsDict = signSettingsDict.copy()
        self._recoverLastSettings()

    def _setLanguage( self ):
        runtimeSettings = uivar.getRuntimeSettings()
        langIndex = runtimeSettings[3]
        self.m_notebook_signOpt.SetPageText(0, uilang.kSubLanguageContentDict['panel_signOpt'][langIndex])
        self.m_staticText_signPart.SetLabel(uilang.kSubLanguageContentDict['sText_signPart'][langIndex])
        self.m_staticText_signStart0.SetLabel(uilang.kSubLanguageContentDict['sText_signStart0'][langIndex])
        self.m_staticText_signSize0.SetLabel(uilang.kSubLanguageContentDict['sText_signSize0'][langIndex])
        self.m_staticText_signStart1.SetLabel(uilang.kSubLanguageContentDict['sText_signStart1'][langIndex])
        self.m_staticText_signSize1.SetLabel(uilang.kSubLanguageContentDict['sText_signSize1'][langIndex])
        self.m_staticText_signStart2.SetLabel(uilang.kSubLanguageContentDict['sText_signStart2'][langIndex])
        self.m_staticText_signSize2.SetLabel(uilang.kSubLanguageContentDict['sText_signSize2'][langIndex])
        self.m_button_ok.SetLabel(uilang.kSubLanguageContentDict['button_sign_ok'][langIndex])
        self.m_button_cancel.SetLabel(uilang.kSubLanguageContentDict['button_sign_cancel'][langIndex])

    def _updateSignRegionField ( self, isEnabled ):
        if isEnabled:
            self.m_textCtrl_signStart0.Enable( True )
            self.m_textCtrl_signSize0.Enable( True )
            self.m_textCtrl_signStart1.Enable( True )
            self.m_textCtrl_signSize1.Enable( True )
            self.m_textCtrl_signStart2.Enable( True )
            self.m_textCtrl_signSize2.Enable( True )
        else:
            self.m_textCtrl_signStart0.Enable( False )
            self.m_textCtrl_signSize0.Enable( False )
            self.m_textCtrl_signStart1.Enable( False )
            self.m_textCtrl_signSize1.Enable( False )
            self.m_textCtrl_signStart2.Enable( False )
            self.m_textCtrl_signSize2.Enable( False )

    def _recoverLastSettings ( self ):
        self.m_textCtrl_signStart0.Clear()
        self.m_textCtrl_signStart0.write(str(hex(self.signSettingsDict['signedStart0'])))
        self.m_textCtrl_signSize0.Clear()
        self.m_textCtrl_signSize0.write(str(hex(self.signSettingsDict['signedSize0'])))
        self.m_textCtrl_signStart1.Clear()
        self.m_textCtrl_signStart1.write(str(hex(self.signSettingsDict['signedStart1'])))
        self.m_textCtrl_signSize1.Clear()
        self.m_textCtrl_signSize1.write(str(hex(self.signSettingsDict['signedSize1'])))
        self.m_textCtrl_signStart2.Clear()
        self.m_textCtrl_signStart2.write(str(hex(self.signSettingsDict['signedStart2'])))
        self.m_textCtrl_signSize2.Clear()
        self.m_textCtrl_signSize2.write(str(hex(self.signSettingsDict['signedSize2'])))
        if self.signSettingsDict['isPartSigned']:
            self.m_choice_signPart.SetSelection(1)
        else:
            self.m_choice_signPart.SetSelection(0)
        self._updateSignRegionField(self.signSettingsDict['isPartSigned'])

    def callbackSignPart( self, event ):
        isPartSigned = False
        if self.m_choice_signPart.GetString(self.m_choice_signPart.GetSelection()) == 'Yes':
            isPartSigned = True
        self.signSettingsDict['isPartSigned'] = isPartSigned
        self._updateSignRegionField(isPartSigned)

    def popupMsgBox( self, msgStr ):
        messageText = (msgStr)
        wx.MessageBox(messageText, "Error", wx.OK | wx.ICON_INFORMATION)

    def _convertRegionInfoToVal32( self, regionInfoStr ):
        status = False
        val32 = None
        if len(regionInfoStr) > 2 and regionInfoStr[0:2] == '0x':
            try:
                val32 = int(regionInfoStr[2:len(regionInfoStr)], 16)
                status = True
            except:
                pass
        if not status:
            self.popupMsgBox('Illegal input detected! You should input like this format: 0x5000')
        return status, val32

    def _getSignRegionInfo( self ):
        convertStatus, start0 = self._convertRegionInfoToVal32(self.m_textCtrl_signStart0.GetLineText(0))
        if not convertStatus:
            return False
        convertStatus, size0 = self._convertRegionInfoToVal32(self.m_textCtrl_signSize0.GetLineText(0))
        if not convertStatus:
            return False
        if start0 == 0x0 or size0 == 0x0:
            self.popupMsgBox('Sign Region 0 start address or size shouldn\'t be 0x0')
            return False
        self.signSettingsDict['signedStart0'] = start0
        self.signSettingsDict['signedSize0'] = size0
        self.signSettingsDict['signedStart1'] = 0x0
        self.signSettingsDict['signedSize1'] = 0x0
        self.signSettingsDict['signedStart2'] = 0x0
        self.signSettingsDict['signedSize2'] = 0x0
        convertStatus, start1 = self._convertRegionInfoToVal32(self.m_textCtrl_signStart1.GetLineText(0))
        if not convertStatus:
            return False
        convertStatus, size1 = self._convertRegionInfoToVal32(self.m_textCtrl_signSize1.GetLineText(0))
        if not convertStatus:
            return False
        if start1 != 0x0 and size1 != 0x0:
            if start1 < start0 + size0:
                self.popupMsgBox('Sign Region 1 start address shouldn\'t less than Sign region 0 end address 0x%x' %(start0 + size0))
                return False
            self.signSettingsDict['signedStart1'] = start1
            self.signSettingsDict['signedSize1'] = size1
            convertStatus, start2 = self._convertRegionInfoToVal32(self.m_textCtrl_signStart2.GetLineText(0))
            if not convertStatus:
                return False
            convertStatus, size2 = self._convertRegionInfoToVal32(self.m_textCtrl_signSize2.GetLineText(0))
            if not convertStatus:
                return False
            if start2 != 0x0 and size2 != 0x0:
                if start2 < start1 + size1:
                    self.popupMsgBox('Sign Region 2 start address shouldn\'t less than Sign region 1 end address 0x%x' %(start1 + size1))
                    return False
                self.signSettingsDict['signedStart2'] = start2
                self.signSettingsDict['signedSize2'] = size2
        return True

    def callbackOk( self, event ):
        if self.signSettingsDict['isPartSigned']:
            if not self._getSignRegionInfo():
                return
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Sign, self.signSettingsDict)
        uivar.setRuntimeSettings(False)
        self.Show(False)
        runtimeSettings = uivar.getRuntimeSettings()
        sound.playSoundEffect(runtimeSettings[1], runtimeSettings[2], uidef.kSoundEffectFilename_Progress)

    def callbackCancel( self, event ):
        uivar.setRuntimeSettings(False)
        self.Show(False)

    def callbackClose( self, event ):
        uivar.setRuntimeSettings(False)
        self.Show(False)
