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
## Class bootDeviceWin_DCD
###########################################################################

class bootDeviceWin_DCD ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 636,365 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_dcdOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 290,260 ), 0 )
		self.m_panel_dcdOpt = wx.Panel( self.m_notebook_dcdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 270,-1 ), wx.TAB_TRAVERSAL )
		wSizer_dcdOpt = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_dcdSource = wx.StaticText( self.m_panel_dcdOpt, wx.ID_ANY, u"DCD Source:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_dcdSource.Wrap( -1 )

		wSizer_dcdOpt.Add( self.m_staticText_dcdSource, 0, wx.ALL, 5 )

		m_choice_dcdSourceChoices = [ u"Disable DCD", u"Use DCD bin file", u"Use DCD cfg file", u"Use DCD descriptor" ]
		self.m_choice_dcdSource = wx.Choice( self.m_panel_dcdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 185,-1 ), m_choice_dcdSourceChoices, 0 )
		self.m_choice_dcdSource.SetSelection( 0 )
		wSizer_dcdOpt.Add( self.m_choice_dcdSource, 0, wx.ALL, 5 )

		self.m_staticText_dcdBinFile = wx.StaticText( self.m_panel_dcdOpt, wx.ID_ANY, u"DCD bin file:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_dcdBinFile.Wrap( -1 )

		wSizer_dcdOpt.Add( self.m_staticText_dcdBinFile, 0, wx.ALL, 5 )

		self.m_filePicker_dcdBinFile = wx.FilePickerCtrl( self.m_panel_dcdOpt, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 185,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_dcdOpt.Add( self.m_filePicker_dcdBinFile, 0, wx.ALL, 5 )

		self.m_staticText_dcdCfgFile = wx.StaticText( self.m_panel_dcdOpt, wx.ID_ANY, u"DCD cfg file:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_dcdCfgFile.Wrap( -1 )

		wSizer_dcdOpt.Add( self.m_staticText_dcdCfgFile, 0, wx.ALL, 5 )

		self.m_filePicker_dcdCfgFile = wx.FilePickerCtrl( self.m_panel_dcdOpt, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 185,-1 ), wx.FLP_DEFAULT_STYLE )
		wSizer_dcdOpt.Add( self.m_filePicker_dcdCfgFile, 0, wx.ALL, 5 )

		self.m_staticText_dcdPurpose = wx.StaticText( self.m_panel_dcdOpt, wx.ID_ANY, u"DCD Purpose:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_dcdPurpose.Wrap( -1 )

		wSizer_dcdOpt.Add( self.m_staticText_dcdPurpose, 0, wx.ALL, 5 )

		m_choice_dcdPurposeChoices = [ u"Misc", u"SDRAM" ]
		self.m_choice_dcdPurpose = wx.Choice( self.m_panel_dcdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 185,-1 ), m_choice_dcdPurposeChoices, 0 )
		self.m_choice_dcdPurpose.SetSelection( 0 )
		wSizer_dcdOpt.Add( self.m_choice_dcdPurpose, 0, wx.ALL, 5 )

		self.m_staticText_sdramBase = wx.StaticText( self.m_panel_dcdOpt, wx.ID_ANY, u"SDRAM Base:", wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		self.m_staticText_sdramBase.Wrap( -1 )

		wSizer_dcdOpt.Add( self.m_staticText_sdramBase, 0, wx.ALL, 5 )

		self.m_textCtrl_sdramBase = wx.TextCtrl( self.m_panel_dcdOpt, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 185,-1 ), 0 )
		wSizer_dcdOpt.Add( self.m_textCtrl_sdramBase, 0, wx.ALL, 5 )


		self.m_panel_dcdOpt.SetSizer( wSizer_dcdOpt )
		self.m_panel_dcdOpt.Layout()
		self.m_notebook_dcdOpt.AddPage( self.m_panel_dcdOpt, u"DCD Option:", False )

		wSizer_win.Add( self.m_notebook_dcdOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_notebook_dcdDesc = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 290,260 ), 0 )
		self.m_panel_dcdDesc = wx.Panel( self.m_notebook_dcdDesc, wx.ID_ANY, wx.DefaultPosition, wx.Size( 270,-1 ), wx.TAB_TRAVERSAL )
		wSizer_dcdDesc = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_staticText_dcdModel = wx.StaticText( self.m_panel_dcdDesc, wx.ID_ANY, u"Device Model:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText_dcdModel.Wrap( -1 )

		wSizer_dcdDesc.Add( self.m_staticText_dcdModel, 0, wx.ALL, 5 )

		m_choice_dcdModelChoices = [ u"No", u"Micron_MT48LC16M16A2", u"ISSI_IS42S16160J" ]
		self.m_choice_dcdModel = wx.Choice( self.m_panel_dcdDesc, wx.ID_ANY, wx.DefaultPosition, wx.Size( 180,-1 ), m_choice_dcdModelChoices, 0 )
		self.m_choice_dcdModel.SetSelection( 0 )
		wSizer_dcdDesc.Add( self.m_choice_dcdModel, 0, wx.ALL, 5 )

		self.m_textCtrl_dcdDesc = wx.TextCtrl( self.m_panel_dcdDesc, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 270,190 ), wx.TE_MULTILINE )
		wSizer_dcdDesc.Add( self.m_textCtrl_dcdDesc, 0, wx.ALL, 5 )


		self.m_panel_dcdDesc.SetSizer( wSizer_dcdDesc )
		self.m_panel_dcdDesc.Layout()
		self.m_notebook_dcdDesc.AddPage( self.m_panel_dcdDesc, u"DCD Descriptor:", False )

		wSizer_win.Add( self.m_notebook_dcdDesc, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 330,-1 ), 0 )
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
		self.m_choice_dcdSource.Bind( wx.EVT_CHOICE, self.callbackSetDcdSource )
		self.m_choice_dcdPurpose.Bind( wx.EVT_CHOICE, self.callbackSetDcdPurpose )
		self.m_choice_dcdModel.Bind( wx.EVT_CHOICE, self.callbackSetDeviceModel )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSetDcdSource( self, event ):
		event.Skip()

	def callbackSetDcdPurpose( self, event ):
		event.Skip()

	def callbackSetDeviceModel( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


