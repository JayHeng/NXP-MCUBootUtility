import sys, os

#----------------FDCB----------------------
kFlexspiFdcbOffset_tag = 0x000
kFlexspiFdcbLength_tag = 0x4
kFlexspiFdcbValue_tag  = 0x42464346  # 'FCFB'

kFlexspiFdcbOffset_version = 0x004
kFlexspiFdcbLength_version = 0x4

kFlexspiFdcbOffset_readSampleClkSrc = 0x00c
kFlexspiFdcbLength_readSampleClkSrc = 0x1

kFlexspiFdcbOffset_csHoldTime = 0x00d
kFlexspiFdcbLength_csHoldTime = 0x1

kFlexspiFdcbOffset_csSetupTime = 0x00e
kFlexspiFdcbLength_csSetupTime = 0x1

kFlexspiFdcbOffset_columnAddressWidth = 0x00f
kFlexspiFdcbLength_columnAddressWidth = 0x1

kFlexspiFdcbOffset_deviceModeCfgEnable = 0x010
kFlexspiFdcbLength_deviceModeCfgEnable = 0x1

kFlexspiFdcbOffset_deviceModeType = 0x011
kFlexspiFdcbLength_deviceModeType = 0x1

kFlexspiFdcbOffset_waitTimeCfgCommands = 0x012
kFlexspiFdcbLength_waitTimeCfgCommands = 0x2

kFlexspiFdcbOffset_deviceModeSeq = 0x014
kFlexspiFdcbLength_deviceModeSeq = 0x4

kFlexspiFdcbOffset_deviceModeArg = 0x018
kFlexspiFdcbLength_deviceModeArg = 0x4

kFlexspiFdcbOffset_configCmdEnable = 0x01c
kFlexspiFdcbLength_configCmdEnable = 0x1

kFlexspiFdcbOffset_configModeType = 0x01d
kFlexspiFdcbLength_configModeType = 0x3

kFlexspiFdcbOffset_configCmdSeqs = 0x020
kFlexspiFdcbLength_configCmdSeqs = 0xc

kFlexspiFdcbOffset_configCmdArgs = 0x030
kFlexspiFdcbLength_configCmdArgs = 0xc

kFlexspiFdcbOffset_controllerMiscOption = 0x040
kFlexspiFdcbLength_controllerMiscOption = 0x4

kFlexspiFdcbOffset_deviceType = 0x044
kFlexspiFdcbLength_deviceType = 0x1

kFlexspiFdcbOffset_sflashPadType = 0x045
kFlexspiFdcbLength_sflashPadType = 0x1

kFlexspiFdcbOffset_serialClkFreq = 0x046
kFlexspiFdcbLength_serialClkFreq = 0x1

kFlexspiFdcbOffset_lutCustomSeqEnable = 0x047
kFlexspiFdcbLength_lutCustomSeqEnable = 0x1

kFlexspiFdcbOffset_sflashA1Size = 0x050
kFlexspiFdcbLength_sflashA1Size = 0x4

kFlexspiFdcbOffset_sflashA2Size = 0x054
kFlexspiFdcbLength_sflashA2Size = 0x4

kFlexspiFdcbOffset_sflashB1Size = 0x058
kFlexspiFdcbLength_sflashB1Size = 0x4

kFlexspiFdcbOffset_sflashB2Size = 0x05c
kFlexspiFdcbLength_sflashB2Size = 0x4

kFlexspiFdcbOffset_csPadSettingOverride = 0x060
kFlexspiFdcbLength_csPadSettingOverride = 0x4

kFlexspiFdcbOffset_sclkPadSettingOverride = 0x064
kFlexspiFdcbLength_sclkPadSettingOverride = 0x4

kFlexspiFdcbOffset_dataPadSettingOverride = 0x068
kFlexspiFdcbLength_dataPadSettingOverride = 0x4

kFlexspiFdcbOffset_dqsPadSettingOverride = 0x06c
kFlexspiFdcbLength_dqsPadSettingOverride = 0x4

kFlexspiFdcbOffset_timeoutInMs = 0x070
kFlexspiFdcbLength_timeoutInMs = 0x4

kFlexspiFdcbOffset_commandInterval = 0x074
kFlexspiFdcbLength_commandInterval = 0x4

kFlexspiFdcbOffset_dataValidTime = 0x078
kFlexspiFdcbLength_dataValidTime = 0x4

kFlexspiFdcbOffset_busyOffset = 0x07c
kFlexspiFdcbLength_busyOffset = 0x2

kFlexspiFdcbOffset_busyBitPolarity = 0x07e
kFlexspiFdcbLength_busyBitPolarity = 0x2

kFlexspiFdcbOffset_lookupTable = 0x080
kFlexspiFdcbLength_lookupTable = 0x100

kFlexspiFdcbOffset_lutCustomSeq = 0x180
kFlexspiFdcbLength_lutCustomSeq = 0x30

kFlexspiFdcbOffset_pageSize = 0x1c0
kFlexspiFdcbLength_pageSize = 0x4

kFlexspiFdcbOffset_sectorSize = 0x1c4
kFlexspiFdcbLength_sectorSize = 0x4

kFlexspiFdcbOffset_ipcmdSerialClkFreq = 0x1c8
kFlexspiFdcbLength_ipcmdSerialClkFreq = 0x1

kFlexspiFdcbOffset_isUniformBlockSize = 0x1c9
kFlexspiFdcbLength_isUniformBlockSize = 0x1

kFlexspiFdcbOffset_isDataOrderSwapped = 0x1ca
kFlexspiFdcbLength_isDataOrderSwapped = 0x1

kFlexspiFdcbOffset_serialNorType = 0x1cc
kFlexspiFdcbLength_serialNorType = 0x1

kFlexspiFdcbOffset_needExitNoCmdMode = 0x1cd
kFlexspiFdcbLength_needExitNoCmdMode = 0x1

kFlexspiFdcbOffset_halfClkForNonReadCmd = 0x1ce
kFlexspiFdcbLength_halfClkForNonReadCmd = 0x1

kFlexspiFdcbOffset_needRestoreNoCmdMode = 0x1cf
kFlexspiFdcbLength_needRestoreNoCmdMode = 0x1

kFlexspiFdcbOffset_blockSize = 0x1d0
kFlexspiFdcbLength_blockSize = 0x4

kFlexspiFdcbOffset_isNonBlockingMode = 0x1d1
kFlexspiFdcbLength_isNonBlockingMode = 0x1

kFlexspiLutRegShift_Op0  = 0
kFlexspiLutRegMask_Op0   = 0x000000FF
kFlexspiLutRegShift_Pad0 = 8
kFlexspiLutRegMask_Pad0  = 0x00000300
kFlexspiLutRegShift_Cmd0 = 10
kFlexspiLutRegMask_Cmd0  = 0x0000FC00
kFlexspiLutRegShift_Op1  = 16
kFlexspiLutRegMask_Op1   = 0x00FF0000
kFlexspiLutRegShift_Pad1 = 24
kFlexspiLutRegMask_Pad1  = 0x03000000
kFlexspiLutRegShift_Cmd1 = 26
kFlexspiLutRegMask_Cmd1  = 0xFC000000

