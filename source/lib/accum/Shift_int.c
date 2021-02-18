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

int64x8_t final_result0 = {0};
int64x8_t final_result1 = {0};
int64x8_t final_result2 = {0};
int64x8_t final_result3 = {0};
int64x8_t final_result4 = {0};
int64x8_t final_result5 = {0};
int64x8_t final_result6 = {0};
int64x8_t final_result7 = {0};

int main(void) {
    int error = 0;
    int64x8_t a;
    uint64x8_t b;
    uint32_t b;
    uint32_t imm;
    bool8_t mask = m8(0x100000101000001);
    int64x8_t maskoff;
    int64x8_t result0 = {0};
    int64x8_t result1 = {0};
    int64x8_t result2 = {0};
    int64x8_t result3 = {0};
    int64x8_t result4 = {0};
    int64x8_t result5 = {0};
    int64x8_t result6 = {0};
    int64x8_t result7 = {0};

    data_init(a, 8, 0xffffffffffffffff);
    data_init(b, 8, 0xffffffffffffffff);
    data_init_scalar(b, 0xffffffff);
    imm = rand()%8; // imm do not need to call data_init, 0xffffffff);
    data_init(maskoff, 8, 0xffffffffffffffff);

    //Get Intrinsic result
    result0 = vwsrl_av_i64(a, b, ACCUM0);
    result0 = vwsrl_ax_i64(result0, b, ACCUM0);
    result0 = vwsrl_ai_i64(result0, imm, ACCUM0);
    result0 = vwsrl_as_i64(result0, ACCUM0);
    result0 = vwsrl_av_i64_m(mask, maskoff, result0, b, ACCUM0);
    result0 = vwsrl_ax_i64_m(mask, maskoff, result0, b, ACCUM0);
    result0 = vwsrl_ai_i64_m(mask, maskoff, result0, imm, ACCUM0);
    result0 = vwsrl_as_i64_m(mask, maskoff, result0, ACCUM0);
    result0 = vcsl_i_i64(result0, imm, ACCUM0);
    final_result0 = vcsr_i_i64(result0, imm, ACCUM0);

    //Get Intrinsic result
    result1 = vwsrl_av_i64(a, b, ACCUM1);
    result1 = vwsrl_ax_i64(result1, b, ACCUM1);
    result1 = vwsrl_ai_i64(result1, imm, ACCUM1);
    result1 = vwsrl_as_i64(result1, ACCUM1);
    result1 = vwsrl_av_i64_m(mask, maskoff, result1, b, ACCUM1);
    result1 = vwsrl_ax_i64_m(mask, maskoff, result1, b, ACCUM1);
    result1 = vwsrl_ai_i64_m(mask, maskoff, result1, imm, ACCUM1);
    result1 = vwsrl_as_i64_m(mask, maskoff, result1, ACCUM1);
    result1 = vcsl_i_i64(result1, imm, ACCUM1);
    final_result1 = vcsr_i_i64(result1, imm, ACCUM1);

    //Get Intrinsic result
    result2 = vwsrl_av_i64(a, b, ACCUM2);
    result2 = vwsrl_ax_i64(result2, b, ACCUM2);
    result2 = vwsrl_ai_i64(result2, imm, ACCUM2);
    result2 = vwsrl_as_i64(result2, ACCUM2);
    result2 = vwsrl_av_i64_m(mask, maskoff, result2, b, ACCUM2);
    result2 = vwsrl_ax_i64_m(mask, maskoff, result2, b, ACCUM2);
    result2 = vwsrl_ai_i64_m(mask, maskoff, result2, imm, ACCUM2);
    result2 = vwsrl_as_i64_m(mask, maskoff, result2, ACCUM2);
    result2 = vcsl_i_i64(result2, imm, ACCUM2);
    final_result2 = vcsr_i_i64(result2, imm, ACCUM2);

    //Get Intrinsic result
    result3 = vwsrl_av_i64(a, b, ACCUM3);
    result3 = vwsrl_ax_i64(result3, b, ACCUM3);
    result3 = vwsrl_ai_i64(result3, imm, ACCUM3);
    result3 = vwsrl_as_i64(result3, ACCUM3);
    result3 = vwsrl_av_i64_m(mask, maskoff, result3, b, ACCUM3);
    result3 = vwsrl_ax_i64_m(mask, maskoff, result3, b, ACCUM3);
    result3 = vwsrl_ai_i64_m(mask, maskoff, result3, imm, ACCUM3);
    result3 = vwsrl_as_i64_m(mask, maskoff, result3, ACCUM3);
    result3 = vcsl_i_i64(result3, imm, ACCUM3);
    final_result3 = vcsr_i_i64(result3, imm, ACCUM3);

    //Get Intrinsic result
    result4 = vwsrl_av_i64(a, b, ACCUM4);
    result4 = vwsrl_ax_i64(result4, b, ACCUM4);
    result4 = vwsrl_ai_i64(result4, imm, ACCUM4);
    result4 = vwsrl_as_i64(result4, ACCUM4);
    result4 = vwsrl_av_i64_m(mask, maskoff, result4, b, ACCUM4);
    result4 = vwsrl_ax_i64_m(mask, maskoff, result4, b, ACCUM4);
    result4 = vwsrl_ai_i64_m(mask, maskoff, result4, imm, ACCUM4);
    result4 = vwsrl_as_i64_m(mask, maskoff, result4, ACCUM4);
    result4 = vcsl_i_i64(result4, imm, ACCUM4);
    final_result4 = vcsr_i_i64(result4, imm, ACCUM4);

    //Get Intrinsic result
    result5 = vwsrl_av_i64(a, b, ACCUM5);
    result5 = vwsrl_ax_i64(result5, b, ACCUM5);
    result5 = vwsrl_ai_i64(result5, imm, ACCUM5);
    result5 = vwsrl_as_i64(result5, ACCUM5);
    result5 = vwsrl_av_i64_m(mask, maskoff, result5, b, ACCUM5);
    result5 = vwsrl_ax_i64_m(mask, maskoff, result5, b, ACCUM5);
    result5 = vwsrl_ai_i64_m(mask, maskoff, result5, imm, ACCUM5);
    result5 = vwsrl_as_i64_m(mask, maskoff, result5, ACCUM5);
    result5 = vcsl_i_i64(result5, imm, ACCUM5);
    final_result5 = vcsr_i_i64(result5, imm, ACCUM5);

    //Get Intrinsic result
    result6 = vwsrl_av_i64(a, b, ACCUM6);
    result6 = vwsrl_ax_i64(result6, b, ACCUM6);
    result6 = vwsrl_ai_i64(result6, imm, ACCUM6);
    result6 = vwsrl_as_i64(result6, ACCUM6);
    result6 = vwsrl_av_i64_m(mask, maskoff, result6, b, ACCUM6);
    result6 = vwsrl_ax_i64_m(mask, maskoff, result6, b, ACCUM6);
    result6 = vwsrl_ai_i64_m(mask, maskoff, result6, imm, ACCUM6);
    result6 = vwsrl_as_i64_m(mask, maskoff, result6, ACCUM6);
    result6 = vcsl_i_i64(result6, imm, ACCUM6);
    final_result6 = vcsr_i_i64(result6, imm, ACCUM6);

    //Get Intrinsic result
    result7 = vwsrl_av_i64(a, b, ACCUM7);
    result7 = vwsrl_ax_i64(result7, b, ACCUM7);
    result7 = vwsrl_ai_i64(result7, imm, ACCUM7);
    result7 = vwsrl_as_i64(result7, ACCUM7);
    result7 = vwsrl_av_i64_m(mask, maskoff, result7, b, ACCUM7);
    result7 = vwsrl_ax_i64_m(mask, maskoff, result7, b, ACCUM7);
    result7 = vwsrl_ai_i64_m(mask, maskoff, result7, imm, ACCUM7);
    result7 = vwsrl_as_i64_m(mask, maskoff, result7, ACCUM7);
    result7 = vcsl_i_i64(result7, imm, ACCUM7);
    final_result7 = vcsr_i_i64(result7, imm, ACCUM7);

    return 0;
    }
    /* { dg-final { scan-assembler-times "vwsrl.av\t" 16} }
    /* { dg-final { scan-assembler-times "vwsrl.ax\t" 16} }
    /* { dg-final { scan-assembler-times "vwsrl.ai\t" 16} }
    /* { dg-final { scan-assembler-times "vwsrl.as\t" 16} }
    /* { dg-final { scan-assembler-times "vcsl.i\t" 8} }
    /* { dg-final { scan-assembler-times "vcsr.i\t" 8} }
