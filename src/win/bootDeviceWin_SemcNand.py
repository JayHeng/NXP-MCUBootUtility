# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Aug  8 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class bootDeviceWin_SemcNand
###########################################################################

class bootDeviceWin_SemcNand ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 802,433 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_nandOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_nandOpt = wx.Panel( self.m_notebook_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_nandOpt = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_onfiVersion = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"ONFI Version:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_onfiVersion.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_onfiVersion, 0, wx.ALL, 5 )

		m_choice_onfiVersionChoices = [ u"ONFI 1.x" ]
		self.m_choice_onfiVersion = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_onfiVersionChoices, 0 )
		self.m_choice_onfiVersion.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_onfiVersion, 0, wx.ALL, 5 )

		self.m_staticText_onfiTimingMode = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"ONFI Timing Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_onfiTimingMode.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_onfiTimingMode, 0, wx.ALL, 5 )

		m_choice_onfiTimingModeChoices = [ u"Mode0 - 10MHz", u"Mode1 - 20MHz", u"Mode2 - 28MHz", u"Mode3 - 33MHz", u"Mode4 - 40MHz", u"Mode5 - 50MHz" ]
		self.m_choice_onfiTimingMode = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_onfiTimingModeChoices, 0 )
		self.m_choice_onfiTimingMode.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_onfiTimingMode, 0, wx.ALL, 5 )

		self.m_staticText_edoMode = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"EDO Mode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_edoMode.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_edoMode, 0, wx.ALL, 5 )

		m_choice_edoModeChoices = [ u"Disabled", u"Enabled" ]
		self.m_choice_edoMode = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_edoModeChoices, 0 )
		self.m_choice_edoMode.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_edoMode, 0, wx.ALL, 5 )

		self.m_staticText_ioPortSize = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"I/O Port Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_ioPortSize.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_ioPortSize, 0, wx.ALL, 5 )

		m_choice_ioPortSizeChoices = [ u"x8 bits", u"x16 bits" ]
		self.m_choice_ioPortSize = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_ioPortSizeChoices, 0 )
		self.m_choice_ioPortSize.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_ioPortSize, 0, wx.ALL, 5 )

		self.m_staticText_pcsPort = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"PCS Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pcsPort.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_pcsPort, 0, wx.ALL, 5 )

		m_choice_pcsPortChoices = [ u"CSX0" ]
		self.m_choice_pcsPort = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_pcsPortChoices, 0 )
		self.m_choice_pcsPort.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_pcsPort, 0, wx.ALL, 5 )

		self.m_staticText_eccType = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"ECC Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_eccType.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_eccType, 0, wx.ALL, 5 )

		m_choice_eccTypeChoices = [ u"SW - 1bit ECC", u"HW" ]
		self.m_choice_eccType = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_eccTypeChoices, 0 )
		self.m_choice_eccType.SetSelection( 1 )
		gSizer_nandOpt.Add( self.m_choice_eccType, 0, wx.ALL, 5 )

		self.m_staticText_eccStatus = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Initial ECC status:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_eccStatus.Wrap( -1 )

		gSizer_nandOpt.Add( self.m_staticText_eccStatus, 0, wx.ALL, 5 )

		m_choice_eccStatusChoices = [ u"Enabled", u"Disabled" ]
		self.m_choice_eccStatus = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_eccStatusChoices, 0 )
		self.m_choice_eccStatus.SetSelection( 0 )
		gSizer_nandOpt.Add( self.m_choice_eccStatus, 0, wx.ALL, 5 )


		self.m_panel_nandOpt.SetSizer( gSizer_nandOpt )
		self.m_panel_nandOpt.Layout()
		gSizer_nandOpt.Fit( self.m_panel_nandOpt )
		self.m_notebook_nandOpt.AddPage( self.m_panel_nandOpt, u"Nand Option", False )

		wSizer_win.Add( self.m_notebook_nandOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_fcbOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_fcbOpt = wx.Panel( self.m_notebook_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_fcbOpt = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_searchCount = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, u"Search Count:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_searchCount.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_searchCount, 0, wx.ALL, 5 )

		m_choice_searchCountChoices = [ u"1", u"2" ]
		self.m_choice_searchCount = wx.Choice( self.m_panel_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_searchCountChoices, 0 )
		self.m_choice_searchCount.SetSelection( 0 )
		gSizer_fcbOpt.Add( self.m_choice_searchCount, 0, wx.ALL, 5 )

		self.m_staticText_searchStride = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, u"Search Stride:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_searchStride.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_searchStride, 0, wx.ALL, 5 )

		self.m_textCtrl_searchStride = wx.TextCtrl( self.m_panel_fcbOpt, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 108,-1 ), 0 )
		gSizer_fcbOpt.Add( self.m_textCtrl_searchStride, 0, wx.ALL, 5 )

		self.m_staticText_imageCopies = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, u"Image Copies", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_imageCopies.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_imageCopies, 0, wx.ALL, 5 )

		m_choice_imageCopiesChoices = [ u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8" ]
		self.m_choice_imageCopies = wx.Choice( self.m_panel_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_imageCopiesChoices, 0 )
		self.m_choice_imageCopies.SetSelection( 0 )
		gSizer_fcbOpt.Add( self.m_choice_imageCopies, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull0 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull0.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull0, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull1 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull1.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull1, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull2 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull2.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull2, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull3 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull3.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull3, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull4 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull4.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull4, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull5 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull5.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull5, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull6 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull6.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull6, 0, wx.ALL, 5 )

		self.m_staticText_fcbOptNull7 = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_fcbOptNull7.Wrap( -1 )

		gSizer_fcbOpt.Add( self.m_staticText_fcbOptNull7, 0, wx.ALL, 5 )


		self.m_panel_fcbOpt.SetSizer( gSizer_fcbOpt )
		self.m_panel_fcbOpt.Layout()
		gSizer_fcbOpt.Fit( self.m_panel_fcbOpt )
		self.m_notebook_fcbOpt.AddPage( self.m_panel_fcbOpt, u"FCB Option", False )

		wSizer_win.Add( self.m_notebook_fcbOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_imageInfo = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_imageInfo = wx.Panel( self.m_notebook_imageInfo, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_imageInfo = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_blockIndex = wx.StaticText( self.m_panel_imageInfo, wx.ID_ANY, u"Block Index", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_blockIndex.Wrap( -1 )

		gSizer_imageInfo.Add( self.m_staticText_blockIndex, 0, wx.ALL, 5 )

		self.m_staticText_blockCount = wx.StaticText( self.m_panel_imageInfo, wx.ID_ANY, u"Block Count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_blockCount.Wrap( -1 )

		gSizer_imageInfo.Add( self.m_staticText_blockCount, 0, wx.ALL, 5 )

		self.m_textCtrl_image0Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image0Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image0Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image0Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image1Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image1Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image1Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image1Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image2Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image2Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image2Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image2Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image3Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image3Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image3Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image3Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image4Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image4Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image4Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image4Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image5Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image5Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image5Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image5Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image6Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image6Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image6Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image6Cnt, 0, wx.ALL, 5 )

		self.m_textCtrl_image7Idx = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image7Idx, 0, wx.ALL, 5 )

		self.m_textCtrl_image7Cnt = wx.TextCtrl( self.m_panel_imageInfo, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer_imageInfo.Add( self.m_textCtrl_image7Cnt, 0, wx.ALL, 5 )


		self.m_panel_imageInfo.SetSizer( gSizer_imageInfo )
		self.m_panel_imageInfo.Layout()
		gSizer_imageInfo.Fit( self.m_panel_imageInfo )
		self.m_notebook_imageInfo.AddPage( self.m_panel_imageInfo, u"Image Info", False )

		wSizer_win.Add( self.m_notebook_imageInfo, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 518,-1 ), 0 )
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
		self.m_choice_imageCopies.Bind( wx.EVT_CHOICE, self.callbackChangeImageCopies )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackChangeImageCopies( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


