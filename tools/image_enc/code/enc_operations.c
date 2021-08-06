#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "enc_operations.h"
#include <time.h>
#include "mbedtls/aes.h"

/*********************************************************
    Constants
**********************************************************/
const uint32_t k_enc_hdr_offset[2] = {0x400, 0x800};
enum
{
    kBootImageStart = 0x1000,
};

/*********************************************************
    Prototypes
**********************************************************/
bool create_enc_region_hdr(region_ctx_t *region_ctx, enc_region_hdr_t *phdr, enc_region_hdr_t *ehdr);
bool handle_data(image_gen_ctx_t *gen_ctx, uint8_t *buf, uint32_t start, uint32_t *size, enc_region_hdr_t phdr[2]);
void handle_data_enc_ecb(uint8_t *key, uint8_t *buf, size_t length);
void handle_data_enc_ctr(uint8_t *key, uint8_t *nonce, uint8_t *buf, size_t length);

uint32_t get_random_number(void);

uint32_t get_random_number(void)
{
    srand((uint32_t)time(NULL));

    return (uint32_t)rand();
}

// Asume length is always 16-bytes aligned
void block_swap(uint8_t block[], size_t length)
{
    uint32_t i;
    uint8_t *ptr = block;
    uint8_t tmp;
    while (length)
    {
        if (length >= 16)
        {
            for (i = 0; i<8; i++)
            {
                tmp = ptr[i];
                ptr[i] = ptr[15 - i];
                ptr[15 - i] = tmp;
            }
            ptr += 16;
            length -= 16;
        }
    }
}

bool create_enc_region_hdr(region_ctx_t *region_ctx, enc_region_hdr_t *phdr, enc_region_hdr_t *ehdr)
{
    bool result = false;
    do
    {
        if ((region_ctx == NULL) || (phdr == NULL) | (ehdr == NULL))
        {
            break;
        }
        
        memset(phdr, 0, sizeof(*phdr));
        memset(ehdr, 0, sizeof(*ehdr));
        protect_region_block_t *prdb = &phdr->prdb;

        prdb->tagh = BEE_PROT_REGION_BLK_TAGH;
        prdb->tagl = BEE_PROT_REGION_BLK_TAGL;
        prdb->version = BEE_PROT_REGION_HDR_VER;

        if (region_ctx->ctr_kib_type == k_Kib_Ctr_Type_Zero)
        {
            if (region_ctx->aes_mode == kAesMode_CTR)
            {
                for (uint32_t i = 1; i < 4; i++)
                {
                    prdb->encrypt_region.counter[i] = 0;
                }
            }

            for (uint32_t i = 0; i < 16; i++)
            {
                phdr->kib.key[i] = 0;
                phdr->kib.iv[i] = 0;
            }
        }
        else if (region_ctx->ctr_kib_type == k_Kib_Ctr_Type_Random)
        {
            if (region_ctx->aes_mode == kAesMode_CTR)
            {
                for (uint32_t i = 1; i < 4; i++)
                {
                    prdb->encrypt_region.counter[i] = get_random_number();
                }
            }

            for (uint32_t i = 0; i < 16; i++)
            {
                phdr->kib.key[i] = get_random_number() & 0xFF;
                phdr->kib.iv[i] = get_random_number() & 0xFF;
            }
        }
        else
        {
            break;
        }

        prdb->encrypt_region.lock_option = region_ctx->lock_option;
        prdb->encrypt_region.mode = region_ctx->aes_mode;

        prdb->fac_region_count = region_ctx->fac_region_ctx.fac_region_count;
        uint32_t min_start = region_ctx->fac_region_ctx.fac_regions[0].start;
        uint32_t max_end = region_ctx->fac_region_ctx.fac_regions[0].start + region_ctx->fac_region_ctx.fac_regions[0].length;
        for (uint32_t i = 0; i < prdb->fac_region_count; i++)
        {
            prdb->fac_regions[i].start = region_ctx->fac_region_ctx.fac_regions[i].start;
            prdb->fac_regions[i].end = region_ctx->fac_region_ctx.fac_regions[i].start + region_ctx->fac_region_ctx.fac_regions[i].length;
            prdb->fac_regions[i].mode = region_ctx->fac_region_ctx.fac_regions[i].fac_mode;

            if (min_start > prdb->fac_regions[i].start)
            {
                min_start = prdb->fac_regions[i].start;
            }
            if (max_end < prdb->fac_regions[i].end)
            {
                max_end = prdb->fac_regions[i].end;
            }
        }

        prdb->encrypt_region.start = min_start;
        prdb->encrypt_region.end = max_end;
        
        // Generate EPRDB
        mbedtls_aes_context ctx;
        uint8_t iv[16]; // mbedtls_aes_crypt_cbc will update the iv during encryption/decryption, so need to make a copy of IV
        mbedtls_aes_init(&ctx);
        mbedtls_aes_setkey_enc(&ctx, phdr->kib.key, 128);
        memcpy(iv, phdr->kib.iv, sizeof(iv));
        mbedtls_aes_crypt_cbc(&ctx, MBEDTLS_AES_ENCRYPT, sizeof(*prdb), iv, (uint8_t*)prdb, (uint8_t*)&ehdr->prdb);

        // Generate EKIB
        mbedtls_aes_init(&ctx);
        mbedtls_aes_setkey_enc(&ctx, region_ctx->key, 128);
        mbedtls_aes_crypt_ecb(&ctx, MBEDTLS_AES_ENCRYPT, phdr->kib.key, ehdr->kib.key);
        mbedtls_aes_crypt_ecb(&ctx, MBEDTLS_AES_ENCRYPT, phdr->kib.iv, ehdr->kib.iv);

        result = true;

    } while (0);

    return result;
}

