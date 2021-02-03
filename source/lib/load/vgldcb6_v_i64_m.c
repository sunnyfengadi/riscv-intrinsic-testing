#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 8
#define COMBO_NUM 6
#define ELE_WIDTH 8
#define GROUP_NUM 4
#define GROUP_DEPTH 32
#define ELE_STRIDE 48
#define COMBO_STRIDE 8
#define GROUP_STRIDE 96

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
void vgldcb6_v_i64_m_golden(bool8_t *mask,int64_t maskoff,int64_t *base,int64_t index,int64_t exp_result[][ELE_NUM]) {
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
    int64x8x6_t maskoff;
    int64_t base[ELE_NUM*COMBO_NUM];
    int64x8_t index;
    uint64_t exp_mask[8];
    int64_t exp_maskoff[8*6];
    int64_t exp_base[ELE_NUM*COMBO_NUM];
    int64_t exp_index[8];

    int64x8x6_t result = {0};
    int64_t exp_result[8*6] = {0};

    data_init_bool(mask, exp_mask, 8, 0xffffffffffffffff);
    data_init(maskoff, exp_maskoff, 8*6, 0xffffffffffffffff);
    data_init(base, exp_base, ELE_NUM*COMBO_NUM, 0xffffffffffffffff);
    data_init(index, exp_index, 8, 0xffffffffffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vgldcb6_v_i64_m_golden(exp_mask,exp_maskoff,exp_base,exp_index,exp_result);

    //Get Intrinsic result
    result = vgldcb6_v_i64_m(mask,maskoff,base,index);

    //Compare Result
    for(int i = 0; i < COMBO_NUM; i++) {
        for(int j = 0; j < ELE_NUM; j++) {
            if(exp_result[i*ELE_NUM+j] != result.val[i][j]) {
                printf("Failed: result.val[%d][%d] = %x, exp_result[%d] = %x\n", i,j, result.val[i][j], i*ELE_NUM+j, exp_result[i*ELE_NUM+j]);
                //abort();
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