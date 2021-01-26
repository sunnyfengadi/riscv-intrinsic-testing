#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    bool32_t mask = {1,1,0,1,0,0};
    int16x32_t maskoff = {11,22,33,44,55,66,77,88};
    int16x32_t a = {1,2,3,4,5,6,7,8};
    int16_t b = 0xff;
    int element_num = 32;
    int16x32_t result = {0};
    int16x32_t exp_result = {0};

    start = cycles();
    result = vssub_vx_i16_m(mask,maskoff,a,b);
    stop = cycles();

    printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
    printf("result={");
    for(i=0;i<element_num;i++) {
        if(i==element_num-1)
            printf("%d}\n",result[i]);
        else
            printf("%d,",result[i]);

        if(exp_result[i] != result[i]) error = 1;
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