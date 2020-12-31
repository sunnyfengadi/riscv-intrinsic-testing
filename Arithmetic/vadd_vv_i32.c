#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;
	int error=0;
	int element_num = 16;

    int32x16_t test1={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
	int32x16_t result;
	int32x16_t test2={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
	int32x16_t exp_result={2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32};

	start = cycles();
	result = vadd_vv_i32(test1,test2);
	stop = cycles();
	printf("cycles\t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);

	printf("result={");
	for(i=0;i<element_num;i++) {
		if(i==element_num-1)
			printf("%d}\n",result[i]);
		else
			printf("%d,",result[i]);

		//printf("exp_result[%d]=%d\n",j,exp_result[j]);
		if(exp_result[i] != result[i]) error = 1;
	}

	if(error)
		printf("TEST FAILED!\n");
	else
		printf("TEST PASSED!\n");

	/*
	 *
		cycles	= stop-start 	= 2787585 - 2787562 = 23
		result={2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32}
		TEST PASSED!
	 */
	// The while(1) here is a workaround solution to resolve an issue in simulator.
	// Once the simulator issue is fixed, the while(1) will be removed in the c src.
	while(1);
	return 0;
}
