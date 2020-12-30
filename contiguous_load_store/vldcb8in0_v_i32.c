#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int n=0,i,j,combo_num = 8;
	int element_num = 16;
	int error=0;
	int element_width = 32/8;
	int32_t test[16*8]={0};
	for (i=0;i<40;i++)
		test[i]=i;

	int32x16x8_t result={0};
    int32x16x8_t exp_result={0};

	vwr_csr(RUGRATS_VMELEMENTSTRIDE,32);//element_stride = combo_num * element_width
	vwr_csr(RUGRATS_VMCOMBOSTRIDE,4);  //combo_stride = element_width
	vwr_csr(RUGRATS_VMGROUPSTRIDE,64); //group_stride = element_stride *N( N = 1,2,3... && N <= element_num_per_group)
	vwr_csr(RUGRATS_VMGROUPNUMBER,4);
	vwr_csr(RUGRATS_VMGROUPDEPTH,16);  //group_depth = element_width * element_num_per_group

	start = cycles();
	result = vldcb8in0_v_i32(test,0);
	stop = cycles();

	printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);

	for(i=0;i<combo_num;i++) {
		for(j=0;j<element_num;j++) {
			printf("result[%d][%d]=%d\n",i,j,result.val[i][j]);
			//printf("exp_result[%d][%d]=%d\n",i,j,exp_result.val[i][j]);
			if(exp_result.val[i][j] != result.val[i][j]) error = 1;
		}
	}

	if(error)
		printf("TEST FAILED!\n");
	else
		printf("TEST PASSED!\n");

	// The while(1) here is a workaround solution to resolve an issue in simulator.
	// Once the simulator issue is fixed, the while(1) will be removed in the c src.
	while(1);
	return 0;
}

