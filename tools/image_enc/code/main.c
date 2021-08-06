#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>
#include "mbedtls/aes.h"
#include "image_info.h"
#include "enc_operations.h"
#include <ctype.h>

void show_usage(void);
bool get_gen_ctx(int argc, char *argv[], image_gen_ctx_t *gen_ctx);
bool convert_key_string_to_key_array(char *str, uint8_t *key);
bool convert_region_arg_to_context(char *str, region_ctx_t *ctx);
uint8_t ascii_to_digit(char c);

int main(int argc, char *argv[])
{
    int status = 0;
    image_gen_ctx_t gen_ctx;
    memset(&gen_ctx, 0, sizeof(gen_ctx));

    if (argc == 1)
    {
        show_usage();
    }
    else
    {
        bool result = get_gen_ctx(argc, argv, &gen_ctx);
        if (result)
        {
            result = image_enc(&gen_ctx);
        }
        if (result)
        {
            status = 0;
        }
        else
        {
            status = 1;
        }
    }

    return status;
}

void show_usage(void)
{
    char usage_info[] = 
        "Usage:\r\n\r\n"
        "image_enc ifile=<ifile> ofile=<ofile> base_addr=<base_addr> [Options]\r\n\r\n"
        "Options\r\n"
        "  region0_key=<key string>  16 bytes hex string\r\n"
        "  region0_arg=<0/1>,[start,length,permission]\r\n"
        "              0 - AES ECB mode, 1 - AES CTR mode \r\n"
        "              start and length must be 1KB aligned\r\n"
        "              permision: 0 - No limitation, 1 - Debug disabled\r\n"
        "                         2 - ExecuteOnly, Debug allowed\r\n"
        "                         3 - ExecuteOnly, Debug disabled\r\n"
        "              Maximum [] pairs is 3\r\n"
        "  region0_lock=<0/1/2/3> 0 - NoLock, 1 - Lock Region1\r\n"
        "                         2 - Lock Region0 3 - Lock both regions\r\n"
        "  region1_key=<key string>  16 bytes hex string\r\n"
        "  region1_arg=<0/1>,[start,length,permission] See region0_arg usage\r\n"
        "  region1_lock=<0/1/2/3> See region0_lock usage\r\n"
        "  use_zero_key=<0/1> 0 - Random key, 1 - Zero key, default: 0\r\n"
        "  is_boot_image=<0/1> 0 - Non-bootable image, 1-bootable image, default:1\r\n"
        "-------------------------------------------------------------------\r\n"
        "Example:\r\n"
        "image_enc ifile=plain_img.bin ofile=enc_img.bin base_addr=0x60000000\r\n"
        "          region0_key=00112233445566778899aabbccddeeff\r\n"
        "          region0_arg=1,[0x60001000,0x5000,0]\r\n";


    printf("%s\r\n", usage_info);
}

// Assume c is an ascii digit
uint8_t ascii_to_digit(char c)
{
    uint8_t digit = 0;

    c = toupper(c);

    if (c >= 'A')
    {
        digit = (uint8_t)c - 'A' + 0x0A;
    }
    else
    {
        digit = (uint8_t)c - '0';
    }

    return digit;
}

bool convert_key_string_to_key_array(char *str, uint8_t *key)
{
    if (str == NULL || key == NULL)
    {
        return false;
    }

    size_t length = strlen(str);
    if (length != 32)
    {
        return false;
    }

    for (uint32_t i = 0; i < 32; i += 2)
    {
        uint8_t high_nibble = str[i];
        uint8_t low_nibble = str[i+1];

        if (!isxdigit(high_nibble) || !isxdigit(low_nibble))
        {
            printf("Invalid aes key\r\n");
            return false;
        }

        high_nibble = ascii_to_digit(high_nibble);
        low_nibble = ascii_to_digit(low_nibble);

        key[i / 2] = (high_nibble << 4) | low_nibble;
    }

    return true;
}

bool convert_region_arg_to_context(char *str, region_ctx_t *ctx)
{
    if (str == NULL || ctx == NULL)
    {
        return false;
    }
    uint32_t index = 0;
    char *substr = strstr(str, ",");
    if (substr != NULL)
    {
        char c;
        sscanf(str, "%c", &c);
        if (isxdigit(c))
        {
            c = ascii_to_digit(c);
            if (c == kAesMode_ECB || c == kAesMode_CTR)
            {
                ctx->aes_mode = c;
            }
            else
            {
                printf("Invalid AES mode in region arg\r\n");
                return false;
            }
        }
        else
        {
            printf("Invalid AES mode in region arg\r\n");
            return false;
        }
    }
    else
    {
        printf("Invalid region args\r\n");
        return false;
    }
    ++substr;
    char *current_substr_end = NULL;
    char *current_substr_start = NULL;
    while ((current_substr_end = strstr(substr, "]")) != NULL)
    {
        current_substr_start = strstr(substr, "[");
        if (current_substr_start == NULL || current_substr_start > current_substr_end)
        {
            printf("Invalid FAC region paramemters in region arg\r\n");
            return false;
        }

        uint32_t comma_count = 0;
        uint32_t bracket_left_count = 0;
        uint32_t bracket_right_count = 0;
        for (char *tmp = current_substr_start; tmp <= current_substr_end; tmp++)
        {
            if (*tmp == '[')
            {
                bracket_left_count++;
            }
            else if (*tmp == ']')
            {
                bracket_right_count++;
            }
            else if (*tmp == ',')
            {
                comma_count++;
            }
            else if (!isxdigit(*tmp) && toupper(*tmp) != 'X')
            {
                printf("Invalid FAC region parameters in region args\r\n");
                return false;
            }
        }
        if ((comma_count != 2) || (bracket_left_count != 1) || (bracket_right_count != 1))
        {
            printf("Invalid FAC region parameters in region args\r\n");
            return false;
        }

        sscanf(current_substr_start, "[%x,%x,%x]", &ctx->fac_region_ctx.fac_regions[index].start,
            &ctx->fac_region_ctx.fac_regions[index].length,
            &ctx->fac_region_ctx.fac_regions[index].fac_mode);
        if ((ctx->fac_region_ctx.fac_regions[index].start & 0x3FF) || (ctx->fac_region_ctx.fac_regions[index].length & 0x3FF))
        {
            printf("Invalid FAC region range, both start and length must be 1024-byte aligned\r\n");
            return false;
        }
        if (ctx->fac_region_ctx.fac_regions[index].fac_mode > kFacMode_ExecuteOnly)
        {
            printf("Invalid FAC region access permission mode, valid value is 0-3\r\n");
            return false;
        }
        index++;
        substr = ++current_substr_end;
    }
    ctx->fac_region_ctx.fac_region_count = index;
    return true;
}

