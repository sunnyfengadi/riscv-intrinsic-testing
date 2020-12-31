#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;
	int error=0;
	int element_num = 16;

	int32x16_t a={11,22,33,44,55,66,77,88,99,100,110,120,130,140,150,160};
    int32x16_t b={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
	int32x16_t result;
	int32x16_t exp_result={10,20,30,40,50,60,70,80,90,90,99,108,117,126,135,144};

	start = cycles();
	result = vsub_vv_i32(a,b);
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
	cycles	= stop-start 	= 5384399 - 5384376 = 23
	result={10,20,30,40,50,60,70,80,90,90,99,108,117,126,135,144}
	TEST PASSED!
	 */
	// The while(1) here is a workaround solution to resolve an issue in simulator.
	// Once the simulator issue is fixed, the while(1) will be removed in the c src.
	while(1);
	return 0;
}
