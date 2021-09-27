import wx
import sys, os

kToolRunMode_Entry  = 0
kToolRunMode_Master = 1
kToolRunMode_SblOta = 2

kBootSeqColor_Invalid  = wx.Colour( 64, 64, 64 )
kBootSeqColor_Optional = wx.Colour( 166, 255, 255 )
kBootSeqColor_Active   = wx.Colour( 147, 255, 174 )
kBootSeqColor_Failed   = wx.Colour( 255, 0, 0 )

kConnectStage_Rom            = 1
kConnectStage_Flashloader    = 2
kConnectStage_ExternalMemory = 3
kConnectStage_Reset          = 4

kMcuSeries_iMXRT     = 'i.MXRT'
kMcuSeries_iMXRT10yy = 'RT10yy'
kMcuSeries_iMXRTxxx  = 'RTxxx'
kMcuSeries_iMXRT11yy = 'RT11yy'
kMcuSeries_iMXRTyyyy = [kMcuSeries_iMXRT10yy, kMcuSeries_iMXRT11yy]
kMcuSeries_LPC       = 'LPC'
kMcuSeries_Kinetis   = 'Kinetis'

kMcuSeries_v1_0_0 = [kMcuSeries_iMXRT]
kMcuSeries_v2_0_0 = [kMcuSeries_iMXRT]
kMcuSeries_v3_0_0 = [kMcuSeries_iMXRT, kMcuSeries_LPC, kMcuSeries_Kinetis]
kMcuSeries_Latest = kMcuSeries_v3_0_0

kMcuDevice_iMXRT500  = 'i.MXRT5xx'
kMcuDevice_iMXRT500S = 'i.MXRT5xxS'
kMcuDevice_iMXRT600  = 'i.MXRT6xx'
kMcuDevice_iMXRT600S = 'i.MXRT6xxS'
kMcuDevice_iMXRTxxx = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT600]

kMcuDevice_iMXRT1011 = 'i.MXRT1011'
kMcuDevice_iMXRT1015 = 'i.MXRT1015'
kMcuDevice_iMXRT102x = 'i.MXRT1021'
kMcuDevice_iMXRT1024 = 'i.MXRT1024 SIP'
kMcuDevice_iMXRT105x = 'i.MXRT105x'
kMcuDevice_iMXRT106x = 'i.MXRT106x'
kMcuDevice_iMXRT1064 = 'i.MXRT1064 SIP'
kMcuDevice_iMXRT10yy = [kMcuDevice_iMXRT1011, kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT1024, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064]

kMcuDevice_iMXRT116x = 'i.MXRT116x'
kMcuDevice_iMXRT117x = 'i.MXRT117x'
kMcuDevice_iMXRT11yy = [kMcuDevice_iMXRT116x, kMcuDevice_iMXRT117x]

kMcuDevice_L0PB      = 'MKL03Z'
kMcuDevice_L3KS_0    = 'MKL13Z'
kMcuDevice_L2KS_0    = 'MKL27Z'
kMcuDevice_L5K       = 'MKL28Z'
kMcuDevice_L3KS_1    = 'MKL33Z'
kMcuDevice_L4KS_0    = 'MKL43Z'
kMcuDevice_MKL80     = 'MKL8xZ'
kMcuDevice_MT256P    = 'MKE16Z'
kMcuDevice_MT512P    = 'MKE18F'
kMcuDevice_MK28F_0   = 'MK27F'
kMcuDevice_MK28F_1   = 'MK28F'
kMcuDevice_MK80      = 'MK8xF'
kMcuDevice_L2KS_1    = 'K32L2'
kMcuDevice_L4KS_1    = 'K32L3'

