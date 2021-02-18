#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32
#define COMBO_NUM 2

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
void vwnmsac_vv_i16_m_golden(uint64_t *mask,int32_t a[2][16],int16_t *b,int16_t *c,int32_t exp_result[][ELE_NUM]) {
//widden to do 
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool32_t mask = m32(0x5140014551400145);
    int32x16x2_t a;
    int16x32_t b;
    int16x32_t c;
    uint64_t exp_mask[32];
    int32_t exp_a[2][16];
    int16_t exp_b[32];
    int16_t exp_c[32];

    int32x16x2_t result = {0};
    int32_t exp_result[2][16] = {0};

    data_init_matrix(a, exp_a, 16, 2, 0xffffffff);
    data_init(b, exp_b, 32, 0xffff);
    data_init(c, exp_c, 32, 0xffff);

    //Get golden result
    vwnmsac_vv_i16_m_golden(exp_mask,exp_a,exp_b,exp_c,exp_result);

    //Get Intrinsic result
    result = vwnmsac_vv_i16_m(mask,a,b,c);

    // Compare Result
    for(int i = 0; i < COMBO_NUM; i++) {
        for(int j = 0; j < ELE_NUM; j++) {
            if(exp_result[i][j] != result.val[i][j]) {
                printf("Failed: result.val[%d][%d] = %llx, exp_result[%d][%d] = %llx\n", i,j, result.val[i][j], i,j, exp_result[i][j]);
                abort();
                error = 1;
            }
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