#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

kLanguageIndex_English = 0x0
kLanguageIndex_Chinese = 0x1

kMenuPosition_File     = 0x0
kMenuPosition_Edit     = 0x1
kMenuPosition_View     = 0x2
kMenuPosition_Tools    = 0x3
kMenuPosition_Window   = 0x4
kMenuPosition_Help     = 0x5

kPanelIndex_GenSeq   = 0x0
kPanelIndex_LoadSeq  = 0x1
kPanelIndex_fuseUtil = 0x2
kPanelIndex_memView  = 0x3
kPanelIndex_LogView  = 0x4

kMainLanguageContentDict = {
        'menu_file':                          ['File',                                  u"文件"],
        'mItem_exit':                         ['Exit',                                  u"退出"],
        'menu_edit':                          ['Edit',                                  u"编辑"],
        'menu_view':                          ['View',                                  u"查看"],
        'menu_tools':                         ['Tools',                                 u"工具"],
        'subMenu_runMode':                    ['Run Mode',                              u"软件运行模式"],
        'mItem_runModeEntry':                 ['Entry',                                 u"入门级"],
        'mItem_runModeMaster':                ['Master',                                u"专家级"],
        'mItem_runModeOta':                   ['SBL OTA',                               u"OTA升级"],
        'subMenu_usbDetection':               ['USB Detection',                         u"USB识别模式"],
        'mItem_usbDetectionDynamic':          ['Dynamic',                               u"动态"],
        'mItem_usbDetectionStatic':           ['Static',                                u"静态"],
        'subMenu_genSbFile':                  ['Generate .sb file',                     u"生成.sb文件"],
        'mItem_genSbFileYes':                 ['Yes',                                   u"是"],
        'mItem_genSbFileNo':                  ['No',                                    u"否"],
        'subMenu_imageReadback':              ['Image Readback',                        u"程序回读"],
        'mItem_imageReadbackAutomatic':       ['Automatic',                             u"自动"],
        'mItem_imageReadbackManual':          ['Manual',                                u"手动"],
        'subMenu_flashloaderResident':        ['Flashloader Resident',                  u"Flashloader执行空间"],
        'mItem_flashloaderResidentDefault':   ['Default',                               u"默认"],
        'mItem_flashloaderResidentItcm':      ['ITCM',                                  u"ITCM"],
        'mItem_flashloaderResidentDtcm':      ['DTCM',                                  u"DTCM"],
        'mItem_flashloaderResidentOcram':     ['OCRAM',                                 u"OCRAM"],
        'subMenu_efuseGroup':                 ['eFuse Group',                           u"eFuse分组号"],
        'subMenu_efuseLocker':                ['eFuse Locker',                          u"eFuse锁定"],
        'mItem_efuseLockerAutomatic':         ['Automatic',                             u"自动"],
        'mItem_efuseLockerManual':            ['Manual',                                u"手动"],
        'subMenu_ivtEntryType':               ['IVT Entry Type',                        u"启动头IVT中Entry类型"],
        'mItem_ivtEntryReset':                ['Reset Handler',                         u"复位向量函数"],
        'mItem_ivtEntryVector':               ['Vector Table',                          u"中断向量表"],
        'subMenu_edgelockFwOpt':              ['Use Edgelock Fw',                       u"加载Edgelock固件"],
        'mItem_edgelockFwEn':                 ['Enable',                                u"使能"],
        'mItem_edgelockFwDis':                ['Disable',                               u"禁用"],
        'menu_window':                        ['Window',                                u"界面"],
        'subMenu_soundEffect':                ['Sound Effect',                          u"音效模式"],
        'mItem_soundEffectContra':            ['Contra',                                u"魂斗罗"],
        'mItem_soundEffectMario':             ['Mario',                                 u"马里奥"],
        'mItem_soundEffectQuiet':             ['Quiet',                                 u"静音"],
        'menu_help':                          ['Help',                                  u"帮助"],
        'mItem_homePage':                     ['Home Page',                             u"项目主页"],
        'mItem_aboutAuthor':                  ['About Author',                          u"关于作者"],
        'mItem_contributors':                 ['Contributors',                          u"贡献者名单"],
        'mItem_specialThanks':                ['Special Thanks',                        u"特别感谢"],
        'mItem_revisionHistory':              ['Revision History',                      u"版本历史"],

        'panel_targetSetup':                  ['Target Setup',                          u"目标器件设置"],
        'sText_mcuSeries':                    ['MCU Series:',                           u"微控制器系列："],
        'sText_mcuDevice':                    ['MCU Device:',                           u"微控制器型号："],
        'sText_bootDevice':                   ['Boot Device:',                          u"启动设备类型："],
        'button_bootDeviceConfiguration':     ['Boot Device Configuration',             u"启动设备配置"],
        'button_deviceConfigurationData':     ['Device Configuration Data (DCD)',       u"DCD数据配置"],
        'button_externalMemConfigurationData':['Ext Memory Configuration Data (XMCD)',  u"XMCD数据配置"],

        'panel_portSetup':                    ['Port Setup',                            u"下载接口设置"],
        'radioBtn_uart':                      ['UART',                                  u"串口"],
        'radioBtn_usbhid':                    ['USB-HID',                               u"HID设备"],
        'sText_comPort':                      ['COM Port:',                             u"端口号："],
        'sText_baudrate':                     ['Baudrate:',                             u"波特率："],
        'sText_vid':                          ['Vendor ID:',                            u"厂商识别号："],
        'sText_pid':                          ['Product ID:',                           u"产品识别号："],
        'checkBox_oneStepConnect':            ['One Step',                              u"一键连接"],
        'button_connect_black':               ['Connect to ROM',                        u"连接ROM"],
        'button_connect_yellow':              ['Connect to Flashloader',                u"连接Flashloader"],
        'button_connect_yellow_ota':          ['Connect to SBL ISP',                    u"连接SBL ISP组件"],
        'button_connect_green':               ['Configure boot device',                 u"配置启动设备"],
        'button_connect_blue':                ['Reset device',                          u"复位微控制器"],
        'button_connect_red':                 ['Reconnect',                             u"重新连接"],

        'panel_deviceStatus':                 ['Device Status',                         u"目标器件状态"],

        'sText_secureBootType':               ['Secure Boot Type',                      u"安全启动模式："],
        'button_allInOneAction':              ['All-In-One Action',                     u"一键启动"],
        'button_genSbFileAction':             ['Gen-Sb-File Action',                    u"一键生成"],

        'panel_genSeq':                       ['Image Generation Sequence',             u"       生成可启动程序       "],
        'sText_serial':                       ['Serial (8 digits):',                    u"序列号（仅8位数字）："],
        'sText_keyPass':                      ['key_pass (text):',                      u"密钥因子（任意字符）："],
        'button_advCertSettings':             ['Advanced Cert Settings',                u"配置认证参数"],
        'sText_certFmt':                      ['Certificate Format:',                   u"证书格式："],
        'sText_hashAlgo':                     ['Hash Algorithm:',                       u"哈希算法："],
        'button_genCert':                     ['Generate Certificate,SRK',              u"生成证书和SRK"],
        'sText_appPath':                      ['Application Image File:',               u"源应用程序镜像文件："],
        'sText_appBaseAddr':                  ['Base Address for Raw Binary Image:',    u"程序链接起始地址（仅Bin格式）："],
        'button_advSignSettings':             ['Advanced Signature Settings',           u"配置签名区域"],
        'sText_habCryptoAlgo':                ['HAB Encryption Algorithm:',             u"HAB加密算法："],
        'sText_enableCertForHwCrypto':        ['Enable Certificate for HW (BEE/OTFAD) Encryption:',                                           u"是否为硬件加密添加认证："],
        'button_genImage_u':                  ['Generate Unsigned Bootable Image',      u"生成裸启动程序"],
        'button_genImage_c':                  ['Generate CRC Bootable Image',           u"生成含CRC的可启动程序"],
        'button_genImage_s':                  ['Generate Signed Bootable Image',        u"生成含签名的可启动程序"],
        'button_genImage_se':                 ['Generate Encrypted Bootable Image,DEK', u"生成签名加密的可启动程序和DEK"],
        'sText_keyStorageRegion':             ['Key Storage Region:',                   u"密钥存储区域："],
        'sText_availHwCryptoEngines':         ['Max Available HW Crypto Engines:',      u"最大可用硬件加密引擎数："],
        'button_advKeySettings':              ['Advanced Key Settings',                 u"配置密钥参数"],
        'sText_hwCryptoAlgo':                 ['HW Encryption Algorithm:',              u"硬件加密算法："],
        'sText_maxFacCnt':                    ['Max Protection Regions:',               u"最大可保护区域数："],
        'button_prepHwCrypto_p':              ['Prepare For Encryption',                u"准备加密工作"],
        'button_prepHwCrypto_e':              ['Encrypt Bootable Image',                u"加密可启动程序"],

        'panel_loadSeq':                      ['Image Loading Sequence',                u"       下载可启动程序       "],
        'sText_srk256bit':                    ['Burn below SRK data\n (256bits) into Fuse\n SRK0-7 Region:',                                  u"烧写如下SRK数据进\nFuse SRK0-7区域："],
        'button_progSrk':                     ['Burn SRK data',                         u"烧录SRK数据"],
        'sText_hwCryptoKeyInfo':              ['Burn user DEK data \n (128bits * n) into below\n Region for HW Crypto:',                      u"烧写如下DEK进Fuse硬件\n密钥区域："],
        'button_operHwCrypto':                ['Burn DEK data',                         u"烧录DEK数据"],
        'sText_showImage':                    ['Program final bootable image\n to boot device:',                                              u"下载最终可启动应用程序镜像\n文件进启动设备："],
        'button_flashImage_u':                ['Load Unsigned Image',                   u"下载裸程序"],
        'button_flashImage_c':                ['Load CRC Image',                        u"下载含CRC的程序"],
        'button_flashImage_s':                ['Load Signed Image',                     u"下载已签名程序"],
        'button_flashImage_e':                ['Load Encrypted Image',                  u"下载已加密程序"],
        'sText_habDek128bit':                 ['Use below DEK data (128bits)\n to generate keyblob and\n program it to flash for HAB:',       u"根据如下DEK动态生成KeyBlob\n并下载进启动设备："],
        'button_progDek':                     ['Enable HAB, Load KeyBlob Data',         u"使能HAB,下载KeyBlob数据"],

        'panel_fuseUtil':                     ['eFuse Operation Utility',               u"       专用eFuse烧写       "],
        'button_scan':                        ['Scan',                                  u"扫描"],
        'button_burn':                        ['Burn',                                  u"烧写"],

        'panel_memView':                      ['Boot Device Memory',                    u"       通用Flash编程       "],
        'sText_memStart':                     ['Range Start/Offset:',                   u"区域首地址/偏移："],
        'sText_memLength':                    ['Range Length (Byte):',                  u"区域长度（字节）："],
        'sText_memBinFile':                   ['bin/s19/hex:',                          u"源文件："],
        'button_readMem':                     ['Range Read',                            u"区域回读"],
        'button_eraseMem':                    ['Range Erase',                           u"区域擦除"],
        'button_massEraseMem':                ['Chip Erase',                            u"芯片全擦"],
        'button_writeMem':                    ['Write (Auto Erase)',                    u"下载（含自动擦除）"],
        'button_eccWriteMem':                 ['ECC Write',                             u"下载（含ECC）"],
        'button_executeApp':                  ['Execute From Start',                    u"从首地址处执行"],
        'button_viewMem':                     ['View Bootable Image',                   u"回读查看标注的程序"],
        'button_clearMem':                    ['Clear The Screen',                      u"清除屏幕显示"],
        'checkBox_saveImageData':             ['Save image/data file to',               u"将程序/数据保存到"],

        'panel_logView':                      ['Boot Log Analyzer',                     u"       启动日志解析       "],
        'sText_logStart':                     ['Log Start:',                            u"日志首地址："],
        'sText_logLength':                    ['Log Length (Byte):',                    u"日志长度（字节）："],
        'sText_bootLogBinFile':               ['Log Data (.bin):',                       u"日志数据文件："],
        'button_viewBootLog':                 ['View Boot Log',                         u"解析启动日志"],
        'button_clearBootLog':                ['Clear The Screen',                      u"清除屏幕显示"],
        'checkBox_saveBootLog':               ['Save log context file to',              u"将解析后日志保存到"],

        'panel_cmdLog':                       ['Command Log',                           u"命令日志"],
        'button_clearCmdLog':                 ['Clear',                                 u"清除"],
        'button_SaveCmdLog':                  ['Save',                                  u"保存"],

}

