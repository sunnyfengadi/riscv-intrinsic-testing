#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16
#define COMBO_NUM 3
#define ELE_WIDTH 4
#define GROUP_NUM 4
#define GROUP_DEPTH 16
#define ELE_STRIDE 12
#define COMBO_STRIDE 4
#define GROUP_STRIDE 24

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
void vsstcb3_v_i32_golden(int32_t *base,int32_t *index,int32_t value[3][16],) {
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int32_t base[ELE_NUM*COMBO_NUM];
    int32x16_t index;
    int32x16x3_t value;
    int32_t exp_base[ELE_NUM*COMBO_NUM];
    int32_t exp_index[16];
    int32_t exp_value[3][16];


    //base here is output, do not need to call data_init, 0xffffffff);
    data_init(index, exp_index, 16, 0xffffffff);
    data_init_matrix(value, exp_value, 16, 3, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vsstcb3_v_i32_golden(exp_base,exp_index,exp_value,exp_result);

    //Get Intrinsic result
    vsstcb3_v_i32(base,index,value);

    //compare result
    for(i=0;i<ELE_NUM*COMBO_NUM;i++) {
        if(exp_base[i] != base[i]) {
            printf("Failed: result[%d] = %x, exp_result[%d] = %x\n", i, base[i], i, exp_base[i]);
            //abort();
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