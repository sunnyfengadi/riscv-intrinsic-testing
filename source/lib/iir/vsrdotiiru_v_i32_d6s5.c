#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16
#define COMBO_NUM 6

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
void vsrdotiiru_v_i32_d6s5_golden(int32_t *base,int32_t a[5][16],int32_t exp_result[][ELE_NUM]) {
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int32_t base[ELE_NUM*COMBO_NUM];
    int32x16x5_t a;
    int32_t exp_base[ELE_NUM*COMBO_NUM];
    int32_t exp_a[5][16];

    int32x16x6_t result = {0};
    int32_t exp_result[6][16] = {0};

    data_init(base, exp_base, ELE_NUM*COMBO_NUM, 0xffffffff);
    data_init_matrix(a, exp_a, 16, 5, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vsrdotiiru_v_i32_d6s5_golden(exp_base,exp_a,exp_result);

    //Get Intrinsic result
    result = vsrdotiiru_v_i32_d6s5(base,a);

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