kSubLanguageContentDict = {
        #cert
        'cert_title':                         ['Advanced Certificate Settings',         u"配置认证参数"],
        'panel_certOpt':                      ['Certificate Option',                    u"证书选项"],
        'sText_cstVersion':                   ['CST Version:',                          u"CST版本："],
        'sText_useExistingCaKey':             ['Use Existing CA Key:',                  u"复用已有CA密钥："],
        'sText_useEcc':                       ['Use Elliptic Curve Crypto:',            u"采用椭圆曲线加密："],
        'sText_pkiTreeKeyLen':                ['Key Length for PKI Tree (bits):',       u"PKI密钥比特长度："],
        'sText_pkiTreeDuration':              ['PKI Tree Duration (years):',            u"PKI保密时间（年）："],
        'sText_SRKs':                         ['Super Root Keys:',                      u"SRK密码组数："],
        'sText_caFlagSet':                    ['SRK Cert to have CA flag Set:',         u"证书CA标志选项："],
        'button_cert_ok':                     ['Ok',                                    u"确定"],
        'button_cert_cancel':                 ['Cancel',                                u"取消"],

        #sign
        'sign_title':                         ['Advanced Signature Settings',           u"配置签名区域"],
        'panel_signOpt':                      ['Signature Option',                      u"签名选项"],
        'sText_signPart':                     ['Sign Part of Image:',                   u"签名部分程序："],
        'sText_signStart0':                   ['Signed Region 0 Start:',                u"签名区域0起始地址："],
        'sText_signSize0':                    ['Signed Region 0 Size:',                 u"签名区域0长度："],
        'sText_signStart1':                   ['Signed Region 1 Start:',                u"签名区域1起始地址："],
        'sText_signSize1':                    ['Signed Region 1 Size:',                 u"签名区域1长度："],
        'sText_signStart2':                   ['Signed Region 2 Start:',                u"签名区域2起始地址："],
        'sText_signSize2':                    ['Signed Region 2 Size:',                 u"签名区域2长度："],
        'button_sign_ok':                     ['Ok',                                    u"确定"],
        'button_sign_cancel':                 ['Cancel',                                u"取消"],

        #dcd
        'dcd_title':                          ['Device Configuration Data',             u"配置DCD参数"],
        'panel_dcdOpt':                       ['DCD Option',                            u"DCD选项"],
        'sText_dcdSource':                    ['DCD Source:',                           u"DCD来源："],
        'sText_dcdBinFile':                   ['DCD bin file:',                         u"DCD bin文件："],
        'sText_dcdCfgFile':                   ['DCD cfg file:',                         u"DCD cfg文件："],
        'sText_dcdPurpose':                   ['DCD Purpose:',                          u"DCD用途："],
        'sText_sdramBase':                    ['SDRAM Base:',                           u"SDRAM基址："],
        'panel_dcdDesc':                      ['DCD Descriptor',                        u"DCD描述代码"],
        'sText_dcdModel':                     ['Device Model:',                         u"设备模型："],
        'button_dcd_ok':                      ['Ok',                                    u"确定"],
        'button_dcd_cancel':                  ['Cancel',                                u"取消"],

        #xmcd
        'xmcd_title':                         ['External Memory Configuration Data',    u"配置XMCD参数"],
        'sText_xmcdSource':                   ['XMCD Source:',                          u"XMCD来源："],
        'sText_memoryInterface':              ['Memory Interface:',                     u"存储外设接口："],
        'sText_interfaceInstance':            ['Interface Instance:',                   u"外设接口号："],
        'sText_configBlockType':              ['Config Block Type:',                    u"配置块类型："],
        'panel_flexspiRamOpt0':               ['FlexSPI RAM Option0',                   u"FlexSPI RAM选项0"],
        'sText_deviceSizeInMB':               ['Device Size (MB):',                     u"设备容量(MB)："],
        'panel_flexspiRamOpt1':               ['FlexSPI RAM Option1',                   u"FlexSPI RAM选项1"],
        'sText_ramConnection':                ['RAM Connection:',                       u"RAM连接方式："],
        'sText_dataPinmuxGroup':              ['Data Pinmux Group:',                    u"数据Pinmux组："],
        'sText_writeDummyCycles':             ['Write Dummy Cycles:',                   u"写时序冗余周期数："],
        'sText_readDummyCycles':              ['Read Dummy Cycles:',                    u"读时序冗余周期数："],
        'panel_semcSdramOpt':                 ['SEMC SDRAM Option',                     u"SEMC SDRAM选项"],
        'sText_clkFreq':                      ['Clk Freq (MHz):',                       u"时钟频率(MHz)："],
        'sText_deviceSizeInKB':               ['Device Size (KB):',                     u"设备容量(KB)："],
        'sText_xmcdBinFile':                  ['XMCD bin file:',                        u"XMCD bin文件："],
        'button_xmcd_ok':                     ['Ok',                                    u"确定"],
        'button_xmcd_cancel':                 ['Cancel',                                u"取消"],

        #flexspinor/quadspinor
        'flexspinor_title':                   ['FlexSPI NOR Device Configuration',      u"配置FlexSPI接口NOR Flash启动设备"],
        'quadspinor_title':                   ['QuadSPI NOR Device Configuration',      u"配置QuadSPI接口NOR Flash启动设备"],
        'sText_bootInstance':                 ['Boot Instance:',                        u"启动外设号："],
        'sText_deviceModel':                  ['Device Model:',                         u"设备模型："],
        'cBox_keepFdcb':                      ['Keep FDCB',                             u"保留原FDCB"],
        'panel_norOpt0':                      ['Nor Option0',                           u"NOR选项0"],
        'sText_deviceType':                   ['Device Type:',                          u"设备类型："],
        'sText_queryPads':                    ['Query Pads:',                           u"查询管脚数："],
        'sText_cmdPads':                      ['Cmd Pads:',                             u"命令管脚数："],
        'sText_quadModeSetting':              ['Quad Mode Setting:',                    u"四路模式设置："],
        'sText_miscMode':                     ['Misc Mode:',                            u"Misc模式："],
        'sText_maxFrequency':                 ['Max Frequency:',                        u"最大频率："],
        'sText_hasOption1':                   ['Has Option1:',                          u"是否有NOR选项1："],
        'panel_norOpt1':                      ['Nor Option1',                           u"NOR选项1"],
        'sText_flashConnection':              ['Flash Connection:',                     u"Flash连接方式："],
        'sText_driveStrength':                ['Drive Strength:',                       u"Pin驱动强度："],
        'sText_dqsPinmuxGroup':               ['DQS Pinmux Group:',                     u"DQS Pinmux组："],
        'sText_enableSecondPinmux':           ['Enable Second Pinmux:',                 u"使能第二组Pinmux："],
        'sText_statusOverride':               ['Status Override:',                      u"状态位覆盖："],
        'sText_dummyCycles':                  ['Dummy Cycles:',                         u"冗余周期数："],
        'panel_dualImageOpt':                 ['Dual Image Option',                     u"双程序启动选项"],
        'sText_dualImage0Version':            ['Image 0 Version(0-65535):',             u"程序0版本(0-65535)："],
        'sText_dualImage1Version':            ['Image 1 Version(0-65535):',             u"程序1版本(0-65535)："],
        'sText_dualImage1Offset':             ['Image 1 Offset:',                       u"程序1偏移地址："],
        'sText_dualImage1Size':               ['Image 1 Size:',                         u"程序1大小："],
        'button_completeFdcb':                ['Complete FDCB CFG (512bytes)',          u"完整FDCB配置(512字节)"],
        'button_flexspinor_ok':               ['Ok',                                    u"确定"],
        'button_flexspinor_cancel':           ['Cancel',                                u"取消"],

        #flexspinand
        'flexspinand_title':                  ['FlexSPI NAND Device Configuration',     u"配置FlexSPI接口NAND Flash启动设备"],
        'sText_flashSize':                    ['Flash Size:',                           u"Flash容量："],
        'sText_hasMultiplanes':               ['Has Multiplanes:',                      u"多层情况："],
        'sText_pagesPerBlock':                ['Pages Per Block:',                      u"每块所含页个数："],
        'sText_nandPageSize':                 ['Page Size:',                            u"页大小："],
        'sText_manufacturerId':               ['Manufacturer ID:',                      u"厂商代码："],
        'sText_addressType':                  ['Address Type:',                         u"地址类型："],
        'button_flexspinand_ok':              ['Ok',                                    u"确定"],
        'button_flexspinand_cancel':          ['Cancel',                                u"取消"],

        #lpspinor
        'lpspinor_title':                     ['LPSPI NOR/EEPROM Device Configuration', u"配置LPSPI接口NOR/EEPROM启动设备"],
        'flexcommspinor_title':               ['Flexcomm SPI NOR Device Configuration', u"配置Flexcomm SPI接口NOR Flash启动设备"],
        'panel_memOpt':                       ['Memory Option',                         u"存储器选项"],
        'sText_pageSize':                     ['Page Size (Bytes):',                    u"页大小(B)："],
        'sText_sectorSize':                   ['Sector Size (KBytes):',                 u"扇区大小（KB）："],
        'sText_totalSize':                    ['Total Size (KBytes):',                  u"总容量（KB）："],
        'panel_spiOpt':                       ['Spi Option',                            u"SPI选项"],
        'sText_spiIndex':                     ['Spi Index:',                            u"Spi编号："],
        'sText_spiPcs':                       ['Spi Pcs:',                              u"Spi片选："],
        'sText_spiSpeed':                     ['Spi Speed:',                            u"Spi速度："],
        'button_lpspinor_ok':                 ['Ok',                                    u"确定"],
        'button_lpspinor_cancel':             ['Cancel',                                u"取消"],

        #semcnand
        'semcnand_title':                     ['SEMC NAND Device Configuration',        u"配置SEMC接口NAND Flash启动设备"],
        'panel_nandOpt':                      ['Nand Option',                           u"Nand选项"],
        'sText_onfiVersion':                  ['ONFI Version:',                         u"ONFI版本："],
        'sText_onfiTimingMode':               ['ONFI Timing Mode:',                     u"ONFI速度模式："],
        'sText_edoMode':                      ['EDO Mode:',                             u"EDO模式："],
        'sText_ioPortSize':                   ['I/O Port Size:',                        u"I/O端口宽度："],
        'sText_pcsPort':                      ['PCS Port:',                             u"片选端口："],
        'sText_eccType':                      ['ECC Type:',                             u"ECC类型："],
        'sText_eccStatus':                    ['Initial ECC status:',                   u"初始ECC状态："],
        'panel_fcbOpt':                       ['FCB Option',                            u"FCB选项"],
        'sText_searchCount':                  ['Search Count:',                         u"搜索次数："],
        'sText_searchStride':                 ['Search Stride:',                        u"搜索步长："],
        'sText_imageCopies':                  ['Image Copies:',                         u"程序总备份数："],
        'panel_imageInfo':                    ['Image Info',                            u"程序信息"],
        'sText_blockIndex':                   ['Block Index:',                          u"所在块索引："],
        'sText_blockCount':                   ['Block Count:',                          u"所占块个数："],
        'button_semcnand_ok':                 ['Ok',                                    u"确定"],
        'button_semcnand_cancel':             ['Cancel',                                u"取消"],

        #usdhcsd
        'usdhcsd_title':                      ['uSDHC SD Device Configuration',         u"配置uSDHC接口SD卡启动设备"],
        'panel_sdOpt':                        ['SD Option',                             u"SD卡选项"],
        'sText_instance':                     ['Instance:',                             u"uSDHC序号："],
        'sText_busWidth':                     ['Bus Width:',                            u"总线宽度："],
        'sText_timingInterface':              ['Timing Interface:',                     u"总线时序模式："],
        'sText_enablePowerCycle':             ['Enable Power Cycle:',                   u"使能供电时序："],
        'sText_powerPolarity':                ['Power Polarity:',                       u"供电极性"],
        'sText_powerUpTime':                  ['Power Up Time:',                        u"上电时间："],
        'sText_powerDownTime':                ['Power Down Time:',                      u"掉电时间："],
        'button_usdhcsd_ok':                  ['Ok',                                    u"确定"],
        'button_usdhcsd_cancel':              ['Cancel',                                u"取消"],

        #usdhcmmc
        'usdhcmmc_title':                     ['uSDHC (e)MMC Device Configuration',     u"配置uSDHC接口MMC卡启动设备"],
        'panel_mmcOpt0':                      ['MMC Option0',                           u"MMC卡选项0"],
        'sText_partitionAccess':              ['Partition Access:',                     u"分割访问权限："],
        'sText_enableBootConfig':             ['Enable Boot Config:',                   u"使能启动配置："],
        'sText_bootBusWidth':                 ['Boot Bus Width:',                       u"启动总线宽度："],
        'sText_bootMode':                     ['Boot Mode:',                            u"启动模式："],
        'sText_enableBootPartition':          ['Enable Boot Partition:',                u"使能启动分割："],
        'sText_enableBootAck':                ['Enable Boot Ack:',                      u"使能启动确认："],
        'sText_resetBootBusConditions':       ['Reset Boot Bus Conditions:',            u"复位启动总线条件："],
        'panel_mmcOpt1':                      ['MMC Option1',                           u"MMC卡选项1"],
        'sText_enable1V8':                    ['Enable 1.8V:',                          u"使能1.8V："],
        'button_usdhcmmc_ok':                 ['Ok',                                    u"确定"],
        'button_usdhcmmc_cancel':             ['Cancel',                                u"取消"],

        #bee/otfad otpmk
        'otpmkKey_title':                     ['Advanced Key Settings - Fixed OTPMK',   u"配置预设OTPMK密钥参数"],
        'panel_encryptionOpt':                ['Encryption Option',                     u"加密选项"],
        'sText_keySource':                    ['Key Source:',                           u"密钥源："],
        'sText_aesMode':                      ['AES Mode:',                             u"AES模式："],
        'sText_regionCnt':                    ['Region Count:',                         u"加密区域总数："],
        'sText_redundantImageOffset':         ['Redundant Image Offset (in 256KB):',    u"备份程序偏移（以256KB为单位）："],
        'panel_regionInfo':                   ['Encrypted Region Info',                 u"加密区域信息"],
        'sText_regionStart':                  ['Region Start:',                         u"区域首地址："],
        'sText_regionLength':                 ['Region Length:',                        u"区域长度："],
        'button_otpmkkey_ok':                 ['Ok',                                    u"确定"],
        'button_otpmkkey_cancel':             ['Cancel',                                u"取消"],

        #bee/otfad user key
        'userKey_title':                      ['Advanced Key Settings - Flexible User', u"配置灵活用户密钥参数"],
        'panel_encryptionOpt':                ['Encryption Option',                     u"加密选项"],
        'sText_xipBaseAddr':                  ['XIP Base Address:',                     u"XIP基址："],
        'button_userkeys_genRandomKey':       ['Generate Random User Key',              u"产生随机用户密钥"],
        'button_userkeys_ok':                 ['Ok',                                    u"确定"],
        'button_userkeys_cancel':             ['Cancel',                                u"取消"],

        #bee user key
        'sText_engineSel':                    ['Engine Selection:',                     u"引擎选择："],
        'sText_beeEngKeySel':                 ['BEE Engine Key Selection:',             u"BEE引擎密钥选择："],
        'sText_imageType':                    ['Image Type:',                           u"程序类型："],
        'panel_engine0Info':                  ['BEE Engine 0 Info',                     u"BEE引擎0信息"],
        'panel_engine1Info':                  ['BEE Engine 1 Info',                     u"BEE引擎1信息"],
        'sText_enginexkeySource':             ['Key Source:',                           u"用户密钥源："],
        'sText_enginexUserKeyData':           ['User Key Data (16-bytes):',             u"用户密钥（16字节）："],
        'sText_enginexAesMode':               ['AES Mode:',                             u"AES模式："],
        'sText_enginexFacCnt':                ['Protected Region Count:',               u"受保护区域个数："],
        'sText_enginexFac0Start':             ['Protected Region 0 Start:',             u"受保护区域0首地址："],
        'sText_enginexFac0Length':            ['Protected Region 0 Length:',            u"受保护区域0长度："],
        'sText_enginexFac1Start':             ['Protected Region 1 Start:',             u"受保护区域1首地址："],
        'sText_enginexFac1Length':            ['Protected Region 1 Length:',            u"受保护区域1长度："],
        'sText_enginexFac2Start':             ['Protected Region 2 Start:',             u"受保护区域2首地址："],
        'sText_enginexFac2Length':            ['Protected Region 2 Length:',            u"受保护区域2长度："],
        'sText_enginexAccessPermision':       ['Access Permision:',                     u"访问权限："],
        'sText_enginexLock':                  ['Region Lock:',                          u"区域锁定："],

        #otfad user key
        'sText_totalRegions':                 ['Total Regions:',                        u"区域总数："],
        'sText_kekSource':                    ['Kek Source:',                           u"全局密钥源："],
        'sText_kekData':                      ['Kek Data (16-bytes):',                  u"全局密钥（16字节）："],
        'sText_scrambleAlgo':                 ['Scramble Algorithm:',                   u"扰乱算法："],
        'sText_scrambleAlignment':            ['Scramble Alignment:',                   u"扰乱对齐："],
        'panel_region0Info':                  ['OTFAD Region 0 Info',                   u"OTFAD区域0信息"],
        'panel_region1Info':                  ['OTFAD Region 1 Info',                   u"OTFAD区域1信息"],
        'panel_region2Info':                  ['OTFAD Region 2 Info',                   u"OTFAD区域2信息"],
        'panel_region3Info':                  ['OTFAD Region 3 Info',                   u"OTFAD区域3信息"],
        'sText_regionxUserKeyData':           ['User Key Data (16-bytes):',             u"用户密钥（16字节）："],
        'sText_regionxCounterData':           ['Counter Data (8-bytes):',               u"硬件计数器（8字节）："],
        'sText_regionxFacStart':              ['Protected Region Start:',               u"受保护区域首地址："],
        'sText_regionxFacLength':             ['Protected Region Length:',              u"受保护区域长度："],
        'sText_regionxLock':                  ['Region Lock:',                          u"区域锁定："],
        'button_userkeys_genRandomKek':       ['Generate Random Kek',                   u"产生随机全局密钥"],
}

