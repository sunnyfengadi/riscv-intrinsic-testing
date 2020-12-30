#ifdef vmul_vv_i32_test
void vmul_vv_i32_test_main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;

    int32x16_t test1={1,2,3,4,5,6,7,8,9,10};
	int32x16_t result;
	int32x16_t test2={1,2,3,4,5,6,7,8,9,10};

	start = cycles();
	result = vmul_vv_i32(test1,test2);
	stop = cycles();
	printf("cyclesu \t= stopu-startu \t= %u - %u = %u\n",stop,start,stop-start);

	for(i=0;i<16;i++)
		printf("result[%d]=%d\n",i,result[i]);
}
#endif
