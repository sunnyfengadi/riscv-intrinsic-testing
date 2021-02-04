#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32
#define COMBO_NUM 2

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
void vwmul_vx_i16_golden(int16_t *a,int16_t b,int32_t exp_result[][ELE_NUM]) {
     for (int i = 0; i < ELE_NUM; i++) {
        exp_result[i] = a[i]*b;
  }

}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int16x32_t a;
    int16_t b;
    int16_t exp_a[32];
    int16_t exp_b;

    int32x16x2_t result = {0};
    int32_t exp_result[2][16] = {0};

    data_init(a, exp_a, 32, 0xffff);
    data_init_scalar(b, exp_b, 0xffff);

    //Get golden result
    vwmul_vx_i16_golden(exp_a,exp_b,exp_result);

    //Get Intrinsic result
    result = vwmul_vx_i16(a,b);

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