kRevision_1_0_0_en =  "【v1.0.0】 - 2018.12\n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1021, i.MXRT1051/1052, i.MXRT1061/1062, i.MXRT1064 SIP \n" + \
                      "     2. Support both UART and USB-HID serial downloader modes \n" + \
                      "     3. Support various user application image file formats (elf/axf/srec/hex/bin) \n" + \
                      "     4. Can validate the range and applicability of user application image \n" + \
                      "     5. Support for converting bare image into bootable image \n" + \
                      "     6. Support for loading bootable image into FlexSPI NOR and SEMC NAND boot devices \n" + \
                      "     7. Support for loading bootable image into LPSPI NOR/EEPROM recovery boot device \n" + \
                      "     8. Support DCD which can help configure device(eg. SDRAM) \n" + \
                      "     9. Support development boot case (Unsigned) \n" + \
                      "    10. Support HAB encryption secure boot case (Signed only, Signed and Encrypted) \n" + \
                      "    11. Can back up certificate with time stamp \n" + \
                      "    12. Support BEE encryption secure boot case (SNVS Key, User Keys) \n" + \
                      "    13. Support common eFuse memory operation \n" + \
                      "    14. Support common boot device memory operation \n" + \
                      "    15. Support for reading back and marking bootable image(NFCB/DBBT/FDCB/EKIB/EPRDB/IVT/Boot Data/DCD/Image/CSF/DEK KeyBlob) from boot device \n\n"
kRevision_1_0_0_zh = u"【v1.0.0】 - 2018.12\n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT全系列MCU，包含i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP \n" + \
                     u"     2. 支持UART和USB-HID两种串行下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     3. 支持五种常用格式(elf/axf/srec/hex/bin)裸源image文件输入并检查其链接地址的合法性 \n" + \
                     u"     4. 能够检查用户源image文件的适用性与合法性 \n" + \
                     u"     5. 支持将裸源image文件自动转换成i.MXRT能启动的Bootable image \n" + \
                     u"     6. 支持下载Bootable image进主动启动设备 - FlexSPI NOR、SEMC NAND接口Flash \n" + \
                     u"     7. 支持下载Bootable image进备份启动设备 - LPSPI接口NOR/EEPROM Flash \n" + \
                     u"     8. 支持DCD配置功能，可用于加载image进SDRAM执行 \n" + \
                     u"     9. 支持用于开发阶段的非安全加密启动（未签名加密） \n" + \
                     u"    10. 支持基于HAB实现的安全加密启动（单签名，签名和加密） \n" + \
                     u"    11. 能够自动备份证书并用时间戳记录 \n" + \
                     u"    12. 支持基于BEE实现的安全加密启动（唯一SNVS key，用户自定义key） \n" + \
                     u"    13. 支持MCU芯片内部eFuse的回读和烧写操作（即专用eFuse烧写器） \n" + \
                     u"    14. 支持外部启动设备的任意读写擦操作（即通用Flash编程器） \n" + \
                     u"    15. 支持从外部启动设备回读Bootable image，并对其组成部分（NFCB/DBBT/FDCB/EKIB/EPRDB/IVT/Boot Data/DCD/Image/CSF/DEK KeyBlob）进行标注 \n\n"
kRevision_1_1_0_en =  "【v1.1.0】 - 2019.01\n" + \
                      "  Feature: \n" + \
                      "     1. Support i.MXRT1015 \n" + \
                      "     2. Add Language option in Menu/View and support Chinese\n" + \
                      "  Improvement: \n" + \
                      "     1. USB device auto-detection can be disabled \n" + \
                      "     2. Original image can be a bootable image (with IVT&BootData/DCD) \n" + \
                      "     3. Show boot sequence page dynamically according to action \n" + \
                      "  Interest: \n" + \
                      "     1. Add sound effect (Mario) \n\n"
kRevision_1_1_0_zh = u"【v1.1.0】 - 2019.01\n" + \
                     u"  特性: \n" + \
                     u"     1. 支持i.MXRT1015 \n" + \
                     u"     2. 支持界面中文显示\n" + \
                     u"  改进: \n" + \
                     u"     1. USB自动识别的功能可以禁掉 \n" + \
                     u"     2. 用户输入的源程序文件可以包含i.MXRT启动头 (IVT&BootData/DCD) \n" + \
                     u"     3. 根据操作过程自动跟随显示操作页面 \n" + \
                     u"  个性: \n" + \
                     u"     1. 增加马里奥音效 \n\n"
kRevision_1_2_0_en =  "【v1.2.0】 - 2019.04\n" + \
                      "  Feature: \n" + \
                      "     1. Can generate .sb file by all-in-one action for MfgTool and RT-Flash \n" + \
                      "     2. Can show cost time along with gauge \n" + \
                      "  Improvement: \n" + \
                      "     1. Non-XIP image can also be supported for BEE Encryption case \n" + \
                      "     2. Display guage in real time \n" + \
                      "  Bugfix: \n" + \
                      "     1. Region count cannot be set more than 1 for Fixed OTPMK Key case \n" + \
                      "     2. Option1 field is not implemented for FlexSPI NOR configuration \n\n"
kRevision_1_2_0_zh = u"【v1.2.0】 - 2019.04\n" + \
                     u"  特性: \n" + \
                     u"     1. 支持生成.sb格式的应用程序(通过all-in-one按钮)，可用于MfgTool和RT-Flash \n" + \
                     u"     2. 可以实时显示操作消耗的时间，随着进度条同步更新 \n" + \
                     u"  改进: \n" + \
                     u"     1. BEE加密模式下也能支持Non-XIP应用程序 \n" + \
                     u"     2. 进度条可以实时更新，更新速度由快到慢 \n" + \
                     u"  修复: \n" + \
                     u"     1. 使用Fixed OTPMK Key的BEE加密模式下，加密区域不能被设超过1 \n" + \
                     u"     2. FlexSPI NOR启动设备配置界面，Option1不能被有效设置 \n\n"
