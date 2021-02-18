#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define random(threshold) rand()%threshold
#define data_init_scalar(a, threshold) \
  a = random(threshold);
#define data_init(a, n, threshold) \
  for(int i = 0; i < n; i++) { \
    a[i] = random(threshold); \
  }
#define data_init_matrix(a, m, n, threshold) \
  for(int i = 0; i < m; i++) { \
    for(int j = 0; j < n; j++) { \
      a.val[i][j] = random(threshold); \
    } \
  }

#define ELE_NUM 8

uint64x8_t final_result0 = {0};
uint64x8_t final_result1 = {0};
uint64x8_t final_result2 = {0};
uint64x8_t final_result3 = {0};
uint64x8_t final_result4 = {0};
uint64x8_t final_result5 = {0};
uint64x8_t final_result6 = {0};
uint64x8_t final_result7 = {0};

int main(void) {
    int error = 0;
    uint64x8_t a;
    uint32x16_t b;
    uint32x16_t c;
    bool8_t dst_mask = m8(0x100000101000001);
    bool16_t src_mask = m16(0x1101100000011011);
    uint64x8_t result0 = {0};
    uint64x8_t result1 = {0};
    uint64x8_t result2 = {0};
    uint64x8_t result3 = {0};
    uint64x8_t result4 = {0};
    uint64x8_t result5 = {0};
    uint64x8_t result6 = {0};
    uint64x8_t result7 = {0};

    data_init(a, 8, 0xffffffffffffffff);
    data_init(b, 16, 0xffffffff);
    data_init(c, 16, 0xffffffff);

    //Get Intrinsic result
    result0 = vardotacc_vv_u32(a, b, c, ACCUM0);
    result0 = vardotacc_vv_u32_m1(dst_mask, result0, b, c, ACCUM0);
    final_result0 = vardotacc_vv_u32_m(src_mask, dst_mask, result0, b, c, ACCUM0);

    //Get Intrinsic result
    result1 = vardotacc_vv_u32(a, b, c, ACCUM1);
    result1 = vardotacc_vv_u32_m1(dst_mask, result1, b, c, ACCUM1);
    final_result1 = vardotacc_vv_u32_m(src_mask, dst_mask, result1, b, c, ACCUM1);

    //Get Intrinsic result
    result2 = vardotacc_vv_u32(a, b, c, ACCUM2);
    result2 = vardotacc_vv_u32_m1(dst_mask, result2, b, c, ACCUM2);
    final_result2 = vardotacc_vv_u32_m(src_mask, dst_mask, result2, b, c, ACCUM2);

    //Get Intrinsic result
    result3 = vardotacc_vv_u32(a, b, c, ACCUM3);
    result3 = vardotacc_vv_u32_m1(dst_mask, result3, b, c, ACCUM3);
    final_result3 = vardotacc_vv_u32_m(src_mask, dst_mask, result3, b, c, ACCUM3);

    //Get Intrinsic result
    result4 = vardotacc_vv_u32(a, b, c, ACCUM4);
    result4 = vardotacc_vv_u32_m1(dst_mask, result4, b, c, ACCUM4);
    final_result4 = vardotacc_vv_u32_m(src_mask, dst_mask, result4, b, c, ACCUM4);

    //Get Intrinsic result
    result5 = vardotacc_vv_u32(a, b, c, ACCUM5);
    result5 = vardotacc_vv_u32_m1(dst_mask, result5, b, c, ACCUM5);
    final_result5 = vardotacc_vv_u32_m(src_mask, dst_mask, result5, b, c, ACCUM5);

    //Get Intrinsic result
    result6 = vardotacc_vv_u32(a, b, c, ACCUM6);
    result6 = vardotacc_vv_u32_m1(dst_mask, result6, b, c, ACCUM6);
    final_result6 = vardotacc_vv_u32_m(src_mask, dst_mask, result6, b, c, ACCUM6);

    //Get Intrinsic result
    result7 = vardotacc_vv_u32(a, b, c, ACCUM7);
    result7 = vardotacc_vv_u32_m1(dst_mask, result7, b, c, ACCUM7);
    final_result7 = vardotacc_vv_u32_m(src_mask, dst_mask, result7, b, c, ACCUM7);

    return 0;
    }
    /* { dg-final { scan-assembler-times "vardotacc.vv\t" 24} } */
