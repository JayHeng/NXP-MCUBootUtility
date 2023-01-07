import wx
import sys, os

kConnectStep_Normal = 1

kBootDevice_InternalNor    = 'On-chip NOR' #'FTFx NOR'
kBootDevice_QuadspiNor     = 'FLEXSPI NOR'

kBootDevice_v4_0_0 = [kBootDevice_InternalNor]
kBootDevice_Latest = kBootDevice_v4_0_0

kSecureBootType_PlainUnsigned        = 'Plain Unsigned Image Boot'

kSecureBootType_v4_0_0 = [kSecureBootType_PlainUnsigned]
kSecureBootType_Latest = kSecureBootType_v4_0_0

kMemBlockColor_Image      = wx.BLUE