kMcuDevice_L3KSs     = [kMcuDevice_L3KS_0, kMcuDevice_L3KS_1]
kMcuDevice_MK28Fs    = [kMcuDevice_MK28F_0, kMcuDevice_MK28F_1]
kMcuDevice_Kinetis   = [kMcuDevice_L0PB, kMcuDevice_L3KS_0, kMcuDevice_L3KS_1, kMcuDevice_L2KS_0, kMcuDevice_L5K, kMcuDevice_L4KS_0, kMcuDevice_MKL80, kMcuDevice_MT256P, kMcuDevice_MT512P, kMcuDevice_MK28F_0, kMcuDevice_MK28F_1, kMcuDevice_MK80, kMcuDevice_L2KS_1, kMcuDevice_L4KS_1]

kMcuDevice_Niobe4mini_0 = 'LPC55(S)0x'
kMcuDevice_Niobe4mini_1 = 'LPC55(S)1x'
kMcuDevice_Niobe4_0     = 'LPC55(S)2x'
kMcuDevice_Niobe4_1     = 'LPC55S6x'

kMcuDevice_Niobe4minis = [kMcuDevice_Niobe4mini_0, kMcuDevice_Niobe4mini_1]
kMcuDevice_Niobe4s     = [kMcuDevice_Niobe4_0, kMcuDevice_Niobe4_1]
kMcuDevice_LPC         = [kMcuDevice_Niobe4mini_0, kMcuDevice_Niobe4mini_1, kMcuDevice_Niobe4_0, kMcuDevice_Niobe4_1]

kMcuDevice_iMXRT_v1_0_0 = [kMcuDevice_iMXRT102x, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064]
kMcuDevice_iMXRT_v1_1_0 = [kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064]
kMcuDevice_iMXRT_v2_0_0 = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT600, kMcuDevice_iMXRT1011, kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064, kMcuDevice_iMXRT117x]
kMcuDevice_iMXRT_v3_1_0 = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT600, kMcuDevice_iMXRT1011, kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT1024, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064, kMcuDevice_iMXRT117x]
kMcuDevice_iMXRT_v3_2_0 = [kMcuDevice_iMXRT500, kMcuDevice_iMXRT600, kMcuDevice_iMXRT1011, kMcuDevice_iMXRT1015, kMcuDevice_iMXRT102x, kMcuDevice_iMXRT1024, kMcuDevice_iMXRT105x, kMcuDevice_iMXRT106x, kMcuDevice_iMXRT1064, kMcuDevice_iMXRT116x, kMcuDevice_iMXRT117x]
kMcuDevice_Kinetis_v3_0_0 = [kMcuDevice_L0PB, kMcuDevice_L3KS_0, kMcuDevice_L2KS_0, kMcuDevice_L5K, kMcuDevice_L3KS_1, kMcuDevice_L4KS_0, kMcuDevice_MKL80, kMcuDevice_MT256P, kMcuDevice_MT512P, kMcuDevice_MK28F_0, kMcuDevice_MK28F_1, kMcuDevice_MK80]
kMcuDevice_Kinetis_v3_1_0 = [kMcuDevice_L0PB, kMcuDevice_L3KS_0, kMcuDevice_L2KS_0, kMcuDevice_L5K, kMcuDevice_L3KS_1, kMcuDevice_L4KS_0, kMcuDevice_MKL80, kMcuDevice_MT256P, kMcuDevice_MT512P, kMcuDevice_MK28F_0, kMcuDevice_MK28F_1, kMcuDevice_MK80, kMcuDevice_L2KS_1, kMcuDevice_L4KS_1]
kMcuDevice_LPC_v3_0_0     = [kMcuDevice_Niobe4mini_0, kMcuDevice_Niobe4mini_1, kMcuDevice_Niobe4_0, kMcuDevice_Niobe4_1]
kMcuDevice_iMXRT_Latest   = kMcuDevice_iMXRT_v3_2_0
kMcuDevice_Kinetis_Latest = kMcuDevice_Kinetis_v3_1_0
kMcuDevice_LPC_Latest     = kMcuDevice_LPC_v3_0_0

kBootDevice_XspiNor        = 'XSPI NOR'

