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
## Class bootDeviceWin_UsdhcSd
###########################################################################

class bootDeviceWin_UsdhcSd ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 349,374 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_notebook_sdOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_sdOpt = wx.Panel( self.m_notebook_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer_sdOpt = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText_instance = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Instance:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_instance.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_instance, 0, wx.ALL, 5 )

        m_choice_instanceChoices = [ u"0", u"1", u"2" ]
        self.m_choice_instance = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_instanceChoices, 0 )
        self.m_choice_instance.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_instance, 0, wx.ALL, 5 )

        self.m_staticText_busWidth = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Bus Width:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_busWidth.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_busWidth, 0, wx.ALL, 5 )

        m_choice_busWidthChoices = [ u"1bit", u"4bit" ]
        self.m_choice_busWidth = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_busWidthChoices, 0 )
        self.m_choice_busWidth.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_busWidth, 0, wx.ALL, 5 )

        self.m_staticText_timingInterface = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Timing Interface:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_timingInterface.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_timingInterface, 0, wx.ALL, 5 )

        m_choice_timingInterfaceChoices = [ u"SDR12/Normal", u"SDR25/HighSpeed", u"SDR50", u"SDR104", u"DDR50" ]
        self.m_choice_timingInterface = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_timingInterfaceChoices, 0 )
        self.m_choice_timingInterface.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_timingInterface, 0, wx.ALL, 5 )

        self.m_staticText_enablePowerCycle = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Enable Power Cycle:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_enablePowerCycle.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_enablePowerCycle, 0, wx.ALL, 5 )

        m_choice_enablePowerCycleChoices = [ u"No", u"Yes" ]
        self.m_choice_enablePowerCycle = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_enablePowerCycleChoices, 0 )
        self.m_choice_enablePowerCycle.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_enablePowerCycle, 0, wx.ALL, 5 )

        self.m_staticText_powerPolarity = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Power Polarity:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_powerPolarity.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_powerPolarity, 0, wx.ALL, 5 )

        m_choice_powerPolarityChoices = [ u"RST Low-Disable", u"RST High-Disable" ]
        self.m_choice_powerPolarity = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_powerPolarityChoices, 0 )
        self.m_choice_powerPolarity.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_powerPolarity, 0, wx.ALL, 5 )

        self.m_staticText_powerUpTime = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Power Up Time:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_powerUpTime.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_powerUpTime, 0, wx.ALL, 5 )

        m_choice_powerUpTimeChoices = [ u"5ms", u"2.5ms" ]
        self.m_choice_powerUpTime = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_powerUpTimeChoices, 0 )
        self.m_choice_powerUpTime.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_powerUpTime, 0, wx.ALL, 5 )

        self.m_staticText_powerDownTime = wx.StaticText( self.m_panel_sdOpt, wx.ID_ANY, u"Power Down Time:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_powerDownTime.Wrap( -1 )

        gSizer_sdOpt.Add( self.m_staticText_powerDownTime, 0, wx.ALL, 5 )

        m_choice_powerDownTimeChoices = [ u"20ms", u"10ms", u"5ms", u"2.5ms" ]
        self.m_choice_powerDownTime = wx.Choice( self.m_panel_sdOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_choice_powerDownTimeChoices, 0 )
        self.m_choice_powerDownTime.SetSelection( 0 )
        gSizer_sdOpt.Add( self.m_choice_powerDownTime, 0, wx.ALL, 5 )


        self.m_panel_sdOpt.SetSizer( gSizer_sdOpt )
        self.m_panel_sdOpt.Layout()
        gSizer_sdOpt.Fit( self.m_panel_sdOpt )
        self.m_notebook_sdOpt.AddPage( self.m_panel_sdOpt, u"SD Option", False )

        wSizer_win.Add( self.m_notebook_sdOpt, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 38,-1 ), 0 )
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
        self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
        self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def callbackClose( self, event ):
        event.Skip()

    def callbackOk( self, event ):
        event.Skip()

    def callbackCancel( self, event ):
        event.Skip()