kRevision_1_3_0_en =  "【v1.3.0】 - 2019.04\n" + \
                      "  Feature: \n" + \
                      "     1. Can generate .sb file by actions in efuse operation utility window \n" + \
                      "  Improvement: \n" + \
                      "     1. HAB signed mode should not appliable for FlexSPI/SEMC NOR device Non-XIP boot with RT1020/1015 ROM \n" + \
                      "     2. HAB encrypted mode should not appliable for FlexSPI/SEMC NOR device boot with RT1020/1015 ROM \n" + \
                      "     3. Multiple .sb files(all, flash, efuse) should be generated if there is efuse operation in all-in-one action \n" + \
                      "     4. Can generate .sb file without board connection when boot device type is NOR \n" + \
                      "     5. Automatic image readback can be disabled to save operation time \n" + \
                      "     6. The text of language option in menu bar should be static and easy understanding \n" + \
                      "  Bugfix: \n" + \
                      "     1. Cannot generate bootable image when original image (hex/bin) size is larger than 64KB \n" + \
                      "     2. Cannot download large image file (eg 6.8MB) in some case \n" + \
                      "     3. There is language switch issue with some dynamic labels \n" + \
                      "     4. Some led demos of RT1050 EVKB board are invalid \n\n"
kRevision_1_3_0_zh = u"【v1.3.0】 - 2019.04\n" + \
                     u"  特性: \n" + \
                     u"     1. 支持生成仅含自定义efuse烧写操作(在efuse operation windows里指定)的.sb格式文件 \n" + \
                     u"  改进: \n" + \
                     u"     1. HAB签名模式在i.MXRT1020/1015下应不支持从FlexSPI NOR/SEMC NOR启动设备中Non-XIP启动 \n" + \
                     u"     2. HAB加密模式在i.MXRT1020/1015下应不支持从FlexSPI NOR/SEMC NOR启动设备中启动 \n" + \
                     u"     3. 当All-In-One操作中包含efuse烧写操作时，会生成3个.sb文件(全部操作、仅flash操作、仅efuse操作) \n" + \
                     u"     4. 当启动设备是NOR型Flash时，可以不用连接板子直接生成.sb文件 \n" + \
                     u"     5. 一键操作下的自动程序回读可以被禁掉，用以节省操作时间 \n" + \
                     u"     6. 菜单栏里的语言选项标签应该是静态且易于理解的(中英双语同时显示) \n" + \
                     u"  修复: \n" + \
                     u"     1. 当输入的源image文件格式为hex或者bin且其大小超过64KB时，生成可启动程序会失败 \n" + \
                     u"     2. 当输入的源image文件非常大时(比如6.8MB)，下载可能会超时失败 \n" + \
                     u"     3. 当切换显示语言时，有一些控件标签(如Connect按钮)不能实时更新 \n" + \
                     u"     4. /apps目录下RT1050 EVKB板子的一些LED demo是无效的 \n\n"
kRevision_1_4_0_en =  "【v1.4.0】 - 2019.05\n" + \
                      "  Feature: \n" + \
                      "     1. Support for loading bootable image into uSDHC SD/eMMC boot device  \n" + \
                      "     2. Provide friendly way to view and set mixed eFuse fields  \n" + \
                      "  Improvement: \n" + \
                      "     1. Set default FlexSPI NOR device to align with  NXP EVK boards \n" + \
                      "     2. Enable real-time gauge for Flash Programmer actions \n\n"
kRevision_1_4_0_zh = u"【v1.4.0】 - 2019.05\n" + \
                     u"  特性: \n" + \
                     u"     1. 支持下载Bootable image进主动启动设备 - uSDHC接口SD/eMMC卡 \n" + \
                     u"     2. 支持更直观友好的方式去查看/设置某些混合功能的eFuse区域 \n" + \
                     u"  改进: \n" + \
                     u"     1. 默认FlexSPI NOR device应与恩智浦官方EVK板卡相匹配 \n" + \
                     u"     2. 为通用Flash编程器里的操作添加实时进度条显示 \n\n"
kRevision_2_0_0_en =  "【v2.0.0】 - 2019.07\n" + \
                      "  Feature: \n" + \
                      "     1. [RTxxx] Support i.MXRT5xx A0, i.MXRT6xx A0 \n" + \
                      "     2. [RTyyyy] Support i.MXRT1011, i.MXRT117x A0 \n" + \
                      "     3. [RTyyyy] Support OTFAD encryption secure boot case (SNVS Key, User Key) \n" + \
                      "     4. [RTxxx] Support both UART and USB-HID ISP modes \n" + \
                      "     5. [RTxxx] Support for converting bare image into bootable image \n" + \
                      "     6. [RTxxx] Original image can be a bootable image (with FDCB) \n" + \
                      "     7. [RTxxx] Support for loading bootable image into FlexSPI/QuadSPI NOR boot device \n" + \
                      "     8. [RTxxx] Support development boot case (Unsigned, CRC) \n" + \
                      "     9. Add Execute action support for Flash Programmer \n" + \
                      "    10. [RTyyyy] Can show FlexRAM info in device status  \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Improve stability of USB connection of i.MXRT105x board \n" + \
                      "     2. Can write/read RAM via Flash Programmer \n" + \
                      "     3. [RTyyyy] Provide Flashloader resident option to adapt to different FlexRAM configurations \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Sometimes tool will report error \"xx.bat file cannot be found\" \n" + \
                      "     2. [RTyyyy] Editing mixed eFuse fields is not working as expected \n" + \
                      "     3. [RTyyyy] Cannot support 32MB or larger LPSPI NOR/EEPROM device \n" + \
                      "     4. Cannot erase/read the last two pages of boot device via Flash Programmer \n\n"
kRevision_2_0_0_zh = u"【v2.0.0】 - 2019.07\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTxxx] 支持i.MXRT5xx A0, i.MXRT6xx A0 \n" + \
                     u"     2. [RTyyyy] 支持i.MXRT1011, i.MXRT117x A0 \n" + \
                     u"     3. [RTyyyy] 支持基于OTFAD实现的安全加密启动（唯一SNVS key，用户自定义key） \n" + \
                     u"     4. [RTxxx] 支持UART和USB-HID两种串行编程方式（COM端口/USB设备自动识别） \n" + \
                     u"     5. [RTxxx] 支持将裸源image文件自动转换成i.MXRT能启动的Bootable image \n" + \
                     u"     6. [RTxxx] 用户输入的源程序文件可以包含i.MXRT启动头 (FDCB) \n" + \
                     u"     7. [RTxxx] 支持下载Bootable image进主动启动设备 - FlexSPI/QuadSPI NOR接口Flash \n" + \
                     u"     8. [RTxxx] 支持用于开发阶段的非安全加密启动（未签名，CRC校验） \n" + \
                     u"     9. 在通用Flash编程器模式下增加执行(跳转)操作 \n" + \
                     u"    10. [RTyyyy] 支持在device status里显示当前FlexRAM配置情况 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 提高i.MXRT105x目标板USB连接稳定性 \n" + \
                     u"     2. 通用Flash编程器里也支持读写RAM \n" + \
                     u"     3. [RTyyyy] 提供Flashloader执行空间选项以适应不同的FlexRAM配置 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 有时候生成证书时会提示bat文件无法找到，导致证书无法生成 \n" + \
                     u"     2. [RTyyyy] 可视化方式去编辑混合eFuse区域并没有生效 \n" + \
                     u"     3. [RTyyyy] 无法支持32MB及以上容量的LPSPI NOR/EEPROM设备 \n" + \
                     u"     4. 在通用Flash编程器模式下无法擦除/读取外部启动设备的最后两个Page \n\n"
kRevision_2_1_0_en =  "【v2.1.0】 - 2019.12\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support for loading bootable image into SEMC NOR boot device \n" + \
                      "     2. [RTyyyy] Support operation under both CM7 and CM4 of RT117x A0 \n" + \
                      "     3. [RTyyyy] Support two FlexSPI map addresses for RT117x A0 \n" + \
                      "     4. [RTyyyy] Support efuse memory operation for RT117x A0 \n" + \
                      "     5. [RTyyyy] Can import user fuse table file to set efuse value \n" + \
                      "     6. [RTyyyy] Enable OTFAD encryption secure boot mode (User Key) for RT117x A0 \n" + \
                      "     7. [RTyyyy] Support RT1170/1010 bootable image from SDK as source input \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Lock word should be placed at the end of operation when generating user efuse .sb file \n" + \
                      "     2. [RTyyyy] Image format auto detection can be used for axf file from MCUX or GCC \n" + \
                      "     3. Specify file path instead of file to save readback data \n" + \
                      "     4. If readback data is enabled to be saved in file, then it will not displayed on the screen \n" + \
                      "  Bugfix: \n" + \
                      "     1. 'Cmd Pads' is not set correctly for some typical octal-flash models in FlexSPI NOR configuration \n" + \
                      "     2. 'Max Frequency' option is not exactly aligned with selected MCU device in FlexSPI NOR configuration \n" + \
                      "     3. [RTyyyy] Cannot show total size of SD/eMMC correctly, so SD/eMMC cannot be programmed \n" + \
                      "     4. [RTyyyy] Cannot save eMMC device configuration \n" + \
                      "     5. [RTyyyy] Some fields are not aligned with selected MCU device in Flexible User Key Setting \n" + \
                      "     6. [RTyyyy] Cannot generate bootable image when original image size is less than 4KB \n" + \
                      "     7. [RTyyyy] Sometimes tool cannot recognize .axf format from MCUX or Keil MDK \n" + \
                      "     8. [RTyyyy] Signed flashloader cannot be generated if DCD is enabled \n" + \
                      "     9. [RTyyyy] Cannot mark DCD in readback image if it comes from source bootable image \n" + \
                      "  Interest: \n" + \
                      "     1. Add sound effect (Contra) \n\n"
kRevision_2_1_0_zh = u"【v2.1.0】 - 2019.12\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持下载Bootable image进主动启动设备 - SEMC NOR接口Flash \n" + \
                     u"     2. [RTyyyy] 在RT1170无论是CM7还是CM4作为主核下均能正常工作 \n" + \
                     u"     3. [RTyyyy] 支持RT1170的两个FlexSPI XIP映射地址 \n" + \
                     u"     4. [RTyyyy] 支持RT1170的eFuse回读与烧写 \n" + \
                     u"     5. [RTyyyy] 支持导入用户fuse配置文件去设置fuse \n" + \
                     u"     6. [RTyyyy] 为RT1170 A0开启OTFAD加密(User Key)支持 \n" + \
                     u"     7. [RTyyyy] 支持RT1170/RT1010 SDK生成的Bootable image作为源文件输入 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 生成用户efuse烧录sb文件时应将lock位操作放在最后面 \n" + \
                     u"     2. [RTyyyy] 程序格式自动检测选项也可用于MCUX生成的axf格式源文件 \n" + \
                     u"     3. 指定目录而不是指定文件去存放回读的数据 \n" + \
                     u"     4. 如果回读的数据已经选择保存到文件中，那么点击Read按钮将不会在窗口显示数据 \n" + \
                     u"  修复: \n" + \
                     u"     1. 在FlexSPI NOR配置界面里，对于一些octal-flash模型，其Cmd Pads参数没有被正确设置 \n" + \
                     u"     2. 在FlexSPI NOR配置界面里，Max Frequency参数选项与当前MCU型号不完全匹配 \n" + \
                     u"     3. [RTyyyy] SD/eMMC总容量未能正确显示，导致无法编程SD/eMMC \n" + \
                     u"     4. [RTyyyy] 无法正常保存默认eMMC设备配置(主要是Partition Access参数) \n" + \
                     u"     5. [RTyyyy] 在用户自定义Key设置界面里，有些选项与当前选中的MCU型号不匹配 \n" + \
                     u"     6. [RTyyyy] 当输入的源image文件大小小于4KB时，生成可启动程序会失败 \n" + \
                     u"     7. [RTyyyy] 有时候无法识别MCUX或Keil MDK生成的axf格式源文件 \n" + \
                     u"     8. [RTyyyy] 当DCD使能的时候，无法生成含签名的Flashloader \n" + \
                     u"     9. [RTyyyy] 如果DCD来自源Bootable image，则无法在读回的image中标记DCD \n" + \
                     u"  个性: \n" + \
                     u"     1. 增加魂斗罗音效 \n\n"
kRevision_2_2_0_en =  "【v2.2.0】 - 2019.12\n" + \
                      "  Feature: \n" + \
                      "     1. [RTxxx] Support i.MXRT6xx B0, switch to FlexSPI NOR boot device \n" + \
                      "     2. [RTxxx] Support for loading bootable image into Flexcomm SPI NOR recovery boot device \n" + \
                      "     3. [RTxxx] Support otp memory operation \n\n"
kRevision_2_2_0_zh = u"【v2.2.0】 - 2019.12\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTxxx] 将i.MXRT6xx B0启动设备从QuadSPI NOR切换到FlexSPI NOR \n" + \
                     u"     2. [RTxxx] 支持下载Bootable image进主动启动设备 - Flexcomm SPI接口NOR Flash \n" + \
                     u"     3. [RTxxx] 支持OTP回读与烧写 \n\n"