bool get_gen_ctx(int argc, char *argv[], image_gen_ctx_t *gen_ctx)
{
    bool has_ifile = false;
    bool has_ofile = false;
    bool has_base_addr = false;

    bool region_key_exists[2] = { false, false };
    bool region_arg_exists[2] = { false, false };

    gen_ctx->regions[0].ctr_kib_type = k_Kib_Ctr_Type_Random;
    gen_ctx->regions[1].ctr_kib_type = k_Kib_Ctr_Type_Random;
    gen_ctx->is_boot_image = true;

    for (uint32_t i = 1; i < (uint32_t)argc; i++)
    {
        if (!strncmp(argv[i], "ifile=", 6))
        {
            gen_ctx->input_file = &argv[i][6];
            has_ifile = true;
        }
        else if (!strncmp(argv[i], "ofile=", 6))
        {
            gen_ctx->output_file = &argv[i][6];
            has_ofile = true;
        }
        else if (!strncmp(argv[i], "base_addr=", 10))
        {
            sscanf(argv[i] + 10, "%x", &gen_ctx->base_addr);
            has_base_addr = true;
        }
        else if (!strncmp(argv[i], "region0_lock=", 13))
        {
            sscanf(argv[i] + 13, "%d", &gen_ctx->regions[0].lock_option);
        }
        else if (!strncmp(argv[i], "region1_lock=", 13))
        {
            sscanf(argv[i] + 13, "%d", &gen_ctx->regions[1].lock_option);
        }
        else if (!strncmp(argv[i], "use_zero_key=", 13))
        {
            uint32_t temp;
            sscanf(argv[i] + 13, "%d", &temp);

            if (temp == 1)
            {
                gen_ctx->regions[0].ctr_kib_type = k_Kib_Ctr_Type_Zero;
                gen_ctx->regions[1].ctr_kib_type = k_Kib_Ctr_Type_Zero;
            }
        }
        else if (!strncmp(argv[i], "region0_key=", 12))
        {
            char key_string[64];
            sscanf(argv[i] + 12, "%s", key_string);
            
            bool result = convert_key_string_to_key_array(key_string, gen_ctx->regions[0].key);
            if (!result)
            {
                return false;
            }
            region_key_exists[0] = true;
        }
        else if (!strncmp(argv[i], "region1_key=", 12))
        {
            char key_string[64];
            sscanf(argv[i] + 12, "%s", key_string);

            bool result = convert_key_string_to_key_array(key_string, gen_ctx->regions[1].key);
            if (!result)
            {
                return false;
            }
            region_key_exists[1] = true;
        }
        else if (!strncmp(argv[i], "region0_arg=", 12))
        {
            char arg_string[512];
            sscanf(argv[i] + 12, "%s", arg_string);
            bool result = convert_region_arg_to_context(arg_string, &gen_ctx->regions[0]);
            if (!result)
            {
                return false;
            }
            region_arg_exists[0] = true;
        }
        else if (!strncmp(argv[i], "region1_arg=", 12))
        {
            char arg_string[512];
            sscanf(argv[i] + 12, "%s", arg_string);
            bool result = convert_region_arg_to_context(arg_string, &gen_ctx->regions[1]);
            if (!result)
            {
                return false;
            }
            region_arg_exists[1] = true;
        }
        else if (!strncmp(argv[i], "is_boot_image=", 14))
        {
            uint32_t temp;
            sscanf(argv[i] + 14, "%d", &temp);
            if (temp == 0)
            {
                gen_ctx->is_boot_image = false;
            }
        }
        else
        {
            printf("Unsupported argument\r\n");
            return false;
        }
    }

    if (!has_ifile || !has_ofile || !has_base_addr)
    {
        return false;
    }

    if ((region_arg_exists[0] ^ region_key_exists[0]) != 0)
    {
        printf("Region 0 Info is incomplete, lack key or args\r\n");
        return false;
    }

    if ((region_arg_exists[1] ^ region_key_exists[1]) != 0)
    {
        printf("Region 1 Info is incomplete, lack key or args\r\n");
        return false;
    }

    for(uint32_t i=0; i<2; i++)
    {
        if (region_arg_exists[i] && region_key_exists[i])
        {
            gen_ctx->regions[i].is_present = true;
        }
    }

    return true;
}