#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    uint32_t base[32] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32};
    uint32_t imm = ;
    int combo_num = 2;
    int element_num = 16;
    uint32x16x2_t result = {0};
    uint32x16x2_t exp_result = {0};
    int element_width = 32/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,8);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,16);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,16);

    start = cycles();
    result = vldcb2in0_v_u32(base,0);
    stop = cycles();
    
    printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
    printf("result={");
    for(i=0;i<combo_num;i++) {
    printf(".val[%d]={",i);
        for(j=0;j<element_num;j++) {
            if(j==element_num-1) printf("%d",result.val[i][j]);
            else printf("%d,",result.val[i][j]);

            if(exp_result.val[i][j] != result.val[i][j]) error = 1;
        }
    if (i==combo_num-1) printf("}}\n");
    else printf("},");

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