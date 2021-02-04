#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32
#define COMBO_NUM 7
#define ELE_WIDTH 2
#define GROUP_NUM 4
#define GROUP_DEPTH 8
#define ELE_STRIDE 14
#define COMBO_STRIDE 2
#define GROUP_STRIDE 28

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
void vstcb7in0_v_i16_golden(int16_t *base,int16_t value[7][32],uint32_t imm,) {
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int16_t base[ELE_NUM*COMBO_NUM];
    int16x32x7_t value;
    uint32_t imm;
    int16_t exp_base[ELE_NUM*COMBO_NUM];
    int16_t exp_value[7][32];
    uint32_t exp_imm;


    //base here is output, do not need to call data_init, 0xffff);
    data_init_matrix(value, exp_value, 32, 7, 0xffff);
    imm = exp_imm = 0; // imm and exp_imm do not need to call data_init, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vstcb7in0_v_i16_golden(exp_base,exp_value,exp_imm,exp_result);

    //Get Intrinsic result
    vstcb7in0_v_i16(base,value,0);

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