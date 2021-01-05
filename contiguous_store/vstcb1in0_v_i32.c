#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {

	/* Begin adding your custom code here */
	int i,error=0;
	int32_t base[16]={0};
	int32x16_t value={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
	uint32_t imm=0;
	int element_num = 16;
	int32_t exp_result[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};

	vstcb1in0_v_i32(base,value,0);

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
