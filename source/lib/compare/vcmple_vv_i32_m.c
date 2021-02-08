#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16

#define random(threshold) rand()%threshold
//#define data_init_bool(a, b, n, threshold) \
//	a = b = 1;
#define data_init_scalar(a, b, threshold) \
  a = b = random(threshold);
#define data_init(a, b, n, threshold) \
  for(int i = 0; i < n; i++) { \
    a[i] = random(threshold); \
    b[i] = a[i]; \
  }

#define data_init_matrix(a, b, m, n, threshold) \
  for(int i = 0; i < m; i++) { \
    for(int j = 0; j < n; j++) { \
      a.val[i][j] = random(threshold); \
      b[i][j] = a.val[i][j]; \
    } \
  }

#pragma GCC push_options
#pragma GCC optimize("O0")
__attribute__((noinline, noclone))
void vcmple_vv_i32_m_golden(uint64_t *mask, int32_t *a, int32_t *b, int32_t *c, int32_t *d, int32_t *exp_result, ) {
  for (int i = 0; i < ELE_NUM; i++)
    exp_result[i] =mask[i] ? (a[i]<=b[i]? c[i] : d[i]) : d[i];
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool16_t mask = m16(0x1101100000011011);
    int32x16_t a;
    int32x16_t b;
    int32x16_t c;
    int32x16_t d;
    uint64_t exp_mask[ELE_NUM] = {1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};
    int32_t exp_a[16];
    int32_t exp_b[16];
    int32_t exp_c[16];
    int32_t exp_d[16];
    int32x16_t result = {0};
    int32_t exp_result[ELE_NUM] = {0};

    data_init(a, exp_a, 16, 0xffffffff);
    data_init(b, exp_b, 16, 0xffffffff);
    data_init(c, exp_c, 16, 0xffffffff);
    data_init(d, exp_d, 16, 0xffffffff);

    //Get golden result
    vcmple_vv_i32_m_golden(exp_mask,exp_a,exp_b, exp_c, exp_d, exp_result);

    //Get Intrinsic result
    bool16_t compare_result = vcmple_vv_i32_m(mask,a,b);
    result = vmerge_vv_i32(compare_result, c, d);

    //compare result
    for(int i = 0; i < ELE_NUM; i++) {
        if(exp_result[i] != result[i]) {
            printf("Failed: result[%d] = %x, exp_result[%d] = %x\n", i, result[i], i, exp_result[i]);
            abort();
            error = 1;
        }
    }

    if(error)
        printf("TEST FAILED!\n");
    else
        printf("TEST PASSED!\n");

    // The //while(1) here is a workaround solution to resolve an issue in simulator.
    // Once the simulator issue is fixed, the //while(1) will be removed in the c src.
    //while(1);
    return 0;
}