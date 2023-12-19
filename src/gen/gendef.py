import sys, os

kToolchainSymbolList_EntryAddr = ['Reset_Handler', '__iar_program_start']
kToolchainSymbolList_VectorAddr = ['__VECTOR_TABLE', '__vector_table', '__Vectors']

kAppImageFileExtensionList_Elf = ['.out', '.elf', '.axf']
kAppImageFileExtensionList_S19 = ['.srec', '.s19', '.mot', '.mxt', '.m32', '.s28', '.s37']
kAppImageFileExtensionList_Hex = ['.hex']
kAppImageFileExtensionList_Bin = ['.bin']

kIdeType_MCUX = 0
kIdeType_IAR  = 1
kIdeType_MDK  = 2

kSbLoaderVersion_v1_0 = 0
kSbLoaderVersion_v2_0 = 1
kSbLoaderVersion_v2_1 = 2
kSbLoaderVersion_v3_1 = 3

kImgVerOffset_NOR = 0x600

kBootHeaderType_Vector    = 0
kBootHeaderType_IVT       = 1
kBootHeaderType_Container = 2