kFlexspiNorDevice_None                  = 'No'
kFlexspiNorDevice_FDCB                  = 'Complete_FDCB'
kFlexspiNorDevice_ISSI_IS25LP064A       = 'ISSI_IS25LPxxxA_IS25WPxxxA'
kFlexspiNorDevice_ISSI_IS26KS512S       = 'ISSI_IS26KSxxxS_IS26KLxxxS'
kFlexspiNorDevice_MXIC_MX25L12845G      = 'Macronix_MX25Uxxx32F_MX25Lxxx45G'
kFlexspiNorDevice_MXIC_MX25UM51245G     = 'Macronix_MX25UMxxx45G_MX66UMxxx45G_MX25LMxxx45G'
kFlexspiNorDevice_MXIC_MX25UM51345G     = 'Macronix_MX25UM51345G'
kFlexspiNorDevice_MXIC_MX25UM51345G_2nd = 'Macronix_MX25UM51345G_2nd'
kFlexspiNorDevice_Micron_MT25QL128A     = 'Micron_MT25QLxxxA'
kFlexspiNorDevice_Micron_MT35X          = 'Micron_MT35XLxxxA_MT35XUxxxA'
kFlexspiNorDevice_Adesto_AT25SF128A     = 'Adesto_AT25SFxxxA'
kFlexspiNorDevice_Adesto_ATXP032        = 'Adesto_ATXPxxx'
kFlexspiNorDevice_Cypress_S25FL128S     = 'Cypress_S25FSxxxS_S25FLxxxS'
kFlexspiNorDevice_Cypress_S26KS512S     = 'Cypress_S26KSxxxS_S26KLxxxS'
kFlexspiNorDevice_GigaDevice_GD25Q64C   = 'GigaDevice_GD25QxxxC'
kFlexspiNorDevice_GigaDevice_GD25LB256E = 'GigaDevice_GD25LBxxxE'
kFlexspiNorDevice_GigaDevice_GD25LT256E = 'GigaDevice_GD25LTxxxE'
kFlexspiNorDevice_GigaDevice_GD25LX256E = 'GigaDevice_GD25LXxxxE'
kFlexspiNorDevice_Winbond_W25Q128JV     = 'Winbond_W25QxxxJV'
kFlexspiNorDevice_Microchip_SST26VF064B = 'Microchip_SST26VFxxxB'
kFlexspiNorDevice_FudanMicro_FM25Q64    = 'FudanMicro_FM25Qxxx'
kFlexspiNorDevice_BoyaMicro_BY25Q16BS   = 'BoyaMicro_BY25QxxxBS'
kFlexspiNorDevice_XMC_XM25QH64B         = 'XMC_XM25QHxxxB_XM25QUxxxB'
kFlexspiNorDevice_XTXtech_X25Q64D       = 'XTXtech_X25FxxxB_X25QxxxD'
kFlexspiNorDevice_Puya_P25Q64LE         = 'Puya_P25QxxxLE_P25QxxxH_P25QxxxU'
kFlexspiNorDevice_AMIC_A25LQ64          = 'AMIC_A25LQxxx'

