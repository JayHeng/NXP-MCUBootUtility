# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class bootDeviceWin_FDCB
###########################################################################

class bootDeviceWin_FDCB ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1374,699 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_ipCfg0 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_ipCfg0 = wx.Panel( self.m_notebook_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer_ipCfg0 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer_ipCfg0.SetFlexibleDirection( wx.BOTH )
		fgSizer_ipCfg0.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText_tag = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"tag:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_tag.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_tag, 0, wx.ALL, 5 )

		self.m_textCtrl_tag = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, u"0x42464346", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_tag, 0, wx.ALL, 5 )

		self.m_staticText_version = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"version:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_version.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_version, 0, wx.ALL, 5 )

		self.m_textCtrl_version = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, u"0x56010400", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_version, 0, wx.ALL, 5 )

		self.m_staticText_readSampleClkSrc = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"readSampleClkSrc:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_readSampleClkSrc.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_readSampleClkSrc, 0, wx.ALL, 5 )

		m_choice_readSampleClkSrcChoices = [ u"0 - LoopbackInternally", u"1 - LoopbackFromDqsPad", u"2 - LoopbackFromSckPad", u"3 - ExternalInputFromDqsPad" ]
		self.m_choice_readSampleClkSrc = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 145,-1 ), m_choice_readSampleClkSrcChoices, 0 )
		self.m_choice_readSampleClkSrc.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_readSampleClkSrc, 0, wx.ALL, 5 )

		self.m_staticText_csHoldTime = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"csHoldTime:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_csHoldTime.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_csHoldTime, 0, wx.ALL, 5 )

		self.m_textCtrl_csHoldTime = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, u"0x3", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_csHoldTime, 0, wx.ALL, 5 )

		self.m_staticText_csSetupTime = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"csSetupTime:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_csSetupTime.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_csSetupTime, 0, wx.ALL, 5 )

		self.m_textCtrl_csSetupTime = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, u"0x3", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_csSetupTime, 0, wx.ALL, 5 )

		self.m_staticText_columnAddressWidth = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"columnAddressWidth:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_columnAddressWidth.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_columnAddressWidth, 0, wx.ALL, 5 )

		m_choice_columnAddressWidthChoices = [ u"0 - Other devices", u"3 - For HyperFlash" ]
		self.m_choice_columnAddressWidth = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_columnAddressWidthChoices, 0 )
		self.m_choice_columnAddressWidth.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_columnAddressWidth, 0, wx.ALL, 5 )

		self.m_staticText_deviceModeCfgEnable = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"deviceModeCfgEnable:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceModeCfgEnable.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_deviceModeCfgEnable, 0, wx.ALL, 5 )

		m_choice_deviceModeCfgEnableChoices = [ u"0 - Disable", u"1 - Enable" ]
		self.m_choice_deviceModeCfgEnable = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_deviceModeCfgEnableChoices, 0 )
		self.m_choice_deviceModeCfgEnable.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_deviceModeCfgEnable, 0, wx.ALL, 5 )

		self.m_staticText_deviceModeType = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"deviceModeType:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceModeType.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_deviceModeType, 0, wx.ALL, 5 )

		m_choice_deviceModeTypeChoices = [ u"0 - Generic", u"1 - Quad Enable", u"2 - SPI to xSPI mode", u"3 - xSPI to SPI mode", u"4 - SPI to NoCmd mode" ]
		self.m_choice_deviceModeType = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 135,-1 ), m_choice_deviceModeTypeChoices, 0 )
		self.m_choice_deviceModeType.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_deviceModeType, 0, wx.ALL, 5 )

		self.m_staticText_waitTimeCfgCommands = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"waitTimeCfgCommands:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_waitTimeCfgCommands.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_waitTimeCfgCommands, 0, wx.ALL, 5 )

		self.m_textCtrl_waitTimeCfgCommands = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_waitTimeCfgCommands, 0, wx.ALL, 5 )

		self.m_staticText_deviceModeArg = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"deviceModeArg:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceModeArg.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_deviceModeArg, 0, wx.ALL, 5 )

		self.m_textCtrl_deviceModeArg = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_deviceModeArg, 0, wx.ALL, 5 )

		self.m_staticText_configCmdEnable = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configCmdEnable:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdEnable.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configCmdEnable, 0, wx.ALL, 5 )

		m_choice_configCmdEnableChoices = [ u"0 - Disable", u"1 - Enable" ]
		self.m_choice_configCmdEnable = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdEnableChoices, 0 )
		self.m_choice_configCmdEnable.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_configCmdEnable, 0, wx.ALL, 5 )

		self.m_staticText_configModeType0 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configModeType[0]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configModeType0.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configModeType0, 0, wx.ALL, 5 )

		m_choice_configModeType0Choices = [ u"0 - Generic", u"1 - Quad Enable", u"2 - SPI to xSPI mode", u"3 - xSPI to SPI mode", u"4 - SPI to NoCmd mode" ]
		self.m_choice_configModeType0 = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 135,-1 ), m_choice_configModeType0Choices, 0 )
		self.m_choice_configModeType0.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_configModeType0, 0, wx.ALL, 5 )

		self.m_staticText_configModeType1 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configModeType[1]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configModeType1.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configModeType1, 0, wx.ALL, 5 )

		m_choice_configModeType1Choices = [ u"0 - Generic", u"1 - Quad Enable", u"2 - SPI to xSPI mode", u"3 - xSPI to SPI mode", u"4 - SPI to NoCmd mode" ]
		self.m_choice_configModeType1 = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 135,-1 ), m_choice_configModeType1Choices, 0 )
		self.m_choice_configModeType1.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_configModeType1, 0, wx.ALL, 5 )

		self.m_staticText_configModeType2 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configModeType[2]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configModeType2.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configModeType2, 0, wx.ALL, 5 )

		m_choice_configModeType2Choices = [ u"0 - Generic", u"1 - Quad Enable", u"2 - SPI to xSPI mode", u"3 - xSPI to SPI mode", u"4 - SPI to NoCmd mode" ]
		self.m_choice_configModeType2 = wx.Choice( self.m_panel_ipCfg0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 135,-1 ), m_choice_configModeType2Choices, 0 )
		self.m_choice_configModeType2.SetSelection( 0 )
		fgSizer_ipCfg0.Add( self.m_choice_configModeType2, 0, wx.ALL, 5 )

		self.m_staticText_configCmdArgs0 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configCmdArgs[0]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdArgs0.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configCmdArgs0, 0, wx.ALL, 5 )

		self.m_textCtrl_configCmdArgs0 = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_configCmdArgs0, 0, wx.ALL, 5 )

		self.m_staticText_configCmdArgs1 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configCmdArgs[1]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdArgs1.SetLabelMarkup( u"configCmdArgs[1]:" )
		self.m_staticText_configCmdArgs1.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configCmdArgs1, 0, wx.ALL, 5 )

		self.m_textCtrl_configCmdArgs1 = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_configCmdArgs1, 0, wx.ALL, 5 )

		self.m_staticText_configCmdArgs2 = wx.StaticText( self.m_panel_ipCfg0, wx.ID_ANY, u"configCmdArgs[2]:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdArgs2.Wrap( -1 )

		fgSizer_ipCfg0.Add( self.m_staticText_configCmdArgs2, 0, wx.ALL, 5 )

		self.m_textCtrl_configCmdArgs2 = wx.TextCtrl( self.m_panel_ipCfg0, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg0.Add( self.m_textCtrl_configCmdArgs2, 0, wx.ALL, 5 )


		self.m_panel_ipCfg0.SetSizer( fgSizer_ipCfg0 )
		self.m_panel_ipCfg0.Layout()
		fgSizer_ipCfg0.Fit( self.m_panel_ipCfg0 )
		self.m_notebook_ipCfg0.AddPage( self.m_panel_ipCfg0, u"flexspi ip cfg0", False )

		wSizer_win.Add( self.m_notebook_ipCfg0, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_ipCfg1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_ipCfg1 = wx.Panel( self.m_notebook_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer_ipCfg1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer_ipCfg1.SetFlexibleDirection( wx.BOTH )
		fgSizer_ipCfg1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_button_controllerMiscOption = wx.Button( self.m_panel_ipCfg1, wx.ID_ANY, u"controllerMiscOption", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_button_controllerMiscOption, 0, wx.ALL, 5 )

		self.m_textCtrl_controllerMiscOption = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_controllerMiscOption, 0, wx.ALL, 5 )

		self.m_staticText_deviceType = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"deviceType:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceType.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_deviceType, 0, wx.ALL, 5 )

		m_choice_deviceTypeChoices = [ u"1 - Serial NOR" ]
		self.m_choice_deviceType = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_deviceTypeChoices, 0 )
		self.m_choice_deviceType.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_deviceType, 0, wx.ALL, 5 )

		self.m_staticText_sflashPadType = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"sflashPadType:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sflashPadType.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_sflashPadType, 0, wx.ALL, 5 )

		m_choice_sflashPadTypeChoices = [ u"1 - Single pad", u"2 - Dual Pads", u"4 - Quad pads", u"8 - Octal pads" ]
		self.m_choice_sflashPadType = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_sflashPadTypeChoices, 0 )
		self.m_choice_sflashPadType.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_sflashPadType, 0, wx.ALL, 5 )

		self.m_staticText_serialClkFreq = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"serialClkFreq:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_serialClkFreq.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_serialClkFreq, 0, wx.ALL, 5 )

		m_choice_serialClkFreqChoices = []
		self.m_choice_serialClkFreq = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_serialClkFreqChoices, 0 )
		self.m_choice_serialClkFreq.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_serialClkFreq, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeqEnable = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"lutCustomSeqEnable:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeqEnable.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_lutCustomSeqEnable, 0, wx.ALL, 5 )

		m_choice_lutCustomSeqEnableChoices = [ u"0 - Pre-defined id & num", u"1 -Parameters in this block" ]
		self.m_choice_lutCustomSeqEnable = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 145,-1 ), m_choice_lutCustomSeqEnableChoices, 0 )
		self.m_choice_lutCustomSeqEnable.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_lutCustomSeqEnable, 0, wx.ALL, 5 )

		self.m_staticText_csPadSettingOverride = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"csPadSettingOverride:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_csPadSettingOverride.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_csPadSettingOverride, 0, wx.ALL, 5 )

		self.m_textCtrl_csPadSettingOverride = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_csPadSettingOverride, 0, wx.ALL, 5 )

		self.m_staticText_sclkPadSettingOverride = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"sclkPadSettingOverride:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sclkPadSettingOverride.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_sclkPadSettingOverride, 0, wx.ALL, 5 )

		self.m_textCtrl_sclkPadSettingOverride = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_sclkPadSettingOverride, 0, wx.ALL, 5 )

		self.m_staticText_dataPadSettingOverride = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dataPadSettingOverride", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_dataPadSettingOverride.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dataPadSettingOverride, 0, wx.ALL, 5 )

		self.m_textCtrl_dataPadSettingOverride = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dataPadSettingOverride, 0, wx.ALL, 5 )

		self.m_staticText_dqsPadSettingOverride = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dqsPadSettingOverride:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_dqsPadSettingOverride.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dqsPadSettingOverride, 0, wx.ALL, 5 )

		self.m_textCtrl_dqsPadSettingOverride = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dqsPadSettingOverride, 0, wx.ALL, 5 )

		self.m_staticText_timeoutInMs = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"timeoutInMs:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_timeoutInMs.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_timeoutInMs, 0, wx.ALL, 5 )

		self.m_textCtrl_timeoutInMs = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_timeoutInMs, 0, wx.ALL, 5 )

		self.m_staticText_commandInterval = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"commandInterval:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_commandInterval.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_commandInterval, 0, wx.ALL, 5 )

		self.m_textCtrl_commandInterval = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_commandInterval, 0, wx.ALL, 5 )

		self.m_staticText_dataValidTime0time_100ps = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dataValidTime[0].time_100ps:", wx.DefaultPosition, wx.Size( 160,-1 ), 0 )
		self.m_staticText_dataValidTime0time_100ps.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dataValidTime0time_100ps, 0, wx.ALL, 5 )

		self.m_textCtrl_dataValidTime0time_100ps = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dataValidTime0time_100ps, 0, wx.ALL, 5 )

		self.m_staticText_dataValidTime0delay_cells = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dataValidTime[0].delay_cells:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_dataValidTime0delay_cells.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dataValidTime0delay_cells, 0, wx.ALL, 5 )

		self.m_textCtrl_dataValidTime0delay_cells = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dataValidTime0delay_cells, 0, wx.ALL, 5 )

		self.m_staticText_dataValidTime1time_100ps = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dataValidTime[1].time_100ps:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_dataValidTime1time_100ps.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dataValidTime1time_100ps, 0, wx.ALL, 5 )

		self.m_textCtrl_dataValidTime1time_100ps = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dataValidTime1time_100ps, 0, wx.ALL, 5 )

		self.m_staticText_dataValidTime1delay_cells = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"dataValidTime[1].delay_cells:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_dataValidTime1delay_cells.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_dataValidTime1delay_cells, 0, wx.ALL, 5 )

		self.m_textCtrl_dataValidTime1delay_cells = wx.TextCtrl( self.m_panel_ipCfg1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_ipCfg1.Add( self.m_textCtrl_dataValidTime1delay_cells, 0, wx.ALL, 5 )

		self.m_staticText_busyOffset = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"busyOffset:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_busyOffset.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_busyOffset, 0, wx.ALL, 5 )

		m_choice_busyOffsetChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16", u"17", u"18", u"19", u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27", u"28", u"29", u"30", u"31" ]
		self.m_choice_busyOffset = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_busyOffsetChoices, 0 )
		self.m_choice_busyOffset.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_busyOffset, 0, wx.ALL, 5 )

		self.m_staticText_busyBitPolarity = wx.StaticText( self.m_panel_ipCfg1, wx.ID_ANY, u"busyBitPolarity:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_busyBitPolarity.Wrap( -1 )

		fgSizer_ipCfg1.Add( self.m_staticText_busyBitPolarity, 0, wx.ALL, 5 )

		m_choice_busyBitPolarityChoices = [ u"0 - busy bit is 1", u"1 - busy bit is 0" ]
		self.m_choice_busyBitPolarity = wx.Choice( self.m_panel_ipCfg1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_busyBitPolarityChoices, 0 )
		self.m_choice_busyBitPolarity.SetSelection( 0 )
		fgSizer_ipCfg1.Add( self.m_choice_busyBitPolarity, 0, wx.ALL, 5 )


		self.m_panel_ipCfg1.SetSizer( fgSizer_ipCfg1 )
		self.m_panel_ipCfg1.Layout()
		fgSizer_ipCfg1.Fit( self.m_panel_ipCfg1 )
		self.m_notebook_ipCfg1.AddPage( self.m_panel_ipCfg1, u"flexspi ip cfg1", False )

		wSizer_win.Add( self.m_notebook_ipCfg1, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_lutSeq = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_lutSeq = wx.Panel( self.m_notebook_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer_lutSeq = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer_lutSeq.SetFlexibleDirection( wx.BOTH )
		fgSizer_lutSeq.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText_deviceModeSeqNum = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"deviceModeSeq.Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceModeSeqNum.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_deviceModeSeqNum, 0, wx.ALL, 5 )

		m_choice_deviceModeSeqNumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_deviceModeSeqNum = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_deviceModeSeqNumChoices, 0 )
		self.m_choice_deviceModeSeqNum.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_deviceModeSeqNum, 0, wx.ALL, 5 )

		self.m_staticText_deviceModeSeqId = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"deviceModeSeq.Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceModeSeqId.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_deviceModeSeqId, 0, wx.ALL, 5 )

		m_choice_deviceModeSeqIdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_deviceModeSeqId = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_deviceModeSeqIdChoices, 0 )
		self.m_choice_deviceModeSeqId.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_deviceModeSeqId, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs0Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[0].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs0Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs0Num, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs0NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_configCmdSeqs0Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs0NumChoices, 0 )
		self.m_choice_configCmdSeqs0Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs0Num, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs0Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[0].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs0Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs0Id, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs0IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_configCmdSeqs0Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs0IdChoices, 0 )
		self.m_choice_configCmdSeqs0Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs0Id, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs1Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[1].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs1Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs1Num, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs1NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_configCmdSeqs1Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs1NumChoices, 0 )
		self.m_choice_configCmdSeqs1Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs1Num, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs1Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[1].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs1Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs1Id, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs1IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_configCmdSeqs1Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs1IdChoices, 0 )
		self.m_choice_configCmdSeqs1Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs1Id, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs2Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[2].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs2Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs2Num, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs2NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_configCmdSeqs2Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs2NumChoices, 0 )
		self.m_choice_configCmdSeqs2Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs2Num, 0, wx.ALL, 5 )

		self.m_staticText_configCmdSeqs2Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"configCmdSeqs[2].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_configCmdSeqs2Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_configCmdSeqs2Id, 0, wx.ALL, 5 )

		m_choice_configCmdSeqs2IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_configCmdSeqs2Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_configCmdSeqs2IdChoices, 0 )
		self.m_choice_configCmdSeqs2Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_configCmdSeqs2Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq0Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[0].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq0Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq0Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq0NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq0Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq0NumChoices, 0 )
		self.m_choice_lutCustomSeq0Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq0Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq0Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[0].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq0Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq0Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq0IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq0Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq0IdChoices, 0 )
		self.m_choice_lutCustomSeq0Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq0Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq1Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[1].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq1Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq1Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq1NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq1Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq1NumChoices, 0 )
		self.m_choice_lutCustomSeq1Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq1Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq1Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[1].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq1Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq1Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq1IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq1Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq1IdChoices, 0 )
		self.m_choice_lutCustomSeq1Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq1Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq2Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[2].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq2Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq2Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq2NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq2Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq2NumChoices, 0 )
		self.m_choice_lutCustomSeq2Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq2Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq2Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[2].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq2Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq2Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq2IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq2Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq2IdChoices, 0 )
		self.m_choice_lutCustomSeq2Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq2Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq3Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[3].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq3Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq3Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq3NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq3Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq3NumChoices, 0 )
		self.m_choice_lutCustomSeq3Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq3Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq3Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[3].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq3Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq3Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq3IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq3Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq3IdChoices, 0 )
		self.m_choice_lutCustomSeq3Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq3Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq4Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[4].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq4Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq4Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq4NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq4Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq4NumChoices, 0 )
		self.m_choice_lutCustomSeq4Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq4Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq4Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[4].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq4Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq4Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq4IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq4Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq4IdChoices, 0 )
		self.m_choice_lutCustomSeq4Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq4Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq5Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[5].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq5Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq5Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq5NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq5Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq5NumChoices, 0 )
		self.m_choice_lutCustomSeq5Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq5Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq5Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[5].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq5Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq5Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq5IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq5Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq5IdChoices, 0 )
		self.m_choice_lutCustomSeq5Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq5Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq6Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[6].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq6Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq6Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq6NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq6Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq6NumChoices, 0 )
		self.m_choice_lutCustomSeq6Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq6Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq6Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[6].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq6Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq6Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq6IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq6Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq6IdChoices, 0 )
		self.m_choice_lutCustomSeq6Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq6Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq7Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[7].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq7Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq7Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq7NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq7Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq7NumChoices, 0 )
		self.m_choice_lutCustomSeq7Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq7Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq7Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[7].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq7Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq7Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq7IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq7Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq7IdChoices, 0 )
		self.m_choice_lutCustomSeq7Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq7Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq8Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[8].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq8Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq8Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq8NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq8Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq8NumChoices, 0 )
		self.m_choice_lutCustomSeq8Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq8Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq8Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[8].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq8Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq8Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq8IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq8Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq8IdChoices, 0 )
		self.m_choice_lutCustomSeq8Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq8Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq9Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[9].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq9Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq9Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq9NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq9Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq9NumChoices, 0 )
		self.m_choice_lutCustomSeq9Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq9Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq9Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[9].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq9Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq9Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq9IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq9Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq9IdChoices, 0 )
		self.m_choice_lutCustomSeq9Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq9Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq10Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[10].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq10Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq10Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq10NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq10Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq10NumChoices, 0 )
		self.m_choice_lutCustomSeq10Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq10Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq10Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[10].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq10Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq10Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq10IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq10Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq10IdChoices, 0 )
		self.m_choice_lutCustomSeq10Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq10Id, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq11Num = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[11].Num:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq11Num.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq11Num, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq11NumChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15", u"16" ]
		self.m_choice_lutCustomSeq11Num = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq11NumChoices, 0 )
		self.m_choice_lutCustomSeq11Num.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq11Num, 0, wx.ALL, 5 )

		self.m_staticText_lutCustomSeq11Id = wx.StaticText( self.m_panel_lutSeq, wx.ID_ANY, u"lutCustomSeq[11].Id:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutCustomSeq11Id.Wrap( -1 )

		fgSizer_lutSeq.Add( self.m_staticText_lutCustomSeq11Id, 0, wx.ALL, 5 )

		m_choice_lutCustomSeq11IdChoices = [ u"0", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"10", u"11", u"12", u"13", u"14", u"15" ]
		self.m_choice_lutCustomSeq11Id = wx.Choice( self.m_panel_lutSeq, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutCustomSeq11IdChoices, 0 )
		self.m_choice_lutCustomSeq11Id.SetSelection( 0 )
		fgSizer_lutSeq.Add( self.m_choice_lutCustomSeq11Id, 0, wx.ALL, 5 )

		self.m_button_lookupTable = wx.Button( self.m_panel_lutSeq, wx.ID_ANY, u"lookupTable", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		fgSizer_lutSeq.Add( self.m_button_lookupTable, 0, wx.ALL, 5 )


		self.m_panel_lutSeq.SetSizer( fgSizer_lutSeq )
		self.m_panel_lutSeq.Layout()
		fgSizer_lutSeq.Fit( self.m_panel_lutSeq )
		self.m_notebook_lutSeq.AddPage( self.m_panel_lutSeq, u"flexspi lut seq", False )

		wSizer_win.Add( self.m_notebook_lutSeq, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_memInfo = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_memInfo = wx.Panel( self.m_notebook_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer_memInfo = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer_memInfo.SetFlexibleDirection( wx.BOTH )
		fgSizer_memInfo.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticTex_sflashA1Size = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"sflashA1Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTex_sflashA1Size.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticTex_sflashA1Size, 0, wx.ALL, 5 )

		self.m_textCtrl_sflashA1Size = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_sflashA1Size, 0, wx.ALL, 5 )

		self.m_staticText_sflashA2Size = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"sflashA2Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sflashA2Size.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_sflashA2Size, 0, wx.ALL, 5 )

		self.m_textCtrl_sflashA2Size = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_sflashA2Size, 0, wx.ALL, 5 )

		self.m_staticText_sflashB1Size = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"sflashB1Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sflashB1Size.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_sflashB1Size, 0, wx.ALL, 5 )

		self.m_textCtrl_sflashB1Size = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_sflashB1Size, 0, wx.ALL, 5 )

		self.m_staticText_sflashB2Size = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"sflashB2Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sflashB2Size.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_sflashB2Size, 0, wx.ALL, 5 )

		self.m_textCtrl_sflashB2Size = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_sflashB2Size, 0, wx.ALL, 5 )

		self.m_staticText_pageSize = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"pageSize:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pageSize.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_pageSize, 0, wx.ALL, 5 )

		self.m_textCtrl_pageSize = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_pageSize, 0, wx.ALL, 5 )

		self.m_staticText_sectorSize = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"sectorSize:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_sectorSize.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_sectorSize, 0, wx.ALL, 5 )

		self.m_textCtrl_sectorSize = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_sectorSize, 0, wx.ALL, 5 )

		self.m_staticText_ipcmdSerialClkFreq = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"ipcmdSerialClkFreq:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ipcmdSerialClkFreq.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_ipcmdSerialClkFreq, 0, wx.ALL, 5 )

		m_choice_ipcmdSerialClkFreqChoices = []
		self.m_choice_ipcmdSerialClkFreq = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_ipcmdSerialClkFreqChoices, 0 )
		self.m_choice_ipcmdSerialClkFreq.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_ipcmdSerialClkFreq, 0, wx.ALL, 5 )

		self.m_staticText_isUniformBlockSize = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"isUniformBlockSize:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_isUniformBlockSize.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_isUniformBlockSize, 0, wx.ALL, 5 )

		m_choice_isUniformBlockSizeChoices = [ u"0 - No", u"1 - Yes" ]
		self.m_choice_isUniformBlockSize = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_isUniformBlockSizeChoices, 0 )
		self.m_choice_isUniformBlockSize.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_isUniformBlockSize, 0, wx.ALL, 5 )

		self.m_staticText_isDataOrderSwapped = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"isDataOrderSwapped:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_isDataOrderSwapped.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_isDataOrderSwapped, 0, wx.ALL, 5 )

		m_choice_isDataOrderSwappedChoices = [ u"0 - Not swapped", u"1 - Swapped" ]
		self.m_choice_isDataOrderSwapped = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_isDataOrderSwappedChoices, 0 )
		self.m_choice_isDataOrderSwapped.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_isDataOrderSwapped, 0, wx.ALL, 5 )

		self.m_staticText_serialNorType = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"serialNorType:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_serialNorType.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_serialNorType, 0, wx.ALL, 5 )

		m_choice_serialNorTypeChoices = [ u"0 - ", u"1 - ", u"2 - ", u"3 - " ]
		self.m_choice_serialNorType = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_serialNorTypeChoices, 0 )
		self.m_choice_serialNorType.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_serialNorType, 0, wx.ALL, 5 )

		self.m_staticText_needExitNoCmdMode = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"needExitNoCmdMode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_needExitNoCmdMode.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_needExitNoCmdMode, 0, wx.ALL, 5 )

		m_choice_needExitNoCmdModeChoices = [ u"0 - No", u"1 - Yes" ]
		self.m_choice_needExitNoCmdMode = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_needExitNoCmdModeChoices, 0 )
		self.m_choice_needExitNoCmdMode.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_needExitNoCmdMode, 0, wx.ALL, 5 )

		self.m_staticText_halfClkForNonReadCmd = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"halfClkForNonReadCmd:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_halfClkForNonReadCmd.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_halfClkForNonReadCmd, 0, wx.ALL, 5 )

		m_choice_halfClkForNonReadCmdChoices = [ u"0 - False", u"1 - True" ]
		self.m_choice_halfClkForNonReadCmd = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_halfClkForNonReadCmdChoices, 0 )
		self.m_choice_halfClkForNonReadCmd.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_halfClkForNonReadCmd, 0, wx.ALL, 5 )

		self.m_staticText_needRestoreNoCmdMode = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"needRestoreNoCmdMode:", wx.DefaultPosition, wx.Size( 145,-1 ), 0 )
		self.m_staticText_needRestoreNoCmdMode.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_needRestoreNoCmdMode, 0, wx.ALL, 5 )

		m_choice_needRestoreNoCmdModeChoices = [ u"0 - No", u"1 - Yes" ]
		self.m_choice_needRestoreNoCmdMode = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_needRestoreNoCmdModeChoices, 0 )
		self.m_choice_needRestoreNoCmdMode.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_needRestoreNoCmdMode, 0, wx.ALL, 5 )

		self.m_staticText_blockSize = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"blockSize:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_blockSize.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_blockSize, 0, wx.ALL, 5 )

		self.m_textCtrl_blockSize = wx.TextCtrl( self.m_panel_memInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_memInfo.Add( self.m_textCtrl_blockSize, 0, wx.ALL, 5 )

		self.m_staticText_isNonBlockingMode = wx.StaticText( self.m_panel_memInfo, wx.ID_ANY, u"isNonBlockingMode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_isNonBlockingMode.Wrap( -1 )

		fgSizer_memInfo.Add( self.m_staticText_isNonBlockingMode, 0, wx.ALL, 5 )

		m_choice_isNonBlockingModeChoices = [ u"0 - No", u"1 - Yes" ]
		self.m_choice_isNonBlockingMode = wx.Choice( self.m_panel_memInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_isNonBlockingModeChoices, 0 )
		self.m_choice_isNonBlockingMode.SetSelection( 0 )
		fgSizer_memInfo.Add( self.m_choice_isNonBlockingMode, 0, wx.ALL, 5 )


		self.m_panel_memInfo.SetSizer( fgSizer_memInfo )
		self.m_panel_memInfo.Layout()
		fgSizer_memInfo.Fit( self.m_panel_memInfo )
		self.m_notebook_memInfo.AddPage( self.m_panel_memInfo, u"flexspi memory info", False )

		wSizer_win.Add( self.m_notebook_memInfo, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText_winNull0.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_winNull0, 0, wx.ALL, 5 )

		self.m_staticText_binFile = wx.StaticText( self, wx.ID_ANY, u"Load FDCB bin file:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_binFile.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_binFile, 0, wx.ALL, 5 )

		self.m_filePicker_binFile = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 600,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_win.Add( self.m_filePicker_binFile, 0, wx.ALL, 5 )

		self.m_staticText_winNull1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 91,-1 ), 0 )
		self.m_staticText_winNull1.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_winNull1, 0, wx.ALL, 5 )

		self.m_button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_win.Add( self.m_button_ok, 0, wx.ALL, 5 )

		self.m_button_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_win.Add( self.m_button_cancel, 0, wx.ALL, 5 )


		self.SetSizer( wSizer_win )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.callbackClose )
		self.m_button_lookupTable.Bind( wx.EVT_BUTTON, self.callbackSetLookupTable )
		self.m_filePicker_binFile.Bind( wx.EVT_FILEPICKER_CHANGED, self.callbackSelectFdcbFile )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSetLookupTable( self, event ):
		event.Skip()

	def callbackSelectFdcbFile( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


