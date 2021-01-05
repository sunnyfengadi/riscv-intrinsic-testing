#include "rivai_rugrats.h"
#include "rivai_bare.h"

int main(void) {
	unsigned long start=0,stop=0;
	int i,j,combo_num = 1;
	int element_width=32/8,element_num = 16;
	int error=0;
	int16x32_t a = {0x1,0x2,0x4,0x8,0x10,0x100,0x1000,0xf,0xff,0xfff,0xffff};
	int16x32_t b = {0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff,0xffff};

	int16x32_t result={0};
	int16x32_t exp_result={0x1,0x2,0x4,0x8,0x10,0x100,0x1000,0xf,0xff,0xfff,0xffff};

    start = cycles();
	result = vand_vv_i16(a,b);
	stop = cycles();

	printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
	printf("result={");
	for(i=0;i<element_num;i++) {
		if(i==element_num-1)
			printf("0x%x}\n",result[i]);
		else
			printf("0x%x,",result[i]);

		//printf("exp_result[%d]=%d\n",j,exp_result[j]);
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