kRevision_2_3_0_en =  "【v2.3.0】 - 2020.05\n" + \
                      "  Feature: \n" + \
                      "     1. [RTxxx] Support i.MXRT5xx B0/1 \n" + \
                      "     2. [RTxxx] Add more selections of FlexSPI NOR model \n" + \
                      "     3. Support complete FDCB as FlexSPI NOR device model \n" + \
                      "  Improvement: \n" + \
                      "     1. Can show ROM/Flashloader version info in device status window \n" + \
                      "     2. Provide option to keep FDCB from source image file \n" + \
                      "     3. [RTyyyy] Provide fuse lock control option for secure boot cases \n" + \
                      "  Bugfix: \n" + \
                      "     1. Sometimes fuse/otp programming returns error status \n" + \
                      "     2. Sometimes it cannot show correct flash memory info \n" + \
                      "     3. [RTyyyy] Erase region for FDCB is incorrect in generated sb-file \n" + \
                      "     4. [RTyyyy] fuse lock programming limitation doesn't exist in all RT devices \n\n"
kRevision_2_3_0_zh = u"【v2.3.0】 - 2020.05\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTxxx] 支持i.MXRT5xx B0/1 \n" + \
                     u"     2. [RTxxx] 在FlexSPI NOR模型参数里增加更多选项 \n" + \
                     u"     3. 支持512字节完整的FDCB配置作为FlexSPI NOR模型 \n" + \
                     u"  改进: \n" + \
                     u"     1. 可以在目标器件状态窗口显示ROM/Flashloader的版本信息 \n" + \
                     u"     2. 提供保留源image文件里的FDCB头的选项设置 \n" + \
                     u"     3. [RTyyyy] 加密启动模式下，提供烧进fuse的用户密钥锁定设置 \n" + \
                     u"  修复: \n" + \
                     u"     1. 有时候烧写fuse/otp时会返回错误状态 \n" + \
                     u"     2. 有时候配置flash时无法显示其Page/Sector/Block Size信息 \n" + \
                     u"     3. [RTyyyy] 生成的.sb文件里擦除FDCB区域的长度指定有误 \n" + \
                     u"     4. [RTyyyy] Fuse Lock烧写限制不是存在于所有i.MXRT型号 \n\n"
kRevision_2_3_1_en =  "【v2.3.1】 - 2020.08\n" + \
                      "  Improvement: \n" + \
                      "     1. Can recognize source bootable image if FDCB doesn't start from offset 0 \n" + \
                      "     2. [RTyyyy] Do some blank check if erase unit is always 64KB in flashloader \n" + \
                      "  Bugfix: \n" + \
                      "     1. Read or Erase does sometimes not use correct parameters \n" + \
                      "     2. Setting spi speed option for 1bit SPI NOR device doesn't take effect \n" + \
                      "     3. [RTyyyy] Cannot edit fuse cfg0 for RT1011 in friendly way \n\n"
kRevision_2_3_1_zh = u"【v2.3.1】 - 2020.08\n" + \
                     u"  改进: \n" + \
                     u"     1. 可以支持FDCB位置不在偏移0地址的Bootable Image作为源文件 \n" + \
                     u"     2. [RTyyyy] 在使用Flashloader里擦除操作时，某些情况下需要先检查目标区域是否为空 \n" + \
                     u"  修复: \n" + \
                     u"     1. 当连接得到的flash Page/Sector/Block Size信息有误时，无法做进一步下载 \n" + \
                     u"     2. 设置恢复启动设备(1bit SPI NOR)的速度选项不生效 \n" + \
                     u"     3. [RTyyyy] 在RT1011下，无法确认fuse cfg0区域的可视化设置 \n\n"
kRevision_2_4_0_en =  "【v2.4.0】 - 2020.10\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT117x B0 \n" + \
                      "     2. [RTyyyy] Can recognize custom compiled flashloader to use \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTxxx] Complete OTP memory operation \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Fix issue when using FlexibleUserKeys for OTFAD encryption \n\n"
kRevision_2_4_0_zh = u"【v2.4.0】 - 2020.10\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持i.MXRT117x B0 \n" + \
                     u"     2. [RTyyyy] 可以自动识别使用由用户生成的Flashloader \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTxxx] 完善OTP烧写范围支持 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 解决OTFAD加密模式下使用Flexible User Keys报错的问题 \n\n"
kRevision_3_0_0_en =  "【v3.0.0】 - 2021.01\n" + \
                      "  Feature: \n" + \
                      "     1. [Kinetis] Support Kinetis with ROM \n" + \
                      "     2. [Kinetis] Support both UART and USB-HID download modes \n" + \
                      "     3. [Kinetis] Support for loading bootable image into FTFx NOR Flash \n" + \
                      "     4. [Kinetis] Support development boot case (Unsigned) \n" + \
                      "     5. [LPC] Support LPC5500 Series(550x/551x/552x/55S6x) \n" + \
                      "     6. [LPC] Support both UART and USB-HID download modes \n" + \
                      "     7. [LPC] Support for loading bootable image into C040HD NOR Flash \n" + \
                      "     8. [LPC] Support development boot case (Unsigned) \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTxxx] Cannot restore user image info (path, base, format) of last time setting \n\n"
kRevision_3_0_0_zh = u"【v3.0.0】 - 2021.01\n" + \
                     u"  特性: \n" + \
                     u"     1. [Kinetis] 支持所有含ROM的Kinetis系列 \n" + \
                     u"     2. [Kinetis] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     3. [Kinetis] 支持下载Bootable image进内部Flash \n" + \
                     u"     4. [Kinetis] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"     5. [LPC] 支持LPC5500系列(550x/551x/552x/55S6x) \n" + \
                     u"     6. [LPC] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     7. [LPC] 支持下载Bootable image进内部Flash \n" + \
                     u"     8. [LPC] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTxxx] 不能恢复上一次用户源应用程序设置(文件路径、基地址、格式) \n\n"
kRevision_3_1_0_en =  "【v3.1.0】 - 2021.01\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT1024 SIP \n" + \
                      "     2. [Kinetis] Support Kinetis K32L \n\n"
kRevision_3_1_0_zh = u"【v3.1.0】 - 2021.01\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持i.MXRT1024 SIP \n" + \
                     u"     2. [Kinetis] 支持Kinetis K32L系列 \n\n"
kRevision_3_1_1_en =  "【v3.1.1】 - 2021.01\n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Fix UART download issue for RT1170 \n\n"
kRevision_3_1_1_zh = u"【v3.1.1】 - 2021.01\n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 修复RT1170下UART口无法正常下载问题 \n\n"
kRevision_3_2_0_en =  "【v3.2.0】 - 2021.03\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT116x \n" + \
                      "     2. [RTxxx] Support SB file generation for RT500/600 \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Fix .SB file generation issue for RT1170 \n\n"
kRevision_3_2_0_zh = u"【v3.2.0】 - 2021.03\n" + \
                     u"  特性: \n" + \
                      "     1. [RTyyyy] 支持i.MXRT116x \n" + \
                     u"     2. [RTxxx] 支持RT500/600下SB文件生成 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 修复RT1170下SB文件无法正常生成问题 \n\n"
kRevision_3_3_0_en =  "【v3.3.0】 - 2021.05\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Can sign part of user application \n" + \
                      "     2. [RT/LPC] Support ISP downloading for SBL target \n" + \
                      "     3. Support more image formats (hex/s19) in Programmer \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Both entry point address and vector table address can be set as IVT.entry \n\n"
kRevision_3_3_0_zh = u"【v3.3.0】 - 2021.05\n" + \
                     u"  特性: \n" + \
                      "     1. [RTyyyy] 支持对源image文件进行部分签名 \n" + \
                      "     2. [RT/LPC] 支持SBL设备的ISP下载 \n" + \
                      "     3. 通用编程器模式下增加支持带格式源image文件(hex/s19) \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 启动头IVT中entry参数既支持设为复位函数也支持中断向量表 \n\n"
kRevision_3_3_1_en =  "【v3.3.1】 - 2021.09\n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTxxx/LPC] Cannot connect to SBL target \n" + \
                      "     2. [LPC] Cannot r/w SBL target \n\n"
kRevision_3_3_1_zh = u"【v3.3.1】 - 2021.09\n" + \
                     u"  修复: \n" + \
                     u"     1. [RTxxx/LPC] 修复SBL设备无法连接的问题 \n" + \
                     u"     2. [LPC] 修复SBL设备无法擦写的问题 \n\n"
kRevision_3_4_0_en =  "【v3.4.0】 - 2022.03\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support for loading bootable image into FlexSPI NAND boot device  \n" + \
                      "     2. Add memory mass erase support \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Support bootable image generated from SDK 2.10 \n\n"
kRevision_3_4_0_zh = u"【v3.4.0】 - 2022.03\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持下载Bootable image进主动启动设备 - FlexSPI NAND接口Flash \n" + \
                     u"     2. 支持对启动设备进行全擦操作 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 支持SDK 2.10及其之后生成的可启动文件作为源文件 \n\n"
kRevision_3_5_0_en =  "【v3.5.0】 - 2022.03\n" + \
                      "  Feature: \n" + \
                      "     1. [RT] Provide dual image download option for FlexSPI NOR device \n" + \
                      "     2. [RTxxx] Add support for uSDHC SD/eMMC boot device \n" + \
                      "     3. [RTyyyy] Support XECC write for RT1160/1170 \n" + \
                      "     4. [RTyyyy] Enable SD/eMMC 2nd instance support for RT10xx \n" + \
                      "  Improvement: \n" + \
                      "     1. [RT] Can keep image version header from source bootable image file \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RT] Fix bit width recover issue in eMMC settings \n" + \
                      "     2. [RTxxx] Fix Plain CRC image boot support issue \n" + \
                      "     3. [RTyyyy] Correct M7SRK efuse idx for RT1170 \n" + \
                      "     4. [RTyyyy] Correct Auth HW engine type for RT1170 \n\n"
kRevision_3_5_0_zh = u"【v3.5.0】 - 2022.03\n" + \
                     u"  特性: \n" + \
                     u"     1. [RT] 提供FlexSPI NOR设备的双程序启动设置选项 \n" + \
                     u"     2. [RTxxx] 新增SD/eMMC启动设备支持 \n" + \
                     u"     3. [RTyyyy] 为RT1160/1170 FlexSPI NOR设备增加ECC方式写入支持 \n" + \
                     u"     4. [RTyyyy] 使能RT10xx系列上SD/eMMC设备第二组接口支持 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RT] 能保留含启动头源image文件中的程序版本信息 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RT] 修复eMMC设备配置时位宽度参数无法保存问题 \n" + \
                     u"     2. [RTxxx] 修复Plain CRC启动模式下不可用的问题 \n" + \
                     u"     3. [RTyyyy] 修复RT1170下M7SRK efuse位置定义错误问题 \n" + \
                     u"     4. [RTyyyy] 修复RT1170下HAB验签硬件引擎类型选择错误问题 \n\n"
kRevision_4_0_0_en =  "【v4.0.0】 - 2023.01\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT1061X/1062X \n" + \
                      "     2. [RTyyyy] Support i.MXRT1042 \n" + \
                      "     3. [LPC] Support LPC5500 Series(553x/S3x) \n" + \
                      "     4. [MCX] Support MCXN94x/N54x \n" + \
                      "     5. [MCX] Support both UART and USB-HID download modes \n" + \
                      "     6. [MCX] Support for loading bootable image into C040HD NOR Flash \n" + \
                      "     7. [MCX] Support development boot case (Unsigned) \n" + \
                      "  Improvement: \n" + \
                      "     1. [RT] Can set free RAM addresses for loading temporary data \n" + \
                      "     2. [RTyyyy] Can set Serial NOR flash option for SiP device(RT1024/RT1064) \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Use SECv5 version flashloader of RT116x/RT117x to fix FlexSPI NAND issue \n\n"
kRevision_4_0_0_zh = u"【v4.0.0】 - 2023.01\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持i.MXRT1061X/1062X \n" + \
                     u"     2. [RTyyyy] 支持i.MXRT1042 \n" + \
                     u"     3. [LPC] 支持LPC5500系列(553x/S3x) \n" + \
                     u"     4. [MCX] 支持MCXN94x/N54x \n" + \
                     u"     5. [MCX] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     6. [MCX] 支持下载Bootable image进内部Flash \n" + \
                     u"     7. [MCX] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"  改进: \n" + \
                     u"     1. [RT] 支持用户配置空闲RAM地址用于加载临时数据 \n" + \
                     u"     2. [RTyyyy] 对于SiP芯片（(RT1024/RT1064)）支持设置串行 NOR flash 选项 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 对于RT116x/RT117x，切换使用SECv5里的Flashloader以修复串行NAND烧写问题 \n\n"
