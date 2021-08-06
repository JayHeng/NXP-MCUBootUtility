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
## Class advSettingsWin_Sign
###########################################################################

class advSettingsWin_Sign ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 303,371 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_signOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_signOpt = wx.Panel( self.m_notebook_signOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer_signOpt = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_signPart = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Sign Part of Image:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signPart.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signPart, 0, wx.ALL, 5 )

		m_choice_signPartChoices = [ u"No", u"Yes" ]
		self.m_choice_signPart = wx.Choice( self.m_panel_signOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 120,-1 ), m_choice_signPartChoices, 0 )
		self.m_choice_signPart.SetSelection( 0 )
		gSizer_signOpt.Add( self.m_choice_signPart, 0, wx.ALL, 5 )

		self.m_staticText_signStart0 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 0 Start:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signStart0.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signStart0, 0, wx.ALL, 5 )

		self.m_textCtrl_signStart0 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signStart0, 0, wx.ALL, 5 )

		self.m_staticText_signSize0 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 0 Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signSize0.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signSize0, 0, wx.ALL, 5 )

		self.m_textCtrl_signSize0 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signSize0, 0, wx.ALL, 5 )

		self.m_staticText_signStart1 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 1 Start:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signStart1.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signStart1, 0, wx.ALL, 5 )

		self.m_textCtrl_signStart1 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signStart1, 0, wx.ALL, 5 )

		self.m_staticText_signSize1 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 1 Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signSize1.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signSize1, 0, wx.ALL, 5 )

		self.m_textCtrl_signSize1 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signSize1, 0, wx.ALL, 5 )

		self.m_staticText_signStart2 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 2 Start:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signStart2.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signStart2, 0, wx.ALL, 5 )

		self.m_textCtrl_signStart2 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signStart2, 0, wx.ALL, 5 )

		self.m_staticText_signSize2 = wx.StaticText( self.m_panel_signOpt, wx.ID_ANY, u"Signed Region 2 Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_signSize2.Wrap( -1 )

		gSizer_signOpt.Add( self.m_staticText_signSize2, 0, wx.ALL, 5 )

		self.m_textCtrl_signSize2 = wx.TextCtrl( self.m_panel_signOpt, wx.ID_ANY, u"0x0", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		gSizer_signOpt.Add( self.m_textCtrl_signSize2, 0, wx.ALL, 5 )


		self.m_panel_signOpt.SetSizer( gSizer_signOpt )
		self.m_panel_signOpt.Layout()
		gSizer_signOpt.Fit( self.m_panel_signOpt )
		self.m_notebook_signOpt.AddPage( self.m_panel_signOpt, u"Signature Option", False )

		wSizer_win.Add( self.m_notebook_signOpt, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 18,-1 ), 0 )
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
		self.m_choice_signPart.Bind( wx.EVT_CHOICE, self.callbackSignPart )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSignPart( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


