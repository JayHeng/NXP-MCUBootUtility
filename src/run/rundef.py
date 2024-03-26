import sys, os

kUartSpeed_Blhost = ['115200', '57600', '19200', '9600', '4800']
kUartSpeed_Sdphost = ['115200']

kBootDeviceMemId_QuadspiNor   = 0x1
kBootDeviceMemId_SemcNor      = 0x8
kBootDeviceMemId_FlexspiNor   = 0x9
kBootDeviceMemId_SpifiNor     = 0xa
kBootDeviceMemId_XspiNor      = 0xb
kBootDeviceMemId_SemcNand     = 0x100
kBootDeviceMemId_FlexspiNand  = 0x101
kBootDeviceMemId_SpiNor       = 0x110
kBootDeviceMemId_UsdhcSd      = 0x120
kBootDeviceMemId_UsdhcMmc     = 0x121

#----------------FlexSPI NOR---------------------
kFlexspiNorContent_Blank8 = 0xFF
kFlexspiNorContent_Blank32 = 0xFFFFFFFF

#kFlexspiNorCfgInfo_StartAddr = 0x0/0x400
kFlexspiNorCfgInfo_Notify    = 0xF000000F
kFlexspiDevCfgInfo_Instance  = 0xCF900001
kXspiDevCfgInfo_Instance     = 0xCF900000

kFlexspiNorCfgTag_Flexspi = 0x42464346  # 'FCFB'
kFlexspiNorCfgOffset_FlexspiTag     = 0x000
kFlexspiNorCfgOffset_PageByteSize   = 0x1c0
kFlexspiNorCfgOffset_SectorByteSize = 0x1c4
kFlexspiNorCfgOffset_BlockByteSize  = 0x1d0

kXspiNorCfgTag_Xspi       = 0x42464346  # 'FCFB'
kXspiNorCfgOffset_XspiTag           = 0x000
kXspiNorCfgOffset_PageByteSize      = 0x200
kXspiNorCfgOffset_SectorByteSize    = 0x204
kXspiNorCfgOffset_BlockByteSize     = 0x210

kXspiNorDefaultMemInfo_PageSize    = 0x100
kXspiNorDefaultMemInfo_SectorSize  = 0x1000
kXspiNorDefaultMemInfo_BlockSize   = 0x20000

kBootDeviceMemXipSize_FlexspiNor   = 0x10000000 #256MB
kBootDeviceMemXipSize_FlexspiNor504MB   = 0x1F800000
kBootDeviceMemXipSize_FlexspiNor256MB   = 0x10000000
kBootDeviceMemXipSize_FlexspiNor240MB   = 0x0F000000
kBootDeviceMemXipSize_FlexspiNor128MB   = 0x08000000
kBootDeviceMemXipSize_FlexspiNor64MB    = 0x04000000
kBootDeviceMemXipSize_FlexspiNor32MB    = 0x02000000
kBootDeviceMemXipSize_FlexspiNor4MB     = 0x00400000
