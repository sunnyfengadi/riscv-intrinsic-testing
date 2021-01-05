#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {
	unsigned long start=0,stop=0;
	int i,j,combo_num = 1;
	int element_num = 16;
	int error=0;
	uint32_t imm=0;
    int32_t test[]={1,2,3,4,5,6,7,8,9,10,11,12,14,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32};
    int32x16_t result;
    int32x16_t exp_result={1,0,2,0,3,0,4,0,5,0,6,0,7,0,8,0};

    start = cycles();
	result = vldcb1in1_v_i32(test,0);
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
