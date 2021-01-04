#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {

	/* Begin adding your custom code here */
	int i,error=0;
	int32_t base[16]={0};
	int32x16_t value={11,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
	uint32_t imm=0;
	int element_width = 32/8,element_num = 16,combo_num=1;
	bool16_t mask = {1,1,0,1,0,0};
	int32_t exp_result[16]={11,1,0,3,0};

//	vwr_csr(RUGRATS_VMELEMENTSTRIDE,element_width*combo_num);//element_stride = combo_num * element_width
//	vwr_csr(RUGRATS_VMCOMBOSTRIDE,element_width);  //combo_stride = element_width
//	vwr_csr(RUGRATS_VMGROUPSTRIDE,element_width*combo_num*2); //group_stride = element_stride *N( N = 1,2,3... && N <= element_num_per_group)
//	vwr_csr(RUGRATS_VMGROUPNUMBER,4);
//	vwr_csr(RUGRATS_VMGROUPDEPTH,combo_num*4);  //group_depth = element_width * element_num_per_group

	vstcb1in0_v_i32_m(mask,base,value,0);

	printf("result={");
	for(i=0;i<element_num;i++) {
		if(i==element_num-1)
			printf("%d}\n",base[i]);
		else
			printf("%d,",base[i]);
		//printf("exp_result[%d]=%d\n",i,exp_result[i]);
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