void handle_data_enc_ecb(uint8_t *key, uint8_t *buf, size_t length)
{
    mbedtls_aes_context ctx;
    mbedtls_aes_init(&ctx);
    mbedtls_aes_setkey_enc(&ctx, key, 128);

    while (length > 0)
    {
        mbedtls_aes_crypt_ecb(&ctx, MBEDTLS_AES_ENCRYPT, buf, buf);
        buf += 16;
        length -= 16;
    }
}

void handle_data_enc_ctr(uint8_t *key, uint8_t *nonce, uint8_t *buf, size_t length)
{
    mbedtls_aes_context ctx;
    uint32_t offset = 0;
    uint8_t stream_block[16];
    mbedtls_aes_init(&ctx);
    mbedtls_aes_setkey_enc(&ctx, key, 128);

    mbedtls_aes_crypt_ctr(&ctx, length, &offset, nonce, stream_block, buf, buf);
}

bool handle_data(image_gen_ctx_t *gen_ctx, uint8_t *buf, uint32_t start, uint32_t *size, enc_region_hdr_t phdr[2])
{
    bool is_in_enc_region = false;
    uint32_t region_index = 0;
    for (uint32_t i = 0; i < 2; i++)
    {
        if (start >= phdr[i].prdb.encrypt_region.start && start < phdr[i].prdb.encrypt_region.end)
        {
            is_in_enc_region = true;
            bool is_in_fac_region = false;
            fac_region_t *fac_region = &phdr[i].prdb.fac_regions[0];
            for (uint32_t j = 0; j < phdr[i].prdb.fac_region_count; j++)
            {
                if (start >= fac_region[j].start && start < fac_region[j].end)
                {
                    is_in_fac_region = true;
                    break;
                }
            }

            is_in_enc_region = is_in_fac_region;
            if (is_in_enc_region)
            {
                region_index = i;
                break;
            }
        }
    }

    if (is_in_enc_region)
    {
        if (*size & 0x0f)
        {
            *size = (*size + 0x0F) & ~0x0F;
        }
        protect_region_block_t *prdb = &phdr[region_index].prdb;

        uint8_t *key = gen_ctx->regions[region_index].key;
        if (prdb->encrypt_region.mode == kAesMode_ECB)
        {
            handle_data_enc_ecb(key, buf, *size);
        }
        else
        {
            uint32_t counter[4];
            memcpy(&counter, prdb->encrypt_region.counter, sizeof(counter));
            counter[0] = start >> 4;
            block_swap((uint8_t*)&counter, sizeof(counter));
            handle_data_enc_ctr(key, (uint8_t*)&counter, buf, *size);
        }
    }

    return true;
}

