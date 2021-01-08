#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    uint16_t base[32] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32};
    uint32_t imm = ;
    int combo_num = 1;
    int element_num = 32;
    uint16x32_t result = {0};
    uint16x32_t exp_result = {0};
    int element_width = 16/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,2);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,2);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,8);

    start = cycles();
    result = vldcb1in0_v_u16(base,0);
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