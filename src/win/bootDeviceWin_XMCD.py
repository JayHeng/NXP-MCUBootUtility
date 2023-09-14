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
## Class bootDeviceWin_XMCD
###########################################################################

class bootDeviceWin_XMCD ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 987,335 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_xmcdSource = wx.StaticText( self, wx.ID_ANY, u"XMCD Source:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText_xmcdSource.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_xmcdSource, 0, wx.ALL, 5 )

		m_choice_xmcdSourceChoices = [ u"Disable XMCD", u"Use XMCD option", u"Use XMCD bin file" ]
		self.m_choice_xmcdSource = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,-1 ), m_choice_xmcdSourceChoices, 0 )
		self.m_choice_xmcdSource.SetSelection( 0 )
		wSizer_win.Add( self.m_choice_xmcdSource, 0, wx.ALL, 5 )

		self.m_staticText_memoryInterface = wx.StaticText( self, wx.ID_ANY, u"Memory Interface:", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText_memoryInterface.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_memoryInterface, 0, wx.ALL, 5 )

		m_choice_memoryInterfaceChoices = [ u"FlexSPI", u"SEMC" ]
		self.m_choice_memoryInterface = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice_memoryInterfaceChoices, 0 )
		self.m_choice_memoryInterface.SetSelection( 0 )
		wSizer_win.Add( self.m_choice_memoryInterface, 0, wx.ALL, 5 )

		self.m_staticText_interfaceInstance = wx.StaticText( self, wx.ID_ANY, u"Interface Instance:", wx.DefaultPosition, wx.Size( 110,-1 ), 0 )
		self.m_staticText_interfaceInstance.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_interfaceInstance, 0, wx.ALL, 5 )

		m_choice_interfaceInstanceChoices = [ u"1st", u"2nd" ]
		self.m_choice_interfaceInstance = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 75,-1 ), m_choice_interfaceInstanceChoices, 0 )
		self.m_choice_interfaceInstance.SetSelection( 0 )
		wSizer_win.Add( self.m_choice_interfaceInstance, 0, wx.ALL, 5 )

		self.m_staticText_cfgBlockType = wx.StaticText( self, wx.ID_ANY, u"Config Block Type:", wx.DefaultPosition, wx.Size( 110,-1 ), 0 )
		self.m_staticText_cfgBlockType.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_cfgBlockType, 0, wx.ALL, 5 )

		m_choice_cfgBlockTypeChoices = [ u"Simplified Option", u"Full Block" ]
		self.m_choice_cfgBlockType = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 130,-1 ), m_choice_cfgBlockTypeChoices, 0 )
		self.m_choice_cfgBlockType.SetSelection( 0 )
		wSizer_win.Add( self.m_choice_cfgBlockType, 0, wx.ALL, 5 )

		self.m_notebook_flexspiRamOpt0 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_flexspiRamOpt0 = wx.Panel( self.m_notebook_flexspiRamOpt0, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_flexspiRamOpt0 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_deviceType = wx.StaticText( self.m_panel_flexspiRamOpt0, wx.ID_ANY, u"Device Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceType.Wrap( -1 )

		gSizer_flexspiRamOpt0.Add( self.m_staticText_deviceType, 0, wx.ALL, 5 )

		m_choice_deviceTypeChoices = [ u"HyperRAM", u"APMemory" ]
		self.m_choice_deviceType = wx.Choice( self.m_panel_flexspiRamOpt0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_deviceTypeChoices, 0 )
		self.m_choice_deviceType.SetSelection( 0 )
		gSizer_flexspiRamOpt0.Add( self.m_choice_deviceType, 0, wx.ALL, 5 )

		self.m_staticText_miscMode = wx.StaticText( self.m_panel_flexspiRamOpt0, wx.ID_ANY, u"Misc Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_miscMode.Wrap( -1 )

		gSizer_flexspiRamOpt0.Add( self.m_staticText_miscMode, 0, wx.ALL, 5 )

		m_choice_miscModeChoices = [ u"1.8V", u"3.3V" ]
		self.m_choice_miscMode = wx.Choice( self.m_panel_flexspiRamOpt0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_miscModeChoices, 0 )
		self.m_choice_miscMode.SetSelection( 0 )
		gSizer_flexspiRamOpt0.Add( self.m_choice_miscMode, 0, wx.ALL, 5 )

		self.m_staticText_maxFrequency = wx.StaticText( self.m_panel_flexspiRamOpt0, wx.ID_ANY, u"Max Frequency:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_maxFrequency.Wrap( -1 )

		gSizer_flexspiRamOpt0.Add( self.m_staticText_maxFrequency, 0, wx.ALL, 5 )

		m_choice_maxFrequencyChoices = [ u"30MHz", u"50MHz", u"60MHz", u"80MHz", u"100MHz", u"120MHz", u"133MHz", u"166MHz", u"200MHz" ]
		self.m_choice_maxFrequency = wx.Choice( self.m_panel_flexspiRamOpt0, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_maxFrequencyChoices, 0 )
		self.m_choice_maxFrequency.SetSelection( 0 )
		gSizer_flexspiRamOpt0.Add( self.m_choice_maxFrequency, 0, wx.ALL, 5 )

		self.m_staticText_deviceSizeInMB = wx.StaticText( self.m_panel_flexspiRamOpt0, wx.ID_ANY, u"Device Size (MB):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_deviceSizeInMB.Wrap( -1 )

		gSizer_flexspiRamOpt0.Add( self.m_staticText_deviceSizeInMB, 0, wx.ALL, 5 )

		self.m_textCtrl_deviceSizeInMB = wx.TextCtrl( self.m_panel_flexspiRamOpt0, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		gSizer_flexspiRamOpt0.Add( self.m_textCtrl_deviceSizeInMB, 0, wx.ALL, 5 )


		self.m_panel_flexspiRamOpt0.SetSizer( gSizer_flexspiRamOpt0 )
		self.m_panel_flexspiRamOpt0.Layout()
		gSizer_flexspiRamOpt0.Fit( self.m_panel_flexspiRamOpt0 )
		self.m_notebook_flexspiRamOpt0.AddPage( self.m_panel_flexspiRamOpt0, u"FlexSPI RAM Option0", False )

		wSizer_win.Add( self.m_notebook_flexspiRamOpt0, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_flexspiRamOpt1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_flexspiRamOpt1 = wx.Panel( self.m_notebook_flexspiRamOpt1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_flexspiRamOpt1 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_ramConnection = wx.StaticText( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"RAM Connection:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_ramConnection.Wrap( -1 )

		gSizer_flexspiRamOpt1.Add( self.m_staticText_ramConnection, 0, wx.ALL, 5 )

		m_choice_ramConnectionChoices = [ u"Port A", u"Port B" ]
		self.m_choice_ramConnection = wx.Choice( self.m_panel_flexspiRamOpt1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_ramConnectionChoices, 0 )
		self.m_choice_ramConnection.SetSelection( 0 )
		gSizer_flexspiRamOpt1.Add( self.m_choice_ramConnection, 0, wx.ALL, 5 )

		self.m_staticText_dqsPinmuxGroup = wx.StaticText( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"DQS Pinmux Group:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_dqsPinmuxGroup.Wrap( -1 )

		gSizer_flexspiRamOpt1.Add( self.m_staticText_dqsPinmuxGroup, 0, wx.ALL, 5 )

		m_choice_dqsPinmuxGroupChoices = [ u"Default", u"Secondary" ]
		self.m_choice_dqsPinmuxGroup = wx.Choice( self.m_panel_flexspiRamOpt1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_dqsPinmuxGroupChoices, 0 )
		self.m_choice_dqsPinmuxGroup.SetSelection( 0 )
		gSizer_flexspiRamOpt1.Add( self.m_choice_dqsPinmuxGroup, 0, wx.ALL, 5 )

		self.m_staticText_dataPinmuxGroup = wx.StaticText( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"Data Pinmux Group:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_dataPinmuxGroup.Wrap( -1 )

		gSizer_flexspiRamOpt1.Add( self.m_staticText_dataPinmuxGroup, 0, wx.ALL, 5 )

		m_choice_dataPinmuxGroupChoices = [ u"Primary", u"Secondary" ]
		self.m_choice_dataPinmuxGroup = wx.Choice( self.m_panel_flexspiRamOpt1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_dataPinmuxGroupChoices, 0 )
		self.m_choice_dataPinmuxGroup.SetSelection( 0 )
		gSizer_flexspiRamOpt1.Add( self.m_choice_dataPinmuxGroup, 0, wx.ALL, 5 )

		self.m_staticText_writeDummyCycles = wx.StaticText( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"Write Dummy Cycles:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_writeDummyCycles.Wrap( -1 )

		gSizer_flexspiRamOpt1.Add( self.m_staticText_writeDummyCycles, 0, wx.ALL, 5 )

		self.m_textCtrl_writeDummyCycles = wx.TextCtrl( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		gSizer_flexspiRamOpt1.Add( self.m_textCtrl_writeDummyCycles, 0, wx.ALL, 5 )

		self.m_staticText_readDummyCycles = wx.StaticText( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"Read Dummy Cycles:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_readDummyCycles.Wrap( -1 )

		gSizer_flexspiRamOpt1.Add( self.m_staticText_readDummyCycles, 0, wx.ALL, 5 )

		self.m_textCtrl_readDummyCycles = wx.TextCtrl( self.m_panel_flexspiRamOpt1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		gSizer_flexspiRamOpt1.Add( self.m_textCtrl_readDummyCycles, 0, wx.ALL, 5 )


		self.m_panel_flexspiRamOpt1.SetSizer( gSizer_flexspiRamOpt1 )
		self.m_panel_flexspiRamOpt1.Layout()
		gSizer_flexspiRamOpt1.Fit( self.m_panel_flexspiRamOpt1 )
		self.m_notebook_flexspiRamOpt1.AddPage( self.m_panel_flexspiRamOpt1, u"FlexSPI RAM Option1", False )

		wSizer_win.Add( self.m_notebook_flexspiRamOpt1, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_semcSdramOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_semcSdramOpt = wx.Panel( self.m_notebook_semcSdramOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_dualImageOpt = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_clkFreq = wx.StaticText( self.m_panel_semcSdramOpt, wx.ID_ANY, u"Clk Freq (MHz):", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_clkFreq.Wrap( -1 )

		gSizer_dualImageOpt.Add( self.m_staticText_clkFreq, 0, wx.ALL, 5 )

		self.m_textCtrl_clkFreq = wx.TextCtrl( self.m_panel_semcSdramOpt, wx.ID_ANY, u"166", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		gSizer_dualImageOpt.Add( self.m_textCtrl_clkFreq, 0, wx.ALL, 5 )

		self.m_staticText_deviceSizeInKB = wx.StaticText( self.m_panel_semcSdramOpt, wx.ID_ANY, u"Device Size (KB):", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_deviceSizeInKB.Wrap( -1 )

		gSizer_dualImageOpt.Add( self.m_staticText_deviceSizeInKB, 0, wx.ALL, 5 )

		self.m_textCtrl_deviceSizeInKB = wx.TextCtrl( self.m_panel_semcSdramOpt, wx.ID_ANY, u"65536", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		gSizer_dualImageOpt.Add( self.m_textCtrl_deviceSizeInKB, 0, wx.ALL, 5 )

		self.m_staticText_portSize = wx.StaticText( self.m_panel_semcSdramOpt, wx.ID_ANY, u"Port Size:", wx.DefaultPosition, wx.Size( 140,-1 ), 0 )
		self.m_staticText_portSize.Wrap( -1 )

		gSizer_dualImageOpt.Add( self.m_staticText_portSize, 0, wx.ALL, 5 )

		m_choice_portSizeChoices = [ u"8-bit", u"16-bit", u"32-bit" ]
		self.m_choice_portSize = wx.Choice( self.m_panel_semcSdramOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_portSizeChoices, 0 )
		self.m_choice_portSize.SetSelection( 2 )
		gSizer_dualImageOpt.Add( self.m_choice_portSize, 0, wx.ALL, 5 )


		self.m_panel_semcSdramOpt.SetSizer( gSizer_dualImageOpt )
		self.m_panel_semcSdramOpt.Layout()
		gSizer_dualImageOpt.Fit( self.m_panel_semcSdramOpt )
		self.m_notebook_semcSdramOpt.AddPage( self.m_panel_semcSdramOpt, u"SEMC SDRAM Option", False )

		wSizer_win.Add( self.m_notebook_semcSdramOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_xmcdBinFile = wx.StaticText( self, wx.ID_ANY, u"XMCD bin file:", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText_xmcdBinFile.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_xmcdBinFile, 0, wx.ALL, 5 )

		self.m_filePicker_xmcdBinFile = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 520,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_win.Add( self.m_filePicker_xmcdBinFile, 0, wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 35,-1 ), 0 )
		self.m_staticText_winNull0.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_winNull0, 0, wx.ALL, 5 )

		self.m_button_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_win.Add( self.m_button_ok, 0, wx.ALL, 5 )

		self.m_button_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		wSizer_win.Add( self.m_button_cancel, 0, wx.ALL, 5 )


		self.SetSizer( wSizer_win )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.callbackClose )
		self.m_choice_xmcdSource.Bind( wx.EVT_CHOICE, self.callbackSetXmcdSource )
		self.m_choice_memoryInterface.Bind( wx.EVT_CHOICE, self.callbackSetMemoryInterface )
		self.m_choice_cfgBlockType.Bind( wx.EVT_CHOICE, self.callbackSetCfgBlockType )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSetXmcdSource( self, event ):
		event.Skip()

	def callbackSetMemoryInterface( self, event ):
		event.Skip()

	def callbackSetCfgBlockType( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