kRevision_4_1_0_en =  "【v4.1.0】 - 2023.03\n" + \
                      "  Feature: \n" + \
                      "     1. [Kinetis] Support MKE13Z/14Z/15Z/17Z \n" + \
                      "     2. [Kinetis] Support MKW45/K32W148 \n" + \
                      "     3. Support two more Octal NOR devices (ISSI, Winbond) \n\n"
kRevision_4_1_0_zh = u"【v4.1.0】 - 2023.03\n" + \
                     u"  特性: \n" + \
                     u"     1. [Kinetis] 支持MKE13Z/14Z/15Z/17Z \n" + \
                     u"     2. [Kinetis] 支持MKW45/K32W148 \n" + \
                     u"     3. 支持来自ISSI和Winbond的Octal Flash \n\n"
kRevision_4_1_1_en =  "【v4.1.1】 - 2023.04\n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] It doesn't take effect in DCD Descriptor window \n\n"
kRevision_4_1_1_zh = u"【v4.1.1】 - 2023.04\n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 在DCD Desc窗口输入内容不生效 \n\n"
kRevision_5_0_0_en =  "【v5.0.0】 - 2023.05\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT118x A0 \n" + \
                      "     2. [RT1180] Support raw app file(not bootable app) as source image \n" + \
                      "     3. [RT1180] Support both UART and USB-HID download modes \n" + \
                      "     4. [RT1180] Support development boot case (Unsigned) \n" + \
                      "     5. [RT1180] Support FlexSPI NOR boot device \n" + \
                      "     6. [RT1180] Support uSDHC SD&MMC boot device \n\n"
kRevision_5_0_0_zh = u"【v5.0.0】 - 2023.05\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持i.MXRT118x A0 \n" + \
                     u"     2. [RT1180] 支持裸应用程序文件作为输入源文件 \n" + \
                     u"     3. [RT1180] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     4. [RT1180] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"     5. [RT1180] 支持FlexSPI NOR启动设备 \n" + \
                     u"     6. [RT1180] 支持uSDHC SD&MMC启动设备 \n\n"
kRevision_5_1_0_en =  "【v5.1.0】 - 2023.05\n" + \
                      "  Feature: \n" + \
                      "     1. [RT1180] Support edgelock FW \n\n"
kRevision_5_1_0_zh = u"【v5.1.0】 - 2023.05\n" + \
                     u"  特性: \n" + \
                     u"     1. [RT1180] 支持自动加载Edgelock固件 \n\n"
kRevision_5_2_0_en =  "【v5.2.0】 - 2023.07\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support i.MXRT118x B0 \n" + \
                      "     2. [RT] Support both secure and non-secure addr CM33 image for FlexSPI NOR device \n" + \
                      "     3. [RT] Support aliased addr image for FlexSPI NOR device \n" + \
                      "  Improvement: \n" + \
                      "     1. [RT1180] Original image can be a bootable image (with Container) \n\n"
kRevision_5_2_0_zh = u"【v5.2.0】 - 2023.07\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持i.MXRT118x B0 \n" + \
                     u"     2. [RT] 对于FlexSPI NOR设备，支持下载安全与非安全两种地址链接的CM33程序 \n" + \
                     u"     3. [RT] 对于FlexSPI NOR设备，支持别名地址链接的程序 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RT1180] 用户输入的源程序文件可以包含启动头 (Container) \n\n"
kRevision_5_2_1_en =  "【v5.2.1】 - 2023.07\n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Fix support for FlexSPI NAND device \n\n"
kRevision_5_2_1_zh = u"【v5.2.1】 - 2023.07\n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 修复对FlexSPI NAND设备的下载支持 \n\n"
kRevision_5_3_0_en =  "【v5.3.0】 - 2023.09\n" + \
                      "  Feature: \n" + \
                      "     1. [RTyyyy] Support XMCD which can help configure FlexSPI RAM/SEMC SDRAM \n" + \
                      "     2. [RTyyyy] Support secondary FlexSPI instance for NAND boot \n" + \
                      "     3. [RT] Add FlexSPI NAND device model support \n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Change FlexSPI instance selection from menu to config win \n" + \
                      "     2. [RTyyyy] Can recognize Non-XIP image which is linked in FlexSPI RAM region \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Cannot recognize bootable image which offset of reset handler to vector is less than 0xB00 \n\n"
kRevision_5_3_0_zh = u"【v5.3.0】 - 2023.09\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTyyyy] 支持XMCD配置功能，可用于加载image进FlexSPI RAM/SEMC SDRAM执行 \n" + \
                     u"     2. [RTyyyy] 支持第二个FlexSPI去下载启动NAND \n" + \
                     u"     3. [RT] 新增FlexSPI NAND启动设备模型支持 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 将FlexSPI序号选择从菜单栏改至设备配置界面 \n" + \
                     u"     2. [RTyyyy] 可以识别链接在FlexSPI RAM区域的程序 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 无法识别IVT中复位函数地址相对向量表首地址偏移小于0xB00的可启动程序文件 \n\n"
kRevision_5_3_1_en =  "【v5.3.1】 - 2023.09\n" + \
                      "  Improvement: \n" + \
                      "     1. [RT] Can validate the xip region range of different FlexSPI instance \n" + \
                      "     2. [RTxxx] Can recognize Non-XIP image which is linked in FlexSPI RAM region \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RT1180] Cannot generate bootable image for some Non-XIP images under FlexSPI NOR \n\n"
kRevision_5_3_1_zh = u"【v5.3.1】 - 2023.09\n" + \
                     u"  改进: \n" + \
                     u"     1. [RT] 可以检查不同FlexSPI序号的有效XIP范围 \n" + \
                     u"     2. [RTxxx] 可以识别链接在FlexSPI RAM区域的程序 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RT1180] 在FlexSPI NOR启动设备下无法生成一些Non-XIP程序的可启动程序 \n\n"
kRevision_5_3_2_en =  "【v5.3.2】 - 2023.10\n" + \
                      "  Improvement: \n" + \
                      "     1. [RTyyyy] Add XMCD support for RT1180 \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] XMCD write dummy cycles setting doesn't take affect \n\n"
kRevision_5_3_2_zh = u"【v5.3.2】 - 2023.10\n" + \
                     u"  改进: \n" + \
                     u"     1. [RTyyyy] 使能 RT1180 的 XMCD 支持 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] XMCD配置界面里write dummy cycle设置不生效 \n\n"
kRevision_6_0_0_en =  "【v6.0.0】 - 2023.11\n" + \
                      "  Feature: \n" + \
                      "     1. [Wireless] Support K32W0x1 \n" + \
                      "     2. [Wireless] Support RW61x \n" + \
                      "     3. [RW61x] Support raw app file(not bootable app) as source image \n" + \
                      "     4. [RW61x] Support both UART and USB-HID download modes \n" + \
                      "     5. [RW61x] Support development boot case (Unsigned) \n" + \
                      "     6. [RW61x] Support FlexSPI NOR boot device \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RTyyyy] Fix support for 2nd FlexSPI NOR instance \n" + \
                      "     2. [RTxxx] Fix support for FlexSPI NOR device \n\n"
kRevision_6_0_0_zh = u"【v6.0.0】 - 2023.11\n" + \
                     u"  特性: \n" + \
                     u"     1. [Wireless] 支持K32W0x1 \n" + \
                     u"     2. [Wireless] 支持RW61x \n" + \
                     u"     3. [RW61x] 支持裸应用程序文件作为输入源文件 \n" + \
                     u"     4. [RW61x] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     5. [RW61x] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"     6. [RW61x] 支持FlexSPI NOR启动设备 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RTyyyy] 修复对第二个FlexSPI NOR设备的下载支持 \n" + \
                     u"     2. [RTxxx] 修复对FlexSPI NOR设备的下载支持 \n\n"
kRevision_6_1_0_en =  "【v6.1.0】 - 2023.12\n" + \
                      "  Feature: \n" + \
                      "     1. [RTxxx] Support i.MXRT700 A0 \n" + \
                      "     2. [RT700] Support raw app file(not bootable app) as source image \n" + \
                      "     3. [RT700] Support both UART and USB-HID download modes \n" + \
                      "     4. [RT700] Support development boot case (Unsigned) \n" + \
                      "     5. [RT700] Support XSPI NOR boot device \n\n"
kRevision_6_1_0_zh = u"【v6.1.0】 - 2023.12\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTxxx] 支持i.MXRT700 A0 \n" + \
                     u"     2. [RT700] 支持裸应用程序文件作为输入源文件 \n" + \
                     u"     3. [RT700] 支持UART和USB-HID两种下载方式（COM端口/USB设备自动识别） \n" + \
                     u"     4. [RT700] 支持用于开发阶段的非安全加密启动（未签名） \n" + \
                     u"     5. [RT700] 支持XSPI NOR启动设备 \n\n"
kRevision_6_2_0_en =  "【v6.2.0】 - 2024.03\n" + \
                      "  Feature: \n" + \
                      "     1. [RT700] Support boot device connected to secondary XSPI \n" + \
                      "  Bugfix: \n" + \
                      "     1. [RT700] Fix download error when FDCB area in NOR flash is not blank \n" + \
                      "     2. [RT700] Fix support for Non-XIP image when it is linked in secure SRAM  \n\n"
kRevision_6_2_0_zh = u"【v6.2.0】 - 2024.03\n" + \
                     u"  特性: \n" + \
                     u"     1. [RT700] 支持下载程序进第二个XSPI上连接的启动设备 \n" + \
                     u"  修复: \n" + \
                     u"     1. [RT700] 当NOR Flash的FDCB区域非空时，下载可能报错 \n" + \
                     u"     2. [RT700] 当待下载程序链接在安全SRAM地址时，下载会报错 \n\n"
kRevision_6_3_0_en =  "【v6.3.0】 - 2024.09\n" + \
                      "  Feature: \n" + \
                      "     1. [RT] Can support parsing ROM boot log\n" + \
                      "  Improvement: \n" + \
                      "     1. [RT] Can set range erase alignment for FlexSPI NOR device \n" + \
                      "     2. [RT1170] Add support for Infineon octal flash S28H \n\n"
kRevision_6_3_0_zh = u"【v6.3.0】 - 2024.09\n" + \
                     u"  特性: \n" + \
                     u"     1. [RT] 可以支持获取并解析ROM启动日志 \n" + \
                     u"  改进: \n" + \
                     u"     1. [RT] 对FlexSPI NOR设备做擦除时，可自定义对齐长度 \n" + \
                     u"     2. [RT1170] 增加对英飞凌S28H系列Octal Flash支持 \n\n"
kRevision_6_4_0_en =  "【v6.4.0】 - 2025.03\n" + \
                      "  Feature: \n" + \
                      "     1. [RTxxx] Support i.MXRT700 B0\n" + \
                      "  Improvement: \n" + \
                      "     1. Better character alignment in boot device memory window \n\n"
kRevision_6_4_0_zh = u"【v6.4.0】 - 2025.03\n" + \
                     u"  特性: \n" + \
                     u"     1. [RTxxx] 支持i.MXRT700 B0\n" + \
                     u"  改进: \n" + \
                     u"     1. 通用编程器窗口显示等宽字符显示 \n\n"

