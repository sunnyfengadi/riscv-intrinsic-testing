#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32

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
void vssub_vx_i16_m_golden(uint64_t *mask,int16_t *maskoff,int16_t *a,int16_t b,int16_t *exp_result) {
     for (int i = 0; i < ELE_NUM; i++) {
        exp_result[i] = TODO;
  }

}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    bool32_t mask;
    int16x32_t maskoff;
    int16x32_t a;
    int16_t b;
    uint64_t exp_mask[32];
    int16_t exp_maskoff[32];
    int16_t exp_a[32];
    int16_t exp_b;

    int16x32_t result = {0};
    int16_t exp_result[32] = {0};

    data_init_bool(mask, exp_mask, 32, 0xffff);
    data_init(maskoff, exp_maskoff, 32, 0xffff);
    data_init(a, exp_a, 32, 0xffff);
    data_init_scalar(b, exp_b, 0xffff);

    //Get golden result
    vssub_vx_i16_m_golden(exp_mask,exp_maskoff,exp_a,exp_b,exp_result);

    //Get Intrinsic result
    result = vssub_vx_i16_m(mask,maskoff,a,b);

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