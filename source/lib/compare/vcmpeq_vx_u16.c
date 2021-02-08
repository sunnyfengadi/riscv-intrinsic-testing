#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32

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
void vcmpeq_vx_u16_golden(uint16_t *a, uint16_t *b, uint16_t *c, uint16_t *d, uint16_t *exp_result, ) {
  for (int i = 0; i < ELE_NUM; i++)
    exp_result[i] =(a[i]==b) ? c[i] : d[i];
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    uint16x32_t a;
    uint16_t b;
    uint16x32_t c;
    uint16x32_t d;
    uint16_t exp_a[32];
    uint16_t exp_b;
    uint16_t exp_c[32];
    uint16_t exp_d[32];
    uint16x32_t result = {0};
    uint16_t exp_result[ELE_NUM] = {0};

    data_init(a, exp_a, 32, 0xffff);
    data_init_scalar(b, exp_b, 0xffff);
    data_init(c, exp_c, 32, 0xffff);
    data_init(d, exp_d, 32, 0xffff);

    //Get golden result
    vcmpeq_vx_u16_golden(exp_a,exp_b, exp_c, exp_d, exp_result);

    //Get Intrinsic result
    bool32_t compare_result = vcmpeq_vx_u16(a,b);
    result = vmerge_vv_u16(compare_result, c, d);

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