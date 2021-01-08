#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    bool16_t mask = {1,1,0,1,0,0,1,1};
    int32x16x3_t maskoff = {11,22,33,44,55,66,77,88};
    int32_t base[48] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48};
    uint32_t imm = 0;
    int combo_num = 3;
    int element_num = 16;
    int32x16x3_t result = {0};
    int32x16x3_t exp_result = {0};
    int element_width = 32/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,12);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,24);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,16);

    start = cycles();
    result = vldcb3in0_v_i32_m(mask,maskoff,base,0);
    stop = cycles();
    
    printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
    printf("result={");
    for(i=0;i<combo_num;i++) {
        for(j=0;j<element_num;j++) {
            if(j==element_num-1 && i==combo_num-1)
            printf("%d}\n",result.val[i][j]);
        else
            printf("%d,",result.val[i][j]);
            if(exp_result.val[i][j] != result.val[i][j]) error = 1;
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