import wx
import sys, os

kConnectStep_Normal = 1

kBootDevice_InternalNor    = 'On-chip NOR' #'FTFx NOR'
kBootDevice_QuadspiNor     = 'QUADSPI NOR'

kBootDevice_v3_0_0 = [kBootDevice_InternalNor]
kBootDevice_Latest = kBootDevice_v3_0_0

kSecureBootType_PlainUnsigned        = 'Plain Unsigned Image Boot'

kSecureBootType_v3_0_0 = [kSecureBootType_PlainUnsigned]
kSecureBootType_Latest = kSecureBootType_v3_0_0

kMemBlockColor_FCF        = wx.Colour( 0x9f, 0x9f, 0x5f ) #wx.KHAKI
kMemBlockColor_BCA        = wx.Colour( 0xc9, 0xd2, 0x00 ) #wx.DARK_YELLOW
kMemBlockColor_Image      = wx.BLUE

