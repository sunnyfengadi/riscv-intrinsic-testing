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

#pragma GCC push_options
#pragma GCC optimize("O0")
__attribute__((noinline, noclone))
void vsrdotiircu_v_i32_d3s4_golden(int32_t base[],int32_t *a,int32_t *exp_result) {
    for (int i = 0; i < ELE_NUM; i++)
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int32_t base[ELE_NUM*COMBO_NUM];
    int32x16x4_t a;
    int32_t exp_base[ELE_NUM*COMBO_NUM];
    int32_t exp_a[16*4];

    int32x16x3_t result = {0};
    int32_t exp_result[16*3] = {0};

    data_init(base, exp_base, ELE_NUM*COMBO_NUM, 0xffffffff);
    data_init(a, exp_a, 16*4, 0xffffffff);

    vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);
    vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    //Get golden result
    vsrdotiircu_v_i32_d3s4_golden(exp_base,exp_a,exp_result);

    //Get Intrinsic result
    result = vsrdotiircu_v_i32_d3s4(base,a);

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