bool image_enc(image_gen_ctx_t *gen_ctx)
{
    bool result = false;

    do
    {
        if (gen_ctx == NULL)
        {
            break;
        }

        FILE *ifile = fopen(gen_ctx->input_file, "rb");
        if (ifile == NULL)
        {
            printf("Cannot open %s\r\n", gen_ctx->input_file);
            break;
        }
        FILE *ofile = fopen(gen_ctx->output_file, "wb");
        if (ofile == NULL)
        {
            printf("Cannot create %s\r\n", gen_ctx->output_file);
            break;
        }

        enc_region_hdr_t phdr[2];
        enc_region_hdr_t ehdr[2];
        memset(&phdr, 0, sizeof(phdr));
        memset(&ehdr, 0, sizeof(ehdr));

        for (uint32_t i = 0; i < 2; i++)
        {
            if (gen_ctx->regions[i].is_present)
            {
                create_enc_region_hdr(&gen_ctx->regions[i], &phdr[i], &ehdr[i]);
            }
        }

        uint8_t temp_buf[1024];
        size_t write_offset = 0;
        size_t read_len;
        if (gen_ctx->is_boot_image)
        {
            // Header
            read_len = fread(temp_buf, 1, sizeof(temp_buf), ifile);
            if (read_len == sizeof(temp_buf))
            {
                fwrite(temp_buf, 1, sizeof(temp_buf), ofile);
            }
            else
            {
                //TODO: Error handling
            }
            write_offset += read_len;

            for (uint32_t i = 0; i < 2; i++)
            {
                while (write_offset < k_enc_hdr_offset[i])
                {
                    fread(temp_buf, 1, 1, ifile);
                    fwrite(temp_buf, 1, 1, ofile);
                    write_offset++;
                }

                fread(temp_buf, 1, sizeof(ehdr[i]), ifile);
                if (gen_ctx->regions[i].is_present)
                {
                    fwrite(&ehdr[i], 1, sizeof(ehdr[i]), ofile);
                }
                else
                {
                    fwrite(temp_buf, 1, sizeof(ehdr[i]), ofile);
                }
                write_offset += sizeof(ehdr[i]);
            }

            while (write_offset < kBootImageStart)
            {
                fread(temp_buf, 1, 1, ifile);
                fwrite(temp_buf, 1, 1, ofile);
                write_offset++;
            }
        }
        else
        {
            for (uint32_t i = 0; i < 2; i++)
            {
                if (gen_ctx->regions[i].is_present)
                {
                    char file_name[100];
                    sprintf(file_name, "ehdr%d.bin", i);
                    FILE *ofile = fopen(file_name, "wb");
                    fwrite(&ehdr[i], 1, sizeof(ehdr[i]), ofile);
                    fflush(ofile);
                    fclose(ofile);
                }
            }
        }

        do
        {
            uint32_t actual_addr = gen_ctx->base_addr + write_offset;
            // Start encrypting file as needed
            read_len = fread(temp_buf, 1, sizeof(temp_buf), ifile);
            printf("reading 0x%08x, size=0x%x\r\n", actual_addr, read_len);
            if (read_len < 1)
            {
                break;
            }
            
            handle_data(gen_ctx, temp_buf, actual_addr, &read_len, phdr);

            fwrite(temp_buf, 1, read_len, ofile);
            write_offset += read_len;

        } while (read_len == sizeof(temp_buf));
        fclose(ifile);
        fclose(ofile);

        result = true;

    } while (0);

    return result;
}