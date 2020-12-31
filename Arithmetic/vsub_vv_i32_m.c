#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;
	int error=0;
	int element_num = 16;
    int32x16_t result;
    int32x16_t a = {11,22,33,44,55,66,77,88,99,100,110,120,130,140,150,160,170};
	int32x16_t b ={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17};
    int32x16_t mask_off = {111,222,333,444,555,666,777,888,999,1100,1110,1120,1130,1140,1150,1160}; //Initialise V0
    bool16_t mask={1,1,0,1,0,0};
	int32x16_t exp_result={10,20,333,40,555,666,777,888,999,1100,1110,1120,1130,1140,1150,1160};


    start = cycles();
	result = vsub_vv_i32_m(mask,mask_off,a,b);
	stop = cycles();

	printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
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
	cycles 	= stop-start 	= 162668448 - 162668416 = 32
	result={10,20,333,40,555,666,777,888,999,1100,1110,1120,1130,1140,1150,1160}
	TEST PASSED!
*/
	// The //while(1) here is a workaround solution to resolve an issue in simulator.
	// Once the simulator issue is fixed, the //while(1) will be removed in the c src.
	//while(1);
	return 0;
}
