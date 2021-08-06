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
## Class advSettingsWin_Cert
###########################################################################

class advSettingsWin_Cert ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 403,363 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_certOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_certOpt = wx.Panel( self.m_notebook_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_certOpt = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_cstVersion = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"CST Version:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_cstVersion.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_cstVersion, 0, wx.ALL, 5 )

		m_choice_cstVersionChoices = [ u"2.3.3", u"3.0.1", u"3.1.0" ]
		self.m_choice_cstVersion = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_cstVersionChoices, 0 )
		self.m_choice_cstVersion.SetSelection( 1 )
		gSizer_certOpt.Add( self.m_choice_cstVersion, 0, wx.ALL, 5 )

		self.m_staticText_useExistingCaKey = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"Use Existing CA Key:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_useExistingCaKey.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_useExistingCaKey, 0, wx.ALL, 5 )

		m_choice_useExistingCaKeyChoices = [ u"No" ]
		self.m_choice_useExistingCaKey = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_useExistingCaKeyChoices, 0 )
		self.m_choice_useExistingCaKey.SetSelection( 0 )
		gSizer_certOpt.Add( self.m_choice_useExistingCaKey, 0, wx.ALL, 5 )

		self.m_staticText_useEcc = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"Use Elliptic Curve Crypto:", wx.DefaultPosition, wx.Size( 145,-1 ), 0 )
		self.m_staticText_useEcc.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_useEcc, 0, wx.ALL, 5 )

		m_choice_useEccChoices = [ u"No", u"Yes" ]
		self.m_choice_useEcc = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_useEccChoices, 0 )
		self.m_choice_useEcc.SetSelection( 0 )
		gSizer_certOpt.Add( self.m_choice_useEcc, 0, wx.ALL, 5 )

		self.m_staticText_pkiTreeKeyLen = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"Key Length for PKI Tree (bits):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pkiTreeKeyLen.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_pkiTreeKeyLen, 0, wx.ALL, 5 )

		m_choice_pkiTreeKeyLenChoices = [ u"1024", u"2048", u"3072", u"4096" ]
		self.m_choice_pkiTreeKeyLen = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_pkiTreeKeyLenChoices, 0 )
		self.m_choice_pkiTreeKeyLen.SetSelection( 1 )
		gSizer_certOpt.Add( self.m_choice_pkiTreeKeyLen, 0, wx.ALL, 5 )

		self.m_staticText_pkiTreeDuration = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"PKI Tree Duration (years):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pkiTreeDuration.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_pkiTreeDuration, 0, wx.ALL, 5 )

		self.m_textCtrl_pkiTreeDuration = wx.TextCtrl( self.m_panel_certOpt, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( 170,-1 ), 0 )
		gSizer_certOpt.Add( self.m_textCtrl_pkiTreeDuration, 0, wx.ALL, 5 )

		self.m_staticText_SRKs = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"Super Root Keys:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_SRKs.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_SRKs, 0, wx.ALL, 5 )

		m_choice_SRKsChoices = [ u"1", u"2", u"3", u"4" ]
		self.m_choice_SRKs = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_SRKsChoices, 0 )
		self.m_choice_SRKs.SetSelection( 3 )
		gSizer_certOpt.Add( self.m_choice_SRKs, 0, wx.ALL, 5 )

		self.m_staticText_caFlagSet = wx.StaticText( self.m_panel_certOpt, wx.ID_ANY, u"SRK Cert to have CA flag Set:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_caFlagSet.Wrap( -1 )

		gSizer_certOpt.Add( self.m_staticText_caFlagSet, 0, wx.ALL, 5 )

		m_choice_caFlagSetChoices = [ u"Yes - Standard PKI Tree", u"No - Fast Auth Tree" ]
		self.m_choice_caFlagSet = wx.Choice( self.m_panel_certOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 170,-1 ), m_choice_caFlagSetChoices, 0 )
		self.m_choice_caFlagSet.SetSelection( 0 )
		gSizer_certOpt.Add( self.m_choice_caFlagSet, 0, wx.ALL, 5 )


		self.m_panel_certOpt.SetSizer( gSizer_certOpt )
		self.m_panel_certOpt.Layout()
		gSizer_certOpt.Fit( self.m_panel_certOpt )
		self.m_notebook_certOpt.AddPage( self.m_panel_certOpt, u"Certificate Option", False )

		wSizer_win.Add( self.m_notebook_certOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 68,-1 ), 0 )
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
		self.m_choice_cstVersion.Bind( wx.EVT_CHOICE, self.callbackSwitchCstVersion )
		self.m_choice_useEcc.Bind( wx.EVT_CHOICE, self.callbackUseEcc )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSwitchCstVersion( self, event ):
		event.Skip()

	def callbackUseEcc( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


