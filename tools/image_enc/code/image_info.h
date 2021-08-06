#ifndef __IMAGE_INFO_H__
#define __IMAGE_INFO_H__

#include <stdint.h>

enum
{
    kAesMode_ECB = 0,
    kAesMode_CTR = 1,
};

enum
{
    kBeeLockOption_NoLock = 0,  //!< BEE Region related bits are unlocked.
    kBeeLockOption_Region1 = 1,  //!< BEE Region1 related bits are locked.
    kBeeLockOption_Region0 = 2,  //!< BEE Region0 related bits are locked.
    kBeeLockOption_BothRegions = 3,  //!< BEE regions related bits are locked.
};

typedef struct
{
    uint32_t start;      //!< Start address of the encrypted region, align at 1KB boundary
    uint32_t end;        //!< End address of the encrypted region, align at 1KB boundary
    uint32_t mode;       //!< AES mode: 0-CTR, 1-ECB
    uint32_t lock_option;//!< Lock options
    uint32_t counter[4]; //!< Counter for AES-CTR mode
    uint32_t reserved[8];//!< Reserved for future use.
}encrypt_region_t;

enum
{
    kFacMode_M7DebugAllowed = 0,
    kFacMode_M7DebugDisabled = 1,
    kFacMode_ExecuteOnlyDebugAllowed = 2,
    kFacMode_ExecuteOnly = 3,
};

typedef struct
{
    uint32_t start;      //!< Start address of one FAC region, align at 1KB boundary
    uint32_t end;        //!< End address of one FAC region, align at 1KB boundary
    uint32_t mode;       //!< Protected level: 0/1/2/3
    uint32_t reserved[5];//!< Reserved for future use
}fac_region_t;

#define BEE_PROT_REGION_BLK_TAGL  0x5F474154 //"TAG_"
#define BEE_PROT_REGION_BLK_TAGH  0x52444845 //"EHDR"
#define BEE_PROT_REGION_HDR_VER   0x56010000 // Version 1.0.0

typedef struct
{
    uint32_t tagl;                    //!< Lower Half of tag, equal to BEE_PROT_REGION_BLK_TAGL
    uint32_t tagh;                    //!< Upper Half of tag, equal to BEE_PROT_REGION_BLK_TAGH
    uint32_t version;                 //!< Version
    uint32_t fac_region_count;        //!< FAC region count, valid value: 1-4
    encrypt_region_t encrypt_region;  //!< Encrypted region info
    fac_region_t fac_regions[4];      //!< FAC region info
    uint32_t reserved1[12];           //!< Reserved for future use.
}protect_region_block_t;

typedef struct
{
    uint8_t key[16];
    uint8_t iv[16];
}key_info_block_t;



#endif // __IMAGE_INFO_H__