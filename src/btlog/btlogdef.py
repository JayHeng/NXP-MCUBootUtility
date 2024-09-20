import sys, os

#define MAKE_LOG_ENTRY(state, substate, status, entries) (((state) << 24) | ((substate) << 16) | ((status) << 8) | (entries))

btlogIntro0 = '| Log Entry  |          State          |        Sub State        |          Status         |'
btlogIntro1 = '| Log Entry  |          Description                                                        |'
btlogIntro2 = '--------------------------------------------------------------------------------------------'

kBootLogStateType_HardwareInit  = 0x01
kBootLogStateType_MasterBoot    = 0x05
kBootLogStateType_BootDevice    = 0x09
kBootLogStateType_AuthImage     = 0x0b
kBootLogStateType_JumpToImage   = 0x0c

btlogStateDict_RTmix       = {'0x00' :'Startup                   ',
                              '0x01' :'Hardware Init             ',
                              '0x02' :'ROM Patch                 ',
                              '0x03' :'Secure Boot               ',
                              '0x04' :'Boot Mode                 ',
                              '0x05' :'Master Boot               ',
                              '0x06' :'Passive Boot              ',
                              '0x07' :'Recovery Boot             ',
                              '0x08' :'Isp Boot                  ',
                              '0x09' :'Boot Device               ',
                              '0x0a' :'Load Image                ',
                              '0x0b' :'Auth Image                ',
                              '0x0c' :'Jump to Image             ',
                              # For RT500/600
                              '0x0d' :'TZ-M                      ',
                              '0xff' :'Fatal                     ',
                             }

kBootLogSubStateType_Init  = 0x01
kBootLogSubStateType_Call  = 0x02

btlogSubStateDict_RTmix    = {'0x00' :'Common                    ',
                              '0x01' :'Init                      ',
                              '0x02' :'Call                      ',
                              '0x03' :'Deinit                    ',
                              '0x04' :'Source                    ',
                              '0x05' :'Check                     ',

                              '0x20' :'Img - Initial Load        ',
                              '0x21' :'Img - Remaining Load      ',

                              '0x30' :'Auth - Check Secure State ',
                              '0x30' :'Auth - Image Type Check   ',
                              '0x31' :'Auth - Read Key Store     ',
                              '0x32' :'Auth - Read Mac Key       ',
                              '0x33' :'Auth - Verify HMAC        ',
                              '0x34' :'Auth - Image Entry Check  ',
                              '0x35' :'Auth - Authenticate       ',
                              '0x36' :'Auth - Crc Check          ',
                              # For RT500/600
                              '0x37' :'Auth - DICE               ',
                              '0x38' :'Auth - Boot Seed          ',
                              
                              '0x70' :'TZM - Get Device Tzm Mode ',
                              '0x71' :'TZM - Get Fuses Tzm Mode  ',
                              '0x72' :'TZM - Get Image Tzm Mode  ',
                              '0x73' :'TZM - Incmpatible Image   ',
                             }

btlogStatusDict_RTmix      = {
                              '0x01' :'Master Boot               ',
                              '0x02' :'Passive Boot              ',
                              '0x03' :'Recovery Boot             ',
                              '0x04' :'Isp Boot                  ',

                              '0xdc' :'Disabled                  ',
                              '0xea' :'Enabled                   ',

                              '0xf0' :'Pass                      ',
                              '0xf3' :'Fail                      ',
                              '0xf5' :'Fatal                     ',
                              '0xfc' :'Invalid                   ',
                              '0xff' :'Default                   ',
                             }

btDataStateDict_BootDevice0_RTmix = {
                              '0x01' :'Primary Boot              ',
                              '0x02' :'Recovery Boot             ',
                              '0x04' :'Manufacture Boot          ',
                              '0x08' :'Serial Boot               ',
                             }

btDataStateDict_BootDevice1_1_RTmix = {
                              '0x00' :'Primary - QuadSPI         ',
                              '0x01' :'Primary - MMC             ',
                              '0x02' :'Primary - SD              ',
                              '0x03' :'Primary - SEMC NAND       ',
                              '0x04' :'Primary - SEMC NOR        ',
                              '0x05' :'Primary - FLEXSPI NOR     ',
                              '0x06' :'Primary - FLEXSPI NAND    ',
                             }

btDataStateDict_BootDevice1_2_RTmix = {
                              '0x00' :'Recovery - SPI NOR        ',
                             }

btDataStateDict_BootDevice1_4_RTmix = {
                              '0x00' :'Manufacture - SDMMC       ',
                             }

