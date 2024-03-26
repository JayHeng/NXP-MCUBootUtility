--
　　跨界之风吹满地，先锋当属NXP;  
　　微控制器谁独骚？当仁不让看RT！  

　　恩智浦半导体2017年10月正式发布了业内首款跨界处理器—i.MX RT系列，这是MCU界的汗血宝马，更是一匹桀骜不驯的悍马。一年多来，众多骑士（MCU开发者）纷纷想去征服这匹悍马，然而想要驯服这匹悍马没并非易事，除了需要骑士自身马术（嵌入式功底）精湛，还需要善于利用恩智浦提供的一整套马具（工具链软件开发包），方可成功驾驭这匹悍马。今天痞子衡为大家介绍的这款工具名叫NXP-MCUBootUtility，其功能堪比马镫，有了马镫骑士可以轻松上马。  

### 一、i.MX RT启动背景
　　在介绍MCUBootUtility出场之前，咱们先来聊聊i.MX RT的启动背景。众所周知，i.MX RT源自经典的i.MX6ULL平台，同i.MX处理器一样，i.MX RT也是flashless的芯片，其内部没有可供用户存储代码的非易失性存储器，因此在i.MX RT系统设计里需要为其配置一块非易失性存储器（在i.MX RT世界里，我们更喜欢称其为启动设备）。  

　　有了外置启动设备，代码存储的问题解决了，但随之引入了启动问题。要想从启动设备中访问代码数据，首先需要对其进行必要的配置，配置正确之后还需要从中找到正确的应用程序位置来加载启动，那么问题来了，谁负责干这些事？当然是BootROM，BootROM其实是固化在i.MX RT内部一段程序，其功能就类似于PC上的BIOS，i.MX RT上电首先运行的就是BootROM，由BootROM为i.MX RT做好启动的所有准备工作。  

　　翻看i.MX RT的BootROM章节，可以看到BootROM核心功能概括起来主要如下6条：  

> * Support for booting from various boot devices
> * Serial downloader support (USB OTG and UART)
> * Device Configuration Data (DCD) and plugin
> * Digital signature and encryption based High-Assurance Boot (HAB)
> * Wake-up from the low-power modes
> * Encrypted XIP on Serial NOR via FlexSPI interface powered by BEE and DCP
controller

　　BootROM核心功能看起来有6条，其实主要是第1条，后面5条都是为第1条服务的，various boot devices即各种各样的启动设备，启动设备到底有多丰富？且看下图：  

![NXP-MCUBootUtility_boot_device](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/nxpSecBoot_Intro_bootrom_devices.PNG)

　　从上图可以看出i.MX RT BootROM支持的启动设备真的很丰富，有通过FlexSPI接口支持的高速串行NOR、NAND Flash，有通过uSDHC接口支持的SD Card、eMMC，有通过SEMC接口支持的并行NOR、NAND Flash，甚至还有通过LPSPI接口支持的低速EEPROM、NOR Flash，真是应有尽有。  

　　启动设备类型这么多，是好事但也是麻烦事，BootROM为了能够同时支持这么多特性各异的启动设备，必须制定一个通用规则，这个规则就是i.MX RT Boot Data Component，即放在启动设备中的用户Application除了自身image数据外，还必须包含额外的Boot Data以供BootROM识别，那么Boot Data Component到底有哪些呢？继续看下表：  

![NXP-MCUBootUtility_boot_data](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/nxpSecBoot_Intro_boot_data_component.PNG)

　　上表中IVT和Boot Data是最必不可少的Component，也是用于支持众多特性各异的启动设备的关键，IVT与Boot Data合称Bootable header，包含Bootable header的Application即称为Bootable Application，启动设备中仅当存储的是Bootable Application才能够被i.MX RT BootROM正确识别和启动。  

### 二、MCUBootUtility
　　上一节讲完了i.MX RT启动背景，都是理论的东西，该是进入实战环节的时候了。到底如何制作一个Bootable Application？到底怎么将Bootable Application下载到指定类型启动设备中？  