kMsgLanguageContentDict = {
        'homePage_title':                     ['Home Page',                             u"项目主页"],
        'homePage_info':                      ['https://github.com/JayHeng/NXP-MCUBootUtility.git \n',                             u"https://github.com/JayHeng/NXP-MCUBootUtility.git \n"],
        'aboutAuthor_title':                  ['About Author',                          u"关于作者"],
        'aboutAuthor_author':                 [u"Author:  痞子衡 \n",                   u"作者：痞子衡 \n"],
        'aboutAuthor_email1':                 ['Email:     jie.heng@nxp.com \n',        u"邮箱：jie.heng@nxp.com \n"],
        'aboutAuthor_email2':                 ['Email:     hengjie1989@foxmail.com \n', u"邮箱：hengjie1989@foxmail.com \n"],
        'aboutAuthor_blog':                   [u"Blog:      痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n",                   u"博客：痞子衡嵌入式 https://www.cnblogs.com/henjay724/ \n"],
        'contributors_title':                 ['Contributors',                          u"贡献者名单"],
        'contributors_info':                  [u"李嘉奕Joyeee、祁凯Kelvin、范全有James \n",                                        u"李嘉奕Joyeee、祁凯Kelvin、范全有James \n"],
        'specialThanks_title':                ['Special Thanks',                        u"特别感谢"],
        'specialThanks_info':                 [u"Special thanks to 周小朋Clare、杨帆、刘华东Howard、沈浩杰Jayson \n",              u"特别感谢我亲爱的同事们：周小朋Clare、杨帆、刘华东Howard、沈浩杰Jayson \n"],
        'revisionHistory_title':              ['Revision History',                      u"版本历史"],
        'revisionHistory_v1_0_0':             [kRevision_1_0_0_en,                      kRevision_1_0_0_zh],
        'revisionHistory_v1_1_0':             [kRevision_1_1_0_en,                      kRevision_1_1_0_zh],
        'revisionHistory_v1_2_0':             [kRevision_1_2_0_en,                      kRevision_1_2_0_zh],
        'revisionHistory_v1_3_0':             [kRevision_1_3_0_en,                      kRevision_1_3_0_zh],
        'revisionHistory_v1_4_0':             [kRevision_1_4_0_en,                      kRevision_1_4_0_zh],
        'revisionHistory_v2_0_0':             [kRevision_2_0_0_en,                      kRevision_2_0_0_zh],
        'revisionHistory_v2_1_0':             [kRevision_2_1_0_en,                      kRevision_2_1_0_zh],
        'revisionHistory_v2_2_0':             [kRevision_2_2_0_en,                      kRevision_2_2_0_zh],
        'revisionHistory_v2_3_0':             [kRevision_2_3_0_en,                      kRevision_2_3_0_zh],
        'revisionHistory_v2_3_1':             [kRevision_2_3_1_en,                      kRevision_2_3_1_zh],
        'revisionHistory_v2_4_0':             [kRevision_2_4_0_en,                      kRevision_2_4_0_zh],
        'revisionHistory_v3_0_0':             [kRevision_3_0_0_en,                      kRevision_3_0_0_zh],
        'revisionHistory_v3_1_0':             [kRevision_3_1_0_en,                      kRevision_3_1_0_zh],
        'revisionHistory_v3_1_1':             [kRevision_3_1_1_en,                      kRevision_3_1_1_zh],
        'revisionHistory_v3_2_0':             [kRevision_3_2_0_en,                      kRevision_3_2_0_zh],
        'revisionHistory_v3_3_0':             [kRevision_3_3_0_en,                      kRevision_3_3_0_zh],
        'revisionHistory_v3_3_1':             [kRevision_3_3_1_en,                      kRevision_3_3_1_zh],
        'revisionHistory_v3_4_0':             [kRevision_3_4_0_en,                      kRevision_3_4_0_zh],
        'revisionHistory_v3_5_0':             [kRevision_3_5_0_en,                      kRevision_3_5_0_zh],
        'revisionHistory_v4_0_0':             [kRevision_4_0_0_en,                      kRevision_4_0_0_zh],
        'revisionHistory_v4_1_0':             [kRevision_4_1_0_en,                      kRevision_4_1_0_zh],
        'revisionHistory_v4_1_1':             [kRevision_4_1_1_en,                      kRevision_4_1_1_zh],
        'revisionHistory_v5_0_0':             [kRevision_5_0_0_en,                      kRevision_5_0_0_zh],
        'revisionHistory_v5_1_0':             [kRevision_5_1_0_en,                      kRevision_5_1_0_zh],
        'revisionHistory_v5_2_0':             [kRevision_5_2_0_en,                      kRevision_5_2_0_zh],
        'revisionHistory_v5_2_1':             [kRevision_5_2_1_en,                      kRevision_5_2_1_zh],
        'revisionHistory_v5_3_0':             [kRevision_5_3_0_en,                      kRevision_5_3_0_zh],
        'revisionHistory_v5_3_1':             [kRevision_5_3_1_en,                      kRevision_5_3_1_zh],
        'revisionHistory_v5_3_2':             [kRevision_5_3_2_en,                      kRevision_5_3_2_zh],
        'revisionHistory_v6_0_0':             [kRevision_6_0_0_en,                      kRevision_6_0_0_zh],
        'revisionHistory_v6_1_0':             [kRevision_6_1_0_en,                      kRevision_6_1_0_zh],
        'revisionHistory_v6_2_0':             [kRevision_6_2_0_en,                      kRevision_6_2_0_zh],
        'revisionHistory_v6_3_0':             [kRevision_6_3_0_en,                      kRevision_6_3_0_zh],
        'revisionHistory_v6_4_0':             [kRevision_6_4_0_en,                      kRevision_6_4_0_zh],

        'bootDeviceInfo_hasOnchipSerialNor':  ['MCU has on-chip QSPI NOR Flash (4MB, 133MHz), so you don\'t need to configure this boot device!',
                                              u"微控制器内置4MB的QSPI NOR Flash，所以无需配置该启动设备！"],
        'connectError_cannotSetOneStep':      ['One Step mode cannot be set under Entry Mode, Please switch to Master Mode and try again!',
                                              u"在软件入门级模式下，[一键连接]模式不可改，请切换到软件专家级模式下再试！"],
        'connectError_InvalidUserFl':         ['Cannot recognize user flashloader file, please check linker address of flashloader!',
                                              u"无法识别flashloader_user.srec文件，请检查该flashloader地址链接是否合法！"],
        'connectError_failToJumpToFl':        ['MCU has entered ROM SDP mode but failed to jump to Flashloader, Please reset board and try again!',
                                              u"微控制器已成功进入ROM SDP模式，但是未能跳转进入Flashloader，请复位板子再试！"],
        'connectError_doubleCheckBmod':       ['Make sure that you have put MCU in SDP (Serial Downloader Programming) mode (BMOD[1:0] pins = 2\'b01)!',
                                              u"请检查BMOD[1:0]引脚状态是否为2\'b01以确认微控制器处于ROM SDP模式！"],
        'connectError_failToPingFl':          ['Failed to ping Flashloader, Please reset board and consider updating flashloader.srec file under /src/targets/ then try again!',
                                              u"微控制器未能与Flashloader建立连接，请复位板子并考虑更新/src/targets/目录下相应的flashloader.srec文件再试！"],
        'connectError_failToPingSblIsp':      ['Failed to ping SBL ISP component, Please double check it is SBL target !',
                                              u"微控制器未能与SBL ISP组件建立连接，请确认当前设备已集成SBL功能！"],
        'connectError_failToCfgBootDevice':   ['MCU has entered Flashloader but failed to configure external memory, Please reset board and set proper boot device then try again!',
                                              u"微控制器已与Flashloader建立连接，但是未能识别启动设备。请复位板子并配置正确的启动设备再试！"],
        'connectError_hasnotCfgBootDevice':   ['Please configure boot device via Flashloader first!',
                                              u"请先借助Flashloader去完成启动设备的配置！"],
        'connectError_hasnotEnterFl':         ['Please connect to Flashloader first!',
                                              u"请先连接到Flashloader！"],
        'certGenError_notEnabledForHwCrypto': ['Certificate is not enabled for HW Crypto, You can enable it then try again!',
                                              u"当前硬件加密启动模式下没有使能认证，请先使能认证再试！"],
        'certGenError_noNeedToSetForUnsigned':['No need to set certificate option when booting unsigned image!',
                                              u"当前裸启动开发模式下不需要配置认证参数！"],
        'certGenError_noNeedToGenForUnsigned':['No need to generate certificate when booting unsigned image!',
                                              u"当前裸启动开发模式下不需要生成证书！"],
        'certGenInfo_reuseOldCert':           ["There is available certificate, Do you want to reuse existing certificate? \n",
                                              u"当前目录下已有证书文件，你想复用已有的证书吗？"],
        'certGenInfo_haveNewCert':            ["New certificate will be different even you don’t change any settings, Do you really want to have new certificate? \n",
                                              u"即使不改任何认证参数，新证书也会不同于已有证书，你依旧想生成新证书吗？"],
        'keyGenError_onlyForHwCrypto':        ['Key setting is only available when booting HW encrypted image in FlexSPI NOR device!',
                                              u"配置密钥参数仅在硬件加密启动模式下有效！"],
        'operHabError_notAppliableDevice':    ['HAB encryption is not appliable for FlexSPI NOR/SEMC NOR device under selected MCU device!',
                                              u"HAB加密操作在选中的微控制器型号下不支持FlexSPI NOR/SEMC NOR启动设备！"],
        'operHwCryptoError_onlyForHwCrypto':  ['HW encryption is only available when booting HW encrypted image in FlexSPI NOR device!',
                                              u"硬件加密操作仅在硬件加密启动模式下有效！"],
        'operHwCryptoError_onlyForFlexspiNor':['Action is not available because HW encryption boot is only designed for FlexSPI NOR device!',
                                              u"该操作仅在硬件加密启动模式下有效！"],
        'operHwCryptoError_failToPrepareForSnvs':  ['Failed to prepare for fixed OTPMK SNVS encryption, Please reset board and try again!',
                                              u"未能准备好OTPMK SNVS加密，请复位板子再试！！"],
        'operKeyError_srkNotForUnsigned':     ['No need to burn SRK data when booting unsigned image!',
                                              u"当前裸启动开发模式下不需要烧写SRK！"],
        'operKeyError_dekOnlyForHwCrypto':    ['HW Crypto DEK Burning is only available when booting HW encrypted image in FlexSPI NOR device!',
                                              u"烧写DEK操作仅在硬件加密启动模式下有效！"],
        'operKeyError_dekNotForSnvs':         ['No need to burn HW Crypto DEK data as OTPMK key is selected!',
                                              u"当前选择OTPMK SNVS区域存储密钥下不需要烧写DEK！"],
        'operMemError_notAvailUnderEntry':    ['Common memory operation is not available under Entry Mode, Please switch to Master Mode and try again!',
                                              u"在软件入门级模式下，通用Flash操作没有使能，请切换到软件专家级模式下再试！"],
        'separActnError_notAvailUnderEntry':  ['Separated action is not available under Entry Mode, You should use All-In-One Action!',
                                              u"在软件入门级模式下，单步操作不被支持，请直接使用[一键启动]！"],
        'operImgError_failToFlashImage':      ['Failed to flash bootable image into external memory, Please reset board and try again!',
                                              u"未能将应用程序下载进启动设备，请复位板子再试！！"],
        'operImgError_keyBlobOnlyForHab':     ['KeyBlob loading is only available when booting HAB encrypted image!',
                                              u"下载KeyBlob操作仅在HAB加密启动模式下有效！"],
        'operImgError_hasnotFlashImage':      ['Please flash image into boot device first!',
                                              u"请先将应用程序下载进启动设备！"],

        'inputError_illegalFormat':           ['Illegal input detected! You should input like this format: 0x5000',
                                              u"检测到非法输入!参考合法格式示例为: 0x5000（十六进制）"],

        'inputError_serial':                  ['Serial must be 8 digits!',
                                              u"序列号必须是8位数字!"],
        'inputError_keyPass':                 ['You forget to set key_pass!',
                                              u"密钥因子没有设置正确！"],
        'genImgError_vectorNotFound':         ['Cannot find the vector table address in this bootable image file: ',
                                              u"无法根据该可启动文件IVT头找到有效中断向量表地址: "],
        'genImgError_formatNotValid':         ['Cannot recognize/convert the format of image file: ',
                                              u"无法识别/转换该程序文件格式: "],
        'genImgError_bypassXmcd':             ['XMCD is bypassed due to DCD! For this case, you can download bootable binary under Programmer mode.',
                                              u"因为DCD的存在导致XMCD被忽略了! 这种情况建议使用通用编程器模式去下载"],
        'genDcdError_failToGen':              ['DCD binary is not generated successfully! Check your DCD descriptor file and make sure you don\'t put the tool in path with blank space!',
                                              u"DCD文件未成功生成!检查DCD描述符文件, 并确保NXP-MCUBootUtility工具的路径中没有空格!"],
        'srcImgError_invalidVector':          ['Invalid vector address found in image file: ',
                                              u"该程序文件起始链接地址是无效的:"],
        'srcImgError_invalidNonXipRange':     ['Non-XIP Application is detected but it is not in the range of ITCM/DTCM/OCRAM/SDRAM/FlexSPI RAM!',
                                              u"检测到非XIP应用程序,但它没有链接到ITCM/DTCM/OCRAM/SDRAM/FlexSPI RAM范围内!"],
        'srcImgError_nonXipNotAppliable':     ['Non-XIP Application is detected but it is not appliable for HAB Signed image boot when boot device is FlexSPI/SEMC NOR under selected MCU device!',
                                              u"Non-XIP应用程序被检测到, 但它在选中的微控制器型号以及FlexSPI/SEMC NOR启动设备下不适用于HAB签名启动!"],
        'srcImgError_xipNotForHabCrypto':     ['XIP Application is detected but it is not appliable for HAB Encrypted image boot!',
                                              u"XIP应用程序被检测到, 但它不适用于HAB加密启动!"],
        'srcImgError_nonXipNotForHwCrypto':   ['Non-XIP Application is detected but it is not appliable for HW Encrypted image boot!',
                                              u"检测到非XIP应用程序, 但它不适用于硬件加密启动!"],
        'srcImgError_notFound':               ['You should first specify a source image file (.elf/.axf/.srec/.hex/.bin)!',
                                              u"请首先选定一个程序文件 (.elf/.axf/.srec/.hex/.bin)!"],
        'srcImgError_xipSizeTooLarge':        ['XIP Application is detected but the size exceeds maximum XIP size ',
                                              u"XIP应用程序被检测到, 但其大小超过最大XIP范围 "],
        'srcImgError_xipOffsetTooSmall':      ['XIP Application is detected but the offset is less than minimum reserved size ',
                                              u"XIP应用程序被检测到, 但其偏移小于最低保留长度 "],
        'operCertError_notGen':               ['You should first generate certificates, or make sure you don\'t put the tool in path with blank space!',
                                              u"请首先生成证书, 或者确保NXP-MCUBootUtility工具存放的路径中没有空格!"],
        'srcImgError_failToGen':              ['Bootable image is not generated successfully! Make sure you don\'t put the tool in path with blank space!',
                                              u"可启动的程序文件未成功生成!请确保NXP-MCUBootUtility工具存放的路径中没有空格!"],
        'srcImgError_failToGenSb':            ['.sb image is not generated successfully! Make sure you don\'t put the tool in path with blank space!',
                                              u".sb格式程序文件未成功生成!请确保NXP-MCUBootUtility工具存放的路径中没有空格!"],
        'srcImgError_invalidFl':              ['Default Flashloader image file is not usable!',
                                              u"默认的Flashloader程序文件不适用!"],
        'operCertError_notGen1':              ['You should first generate certificates!',
                                              u"请首先生成证书！"],
        'burnFuseError_failToBurnSrk':        ['Fuse SRK Regions were not burned successfully!',
                                              u"SRK数据未成功烧录进Fuse SRK0-7区域!"],
        'burnFuseError_srkHasBeenBurned':     ['Fuse SRK Regions have been burned, it is program-once!',
                                              u"Fuse SRK区域已经被烧录过，它只可被烧写一次！"],
        'certGenError_srkNotGen':             ['Super Root Keys hasn\'t been generated!',
                                              u"SRK数据文件还没有生成！"],
        'burnFuseError_failToBurnSwgp2Lock':  ['Fuse LOCK SW_GP2 region was not burned successfully!',
                                              u"Fuse SW_GP2区域的Lock位未成功烧录!"],
        'burnFuseError_failToBurnGp4Lock':    ['Fuse LOCK GP4 region was not burned successfully!',
                                              u"Fuse GP4区域的Lock位未成功烧录!"],
        'burnFuseError_failToBurnSwgp2':      ['Fuse SW_GP2 Regions were not burned successfully!',
                                              u"Fuse SW_GP2区域未成功烧录!"],
        'burnFuseError_swgp2HasBeenBurned':   ['Fuse SW_GP2 Regions have been burned/locked, it is program-once!',
                                              u"Fuse SW_GP2区域已经被烧录过或锁定，它只可被烧写一次！"],
        'burnFuseError_failToBurnGp4':        ['Fuse GP4 Regions were not burned successfully!',
                                              u"Fuse GP4区域未成功烧录!"],
        'burnFuseError_gp4HasBeenBurned':     ['Fuse GP4 Regions have been burned/locked, it is program-once!',
                                              u"Fuse GP4区域已经被烧录过或锁定，它只可被烧写一次！"],
        'burnFuseError_failToBurnUserkey5':   ['Fuse USER_KEY5 Regions were not burned successfully!',
                                              u"Fuse USER_KEY5区域未成功烧录!"],
        'burnFuseError_userkey5HasBeenBurned':['Fuse USER_KEY5 Regions have been burned/locked, it is program-once!',
                                              u"Fuse USER_KEY5区域已经被烧录过或锁定，它只可被烧写一次！"],
        'burnFuseError_miscConf1HasBeenBurned': ['Fuse MISC_CONF1[31:0] has been burned, it is program-once!',
                                                u"Fuse MISC_CONF1[31:0]区域已经被烧录过，它只可被烧写一次！"],
        'burnFuseError_failToBurnMiscConf1':  ['Fuse MISC_CONF1[31:0] region was not burned successfully!',
                                              u"Fuse MISC_CONF1[31:0]区域未成功烧录！"],
        'burnFuseError_miscConf0HasBeenBurned': ['Fuse MISC_CONF0[28:24] LPSPI_EEPROM has been burned, it is program-once!',
                                                u"Fuse MISC_CONF0[28:24]已经被烧录，它只可被烧写一次！"],
        'burnFuseError_failToBurnMiscConf0':  ['Fuse MISC_CONF0[28:24] LPSPI EEPROM region was not burned successfully!',
                                              u"Fuse MISC_CONF0[28:24]区域未成功烧录！"],
        'burnFuseError_hwCryptoKey0SelHasBeenBurned': ['Fuse BOOT_CFG1[5:4] XX_KEY0_SEL has been burned, it is program-once!',
                                                      u"Fuse BOOT_CFG1[5:4] XX_KEY0_SEL位已经被烧录过，它只可被烧写一次！"],
        'burnFuseError_hwCryptoKey1SelHasBeenBurned': ['Fuse BOOT_CFG1[7:6] XX_KEY1_SEL has been burned, it is program-once!',
                                                      u"Fuse BOOT_CFG1[7:6] XX_KEY1_SEL位已经被烧录过，它只可被烧写一次！"],
        'burnFuseError_failToBurnHwCryptoKeyxSel': ['Fuse BOOT_CFG1[7:4] XX_KEY0/1_SEL region was not burned successfully!',
                                                   u"Fuse BOOT_CFG1[7:4] XX_KEY0/1_SEL位未成功烧录！"],
        'burnFuseError_failToBurnOtfadEnablementBit': ['Fuse 0x630[8] OTFAD_ENABLE region was not burned successfully!',
                                                      u"Fuse 0x630[8] OTFAD_ENABLE位未成功烧录！"],
        'burnFuseError_failToBurnOtfadKeyScramble': ['Fuse OTFAD Key Scramble Region was not burned successfully!',
                                                    u"OTFAD Key Scramble数据未成功烧录进对应Fuse区域!"],
        'burnFuseError_otfadKeyScrambleHasBeenBurned': ['Fuse OTFAD Key Scramble Region has been burned, it is program-once!',
                                                       u"Fuse OTFAD Key Scramble区域已经被烧录过，它只可被烧写一次！"],
        'burnFuseError_failToBurnOtfadScrambleConfigurationField': ['Fuse OTFAD Key Scramble configuration regions were not burned successfully!',
                                                                   u"OTFAD Key Scramble配置数据未成功烧录进对应Fuse区域!"],
        'certGenError_dekNotGen':             ['Dek file hasn\'t been generated!',
                                              u"DEK数据文件还没有生成!"],
        'burnFuseError_failToBurnSecConfig1': ['Fuse BOOT_CFG1[1] SEC_CONFIG[1] region was not burned successfully!',
                                              u"Fuse BOOT_CFG1[1] SEC_CONFIG[1]位未成功烧录！"],

        'burnFuseError_cannotBurnSrkLock':    ['Fuse 0x400[14] - SRK_LOCK is not allowed to be set, because SRK will be OP+RP+WP if SRK_LOCK is set and then ROM cannot get SRK!',
                                              u"Fuse 0x400[14] - SRK_LOCK位不允许被烧写成1，如果SRK_LOCK被置1，SRK区域将会被保护(覆盖&读&写)，导致ROM不能得到SRK数据!"],

        'burnFuseError_failToBurnDualImageMiscConf':  ['Fuse 0x6E0/0xC80[24:12] region was not burned successfully!',
                                                      u"Fuse 0x6E0/0xC80[24:12]区域未成功烧录！"],

        'operImgError_hasnotProgImage':       ['You should program your image first!',
                                              u"请首先下载image文件！"],
        'operImgError_notInRam':              ['Your specified area is not in the range of RAM, Please double check!',
                                              u"当前指定的访问区域超出有效RAM范围，请仔细检查！"],

        'connectError_doubleCheckIsp':        ['Make sure that you have put MCU in ISP (In-System Programming) modes (ISP[2:0] pins = 3\'b010 (USB) or 3\'b110 (UART))!',
                                              u"请检查ISP[2:0]引脚状态是否为3\'b010 (USB)或3\'b110 (UART)以确认微控制器处于ROM ISP模式！"],

        'burnOtpError_bootCfg0HasBeenBurned': ['Otp BOOT_CFG0[19:17] REDUNDANT_SPI_PORT has been burned, it is program-once!',
                                                u"Otp BOOT_CFG0[19:17]已经被烧录，它只可被烧写一次！"],
        'burnOtpError_failToBurnBootCfg0':   ['Otp BOOT_CFG0[19:17] REDUNDANT_SPI_PORT region was not burned successfully!',
                                              u"Otp BOOT_CFG0[19:17]区域未成功烧录！"],

        'connectError_doubleCheckFopt':       ['Make sure that you have put MCU in ROM boot mode (FOPT(FCF - 0x40d) = 0x3D, BOOTCFG0(NMI) pin is asserted)!',
                                              u"请检查FOPT(FCF区域0x40d)是否为0x3D以及上电时BOOTCFG0有没有按住以确认微控制器处于ROM启动模式！"],

        'connectError_doubleCheckIspMode':    ['Make sure that you have put MCU in ISP boot mode (ISPMODE_EN pin = LOW)!',
                                              u"请检查ISPMODE_EN引脚状态是否为低以确认微控制器处于ROM ISP模式！"],

        'connectError_doubleCheckIspBoot':    ['Make sure that you have put MCU in ISP boot mode (ISP0 pin = LOW)!',
                                              u"请检查ISP0引脚状态是否为低以确认微控制器处于ROM ISP模式！"],
        'srcImgError_invalidNonXipRange2':     ['Non-XIP Application is detected but it is not in the range of SRAM!',
                                               u"检测到非XIP应用程序,但它没有链接到SRAM范围内!"],

        'signImgError_invalidStart0':         ['Signed Region 0 start address is invalid, it should be image start address!',
                                              u"签名区域0起始地址设置无效，它应该等于image起始链接地址!"],
        'signImgError_invalidSize0':          ['Signed Region 0 size is invalid!',
                                              u"签名区域0长度设置无效!"],
        'signImgError_invalidRegion1':        ['Signed Region 1 start address or size is invalid!',
                                              u"签名区域1起始地址或者长度设置无效!"],
        'signImgError_invalidRegion2':        ['Signed Region 2 start address or size is invalid!',
                                              u"签名区域2起始地址或者长度设置无效!"],
        'signImgError_failToGen':             ['Part signed image is not generated successfully!',
                                              u"部分区域签名的程序文件未成功生成!"],

        'burnOtpError_failToBurnDualImageBootCfg3':   ['Otp BOOT_CFG3[31:22] Second image offset region was not burned successfully!',
                                                      u"Otp BOOT_CFG3[31:22]区域未成功烧录！"],
        'burnOtpError_failToBurnDualImageBootCfg2':   ['Otp BOOT_CFG2[31:28] FlexSPI remap size region was not burned successfully!',
                                                      u"Otp BOOT_CFG2[31:28]区域未成功烧录！"],

        'edgelockFwError_cntrSizeTooLarge':   ['Edgelock container file is detected but the size exceeds maximum size ',
                                              u"Edgelock启动头被检测到, 但其大小超出最大长度 "],
        'edgelockFwError_imageSizeTooLarge':  ['Edgelock FW file is detected but the size exceeds maximum size ',
                                              u"Edgelock固件被检测到, 但其大小超出最大长度 "],
}