kFlexspiNorOpt0_ISSI_IS25LP064A       = 0xc0000007
kFlexspiNorOpt0_ISSI_IS26KS512S       = 0xc0233007
kFlexspiNorOpt0_MXIC_MX25L12845G      = 0xc0000007
kFlexspiNorOpt0_MXIC_MX25UM51245G     = 0xc0403037
kFlexspiNorOpt0_MXIC_MX25UM51345G     = 0xc0403007
kFlexspiNorOpt0_MXIC_MX25UM51345G_2nd = 0xc1503051
kFlexspiNorOpt1_MXIC_MX25UM51345G_2nd = 0x20000014
kFlexspiNorOpt0_Micron_MT25QL128A     = 0xc0000007
kFlexspiNorOpt0_Micron_MT35X          = 0xC0603005
kFlexspiNorOpt0_Adesto_AT25SF128A     = 0xc0000007
kFlexspiNorOpt0_Adesto_ATXP032        = 0xc0803007
kFlexspiNorOpt0_Cypress_S25FL128S     = 0xc0000007
kFlexspiNorOpt0_Cypress_S26KS512S     = 0xc0233007
kFlexspiNorOpt0_GigaDevice_GD25Q64C   = 0xc0000406
kFlexspiNorOpt0_GigaDevice_GD25LB256E = 0xc0000007
kFlexspiNorOpt0_GigaDevice_GD25LT256E = 0xc0000008
kFlexspiNorOpt0_GigaDevice_GD25LX256E = 0xc0600008
kFlexspiNorOpt0_Winbond_W25Q128JV     = 0xc0000207
kFlexspiNorOpt0_Microchip_SST26VF064B = 0xc0000005
kFlexspiNorOpt0_FudanMicro_FM25Q64    = 0xc0000205
kFlexspiNorOpt0_BoyaMicro_BY25Q16BS   = 0xc0000405
kFlexspiNorOpt0_XMC_XM25QH64B         = 0xc0000007
kFlexspiNorOpt0_XTXtech_X25Q64D       = 0xc0000407
kFlexspiNorOpt0_Puya_P25Q64LE         = 0xc0000405
kFlexspiNorOpt0_AMIC_A25LQ64          = 0xc0000105

kSemcNorDevice_None                  = 'No'
kSemcNorDevice_Micron_MT28EW128ABA   = 'Micron_MT28EW128ABA'
kSemcNorDevice_Micron_MT28UG128ABA   = 'Micron_MT28UG128ABA'

kSemcNorOpt0_Micron_MT28EW128ABA       = 0xD0000600
kSemcNorOpt0_Micron_MT28UG128ABA       = 0xD0000601

kAdvancedSettings_Tool      = 0
kAdvancedSettings_Cert      = 1
kAdvancedSettings_Sign      = 2
kAdvancedSettings_BD        = 3
kAdvancedSettings_OtpmkKey  = 4
kAdvancedSettings_UserKeys  = 5

kAppImageFormat_AutoDetect  = 'Auto-detect image format'
kAppImageFormat_AxfFromMdk  = '.out(axf) from Keil MDK'
kAppImageFormat_ElfFromIar  = '.out(elf) from IAR EWARM'
kAppImageFormat_AxfFromMcux = '.out(axf) from MCUXpresso'
kAppImageFormat_ElfFromGcc  = '.out(elf) from GCC ARM'
kAppImageFormat_MotoSrec    = 'Motorola S-Records (.srec/.s19)'
kAppImageFormat_IntelHex    = 'Intel Extended Hex (.hex)'
kAppImageFormat_RawBinary   = 'Raw Binary (.bin)'

kSoundEffectFilename_Success  = 'snd_success.wav'
kSoundEffectFilename_Failure  = 'snd_failure.wav'
kSoundEffectFilename_Progress = 'snd_progress.wav'
kSoundEffectFilename_Restart  = 'snd_restart.wav'

kMemBlockColor_Background = wx.WHITE
kMemBlockColor_Padding    = wx.BLACK

kSecureBootSeqStep_AllInOne     = 0
kSecureBootSeqStep_GenCert      = 1
kSecureBootSeqStep_GenImage     = 2
kSecureBootSeqStep_PrepHwCrypto = 3
kSecureBootSeqStep_ProgSrk      = 4
kSecureBootSeqStep_OperHwCrypto = 5
kSecureBootSeqStep_FlashImage   = 6
kSecureBootSeqStep_ProgDek      = 7

kPageIndex_ImageGenerationSequence = 0
kPageIndex_ImageLoadingSequence    = 1
kPageIndex_EfuseOperationUtility   = 2
kPageIndex_BootDeviceMemory        = 3