btDataStateDict_BootDevice1_8_RTmix = {
                              '0x0001' :'Serial - UART             ',
                              '0x0002' :'Serial - I2C Slave        ',
                              '0x0004' :'Serial - SPISlave         ',
                              '0x0008' :'Serial - CAN              ',
                              '0x0010' :'Serial - USB HID          ',
                              '0x0020' :'Serial - USB CDC          ',
                              '0x0040' :'Serial - USB DFU          ',
                              '0x0080' :'Serial - USB MSC          ',

                              '0x0011' :'Serial - UART/USB HID     ',
                              # For RT500/600
                              '0x0100' :'Device - QuadSPI          ',
                              '0x0200' :'Device - MMC              ',
                              '0x0400' :'Device - SD               ',
                              '0x0800' :'Device - SEMC             ',
                              '0x1000' :'Device - SpiFlash         ',
                             }

btlogDict_RT10yy    = {
                          '0x00010000' :'BOOTMODE_INTERNAL_FUSE',
                          '0x00010001' :'BOOTMODE_SERIAL',
                          '0x00010002' :'BOOTMODE_INTERNAL',
                          '0x00010003' :'BOOTMODE_TEST',

                          '0x00020000' :'SEC_CONFIG_FAB',
                          '0x00020033' :'SEC_CONFIG_RETURN',
                          '0x000200f0' :'SEC_CONFIG_OPEN',
                          '0x000200cc' :'SEC_CONFIG_CLOSED',

                          '0x00030000' :'DIR_BT_DIS_VALUE0',
                          '0x00030001' :'DIR_BT_DIS_VALUE1',

                          '0x00040000' :'BT_FUSE_SEL_VALUE0',
                          '0x00040001' :'BT_FUSE_SEL_VALUE1',

                          '0x00050000' :'PRIM_IMAGE_SELECT',
                          '0x00050001' :'SEC_IMAGE_SELECT',
                          '0x00050002' :'THIRD_IMAGE_SELECT',
                          '0x00050003' :'FOURTH_IMAGE_SELECT',

                          '0x00060000' :'PRIM_BOOTDEVICE_NAND',
                          '0x00060001' :'PRIM_BOOTDEVICE_USDHC',
                          '0x00060002' :'PRIM_BOOTDEVICE_SATA',
                          '0x00060003' :'PRIM_BOOTDEVICE_I2C',
                          '0x00060004' :'PRIM_BOOTDEVICE_ECSPI',
                          '0x00060005' :'PRIM_BOOTDEVICE_NOR',
                          '0x00060006' :'PRIM_BOOTDEVICE_ONENAND',
                          '0x00060007' :'PRIM_BOOTDEVICE_QSPI',
                          '0x00060008' :'PRIM_BOOTDEVICE_FLEXSPI_NOR',
                          '0x00060009' :'PRIM_BOOTDEVICE_FLEXSPI_NAND',
                          '0x0006000a' :'PRIM_BOOTDEVICE_SEMC_NOR',
                          '0x0006000b' :'PRIM_BOOTDEVICE_SEMC_NAND',
                          '0x00061001' :'REC_BOOTDEVICE_USDHC',
                          '0x00061003' :'REC_BOOTDEVICE_I2C',
                          '0x00061004' :'REC_BOOTDEVICE_ECSPI',
                          '0x00061005' :'REC_BOOTDEVICE_LPSPI',
                          '0x00061fff' :'REC_BOOTDEVICE_NONE',
                          '0x00062001' :'MFG_BOOTDEVICE_USDHC',

                          '0x00070000' :'DEVICE_INIT_CALL',
                          '0x000700f0' :'DEVICE_INIT_PASS',
                          '0x00070033' :'DEVICE_INIT_FAIL',

                          '0x00080000' :'DEVICE_READ_DATA_CALL',
                          '0x000800f0' :'DEVICE_READ_DATA_PASS',
                          '0x00080033' :'DEVICE_READ_DATA_FAIL',

                          '0x00090000' :'AUTHENTICATION_STATUS',

                          '0x000a0000' :'PLUGIN_IMAGE_CALL',
                          '0x000a00f0' :'PLUGIN_IMAGE_PASS',
                          '0x000a0033' :'PLUGIN_IMAGE_FAIL',

                          '0x000b0000' :'PROGRAM_IMAGE_CALL',
                          '0x000c0000' :'SDP_ENTRY',
                          '0x000d0000' :'SDP_IMAGE_CALL',
                          '0x000e0000' :'ROMCP_PATCH',

                      }

