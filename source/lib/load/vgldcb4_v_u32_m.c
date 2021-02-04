#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16
#define COMBO_NUM 4
#define ELE_WIDTH 4
#define GROUP_NUM 4
#define GROUP_DEPTH 16
#define ELE_STRIDE 16
#define COMBO_STRIDE 4
#define GROUP_STRIDE 32

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
void vgldcb4_v_u32_m_golden(uint64_t *mask,uint32_t maskoff[4][16],uint32_t *base,int32_t *index,uint32_t exp_result[][ELE_NUM]) {
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
    bool16_t mask;
    uint32x16x4_t maskoff;
    uint32_t base[ELE_NUM*COMBO_NUM];
    int32x16_t index;
    uint64_t exp_mask[16];
    uint32_t exp_maskoff[4][16];
    uint32_t exp_base[ELE_NUM*COMBO_NUM];
    int32_t exp_index[16];

    uint32x16x4_t result = {0};
    uint32_t exp_result[4][16] = {0};

    data_init_bool(mask, exp_mask, 16, 0xffffffff);
    data_init_matrix(maskoff, exp_maskoff, 16, 4, 0xffffffff);
    data_init(base, exp_base, ELE_NUM*COMBO_NUM, 0xffffffff);
    data_init(index, exp_index, 16, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vgldcb4_v_u32_m_golden(exp_mask,exp_maskoff,exp_base,exp_index,exp_result);

    //Get Intrinsic result
    result = vgldcb4_v_u32_m(mask,maskoff,base,index);

    // Compare Result
    for(int i = 0; i < COMBO_NUM; i++) {
        for(int j = 0; j < ELE_NUM; j++) {
            if(exp_result[i][j] != result.val[i][j]) {
                printf("Failed: result.val[%d][%d] = %d, exp_result[%d][%d] = %d\n", i,j, result.val[i][j], i,j, exp_result[i][j]);
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