　　其实恩智浦早为大家已经准备好一整套工具，BD file、elftosb.exe、MfgTool2.exe等，这些工具都在Flashloader包里，下面是这些工具的联合使用流程：  

![NXP-MCUBootUtility_tool_flow](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/nxpSecBoot_Intro_misc_tool_flow.PNG)

　　首先在自己喜欢的IDE里（比如恩智浦免费提供的MCUXpresso）开发Application，开发结束之后生成可执行文件（.elf/.srec均可），将该可执行文件经过elftosb.exe转换成.sb文件（需要两次转换，第一次生成Bootable Application，第二次生成.sb文件，两次转换需要两个不同BD file），最后使用MfgTool2通过USB口将.sb文件内容下载到启动设备里。  

　　上述整个过程虽然涉及多个命令多步操作，但总算能够顺利完成。如果需要进一步使能HAB签名或者加密，那么需要再联合CST工具，步骤再增加一些。如果是使能BEE加密，那么得注意选对合适的BD file，一些特殊的fuse需要烧录正确，不管怎样，事情总能解决。  

　　但这就够了么？你有没有曾期望过有一个工具能够把上面这些事情全部包进去并且还是一个优雅的GUI？别以为这是妄想，这样的工具早已存在了，它就叫NXP-MCUBootUtility，下图是它的庐山真面目，清爽的界面，强大的功能，有了它，启动i.MX RT从未如此简单。  

![NXP-MCUBootUtility_v1.1.0](https://raw.githubusercontent.com/JayHeng/pzhmcu-picture/master/cnblogs/nxpSecBoot_Intro_v1.1.0_chinese.PNG)

　　NXP-MCUBootUtility是一个专为恩智浦MCU安全启动而设计的工具，其特性与MCU里的BootROM功能相对应，目前主要支持i.MX RT系列MCU芯片，与NXP官方的标准安全启动配套工具集（OpenSSL, CST, sdphost, blhost, elftosb, BD, MfgTool2）相比，NXP-MCUBootUtility是一个真正的一站式工具，一个工具包含NXP官方所有配套启动工具的功能，并且是全图形用户界面操作。借助于NXP-MCUBootUtility，你可以轻松上手NXP MCU安全启动。  

　　NXP-MCUBootUtility主要功能如下：  

> * 支持i.MXRT全系列MCU，包含i.MXRT1015、i.MXRT1021、i.MXRT1051/1052、i.MXRT1061/1062、i.MXRT1064 SIP  
> * 支持UART和USB-HID两种串行下载方式（COM端口/USB设备自动识别）  
> * 支持五种常用格式(elf/axf/srec/hex/bin)源image文件输入并检查其链接地址的合法性  
> * 源image文件既可以是裸源image文件，也可以是含启动文件头的bootable image文件  
> * 支持将裸源image文件自动转换成i.MXRT能启动的Bootable image  
> * 支持下载Bootable image进主动启动设备 - FlexSPI NOR、SEMC NAND接口Flash  
> * 支持下载Bootable image进备份启动设备 - LPSPI接口NOR/EEPROM Flash  
> * 支持DCD配置功能，可用于加载image进SDRAM执行  
> * 支持用于开发阶段的非安全加密启动（未签名加密）  
> * 支持基于HAB实现的安全加密启动（单签名，签名和加密），证书自动备份  
> * 支持基于BEE实现的安全加密启动（唯一SNVS key，用户自定义key）  
> * 支持MCU芯片内部eFuse的回读和烧写操作（即专用eFuse烧写器）  
> * 支持外部启动设备的任意读写擦操作（即通用Flash编程器）  
> * 支持从外部启动设备回读Bootable image，并对其组成部分（NFCB/DBBT/FDCB/EKIB/EPRDB/IVT/Boot Data/DCD/Image/CSF/DEK KeyBlob）进行标注  

　　这么好用的工具去哪里下载？其实MCUBootUtility是一个基于Python的开源项目，其项目地址为 https://github.com/JayHeng/NXP-MCUBootUtility， 核心代码只有9000多行，虽然当前版本（v1.1.0）功能已经非常完备，你还是可以在此基础上再添加自己想要的功能。如此神器，还不快快去下载试用？  
