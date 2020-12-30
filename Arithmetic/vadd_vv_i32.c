#ifdef vadd_vv_i32_test
void vadd_vv_i32_test_main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;
    int32x16_t result;
    int32x16_t a={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17};
    int32x16_t b = {11,22,33,44,55,66,77,88,99,100,110,120,130,140,150,160,170};

    start = cycles();
	result = vadd_vv_i32(a,b);
	stop = cycles();

	printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);

	for(i=0;i<16;i++)
		printf("result[%d]=%d\n",i,result[i]);
	/*
	cycles  = stop-start    = 4304 - 4289 = 15
	result[0]=12
	result[1]=24
	result[2]=36
	result[3]=48
	result[4]=60
	result[5]=72
	result[6]=84
	result[7]=96
	result[8]=108
	result[9]=110
	result[10]=121
	result[11]=132
	result[12]=143
	result[13]=154
	result[14]=165
	result[15]=176
*/
}
#endif
