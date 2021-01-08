#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    int32_t base[16] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
    uint32_t imm = imm;
    int combo_num = 1;
    int element_num = 16;
    int32x16_t result = {0};
    int32x16_t exp_result = {1,3,5,7,5,7,9,11,9,11,13,15,13,15,17,19,2,4,6,8,6,8,10,12,10,12,14,16,14,16,18,20};
    int element_width = 32/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,4);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,8);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,16);

    start = cycles();
    result = vldcb1in0_v_i32(base,0);
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