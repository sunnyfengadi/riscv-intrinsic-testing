#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
    unsigned long start = 0, stop = 0;
    int i,j;
    int error = 0;

    bool16_t mask = {1,1,0,1,0,0,1,1};
    uint32x16x8_t maskoff = {.val[0] = {11,22,33,44,55,66,77,88},
			.val[1] = {11,22,33,44,55,66,77,88},
			.val[2] = {11,22,33,44,55,66,77,88},
			.val[3] = {11,22,33,44,55,66,77,88},
			.val[4] = {11,22,33,44,55,66,77,88},
			.val[5] = {11,22,33,44,55,66,77,88},
			.val[6] = {11,22,33,44,55,66,77,88},
			.val[7] = {11,22,33,44,55,66,77,88}};
    uint32_t base[128] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128};
    uint32_t imm = 0;
    int combo_num = 8;
    int element_num = 16;
    uint32x16x8_t result = {0};
    uint32x16x8_t exp_result = {0};
    int element_width = 32/8;

    vwr_csr(RUGRATS_VMELEMENTSTRIDE,32);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);
    vwr_csr(RUGRATS_VMGROUPSTRIDE,64);
    vwr_csr(RUGRATS_VMGROUPNUMBER,4);
    vwr_csr(RUGRATS_VMGROUPDEPTH,16);

    start = cycles();
    result = vldcb8in0_v_u32_m(mask,maskoff,base,0);
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