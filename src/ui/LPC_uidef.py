import wx
import sys, os

kConnectStep_Normal = 1

kBootDevice_InternalNor    = 'On-chip NOR' #'C040HD NOR'
kBootDevice_QuadspiNor     = 'QUADSPI NOR'

kBootDevice_v3_0_0 = [kBootDevice_InternalNor]
kBootDevice_Latest = kBootDevice_v3_0_0

kSecureBootType_PlainUnsigned        = 'Plain Unsigned Image Boot'

kSecureBootType_v3_0_0 = [kSecureBootType_PlainUnsigned]
kSecureBootType_Latest = kSecureBootType_v3_0_0

kMemBlockColor_Image      = wx.BLUE

