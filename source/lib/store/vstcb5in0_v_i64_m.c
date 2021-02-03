#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 8
#define COMBO_NUM 5
#define ELE_WIDTH 8
#define GROUP_NUM 4
#define GROUP_DEPTH 32
#define ELE_STRIDE 40
#define COMBO_STRIDE 8
#define GROUP_STRIDE 80

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

#pragma GCC push_options
#pragma GCC optimize("O0")
__attribute__((noinline, noclone))
void vstcb5in0_v_i64_m_golden(bool8_t mask,int64_t base[],int64_t *value,uint32_t imm,void *exp_result) {
    for (int i = 0; i < ELE_NUM; i++)
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool8_t mask;
    int64_t base[ELE_NUM*COMBO_NUM];
    int64x8x5_t value;
    uint32_t imm;
    uint64_t exp_mask[8];
    int64_t exp_base[ELE_NUM*COMBO_NUM];
    int64_t exp_value[8*5];
    uint32_t exp_imm;


    data_init_bool(mask, exp_mask, 8, 0xffffffffffffffff);
    //base here is output, do not need to call data_init, 0xffffffffffffffff);
    data_init(value, exp_value, 8*5, 0xffffffffffffffff);
    imm = exp_imm = 0; // imm and exp_imm do not need to call data_init, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vstcb5in0_v_i64_m_golden(exp_mask,exp_base,exp_value,exp_imm,exp_result);

    //Get Intrinsic result
    vstcb5in0_v_i64_m(mask,base,value,0);

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