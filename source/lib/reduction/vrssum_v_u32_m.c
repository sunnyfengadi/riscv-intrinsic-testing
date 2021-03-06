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

#define data_init_matrix(a, b, n, m, threshold) \
  for(int i = 0; i < m; i++) { \
    for(int j = 0; j < n; j++) { \
      a.val[i][j] = random(threshold); \
      b[i][j] = a.val[i][j]; \
    } \
  }

#pragma GCC push_options
#pragma GCC optimize("O0")
__attribute__((noinline, noclone))
void vrssum_v_u32_m_golden(uint64_t *mask[2][16],uint32_t *maskoff,uint32_t *a,uint32_t *exp_result) {
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool16_t mask = m16(0x1101100000011011);
    bool16_t mask = m16(0x1101100000011011);
    uint32x16_t a;
    uint64_t exp_mask[16*2];
    uint32_t exp_maskoff[16];
    uint32_t exp_a[16];

    uint32x16_t result = {0};
    uint32_t exp_result[16] = {0};

    data_init(maskoff, exp_maskoff, 16, 0xffffffff);
    data_init(a, exp_a, 16, 0xffffffff);

    //Get golden result
    vrssum_v_u32_m_golden(exp_mask,exp_maskoff,exp_a,exp_result);

    //Get Intrinsic result
    result = vrssum_v_u32_m(mask,maskoff,a);

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