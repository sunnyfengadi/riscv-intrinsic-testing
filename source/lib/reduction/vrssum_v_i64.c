#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 8

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
void vrssum_v_i64_golden(int64_t *a,int64_t *exp_result) {
    for (int i = 0; i < ELE_NUM; i++)
Operator Line --- TODO
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int64x8_t a;
    int64_t exp_a[8];

    int64x8_t result = {0};
    int64_t exp_result[8] = {0};

    data_init(a, exp_a, 8, 0xffffffffffffffff);

    //Get golden result
    vrssum_v_i64_golden(exp_a,exp_result);

    //Get Intrinsic result
    result = vrssum_v_i64(a);

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