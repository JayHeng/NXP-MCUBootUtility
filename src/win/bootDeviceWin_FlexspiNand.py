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
## Class bootDeviceWin_FlexspiNand
###########################################################################

class bootDeviceWin_FlexspiNand ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 802,458 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        #self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        wSizer_win = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText_bootInstance = wx.StaticText( self, wx.ID_ANY, u"Boot Instance:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
        self.m_staticText_bootInstance.Wrap( -1 )

        wSizer_win.Add( self.m_staticText_bootInstance, 0, wx.ALL, 5 )

        m_choice_bootInstanceChoices = [ u"1st", u"2nd" ]
        self.m_choice_bootInstance = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 55,-1 ), m_choice_bootInstanceChoices, 0 )
        self.m_choice_bootInstance.SetSelection( 0 )
        wSizer_win.Add( self.m_choice_bootInstance, 0, wx.ALL, 5 )

        self.m_staticText_deviceModel = wx.StaticText( self, wx.ID_ANY, u"Device Model:", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
        self.m_staticText_deviceModel.Wrap( -1 )

        wSizer_win.Add( self.m_staticText_deviceModel, 0, wx.ALL, 5 )

        m_choice_deviceModeChoices = [ u"No", u"Winbond_W25N01G", u"Winbond_W25N02K", u"Macronix_MX35UF1G_MX35LF1G", u"Macronix_MX35UF2G_MX35LF2G", u"GigaDevice_GD5F1GQ5", u"GigaDevice_GD5F2GQ5", u"Micron_MT29F1G01AA", u"Micron_MT29F2G01AA", u"Paragon_PN26Q01A_PN26G01A", u"Paragon_PN26Q02A_PN26G02A" ]
        self.m_choice_deviceMode = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_choice_deviceModeChoices, 0 )
        self.m_choice_deviceMode.SetSelection( 0 )
        wSizer_win.Add( self.m_choice_deviceMode, 0, wx.ALL, 5 )

        self.m_staticText_winNull0 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
        self.m_staticText_winNull0.Wrap( -1 )

        wSizer_win.Add( self.m_staticText_winNull0, 0, wx.ALL, 5 )

        self.m_notebook_nandOpt = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel_nandOpt = wx.Panel( self.m_notebook_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer_nandOpt = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText_flashSize = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Flash Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_flashSize.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_flashSize, 0, wx.ALL, 5 )

        m_choice_flashSizeChoices = [ u"512Mb", u"1Gb", u"2Gb", u"4Gb" ]
        self.m_choice_flashSize = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_flashSizeChoices, 0 )
        self.m_choice_flashSize.SetSelection( 0 )
        gSizer_nandOpt.Add( self.m_choice_flashSize, 0, wx.ALL, 5 )

        self.m_staticText_hasMultiplanes = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Has Multiplanes:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_hasMultiplanes.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_hasMultiplanes, 0, wx.ALL, 5 )

        m_choice_hasMultiplanesChoices = [ u"1 plane", u"2 planes" ]
        self.m_choice_hasMultiplanes = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_hasMultiplanesChoices, 0 )
        self.m_choice_hasMultiplanes.SetSelection( 0 )
        gSizer_nandOpt.Add( self.m_choice_hasMultiplanes, 0, wx.ALL, 5 )

        self.m_staticText_pagesPerBlock = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Pages Per Block:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_pagesPerBlock.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_pagesPerBlock, 0, wx.ALL, 5 )

        m_choice_pagesPerBlockChoices = [ u"64", u"128", u"256", u"32" ]
        self.m_choice_pagesPerBlock = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_pagesPerBlockChoices, 0 )
        self.m_choice_pagesPerBlock.SetSelection( 0 )
        gSizer_nandOpt.Add( self.m_choice_pagesPerBlock, 0, wx.ALL, 5 )

        self.m_staticText_pageSize = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Page Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_pageSize.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_pageSize, 0, wx.ALL, 5 )

        m_choice_pageSizeChoices = [ u"2KB", u"4KB" ]
        self.m_choice_pageSize = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_pageSizeChoices, 0 )
        self.m_choice_pageSize.SetSelection( 0 )
        gSizer_nandOpt.Add( self.m_choice_pageSize, 0, wx.ALL, 5 )

        self.m_staticText_maxFreq = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Max Freq:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_maxFreq.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_maxFreq, 0, wx.ALL, 5 )

        m_choice_maxFreqChoices = [ u"30MHz", u"50MHz", u"60MHz", u"72MHz", u"80MHz", u"100MHz", u"133MHz", u"166MHz" ]
        self.m_choice_maxFreq = wx.Choice( self.m_panel_nandOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_maxFreqChoices, 0 )
        self.m_choice_maxFreq.SetSelection( 0 )
        gSizer_nandOpt.Add( self.m_choice_maxFreq, 0, wx.ALL, 5 )

        self.m_staticText_manufacturerId = wx.StaticText( self.m_panel_nandOpt, wx.ID_ANY, u"Manufacturer ID:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_manufacturerId.Wrap( -1 )

        gSizer_nandOpt.Add( self.m_staticText_manufacturerId, 0, wx.ALL, 5 )

        self.m_textCtrl_manufacturerId = wx.TextCtrl( self.m_panel_nandOpt, wx.ID_ANY, u"0x2C", wx.DefaultPosition, wx.Size( 108,-1 ), 0 )
        gSizer_nandOpt.Add( self.m_textCtrl_manufacturerId, 0, wx.ALL, 5 )


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

        m_choice_searchCountChoices = [ u"1", u"2", u"3", u"4" ]
        self.m_choice_searchCount = wx.Choice( self.m_panel_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_searchCountChoices, 0 )
        self.m_choice_searchCount.SetSelection( 0 )
        gSizer_fcbOpt.Add( self.m_choice_searchCount, 0, wx.ALL, 5 )

        self.m_staticText_searchStride = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, u"Search Stride:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_searchStride.Wrap( -1 )

        gSizer_fcbOpt.Add( self.m_staticText_searchStride, 0, wx.ALL, 5 )

        m_choice_searchStrideChoices = [ u"64 pages", u"128 pages", u"256 pages", u"32 pages" ]
        self.m_choice_searchStride = wx.Choice( self.m_panel_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_searchStrideChoices, 0 )
        self.m_choice_searchStride.SetSelection( 0 )
        gSizer_fcbOpt.Add( self.m_choice_searchStride, 0, wx.ALL, 5 )

        self.m_staticText_addressType = wx.StaticText( self.m_panel_fcbOpt, wx.ID_ANY, u"Address Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_addressType.Wrap( -1 )

        gSizer_fcbOpt.Add( self.m_staticText_addressType, 0, wx.ALL, 5 )

        m_choice_addressTypeChoices = [ u"byte address", u"block address" ]
        self.m_choice_addressType = wx.Choice( self.m_panel_fcbOpt, wx.ID_ANY, wx.DefaultPosition, wx.Size( 108,-1 ), m_choice_addressTypeChoices, 0 )
        self.m_choice_addressType.SetSelection( 0 )
        gSizer_fcbOpt.Add( self.m_choice_addressType, 0, wx.ALL, 5 )

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

        self.m_staticText_winNull1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 518,-1 ), 0 )
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
        self.m_choice_deviceMode.Bind( wx.EVT_CHOICE, self.callbackUseTypicalDeviceModel )
        self.m_choice_imageCopies.Bind( wx.EVT_CHOICE, self.callbackChangeImageCopies )
        self.m_button_ok.Bind( wx.EVT_BUTTON, self.callbackOk )
        self.m_button_cancel.Bind( wx.EVT_BUTTON, self.callbackCancel )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def callbackClose( self, event ):
        event.Skip()

    def callbackUseTypicalDeviceModel( self, event ):
        event.Skip()

    def callbackChangeImageCopies( self, event ):
        event.Skip()

    def callbackOk( self, event ):
        event.Skip()

    def callbackCancel( self, event ):
        event.Skip()


