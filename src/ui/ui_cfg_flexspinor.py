#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import sys
import os
import math
import uidef
import uivar
import uilang
import ui_cfg_fdcb
sys.path.append(os.path.abspath(".."))
from win import bootDeviceWin_FlexspiNor
from mem import memdef
from utils import sound

class secBootUiCfgFlexspiNor(bootDeviceWin_FlexspiNor.bootDeviceWin_FlexspiNor):

    def __init__(self, parent):
        bootDeviceWin_FlexspiNor.bootDeviceWin_FlexspiNor.__init__(self, parent)
        self._setLanguage()
        self.mcuSeries = None
        self.flexspiFreqs = None
        self.cfgFdcbBinFilename = None
        self.hasFlexspiNorDualImageBoot = None
        self.hasMultipleFlexspiInstance = None
        flexspiNorOpt0, flexspiNorOpt1, flexspiDeviceModel, isFdcbKept, flexspiNorDualImageInfoList = uivar.getBootDeviceConfiguration(uidef.kBootDevice_XspiNor)
        #1. Prepare Flash option
        # 0xc0000006 is the tag for Serial NOR parameter selection
        # bit [31:28] Tag fixed to 0x0C
        # bit [27:24] Option size fixed to 0
        # bit [23:20] Flash type option
        #             0 - QuadSPI SDR NOR
        #             1 - QUadSPI DDR NOR
        # bit [19:16] Query pads (Pads used for query Flash Parameters)
        #             0 - 1
        # bit [15:12] CMD pads (Pads used for query Flash Parameters)
        #             0 - 1
        # bit [11: 08] Quad Mode Entry Setting
        #             0 - Not Configured, apply to devices:
        #                 - With Quad Mode enabled by default or
        #                 - Compliant with JESD216A/B or later revision
        #             1 - Set bit 6 in Status Register 1
        #             2 - Set bit 1 in Status Register 2
        #             3 - Set bit 7 in Status Register 2
        #             4 - Set bit 1 in Status Register 2 by 0x31 command
        # bit [07: 04]  Misc. control field
        #             3 - Data Order swapped, used for Macronix OctaFLASH devcies only (except MX25UM51345G)
        #             4 - Second QSPI NOR Pinmux
        # bit [03: 00] Flash Frequency, device specific
        self.flexspiNorOpt0 = flexspiNorOpt0
        self.flexspiNorOpt1 = flexspiNorOpt1
        self.flexspiDeviceModel = flexspiDeviceModel
        self.isFdcbKept = isFdcbKept
        self.flexspiNorDualImageInfoList = flexspiNorDualImageInfoList
        toolCommDict = uivar.getAdvancedSettings(uidef.kAdvancedSettings_Tool)
        self.toolCommDict = toolCommDict.copy()

    def _setLanguage( self ):
        runtimeSettings = uivar.getRuntimeSettings()
        langIndex = runtimeSettings[3]
        self.m_staticText_bootInstance.SetLabel(uilang.kSubLanguageContentDict['sText_bootInstance'][langIndex])
        self.m_staticText_deviceModel.SetLabel(uilang.kSubLanguageContentDict['sText_deviceModel'][langIndex])
        self.m_checkBox_keepFdcb.SetLabel(uilang.kSubLanguageContentDict['cBox_keepFdcb'][langIndex])
        self.m_notebook_norOpt0.SetPageText(0, uilang.kSubLanguageContentDict['panel_norOpt0'][langIndex])
        self.m_staticText_deviceType.SetLabel(uilang.kSubLanguageContentDict['sText_deviceType'][langIndex])
        self.m_staticText_queryPads.SetLabel(uilang.kSubLanguageContentDict['sText_queryPads'][langIndex])
        self.m_staticText_cmdPads.SetLabel(uilang.kSubLanguageContentDict['sText_cmdPads'][langIndex])
        self.m_staticText_quadModeSetting.SetLabel(uilang.kSubLanguageContentDict['sText_quadModeSetting'][langIndex])
        self.m_staticText_miscMode.SetLabel(uilang.kSubLanguageContentDict['sText_miscMode'][langIndex])
        self.m_staticText_maxFrequency.SetLabel(uilang.kSubLanguageContentDict['sText_maxFrequency'][langIndex])
        self.m_staticText_hasOption1.SetLabel(uilang.kSubLanguageContentDict['sText_hasOption1'][langIndex])
        self.m_notebook_norOpt1.SetPageText(0, uilang.kSubLanguageContentDict['panel_norOpt1'][langIndex])
        self.m_staticText_flashConnection.SetLabel(uilang.kSubLanguageContentDict['sText_flashConnection'][langIndex])
        self.m_staticText_driveStrength.SetLabel(uilang.kSubLanguageContentDict['sText_driveStrength'][langIndex])
        self.m_staticText_dqsPinmuxGroup.SetLabel(uilang.kSubLanguageContentDict['sText_dqsPinmuxGroup'][langIndex])
        self.m_staticText_enableSecondPinmux.SetLabel(uilang.kSubLanguageContentDict['sText_enableSecondPinmux'][langIndex])
        self.m_staticText_statusOverride.SetLabel(uilang.kSubLanguageContentDict['sText_statusOverride'][langIndex])
        self.m_staticText_dummyCycles.SetLabel(uilang.kSubLanguageContentDict['sText_dummyCycles'][langIndex])
        self.m_notebook_dualImageOpt.SetPageText(0, uilang.kSubLanguageContentDict['panel_dualImageOpt'][langIndex])
        self.m_staticText_image0Version.SetLabel(uilang.kSubLanguageContentDict['sText_dualImage0Version'][langIndex])
        self.m_staticText_image1Version.SetLabel(uilang.kSubLanguageContentDict['sText_dualImage1Version'][langIndex])
        self.m_staticText_image1Offset.SetLabel(uilang.kSubLanguageContentDict['sText_dualImage1Offset'][langIndex])
        self.m_staticText_image1Size.SetLabel(uilang.kSubLanguageContentDict['sText_dualImage1Size'][langIndex])
        self.m_button_completeFdcb.SetLabel(uilang.kSubLanguageContentDict['button_completeFdcb'][langIndex])
        self.m_button_ok.SetLabel(uilang.kSubLanguageContentDict['button_flexspinor_ok'][langIndex])
        self.m_button_cancel.SetLabel(uilang.kSubLanguageContentDict['button_flexspinor_cancel'][langIndex])

    def setNecessaryInfo( self, mcuSeries, flexspiFreqs, cfgFdcbBinFilename, hasFlexspiNorDualImageBoot, hasMultipleFlexspiInstance ):
        if flexspiFreqs != None:
            self.m_choice_maxFrequency.Clear()
            self.m_choice_maxFrequency.SetItems(flexspiFreqs)
            self.m_choice_maxFrequency.SetSelection(0)
            self.flexspiFreqs = flexspiFreqs
        self.mcuSeries = mcuSeries
        self.cfgFdcbBinFilename = cfgFdcbBinFilename
        self.hasFlexspiNorDualImageBoot = hasFlexspiNorDualImageBoot
        self.hasMultipleFlexspiInstance = hasMultipleFlexspiInstance
        self._recoverLastSettings()

    def _updateOpt1Field ( self, isEnabled ):
        if isEnabled:
            self.m_choice_flashConnection.Enable( True )
            self.m_textCtrl_driveStrength.Enable( True )
            self.m_textCtrl_dqsPinmuxGroup.Enable( True )
            self.m_choice_enableSecondPinmux.Enable( True )
            self.m_textCtrl_statusOverride.Enable( True )
            self.m_textCtrl_dummyCycles.Enable( True )
        else:
            self.m_choice_flashConnection.Enable( False )
            self.m_textCtrl_driveStrength.Enable( False )
            self.m_textCtrl_dqsPinmuxGroup.Enable( False )
            self.m_choice_enableSecondPinmux.Enable( False )
            self.m_textCtrl_statusOverride.Enable( False )
            self.m_textCtrl_dummyCycles.Enable( False )

    def _recoverLastSettings ( self ):
        if not self.hasMultipleFlexspiInstance:
            self.m_choice_bootInstance.SetSelection(0)
            self.m_choice_bootInstance.Enable(False)
            self.toolCommDict['flexspiBootInstance'] = 0
        else:
            self.m_choice_bootInstance.SetSelection(self.toolCommDict['flexspiBootInstance'])

        self.m_checkBox_keepFdcb.SetValue(self.isFdcbKept)

        self.m_choice_deviceMode.SetSelection(self.m_choice_deviceMode.FindString(self.flexspiDeviceModel))

        deviceType = (self.flexspiNorOpt0 & 0x00F00000) >> 20
        self.m_choice_deviceType.SetSelection(deviceType)

        queryPads = (self.flexspiNorOpt0 & 0x000F0000) >> 16
        if queryPads == 0:
            self.m_choice_queryPads.SetSelection(queryPads)
        else:
            self.m_choice_queryPads.SetSelection(queryPads - 1)

        cmdPads = (self.flexspiNorOpt0 & 0x0000F000) >> 12
        if cmdPads == 0:
            self.m_choice_cmdPads.SetSelection(cmdPads)
        else:
            self.m_choice_cmdPads.SetSelection(cmdPads - 1)

        quadModeSetting = (self.flexspiNorOpt0 & 0x00000F00) >> 8
        self.m_choice_quadModeSetting.SetSelection(quadModeSetting)

        miscMode = (self.flexspiNorOpt0 & 0x000000F0) >> 4
        if miscMode <= 3:
            self.m_choice_miscMode.SetSelection(miscMode)
        else:
            self.m_choice_miscMode.SetSelection(miscMode - 1)

        maxFrequency = (self.flexspiNorOpt0 & 0x0000000F) >> 0
        self.m_choice_maxFrequency.SetSelection(maxFrequency - 1)

        hasOption1 = (self.flexspiNorOpt0 & 0x0F000000) >> 24
        self.m_choice_hasOption1.SetSelection(hasOption1)
        if hasOption1 == 0:
            self._updateOpt1Field(False)
        else:
            self._updateOpt1Field(True)

            flashConnection = (self.flexspiNorOpt1 & 0xF0000000) >> 28
            self.m_choice_flashConnection.SetSelection(flashConnection)

            driveStrength = (self.flexspiNorOpt1 & 0x0F000000) >> 24
            self.m_textCtrl_driveStrength.Clear()
            self.m_textCtrl_driveStrength.write(str(driveStrength))

            dqsPinmuxGroup = (self.flexspiNorOpt1 & 0x00F00000) >> 20
            self.m_textCtrl_dqsPinmuxGroup.Clear()
            self.m_textCtrl_dqsPinmuxGroup.write(str(dqsPinmuxGroup))

            enableSecondPinmux = (self.flexspiNorOpt1 & 0x000F0000) >> 16
            self.m_choice_enableSecondPinmux.SetSelection(enableSecondPinmux)

            statusOverride = (self.flexspiNorOpt1 & 0x0000FF00) >> 8
            self.m_textCtrl_statusOverride.Clear()
            self.m_textCtrl_statusOverride.write(str(statusOverride))

            dummyCycles = (self.flexspiNorOpt1 & 0x000000FF) >> 0
            self.m_textCtrl_dummyCycles.Clear()
            self.m_textCtrl_dummyCycles.write(str(dummyCycles))

        if not self.hasFlexspiNorDualImageBoot:
            self.m_textCtrl_image0Version.Enable( False )
            self.m_textCtrl_image1Version.Enable( False )
            self.m_textCtrl_image1Offset.Enable( False )
            self.m_choice_image1Size.Enable( False )
        else:
            self.m_textCtrl_image0Version.Clear()
            if self.flexspiNorDualImageInfoList[0] == 0xffffffff:
                self.m_textCtrl_image0Version.write('none')
            else:
                self.m_textCtrl_image0Version.write(str(self.flexspiNorDualImageInfoList[0]))
            self.m_textCtrl_image1Version.Clear()
            if self.flexspiNorDualImageInfoList[1] == 0xffffffff:
                self.m_textCtrl_image1Version.write('none')
            else:
                self.m_textCtrl_image1Version.write(str(self.flexspiNorDualImageInfoList[1]))
            self.m_textCtrl_image1Offset.Clear()
            self.m_textCtrl_image1Offset.write(str(hex((self.flexspiNorDualImageInfoList[2] & 0xffff) * (256 * 1024))))
            self.m_choice_image1Size.SetSelection(self.flexspiNorDualImageInfoList[2] >> 16)

    def _getBootInstance( self ):
        self.toolCommDict['flexspiBootInstance'] = self.m_choice_bootInstance.GetSelection()

    def _getDeviceType( self ):
        txt = self.m_choice_deviceType.GetString(self.m_choice_deviceType.GetSelection())
        if txt == 'QuadSPI SDR NOR':
            val = 0x0
        elif txt == 'QuadSPI DDR NOR':
            val = 0x1
        elif txt == 'Hyper Flash 1.8V':
            val = 0x2
        elif txt == 'Hyper Flash 3.0V':
            val = 0x3
        elif txt == 'Macronix Octal DDR':
            val = 0x4
        elif txt == 'Macronix Octal SDR':
            val = 0x5
        elif txt == 'Micron Octal DDR':
            val = 0x6
        elif txt == 'Micron Octal SDR':
            val = 0x7
        elif txt == 'Adesto EcoXIP DDR':
            val = 0x8
        elif txt == 'Adesto EcoXIP SDR':
            val = 0x9
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFF0FFFFF) | (val << 20)

    def _getQueryPads( self ):
        val = int(self.m_choice_queryPads.GetString(self.m_choice_queryPads.GetSelection()))
        val = int(math.log(val, 2))
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFF0FFFF) | (val << 16)

    def _getCmdPads( self ):
        val = int(self.m_choice_cmdPads.GetString(self.m_choice_cmdPads.GetSelection()))
        val = int(math.log(val, 2))
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFF0FFF) | (val << 12)

    def _getQuadModeSetting( self ):
        txt = self.m_choice_quadModeSetting.GetString(self.m_choice_quadModeSetting.GetSelection())
        if txt == 'Not Configured':
            val = 0x0
        elif txt == 'Set StatusReg1[6]':
            val = 0x1
        elif txt == 'Set StatusReg2[1]':
            val = 0x2
        elif txt == 'Set StatusReg2[7]':
            val = 0x3
        elif txt == 'Set StatusReg2[1] by 0x31':
            val = 0x4
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFF0FF) | (val << 8)

    def _getMiscMode( self ):
        txt = self.m_choice_miscMode.GetString(self.m_choice_miscMode.GetSelection())
        if txt == 'Disabled':
            val = 0x0
        elif txt == '0_4_4 Mode':
            val = 0x1
        elif txt == '0_8_8 Mode':
            val = 0x2
        elif txt == 'Data Order Swapped':
            val = 0x3
        elif txt == 'Data Samp Intr Loopback':
            val = 0x5
        elif txt == 'Stand SPI mode':
            val = 0x6
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFFF0F) | (val << 4)

    def _getMaxFrequency( self ):
        val = self.m_choice_maxFrequency.GetSelection() + 1
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xFFFFFFF0) | (val << 0)

    def _getHasOpt1( self ):
        txt = self.m_choice_hasOption1.GetString(self.m_choice_hasOption1.GetSelection())
        if txt == 'No':
            val = 0x0
        elif txt == 'Yes':
            val = 0x1
        else:
            pass
        self.flexspiNorOpt0 = (self.flexspiNorOpt0 & 0xF0FFFFFF) | (val << 24)

    def _getFlashConnection( self ):
        txt = self.m_choice_flashConnection.GetString(self.m_choice_flashConnection.GetSelection())
        if txt == 'Single Port A':
            val = 0x0
        elif txt == 'Parallel':
            val = 0x1
        elif txt == 'Single Port B':
            val = 0x2
        elif txt == 'Both Ports':
            val = 0x3
        else:
            pass
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0x0FFFFFFF) | (val << 28)

    def _getDriveStrength( self ):
        val = int(self.m_textCtrl_driveStrength.GetLineText(0))
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0xF0FFFFFF) | (val << 24)

    def _getDqsPinmuxGroup( self ):
        val = int(self.m_textCtrl_dqsPinmuxGroup.GetLineText(0))
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0xFF0FFFFF) | (val << 20)

    def _getEnableSecondPinmux( self ):
        txt = self.m_choice_enableSecondPinmux.GetString(self.m_choice_enableSecondPinmux.GetSelection())
        if txt == 'No':
            val = 0x0
        elif txt == 'Yes':
            val = 0x1
        else:
            pass
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0xFFF0FFFF) | (val << 16)

    def _getStatusOverride( self ):
        val = int(self.m_textCtrl_statusOverride.GetLineText(0))
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0xFFFF00FF) | (val << 8)

    def _getDummyCycles( self ):
        val = int(self.m_textCtrl_dummyCycles.GetLineText(0))
        self.flexspiNorOpt1 = (self.flexspiNorOpt1 & 0xFFFFFF00) | (val << 0)

    def _getImage0Version( self ):
        status = True
        content = self.m_textCtrl_image0Version.GetLineText(0)
        if content == 'none':
            val = 0xFFFFFFFF
        else:
            val = int(content)
            if val > 65535:
                status = False
                self.popupMsgBox('Illegal input detected! max image 0 version is 65536')
        if status:
            self.flexspiNorDualImageInfoList[0] = val
        return status

    def _getImage1Version( self ):
        status = True
        content = self.m_textCtrl_image1Version.GetLineText(0)
        if content == 'none':
            val = 0xFFFFFFFF
        else:
            val = int(content)
            if val > 65535:
                status = False
                self.popupMsgBox('Illegal input detected! max image 1 version is 65536')
        if status:
            self.flexspiNorDualImageInfoList[1] = val
        return status

    def _getImage1Offset( self ):
        content = self.m_textCtrl_image1Offset.GetLineText(0)
        status = False
        val32 = None
        if len(content) > 2 and content[0:2] == '0x':
            try:
                val32 = int(content[2:len(content)], 16)
                if val32 % (256 * 1024) != 0:
                    self.popupMsgBox('Invalid setting found! Offset should be aligned with 256KB (0x40000)')
                elif val32 > (1023 * 256 * 1024):
                    self.popupMsgBox('Invalid setting found! Offset should not exceed 255.75MB (0xFFC0000)')
                else:
                    status = True
            except:
                pass
        if not status:
            self.popupMsgBox('Illegal input detected! You should set offset like this format: 0x40000')
        else:
            self.flexspiNorDualImageInfoList[2] = val32 / (256 * 1024)
        return status

    def _getImage1Size( self ):
        val = self.m_choice_image1Size.GetSelection()
        status = True
        size = 0
        if val == 0:
            size = self.flexspiNorDualImageInfoList[2] * (256 * 1024)
        elif (val >= 1 and val <= 12):
            size = val * (1024 * 1024)
        elif val == 13:
            size = 256 * 1024
        elif val == 14:
            size = 512 * 1024
        elif val == 15:
            size = 768 * 1024
        else:
            pass
        if size > self.flexspiNorDualImageInfoList[2] * (256 * 1024):
            status = False
            self.popupMsgBox('Invalid setting found! Size should not exceed offset')
        else:
            self.flexspiNorDualImageInfoList[2] = self.flexspiNorDualImageInfoList[2] + (val << 16)
        return status

    def callbackUseTypicalDeviceModel( self, event ):
        txt = self.m_choice_deviceMode.GetString(self.m_choice_deviceMode.GetSelection())
        self.flexspiDeviceModel = txt
        if txt == uidef.kFlexspiNorDevice_Winbond_W25Q128JV:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Winbond_W25Q128JV
        elif txt == uidef.kFlexspiNorDevice_Winbond_W35T51NW:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Winbond_W35T51NW
        elif txt == uidef.kFlexspiNorDevice_MXIC_MX25L12845G:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25L12845G
        elif txt == uidef.kFlexspiNorDevice_MXIC_MX25UM51245G:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51245G
        elif txt == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G
        elif txt == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G_OPI:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G_OPI
        elif txt == uidef.kFlexspiNorDevice_MXIC_MX25UM51345G_2nd:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_MXIC_MX25UM51345G_2nd
            self.flexspiNorOpt1 = uidef.kFlexspiNorOpt1_MXIC_MX25UM51345G_2nd
        elif txt == uidef.kFlexspiNorDevice_GigaDevice_GD25Q64C:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25Q64C
        elif txt == uidef.kFlexspiNorDevice_GigaDevice_GD25LB256E:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LB256E
        elif txt == uidef.kFlexspiNorDevice_GigaDevice_GD25LT256E:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LT256E
        elif txt == uidef.kFlexspiNorDevice_GigaDevice_GD25LX256E:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_GigaDevice_GD25LX256E
        elif txt == uidef.kFlexspiNorDevice_ISSI_IS25LP064A:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS25LP064A
        elif txt == uidef.kFlexspiNorDevice_ISSI_IS25LX256:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS25LX256
        elif txt == uidef.kFlexspiNorDevice_ISSI_IS26KS512S:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_ISSI_IS26KS512S
        elif txt == uidef.kFlexspiNorDevice_Micron_MT25QL128A:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT25QL128A
        elif txt == uidef.kFlexspiNorDevice_Micron_MT35X_RW303:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT35X_RW303
        elif txt == uidef.kFlexspiNorDevice_Micron_MT35X_RW304:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Micron_MT35X_RW304
        elif txt == uidef.kFlexspiNorDevice_Adesto_AT25SF128A:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Adesto_AT25SF128A
        elif txt == uidef.kFlexspiNorDevice_Adesto_ATXP032:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Adesto_ATXP032
        elif txt == uidef.kFlexspiNorDevice_Cypress_S25FL128S:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S25FL128S
        elif txt == uidef.kFlexspiNorDevice_Cypress_S26KS512S:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Cypress_S26KS512S
        elif txt == uidef.kFlexspiNorDevice_Microchip_SST26VF064B:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Microchip_SST26VF064B
        elif txt == uidef.kFlexspiNorDevice_FudanMicro_FM25Q64:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_FudanMicro_FM25Q64
        elif txt == uidef.kFlexspiNorDevice_BoyaMicro_BY25Q16BS:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_BoyaMicro_BY25Q16BS
        elif txt == uidef.kFlexspiNorDevice_XMC_XM25QH64B:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_XMC_XM25QH64B
        elif txt == uidef.kFlexspiNorDevice_XTXtech_X25Q64D:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_XTXtech_X25Q64D
        elif txt == uidef.kFlexspiNorDevice_Puya_P25Q64LE:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_Puya_P25Q64LE
        elif txt == uidef.kFlexspiNorDevice_AMIC_A25LQ64:
            self.flexspiNorOpt0 = uidef.kFlexspiNorOpt0_AMIC_A25LQ64
        else:
            pass
        if txt != 'No' and  txt != 'Complete_FDCB':
            self._recoverLastSettings()

    def callbackHasOption1( self, event ):
        txt = self.m_choice_hasOption1.GetString(self.m_choice_hasOption1.GetSelection())
        if txt == 'No':
            self._updateOpt1Field(False)
        elif txt == 'Yes':
            self._updateOpt1Field(True)
        else:
            pass

    def callbackSetCompleteFdcb( self, event ):
        if self.flexspiDeviceModel == 'Complete_FDCB':
            fdcbFrame = ui_cfg_fdcb.secBootUiCfgFdcb(None)
            fdcbFrame.SetTitle(u"Complete FDCB Configuration")
            fdcbFrame.setNecessaryInfo(self.mcuSeries, self.flexspiFreqs, self.cfgFdcbBinFilename)
            fdcbFrame.Show(True)

    def _getKeepFdcb( self ):
        self.isFdcbKept = self.m_checkBox_keepFdcb.GetValue()

    def popupMsgBox( self, msgStr ):
        messageText = (msgStr)
        wx.MessageBox(messageText, "Error", wx.OK | wx.ICON_INFORMATION)

    def callbackOk( self, event ):
        self._getBootInstance()
        self._getKeepFdcb()
        if self.flexspiDeviceModel == 'Complete_FDCB':
            if not (os.path.isfile(self.cfgFdcbBinFilename) and os.path.getsize(self.cfgFdcbBinFilename) == memdef.kMemBlockSize_FDCB):
                self.popupMsgBox('FDCB has not been specified！')
                return
        else:
            self._getDeviceType()
            self._getQueryPads()
            self._getCmdPads()
            self._getQuadModeSetting()
            self._getMiscMode()
            self._getMaxFrequency()
            self._getHasOpt1()
            hasOption1 = (self.flexspiNorOpt0 & 0x0F000000) >> 24
            if hasOption1:
                self._getFlashConnection()
                self._getDriveStrength()
                self._getDqsPinmuxGroup()
                self._getEnableSecondPinmux()
                self._getStatusOverride()
                self._getDummyCycles()
        if self.hasFlexspiNorDualImageBoot:
            if not self._getImage0Version():
                return
            if not self._getImage1Version():
                return
            if not self._getImage1Offset():
                return
            if not self._getImage1Size():
                return
        uivar.setBootDeviceConfiguration(uidef.kBootDevice_XspiNor, self.flexspiNorOpt0, self.flexspiNorOpt1, self.flexspiDeviceModel, self.isFdcbKept, self.flexspiNorDualImageInfoList)
        uivar.setAdvancedSettings(uidef.kAdvancedSettings_Tool, self.toolCommDict)
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

