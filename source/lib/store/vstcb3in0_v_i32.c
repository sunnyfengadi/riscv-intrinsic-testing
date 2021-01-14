#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    int32_t base[16] = ;
    int32x16x3_t value = ;
    uint32_t imm = 0;
    int combo_num = 3;
    int element_num = 16;
    int32_t exp_result[16] = {0};
    int element_width = 32/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,12);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,24);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,16);

    vstcb3in0_v_i32(base,value,0);
    
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