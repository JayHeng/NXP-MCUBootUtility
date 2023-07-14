#! /usr/bin/env python
import wx
import sys
import os
import math
import RTyyyy_uidef
import uidef
import uivar
import uilang
sys.path.append(os.path.abspath(".."))
from win import bootDeviceWin_FlexspiNand
from utils import sound

class secBootUiFlexspiNand(bootDeviceWin_FlexspiNand.bootDeviceWin_FlexspiNand):
    def __init__(self, parent):
        bootDeviceWin_FlexspiNand.bootDeviceWin_FlexspiNand.__init__(self, parent)
        self._setLanguage()
        flexspiNandOpt0, flexspiNandOpt1, flexspiNandFcbOpt, flexspiNandImageInfoList = uivar.getBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_FlexspiNand)
        self.flexspiNandOpt0 = flexspiNandOpt0
        self.flexspiNandOpt1 = flexspiNandOpt1
        self.flexspiNandFcbOpt = flexspiNandFcbOpt
        self.flexspiNandImageInfoList = flexspiNandImageInfoList[:]
        self._recoverLastSettings()

    def _setLanguage( self ):
        runtimeSettings = uivar.getRuntimeSettings()
        langIndex = runtimeSettings[3]
        self.m_notebook_nandOpt.SetPageText(0, uilang.kSubLanguageContentDict['panel_nandOpt'][langIndex])
        self.m_staticText_flashSize.SetLabel(uilang.kSubLanguageContentDict['sText_flashSize'][langIndex])
        self.m_staticText_hasMultiplanes.SetLabel(uilang.kSubLanguageContentDict['sText_hasMultiplanes'][langIndex])
        self.m_staticText_pagesPerBlock.SetLabel(uilang.kSubLanguageContentDict['sText_pagesPerBlock'][langIndex])
        self.m_staticText_pageSize.SetLabel(uilang.kSubLanguageContentDict['sText_nandPageSize'][langIndex])
        self.m_staticText_maxFreq.SetLabel(uilang.kSubLanguageContentDict['sText_maxFrequency'][langIndex])
        self.m_staticText_manufacturerId.SetLabel(uilang.kSubLanguageContentDict['sText_manufacturerId'][langIndex])
        self.m_notebook_fcbOpt.SetPageText(0, uilang.kSubLanguageContentDict['panel_fcbOpt'][langIndex])
        self.m_staticText_searchCount.SetLabel(uilang.kSubLanguageContentDict['sText_searchCount'][langIndex])
        self.m_staticText_searchStride.SetLabel(uilang.kSubLanguageContentDict['sText_searchStride'][langIndex])
        self.m_staticText_addressType.SetLabel(uilang.kSubLanguageContentDict['sText_addressType'][langIndex])
        self.m_staticText_imageCopies.SetLabel(uilang.kSubLanguageContentDict['sText_imageCopies'][langIndex])
        self.m_notebook_imageInfo.SetPageText(0, uilang.kSubLanguageContentDict['panel_imageInfo'][langIndex])
        self.m_staticText_blockIndex.SetLabel(uilang.kSubLanguageContentDict['sText_blockIndex'][langIndex])
        self.m_staticText_blockCount.SetLabel(uilang.kSubLanguageContentDict['sText_blockCount'][langIndex])
        self.m_button_ok.SetLabel(uilang.kSubLanguageContentDict['button_semcnand_ok'][langIndex])
        self.m_button_cancel.SetLabel(uilang.kSubLanguageContentDict['button_semcnand_cancel'][langIndex])

    def _updateImageInfoField ( self, imageCopies ):
        if imageCopies < 2:
            self.m_textCtrl_image1Idx.Clear()
            self.m_textCtrl_image1Cnt.Clear()
            self.m_textCtrl_image1Idx.Enable( False )
            self.m_textCtrl_image1Cnt.Enable( False )
        else:
            self.m_textCtrl_image1Idx.Enable( True )
            self.m_textCtrl_image1Cnt.Enable( True )
        if imageCopies < 3:
            self.m_textCtrl_image2Idx.Clear()
            self.m_textCtrl_image2Cnt.Clear()
            self.m_textCtrl_image2Idx.Enable( False )
            self.m_textCtrl_image2Cnt.Enable( False )
        else:
            self.m_textCtrl_image2Idx.Enable( True )
            self.m_textCtrl_image2Cnt.Enable( True )
        if imageCopies < 4:
            self.m_textCtrl_image3Idx.Clear()
            self.m_textCtrl_image3Cnt.Clear()
            self.m_textCtrl_image3Idx.Enable( False )
            self.m_textCtrl_image3Cnt.Enable( False )
        else:
            self.m_textCtrl_image3Idx.Enable( True )
            self.m_textCtrl_image3Cnt.Enable( True )
        if imageCopies < 5:
            self.m_textCtrl_image4Idx.Clear()
            self.m_textCtrl_image4Cnt.Clear()
            self.m_textCtrl_image4Idx.Enable( False )
            self.m_textCtrl_image4Cnt.Enable( False )
        else:
            self.m_textCtrl_image4Idx.Enable( True )
            self.m_textCtrl_image4Cnt.Enable( True )
        if imageCopies < 6:
            self.m_textCtrl_image5Idx.Clear()
            self.m_textCtrl_image5Cnt.Clear()
            self.m_textCtrl_image5Idx.Enable( False )
            self.m_textCtrl_image5Cnt.Enable( False )
        else:
            self.m_textCtrl_image5Idx.Enable( True )
            self.m_textCtrl_image5Cnt.Enable( True )
        if imageCopies < 7:
            self.m_textCtrl_image6Idx.Clear()
            self.m_textCtrl_image6Cnt.Clear()
            self.m_textCtrl_image6Idx.Enable( False )
            self.m_textCtrl_image6Cnt.Enable( False )
        else:
            self.m_textCtrl_image6Idx.Enable( True )
            self.m_textCtrl_image6Cnt.Enable( True )
        if imageCopies < 8:
            self.m_textCtrl_image7Idx.Clear()
            self.m_textCtrl_image7Cnt.Clear()
            self.m_textCtrl_image7Idx.Enable( False )
            self.m_textCtrl_image7Cnt.Enable( False )
        else:
            self.m_textCtrl_image7Idx.Enable( True )
            self.m_textCtrl_image7Cnt.Enable( True )

    def _recoverLastSettings ( self ):
        flashSize = (self.flexspiNandOpt0 & 0x000F0000) >> 16
        self.m_choice_flashSize.SetSelection(flashSize)

        hasMultiplanes = (self.flexspiNandOpt0 & 0x0000F000) >> 12
        self.m_choice_hasMultiplanes.SetSelection(hasMultiplanes)

        pagesPerBlock = (self.flexspiNandOpt0 & 0x00000F00) >> 8
        self.m_choice_pagesPerBlock.SetSelection(pagesPerBlock)

        pageSize = (self.flexspiNandOpt0 & 0x000000F0) >> 4
        pageSize = int(math.log(pageSize, 2))
        self.m_choice_pageSize.SetSelection(pageSize - 1)

        maxFreq = (self.flexspiNandOpt0 & 0x0000000F) - 1
        self.m_choice_maxFreq.SetSelection(maxFreq)

        manufacturerId = (self.flexspiNandOpt1 & 0xFF) >> 0
        self.m_textCtrl_manufacturerId.Clear()
        self.m_textCtrl_manufacturerId.write(str(hex(int(manufacturerId))))

        searchCount = (self.flexspiNandFcbOpt & 0x0F000000) >> 24
        self.m_choice_searchCount.SetSelection(searchCount - 1)

        searchStride = (self.flexspiNandFcbOpt & 0x00F00000) >> 20
        self.m_choice_searchStride.SetSelection(searchStride)

        addressType = (self.flexspiNandFcbOpt & 0x00000F00) >> 8
        self.m_choice_addressType.SetSelection(addressType)

        imageCopies = 1
        while (imageCopies <= 8):
            if self.flexspiNandImageInfoList[imageCopies - 1] == None:
                imageCopies -= 1
                break
            else:
                imageCopies += 1
        self.m_choice_imageCopies.SetSelection(imageCopies - 1)

        self._updateImageInfoField(imageCopies)

        if imageCopies > 0:
            imageIdx = self.flexspiNandImageInfoList[0] >> 16
            imageCnt = self.flexspiNandImageInfoList[0] & 0x0000FFFF
            self.m_textCtrl_image0Idx.Clear()
            self.m_textCtrl_image0Cnt.Clear()
            self.m_textCtrl_image0Idx.write(str(imageIdx))
            self.m_textCtrl_image0Cnt.write(str(imageCnt))
        if imageCopies > 1:
            imageIdx = self.flexspiNandImageInfoList[1] >> 16
            imageCnt = self.flexspiNandImageInfoList[1] & 0x0000FFFF
            self.m_textCtrl_image1Idx.Clear()
            self.m_textCtrl_image1Cnt.Clear()
            self.m_textCtrl_image1Idx.write(str(imageIdx))
            self.m_textCtrl_image1Cnt.write(str(imageCnt))
        if imageCopies > 2:
            imageIdx = self.flexspiNandImageInfoList[2] >> 16
            imageCnt = self.flexspiNandImageInfoList[2] & 0x0000FFFF
            self.m_textCtrl_image2Idx.Clear()
            self.m_textCtrl_image2Cnt.Clear()
            self.m_textCtrl_image2Idx.write(str(imageIdx))
            self.m_textCtrl_image2Cnt.write(str(imageCnt))
        if imageCopies > 3:
            imageIdx = self.flexspiNandImageInfoList[3] >> 16
            imageCnt = self.flexspiNandImageInfoList[3] & 0x0000FFFF
            self.m_textCtrl_image3Idx.Clear()
            self.m_textCtrl_image3Cnt.Clear()
            self.m_textCtrl_image3Idx.write(str(imageIdx))
            self.m_textCtrl_image3Cnt.write(str(imageCnt))
        if imageCopies > 4:
            imageIdx = self.flexspiNandImageInfoList[4] >> 16
            imageCnt = self.flexspiNandImageInfoList[4] & 0x0000FFFF
            self.m_textCtrl_image4Idx.Clear()
            self.m_textCtrl_image4Cnt.Clear()
            self.m_textCtrl_image4Idx.write(str(imageIdx))
            self.m_textCtrl_image4Cnt.write(str(imageCnt))
        if imageCopies > 5:
            imageIdx = self.flexspiNandImageInfoList[5] >> 16
            imageCnt = self.flexspiNandImageInfoList[5] & 0x0000FFFF
            self.m_textCtrl_image5Idx.Clear()
            self.m_textCtrl_image5Cnt.Clear()
            self.m_textCtrl_image5Idx.write(str(imageIdx))
            self.m_textCtrl_image5Cnt.write(str(imageCnt))
        if imageCopies > 6:
            imageIdx = self.flexspiNandImageInfoList[6] >> 16
            imageCnt = self.flexspiNandImageInfoList[6] & 0x0000FFFF
            self.m_textCtrl_image6Idx.Clear()
            self.m_textCtrl_image6Cnt.Clear()
            self.m_textCtrl_image6Idx.write(str(imageIdx))
            self.m_textCtrl_image6Cnt.write(str(imageCnt))
        if imageCopies > 7:
            imageIdx = self.flexspiNandImageInfoList[7] >> 16
            imageCnt = self.flexspiNandImageInfoList[7] & 0x0000FFFF
            self.m_textCtrl_image7Idx.Clear()
            self.m_textCtrl_image7Cnt.Clear()
            self.m_textCtrl_image7Idx.write(str(imageIdx))
            self.m_textCtrl_image7Cnt.write(str(imageCnt))

    def _getFlashSize( self ):
        val = self.m_choice_flashSize.GetSelection()
        self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xFFF0FFFF) | (val << 16)

    def _getHasMultiplanes( self ):
        val = self.m_choice_hasMultiplanes.GetSelection()
        self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xFFFF0FFF) | (val << 12)

    def _getPagesPerBlock( self ):
        val = self.m_choice_pagesPerBlock.GetSelection()
        self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xFFFFF0FF) | (val << 8)

    def _getPageSize( self ):
        val = self.m_choice_pageSize.GetSelection()
        val = int(math.pow(2, val + 1))
        self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xFFFFFF0F) | (val << 4)

    def _getMaxFreq( self ):
        val = self.m_choice_maxFreq.GetSelection() + 1
        self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xFFFFFFF0) | (val << 0)

    def _convertManufacturerIdToVal32( self, idStr ):
        status = False
        val32 = None
        if len(idStr) > 2 and idStr[0:2] == '0x':
            try:
                val32 = int(idStr[2:len(idStr)], 16)
                status = True
            except:
                pass
        if not status:
            self.popupMsgBox('Illegal input detected! You should input like this format: 0x2c')
        return status, val32

    def _getManufacturerId( self ):
        convertStatus, val = self._convertManufacturerIdToVal32(self.m_textCtrl_manufacturerId.GetLineText(0))
        if not convertStatus:
            return False
        else:
            self.flexspiNandOpt1 = (self.flexspiNandOpt1 & 0xFFFFFF00) | (val << 0)
            if val == 0:
                self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xF0FFFFFF) | (0 << 24)
            else:
                self.flexspiNandOpt0 = (self.flexspiNandOpt0 & 0xF0FFFFFF) | (1 << 24)
            return True

    def _getSearchCount( self ):
        val = self.m_choice_searchCount.GetSelection() + 1
        self.flexspiNandFcbOpt = (self.flexspiNandFcbOpt & 0xF0FFFFFF) | (val << 24)

    def _getSearchStride( self ):
        val = self.m_choice_searchStride.GetSelection()
        self.flexspiNandFcbOpt = (self.flexspiNandFcbOpt & 0xFF0FFFFF) | (val << 20)

    def _getAddressType( self ):
        val = self.m_choice_addressType.GetSelection()
        self.flexspiNandFcbOpt = (self.flexspiNandFcbOpt & 0xFFFFF0FF) | (val << 8)

    def _getImageInfo( self ):
        imageCopies = int(self.m_choice_imageCopies.GetString(self.m_choice_imageCopies.GetSelection()))
        if imageCopies > 0:
            self.flexspiNandImageInfoList[0] = (int(self.m_textCtrl_image0Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image0Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[0] = None
        if imageCopies > 1:
            self.flexspiNandImageInfoList[1] = (int(self.m_textCtrl_image1Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image1Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[1] = None
        if imageCopies > 2:
            self.flexspiNandImageInfoList[2] = (int(self.m_textCtrl_image2Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image2Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[2] = None
        if imageCopies > 3:
            self.flexspiNandImageInfoList[3] = (int(self.m_textCtrl_image3Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image3Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[3] = None
        if imageCopies > 4:
            self.flexspiNandImageInfoList[4] = (int(self.m_textCtrl_image4Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image4Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[4] = None
        if imageCopies > 5:
            self.flexspiNandImageInfoList[5] = (int(self.m_textCtrl_image5Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image5Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[5] = None
        if imageCopies > 6:
            self.flexspiNandImageInfoList[6] = (int(self.m_textCtrl_image6Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image6Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[6] = None
        if imageCopies > 7:
            self.flexspiNandImageInfoList[7] = (int(self.m_textCtrl_image7Idx.GetLineText(0)) << 16) + int(self.m_textCtrl_image7Cnt.GetLineText(0))
        else:
            self.flexspiNandImageInfoList[7] = None

        fcbOptBlockSize = imageCopies + 2
        self.flexspiNandFcbOpt = (self.flexspiNandFcbOpt & 0xFFFFFFF0) | fcbOptBlockSize

    def callbackChangeImageCopies( self, event ):
        imageCopies = int(self.m_choice_imageCopies.GetString(self.m_choice_imageCopies.GetSelection()))
        self._updateImageInfoField(imageCopies)

    def callbackOk( self, event ):
        self._getFlashSize()
        self._getHasMultiplanes()
        self._getPagesPerBlock()
        self._getPageSize()
        self._getMaxFreq()
        if not self._getManufacturerId():
            return
        self._getSearchCount()
        self._getSearchStride()
        self._getAddressType()
        self._getImageInfo()
        uivar.setBootDeviceConfiguration(RTyyyy_uidef.kBootDevice_FlexspiNand, self.flexspiNandOpt0, self.flexspiNandOpt1, self.flexspiNandFcbOpt, self.flexspiNandImageInfoList)
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