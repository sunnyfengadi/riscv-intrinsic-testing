#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16

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
void vardotacc_vv_u32_m1_golden(bool8_t dst_mask,uint32_t *a,uint16_t *b,uint16_t *c,uint64_t *exp_result) {
    for (int i = 0; i < ELE_NUM; i++)
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool8_t dst_mask;
    uint32x16_t a;
    uint16x32_t b;
    uint16x32_t c;
    enum ACCUM accum;
    uint64_t exp_dst_mask[8];
    uint32_t exp_a[16];
    uint16_t exp_b[32];
    uint16_t exp_c[32];
    enum ACCUM exp_accum;

    uint64x8_t result = {0};
    uint64_t exp_result[8] = {0};

    data_init_bool(dst_mask, exp_dst_mask, 8, 0xffffffff);
    data_init(a, exp_a, 16, 0xffffffff);
    data_init(b, exp_b, 32, 0xffff);
    data_init(c, exp_c, 32, 0xffff);
    data_init_scalar(accum, exp_accum);

    //Get golden result
    vardotacc_vv_u32_m1_golden(exp_dst_mask,exp_a,exp_b,exp_c,exp_accum,exp_result);

    //Get Intrinsic result
    result = vardotacc_vv_u32_m1(dst_mask,a,b,c,accum);

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