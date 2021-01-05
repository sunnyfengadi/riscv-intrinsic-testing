#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i,j,combo_num = 2;
	int element_num = 16;
	int error=0;
	int element_width = 32/8;
	int32_t test[]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21};
	int32x16x2_t result;
    int32x16x2_t exp_result={1,3,5,7,5,7,9,11,9,11,13,15,13,15,17,19,2,4,6,8,6,8,10,12,10,12,14,16,14,16,18,20};

	vwr_csr(RUGRATS_VMELEMENTSTRIDE,element_width*combo_num);//element_stride = combo_num * element_width
	vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);  //combo_stride = element_width
	vwr_csr(RUGRATS_VMGROUPSTRIDE,16); //group_stride = element_stride *N( N = 1,2,3... && N <= element_num_per_group)
	vwr_csr(RUGRATS_VMGROUPNUMBER,4);
	vwr_csr(RUGRATS_VMGROUPDEPTH,16);  //group_depth = element_width * element_num_per_group

	start = cycles();
	result = vldcb2in0_v_i32(test,0);
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