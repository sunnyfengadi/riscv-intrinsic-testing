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
#define COMBO_NUM 2

int64x8x2_t final_result0 = {0};
int64x8x2_t final_result1 = {0};
int64x8x2_t final_result2 = {0};
int64x8x2_t final_result3 = {0};
int64x8x2_t final_result4 = {0};
int64x8x2_t final_result5 = {0};
int64x8x2_t final_result6 = {0};
int64x8x2_t final_result7 = {0};

int main(void) {
    int error = 0;
    int64x8x2_t a;
    int32x16_t b;
    int32x16_t c;
    bool16_t mask = m16(0x1101100000011011);
    int64x8x2_t result0 = {0};
    int64x8x2_t result1 = {0};
    int64x8x2_t result2 = {0};
    int64x8x2_t result3 = {0};
    int64x8x2_t result4 = {0};
    int64x8x2_t result5 = {0};
    int64x8x2_t result6 = {0};
    int64x8x2_t result7 = {0};

    data_init_matrix(a, 8, 2, 0xffffffffffffffff);
    data_init(b, 16, 0xffffffff);
    data_init(c, 16, 0xffffffff);

    //Get Intrinsic result
    result0 = vwmacc_vv_i32(a, b, c, ACCUM0);
    result0 = vwsmaccq_vv_i32(result0, b, c, ACCUM0);
    result0 = vwmacc_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwsmaccq_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwmsub_vv_i32(result0, b, c, ACCUM0);
    result0 = vwsmsubq_vv_i32(result0, b, c, ACCUM0);
    result0 = vwmsub_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwsmsubq_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwnmsac_vv_i32(result0, b, c, ACCUM0);
    result0 = vwsnmsacq_vv_i32(result0, b, c, ACCUM0);
    result0 = vwnmsac_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwsnmsacq_vv_i32_m(mask, result0, b, c, ACCUM0);
    result0 = vwnmsub_vv_i32(result0, b, c, ACCUM0);
    result0 = vwsnmsubq_vv_i32(result0, b, c, ACCUM0);
    result0 = vwnmsub_vv_i32_m(mask, result0, b, c, ACCUM0);
    final_result0 = vwsnmsubq_vv_i32_m(mask, result0, b, c, ACCUM0);

    //Get Intrinsic result
    result1 = vwmacc_vv_i32(a, b, c, ACCUM1);
    result1 = vwsmaccq_vv_i32(result1, b, c, ACCUM1);
    result1 = vwmacc_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwsmaccq_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwmsub_vv_i32(result1, b, c, ACCUM1);
    result1 = vwsmsubq_vv_i32(result1, b, c, ACCUM1);
    result1 = vwmsub_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwsmsubq_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwnmsac_vv_i32(result1, b, c, ACCUM1);
    result1 = vwsnmsacq_vv_i32(result1, b, c, ACCUM1);
    result1 = vwnmsac_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwsnmsacq_vv_i32_m(mask, result1, b, c, ACCUM1);
    result1 = vwnmsub_vv_i32(result1, b, c, ACCUM1);
    result1 = vwsnmsubq_vv_i32(result1, b, c, ACCUM1);
    result1 = vwnmsub_vv_i32_m(mask, result1, b, c, ACCUM1);
    final_result1 = vwsnmsubq_vv_i32_m(mask, result1, b, c, ACCUM1);

    //Get Intrinsic result
    result2 = vwmacc_vv_i32(a, b, c, ACCUM2);
    result2 = vwsmaccq_vv_i32(result2, b, c, ACCUM2);
    result2 = vwmacc_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwsmaccq_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwmsub_vv_i32(result2, b, c, ACCUM2);
    result2 = vwsmsubq_vv_i32(result2, b, c, ACCUM2);
    result2 = vwmsub_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwsmsubq_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwnmsac_vv_i32(result2, b, c, ACCUM2);
    result2 = vwsnmsacq_vv_i32(result2, b, c, ACCUM2);
    result2 = vwnmsac_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwsnmsacq_vv_i32_m(mask, result2, b, c, ACCUM2);
    result2 = vwnmsub_vv_i32(result2, b, c, ACCUM2);
    result2 = vwsnmsubq_vv_i32(result2, b, c, ACCUM2);
    result2 = vwnmsub_vv_i32_m(mask, result2, b, c, ACCUM2);
    final_result2 = vwsnmsubq_vv_i32_m(mask, result2, b, c, ACCUM2);

    //Get Intrinsic result
    result3 = vwmacc_vv_i32(a, b, c, ACCUM3);
    result3 = vwsmaccq_vv_i32(result3, b, c, ACCUM3);
    result3 = vwmacc_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwsmaccq_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwmsub_vv_i32(result3, b, c, ACCUM3);
    result3 = vwsmsubq_vv_i32(result3, b, c, ACCUM3);
    result3 = vwmsub_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwsmsubq_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwnmsac_vv_i32(result3, b, c, ACCUM3);
    result3 = vwsnmsacq_vv_i32(result3, b, c, ACCUM3);
    result3 = vwnmsac_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwsnmsacq_vv_i32_m(mask, result3, b, c, ACCUM3);
    result3 = vwnmsub_vv_i32(result3, b, c, ACCUM3);
    result3 = vwsnmsubq_vv_i32(result3, b, c, ACCUM3);
    result3 = vwnmsub_vv_i32_m(mask, result3, b, c, ACCUM3);
    final_result3 = vwsnmsubq_vv_i32_m(mask, result3, b, c, ACCUM3);

    //Get Intrinsic result
    result4 = vwmacc_vv_i32(a, b, c, ACCUM4);
    result4 = vwsmaccq_vv_i32(result4, b, c, ACCUM4);
    result4 = vwmacc_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwsmaccq_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwmsub_vv_i32(result4, b, c, ACCUM4);
    result4 = vwsmsubq_vv_i32(result4, b, c, ACCUM4);
    result4 = vwmsub_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwsmsubq_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwnmsac_vv_i32(result4, b, c, ACCUM4);
    result4 = vwsnmsacq_vv_i32(result4, b, c, ACCUM4);
    result4 = vwnmsac_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwsnmsacq_vv_i32_m(mask, result4, b, c, ACCUM4);
    result4 = vwnmsub_vv_i32(result4, b, c, ACCUM4);
    result4 = vwsnmsubq_vv_i32(result4, b, c, ACCUM4);
    result4 = vwnmsub_vv_i32_m(mask, result4, b, c, ACCUM4);
    final_result4 = vwsnmsubq_vv_i32_m(mask, result4, b, c, ACCUM4);

    //Get Intrinsic result
    result5 = vwmacc_vv_i32(a, b, c, ACCUM5);
    result5 = vwsmaccq_vv_i32(result5, b, c, ACCUM5);
    result5 = vwmacc_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwsmaccq_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwmsub_vv_i32(result5, b, c, ACCUM5);
    result5 = vwsmsubq_vv_i32(result5, b, c, ACCUM5);
    result5 = vwmsub_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwsmsubq_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwnmsac_vv_i32(result5, b, c, ACCUM5);
    result5 = vwsnmsacq_vv_i32(result5, b, c, ACCUM5);
    result5 = vwnmsac_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwsnmsacq_vv_i32_m(mask, result5, b, c, ACCUM5);
    result5 = vwnmsub_vv_i32(result5, b, c, ACCUM5);
    result5 = vwsnmsubq_vv_i32(result5, b, c, ACCUM5);
    result5 = vwnmsub_vv_i32_m(mask, result5, b, c, ACCUM5);
    final_result5 = vwsnmsubq_vv_i32_m(mask, result5, b, c, ACCUM5);

    //Get Intrinsic result
    result6 = vwmacc_vv_i32(a, b, c, ACCUM6);
    result6 = vwsmaccq_vv_i32(result6, b, c, ACCUM6);
    result6 = vwmacc_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwsmaccq_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwmsub_vv_i32(result6, b, c, ACCUM6);
    result6 = vwsmsubq_vv_i32(result6, b, c, ACCUM6);
    result6 = vwmsub_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwsmsubq_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwnmsac_vv_i32(result6, b, c, ACCUM6);
    result6 = vwsnmsacq_vv_i32(result6, b, c, ACCUM6);
    result6 = vwnmsac_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwsnmsacq_vv_i32_m(mask, result6, b, c, ACCUM6);
    result6 = vwnmsub_vv_i32(result6, b, c, ACCUM6);
    result6 = vwsnmsubq_vv_i32(result6, b, c, ACCUM6);
    result6 = vwnmsub_vv_i32_m(mask, result6, b, c, ACCUM6);
    final_result6 = vwsnmsubq_vv_i32_m(mask, result6, b, c, ACCUM6);

    //Get Intrinsic result
    result7 = vwmacc_vv_i32(a, b, c, ACCUM7);
    result7 = vwsmaccq_vv_i32(result7, b, c, ACCUM7);
    result7 = vwmacc_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwsmaccq_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwmsub_vv_i32(result7, b, c, ACCUM7);
    result7 = vwsmsubq_vv_i32(result7, b, c, ACCUM7);
    result7 = vwmsub_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwsmsubq_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwnmsac_vv_i32(result7, b, c, ACCUM7);
    result7 = vwsnmsacq_vv_i32(result7, b, c, ACCUM7);
    result7 = vwnmsac_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwsnmsacq_vv_i32_m(mask, result7, b, c, ACCUM7);
    result7 = vwnmsub_vv_i32(result7, b, c, ACCUM7);
    result7 = vwsnmsubq_vv_i32(result7, b, c, ACCUM7);
    result7 = vwnmsub_vv_i32_m(mask, result7, b, c, ACCUM7);
    final_result7 = vwsnmsubq_vv_i32_m(mask, result7, b, c, ACCUM7);

    return 0;
    }
    /* { dg-final { scan-assembler-times "vwmacc.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwsmaccq.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwmsub.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwsmsubq.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwnmsac.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwsnmsacq.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwnmsub.vv\t" 16} } */
    /* { dg-final { scan-assembler-times "vwsnmsubq.vv\t" 16} } */
