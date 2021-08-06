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
## Class bootDeviceWin_LUT
###########################################################################

class bootDeviceWin_LUT ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 895,689 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

		self.m_notebook_lut = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel_lut = wx.Panel( self.m_notebook_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer_lut = wx.FlexGridSizer( 0, 7, 0, 0 )
		fgSizer_lut.SetFlexibleDirection( wx.BOTH )
		fgSizer_lut.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText_lutIndex = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"LUT Index", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_cmd0 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"OPCODE0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_cmd0.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_cmd0, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_pad0 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"NUM_PADS0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pad0.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_pad0, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_op0 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"OPERAND0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_op0.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_op0, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_cmd1 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"OPCODE1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_cmd1.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_cmd1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_pad1 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"NUM_PADS1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_pad1.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_pad1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_op1 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"OPERAND1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_op1.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_op1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText_lutIndex16n = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n, 0, wx.ALL, 5 )

		m_choice_cmd0_16nChoices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16nChoices, 0 )
		self.m_choice_cmd0_16n.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n, 0, wx.ALL, 5 )

		m_choice_pad0_16nChoices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16nChoices, 0 )
		self.m_choice_pad0_16n.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n, 0, wx.ALL, 5 )

		m_choice_cmd1_16nChoices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16nChoices, 0 )
		self.m_choice_cmd1_16n.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n, 0, wx.ALL, 5 )

		m_choice_pad1_16nChoices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16nChoices, 0 )
		self.m_choice_pad1_16n.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n1 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n1.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n1, 0, wx.ALL, 5 )

		m_choice_cmd0_16n1Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n1 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n1Choices, 0 )
		self.m_choice_cmd0_16n1.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n1, 0, wx.ALL, 5 )

		m_choice_pad0_16n1Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n1 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n1Choices, 0 )
		self.m_choice_pad0_16n1.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n1, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n1 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n1, 0, wx.ALL, 5 )

		m_choice_cmd1_16n1Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n1 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n1Choices, 0 )
		self.m_choice_cmd1_16n1.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n1, 0, wx.ALL, 5 )

		m_choice_pad1_16n1Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n1 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n1Choices, 0 )
		self.m_choice_pad1_16n1.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n1, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n1 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n1, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n2 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n2.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n2, 0, wx.ALL, 5 )

		m_choice_cmd0_16n2Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n2 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n2Choices, 0 )
		self.m_choice_cmd0_16n2.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n2, 0, wx.ALL, 5 )

		m_choice_pad0_16n2Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n2 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n2Choices, 0 )
		self.m_choice_pad0_16n2.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n2, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n2 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n2, 0, wx.ALL, 5 )

		m_choice_cmd1_16n2Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n2 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n2Choices, 0 )
		self.m_choice_cmd1_16n2.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n2, 0, wx.ALL, 5 )

		m_choice_pad1_16n2Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n2 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n2Choices, 0 )
		self.m_choice_pad1_16n2.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n2, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n2 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n2, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n3 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n3.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n3, 0, wx.ALL, 5 )

		m_choice_cmd0_16n3Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n3 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n3Choices, 0 )
		self.m_choice_cmd0_16n3.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n3, 0, wx.ALL, 5 )

		m_choice_pad0_16n3Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n3 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n3Choices, 0 )
		self.m_choice_pad0_16n3.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n3, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n3 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n3, 0, wx.ALL, 5 )

		m_choice_cmd1_16n3Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n3 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n3Choices, 0 )
		self.m_choice_cmd1_16n3.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n3, 0, wx.ALL, 5 )

		m_choice_pad1_16n3Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n3 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n3Choices, 0 )
		self.m_choice_pad1_16n3.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n3, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n3 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n3, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n4 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"4", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n4.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n4, 0, wx.ALL, 5 )

		m_choice_cmd0_16n4Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n4 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n4Choices, 0 )
		self.m_choice_cmd0_16n4.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n4, 0, wx.ALL, 5 )

		m_choice_pad0_16n4Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n4 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n4Choices, 0 )
		self.m_choice_pad0_16n4.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n4, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n4 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n4, 0, wx.ALL, 5 )

		m_choice_cmd1_16n4Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n4 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n4Choices, 0 )
		self.m_choice_cmd1_16n4.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n4, 0, wx.ALL, 5 )

		m_choice_pad1_16n4Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n4 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n4Choices, 0 )
		self.m_choice_pad1_16n4.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n4, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n4 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n4, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n5 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"5", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n5.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n5, 0, wx.ALL, 5 )

		m_choice_cmd0_16n5Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n5 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n5Choices, 0 )
		self.m_choice_cmd0_16n5.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n5, 0, wx.ALL, 5 )

		m_choice_pad0_16n5Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n5 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n5Choices, 0 )
		self.m_choice_pad0_16n5.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n5, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n5 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n5, 0, wx.ALL, 5 )

		m_choice_cmd1_16n5Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n5 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n5Choices, 0 )
		self.m_choice_cmd1_16n5.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n5, 0, wx.ALL, 5 )

		m_choice_pad1_16n5Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n5 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n5Choices, 0 )
		self.m_choice_pad1_16n5.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n5, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n5 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n5, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n6 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"6", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n6.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n6, 0, wx.ALL, 5 )

		m_choice_cmd0_16n6Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n6 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n6Choices, 0 )
		self.m_choice_cmd0_16n6.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n6, 0, wx.ALL, 5 )

		m_choice_pad0_16n6Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n6 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n6Choices, 0 )
		self.m_choice_pad0_16n6.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n6, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n6 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n6, 0, wx.ALL, 5 )

		m_choice_cmd1_16n6Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n6 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n6Choices, 0 )
		self.m_choice_cmd1_16n6.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n6, 0, wx.ALL, 5 )

		m_choice_pad1_16n6Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n6 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n6Choices, 0 )
		self.m_choice_pad1_16n6.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n6, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n6 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n6, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n7 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"7", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n7.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n7, 0, wx.ALL, 5 )

		m_choice_cmd0_16n7Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n7 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n7Choices, 0 )
		self.m_choice_cmd0_16n7.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n7, 0, wx.ALL, 5 )

		m_choice_pad0_16n7Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n7 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n7Choices, 0 )
		self.m_choice_pad0_16n7.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n7, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n7 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n7, 0, wx.ALL, 5 )

		m_choice_cmd1_16n7Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n7 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n7Choices, 0 )
		self.m_choice_cmd1_16n7.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n7, 0, wx.ALL, 5 )

		m_choice_pad1_16n7Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n7 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n7Choices, 0 )
		self.m_choice_pad1_16n7.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n7, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n7 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n7, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n8 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"8", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n8.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n8, 0, wx.ALL, 5 )

		m_choice_cmd0_16n8Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n8 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n8Choices, 0 )
		self.m_choice_cmd0_16n8.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n8, 0, wx.ALL, 5 )

		m_choice_pad0_16n8Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n8 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n8Choices, 0 )
		self.m_choice_pad0_16n8.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n8, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n8 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n8, 0, wx.ALL, 5 )

		m_choice_cmd1_16n8Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n8 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n8Choices, 0 )
		self.m_choice_cmd1_16n8.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n8, 0, wx.ALL, 5 )

		m_choice_pad1_16n8Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n8 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n8Choices, 0 )
		self.m_choice_pad1_16n8.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n8, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n8 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n8, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n9 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"9", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n9.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n9, 0, wx.ALL, 5 )

		m_choice_cmd0_16n9Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n9 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n9Choices, 0 )
		self.m_choice_cmd0_16n9.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n9, 0, wx.ALL, 5 )

		m_choice_pad0_16n9Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n9 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n9Choices, 0 )
		self.m_choice_pad0_16n9.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n9, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n9 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n9, 0, wx.ALL, 5 )

		m_choice_cmd1_16n9Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n9 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n9Choices, 0 )
		self.m_choice_cmd1_16n9.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n9, 0, wx.ALL, 5 )

		m_choice_pad1_16n9Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n9 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n9Choices, 0 )
		self.m_choice_pad1_16n9.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n9, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n9 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n9, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n10 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n10.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n10, 0, wx.ALL, 5 )

		m_choice_cmd0_16n10Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n10 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n10Choices, 0 )
		self.m_choice_cmd0_16n10.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n10, 0, wx.ALL, 5 )

		m_choice_pad0_16n10Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n10 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n10Choices, 0 )
		self.m_choice_pad0_16n10.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n10, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n10 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n10, 0, wx.ALL, 5 )

		m_choice_cmd1_16n10Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n10 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n10Choices, 0 )
		self.m_choice_cmd1_16n10.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n10, 0, wx.ALL, 5 )

		m_choice_pad1_16n10Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n10 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n10Choices, 0 )
		self.m_choice_pad1_16n10.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n10, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n10 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n10, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n11 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"11", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n11.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n11, 0, wx.ALL, 5 )

		m_choice_cmd0_16n11Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n11 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n11Choices, 0 )
		self.m_choice_cmd0_16n11.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n11, 0, wx.ALL, 5 )

		m_choice_pad0_16n11Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n11 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n11Choices, 0 )
		self.m_choice_pad0_16n11.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n11, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n11 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n11, 0, wx.ALL, 5 )

		m_choice_cmd1_16n11Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n11 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n11Choices, 0 )
		self.m_choice_cmd1_16n11.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n11, 0, wx.ALL, 5 )

		m_choice_pad1_16n11Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n11 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n11Choices, 0 )
		self.m_choice_pad1_16n11.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n11, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n11 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n11, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n12 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"12", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n12.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n12, 0, wx.ALL, 5 )

		m_choice_cmd0_16n12Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n12 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n12Choices, 0 )
		self.m_choice_cmd0_16n12.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n12, 0, wx.ALL, 5 )

		m_choice_pad0_16n12Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n12 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n12Choices, 0 )
		self.m_choice_pad0_16n12.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n12, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n12 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n12, 0, wx.ALL, 5 )

		m_choice_cmd1_16n12Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n12 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n12Choices, 0 )
		self.m_choice_cmd1_16n12.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n12, 0, wx.ALL, 5 )

		m_choice_pad1_16n12Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n12 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n12Choices, 0 )
		self.m_choice_pad1_16n12.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n12, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n12 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n12, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n13 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"13", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n13.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n13, 0, wx.ALL, 5 )

		m_choice_cmd0_16n13Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n13 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n13Choices, 0 )
		self.m_choice_cmd0_16n13.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n13, 0, wx.ALL, 5 )

		m_choice_pad0_16n13Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n13 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n13Choices, 0 )
		self.m_choice_pad0_16n13.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n13, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n13 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n13, 0, wx.ALL, 5 )

		m_choice_cmd1_16n13Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n13 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n13Choices, 0 )
		self.m_choice_cmd1_16n13.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n13, 0, wx.ALL, 5 )

		m_choice_pad1_16n13Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n13 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n13Choices, 0 )
		self.m_choice_pad1_16n13.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n13, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n13 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n13, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n14 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"14", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n14.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n14, 0, wx.ALL, 5 )

		m_choice_cmd0_16n14Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n14 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n14Choices, 0 )
		self.m_choice_cmd0_16n14.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n14, 0, wx.ALL, 5 )

		m_choice_pad0_16n14Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n14 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n14Choices, 0 )
		self.m_choice_pad0_16n14.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n14, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n14 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n14, 0, wx.ALL, 5 )

		m_choice_cmd1_16n14Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n14 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n14Choices, 0 )
		self.m_choice_cmd1_16n14.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n14, 0, wx.ALL, 5 )

		m_choice_pad1_16n14Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n14 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n14Choices, 0 )
		self.m_choice_pad1_16n14.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n14, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n14 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n14, 0, wx.ALL, 5 )

		self.m_staticText_lutIndex16n15 = wx.StaticText( self.m_panel_lut, wx.ID_ANY, u"15", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutIndex16n15.Wrap( -1 )

		fgSizer_lut.Add( self.m_staticText_lutIndex16n15, 0, wx.ALL, 5 )

		m_choice_cmd0_16n15Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd0_16n15 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd0_16n15Choices, 0 )
		self.m_choice_cmd0_16n15.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd0_16n15, 0, wx.ALL, 5 )

		m_choice_pad0_16n15Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad0_16n15 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad0_16n15Choices, 0 )
		self.m_choice_pad0_16n15.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad0_16n15, 0, wx.ALL, 5 )

		self.m_textCtrl_op0_16n15 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op0_16n15, 0, wx.ALL, 5 )

		m_choice_cmd1_16n15Choices = [ u"0x01 - CMD_SDR", u"0x02 - RADDR_SDR", u"0x03 - CADDR_SDR", u"0x04 - MODE1_SDR", u"0x05 - MODE2_SDR", u"0x06 - MODE4_SDR", u"0x07 - MODE8_SDR", u"0x08 - WRITE_SDR", u"0x09 - READ_SDR", u"0x0A - LEARN_SDR", u"0x0B - DATSZ_SDR", u"0x0C - DUMMY_SDR", u"0x0D - DUMMY_RWDS_SDR", u"0x21 - CMD_DDR", u"0x22 - RADDR_DDR", u"0x23 - CADDR_DDR", u"0x24 - MODE1_DDR", u"0x25 - MODE2_DDR", u"0x26 - MODE4_DDR", u"0x27 - MODE8_DDR", u"0x28 - WRITE_DDR", u"0x29 - READ_DDR", u"0x2A - LEARN_DDR", u"0x2B - DATSZ_DDR", u"0x2C - DUMMY_DDR", u"0x2D - DUMMY_RWDS_DDR", u"0x1F - JMP_ON_CS", u"0x00 - STOP" ]
		self.m_choice_cmd1_16n15 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_cmd1_16n15Choices, 0 )
		self.m_choice_cmd1_16n15.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_cmd1_16n15, 0, wx.ALL, 5 )

		m_choice_pad1_16n15Choices = [ u"0 - 1PAD", u"1 - 2PAD", u"2 - 4PAD", u"3 - 8PAD" ]
		self.m_choice_pad1_16n15 = wx.Choice( self.m_panel_lut, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_pad1_16n15Choices, 0 )
		self.m_choice_pad1_16n15.SetSelection( 0 )
		fgSizer_lut.Add( self.m_choice_pad1_16n15, 0, wx.ALL, 5 )

		self.m_textCtrl_op1_16n15 = wx.TextCtrl( self.m_panel_lut, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer_lut.Add( self.m_textCtrl_op1_16n15, 0, wx.ALL, 5 )


		self.m_panel_lut.SetSizer( fgSizer_lut )
		self.m_panel_lut.Layout()
		fgSizer_lut.Fit( self.m_panel_lut )
		self.m_notebook_lut.AddPage( self.m_panel_lut, u"LUT", False )

		wSizer_win.Add( self.m_notebook_lut, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText_winNull0.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_winNull0, 0, wx.ALL, 5 )

		self.m_staticText_lutGroup = wx.StaticText( self, wx.ID_ANY, u"LUT Group:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_lutGroup.Wrap( -1 )

		wSizer_win.Add( self.m_staticText_lutGroup, 0, wx.ALL, 5 )

		m_choice_lutGroupChoices = [ u"0 - 15", u"16 - 31", u"32 - 47", u"48 - 63" ]
		self.m_choice_lutGroup = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_lutGroupChoices, 0 )
		self.m_choice_lutGroup.SetSelection( 0 )
		wSizer_win.Add( self.m_choice_lutGroup, 0, wx.ALL, 5 )

		self.m_staticText_winNull1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 290,-1 ), 0 )
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
		self.m_choice_lutGroup.Bind( wx.EVT_CHOICE, self.callbackSetLutGroup )
		self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def callbackClose( self, event ):
		event.Skip()

	def callbackSetLutGroup( self, event ):
		event.Skip()

	def callbackOk( self, event ):
		event.Skip()

	def callbackCancel( self, event ):
		event.Skip()


