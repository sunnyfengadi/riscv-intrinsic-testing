#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 8
#define COMBO_NUM 1
#define ELE_WIDTH 8
#define GROUP_NUM 4
#define GROUP_DEPTH 32
#define ELE_STRIDE 8
#define COMBO_STRIDE 8
#define GROUP_STRIDE 16

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
void vgldcb1_v_i64_m_golden(bool8_t *mask,int64_t maskoff,int64_t *base,int64_t index,int64_t *exp_result) {
     for(int i=0; i<COMBO_NUM; i++){
         for(int j=0; j<GROUP_NUM; j++){
             for(int k=0; k<GROUP_DEPTH/ELE_WIDTH; k++){
                 exp_result[i][j*GROUP_DEPTH/ELE_WIDTH+k] = base[i*COMBO_STRIDE/ELE_WIDTH+ j*GROUP_STRIDE/ELE_WIDTH + k*ELE_STRIDE/ELE_WIDTH];
             }
         }
     }
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool8_t mask;
    int64x8_t maskoff;
    int64_t base[ELE_NUM*COMBO_NUM];
    int64x8_t index;
    uint64_t exp_mask[8];
    int64_t exp_maskoff[8];
    int64_t exp_base[ELE_NUM*COMBO_NUM];
    int64_t exp_index[8];

    int64x8_t result = {0};
    int64_t exp_result[8] = {0};

    data_init_bool(mask, exp_mask, 8, 0xffffffffffffffff);
    data_init(maskoff, exp_maskoff, 8, 0xffffffffffffffff);
    data_init(base, exp_base, ELE_NUM*COMBO_NUM, 0xffffffffffffffff);
    data_init(index, exp_index, 8, 0xffffffffffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vgldcb1_v_i64_m_golden(exp_mask,exp_maskoff,exp_base,exp_index,exp_result);

    //Get Intrinsic result
    result = vgldcb1_v_i64_m(mask,maskoff,base,index);

    //compare result
    for(int i = 0; i < ELE_NUM; i++) {
        if(exp_result[i] != result[i]) {
            printf("Failed: result[%d] = %x, exp_result[%d] = %x\n", i, result[i], i, exp_result[i]);
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