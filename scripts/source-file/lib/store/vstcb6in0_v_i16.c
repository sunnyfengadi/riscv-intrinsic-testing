#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    int16_t base[32] = ;
    int16x32x6_t value = ;
    uint32_t imm = 0;
    int combo_num = 6;
    int element_num = 32;
    int16_t exp_result[32] = {0};
    int element_width = 16/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,12);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,2);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,24);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,8);

    vstcb6in0_v_i16(base,value,0);
    
    printf("result={");
    for(i=0;i<element_num*combo_num;i++) {
        if(i==element_num*combo_num-1)
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