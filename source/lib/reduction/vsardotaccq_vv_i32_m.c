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
void vsardotaccq_vv_i32_m_golden(uint64_t *src_mask,uint64_t *dst_mask,int32_t *a,int16_t *b,int16_t *c,accum ,int64_t *exp_result) {
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool16_t src_mask;
    bool8_t dst_mask;
    int32x16_t a;
    int16x32_t b;
    int16x32_t c;
    accum ;
    uint64_t exp_src_mask[16];
    uint64_t exp_dst_mask[8];
    int32_t exp_a[16];
    int16_t exp_b[32];
    int16_t exp_c[32];
    accum exp_;

    int64x8_t result = {0};
    int64_t exp_result[8] = {0};

    data_init_bool(src_mask, exp_src_mask, 16, 0xffffffff);
    data_init_bool(dst_mask, exp_dst_mask, 8, 0xffffffff);
    data_init(a, exp_a, 16, 0xffffffff);
    data_init(b, exp_b, 32, 0xffff);
    data_init(c, exp_c, 32, 0xffff);
    data_init_scalar(, exp_);

    //Get golden result
    vsardotaccq_vv_i32_m_golden(exp_src_mask,exp_dst_mask,exp_a,exp_b,exp_c,exp_result);

    //Get Intrinsic result
    result = vsardotaccq_vv_i32_m(src_mask,dst_mask,a,b,c);

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