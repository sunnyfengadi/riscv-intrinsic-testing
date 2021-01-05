#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    bool16_t mask = {1,1,0,1,0,0};
    uint32_t base[16] = ;
    uint32x16_t value = ;
    uint32_t imm = 0;
    int combo_num = 1;
    int element_num = 16;
    uint32_t exp_result[16] = {0};

    vstcb1in0_v_u32_m(mask,base,value,0);


    printf("result={");
    for(i=0;i<element_num;i++) {
        if(i==element_num-1)
            printf("%d}\n",base[i]);
        else
            printf("%d,",base[i]);
        if(exp_result[i] != base[i]) error = 1;
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