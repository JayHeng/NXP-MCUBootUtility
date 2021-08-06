#ifndef __ENC_OPERATIONS_H__
#define __ENC_OPERATIONS_H__

#include <stdint.h>
#include "image_info.h"
#include <stdbool.h>

enum
{
    k_Kib_Ctr_Type_Zero = 0,
    k_Kib_Ctr_Type_Random = 1,
};

typedef struct
{
    uint32_t start;
    uint32_t length;
    uint32_t fac_mode;
}fac_region_attr;

typedef struct
{
    uint32_t fac_region_count;
    fac_region_attr fac_regions[4];
}fac_region_ctx_t;


typedef struct
{
    bool is_present;
    uint32_t ctr_kib_type;
    uint8_t key[16];
    uint32_t aes_mode;
    uint32_t lock_option;
    fac_region_ctx_t fac_region_ctx;
}region_ctx_t;


typedef struct
{
    char *input_file;
    char *output_file;
    uint32_t base_addr;
    bool is_boot_image;
    region_ctx_t regions[2];
}image_gen_ctx_t;


typedef struct
{
    key_info_block_t kib;
    uint8_t reserved0[0x60];
    protect_region_block_t prdb;
    uint8_t reserved1[0x80];
}enc_region_hdr_t;

#ifdef __cplusplus 
extern "C"
{
#endif 
    
    //!@brief Swap block in terms of 16 bytes
    //!       for example, swap block[0] and block[15], block[1] and block[14], ...
    void block_swap(uint8_t block[], size_t length);


    bool image_enc(image_gen_ctx_t *ctx);

#ifdef __cplusplus 
}
#endif




#endif // __ENC_OPERATIONS_H__