#ifdef vadd_vv_i32_test
void vadd_vv_i32_test_main() {
	/* Begin adding your custom code here */
	unsigned long start=0,stop=0;
	int i;
    int32x16_t result;
    int32x16_t a={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17};
    int32x16_t b = {11,22,33,44,55,66,77,88,99,100,110,120,130,140,150,160,170};

    int32x16_t mask_off = {111,222,333,444,555,666,777,888,999,1100,1110,1120,1130,1140,1150,1160}; //Initialise V0
    bool16_t mask={1,1,0,1,0,0};


    start = cycles();
	result = vadd_vv_i32_m(mask,mask_off,a,b);
	stop = cycles();

	printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);

	for(i=0;i<16;i++)
		printf("result[%d]=%d\n",i,result[i]);
	/*
	cycles  = stop-start    = 4326 - 4298 = 28
	result[0]=12
	result[1]=24
	result[2]=333
	result[3]=48
	result[4]=555
	result[5]=666
	result[6]=777
	result[7]=888
	result[8]=999
	result[9]=1100
	result[10]=1110
	result[11]=1120
	result[12]=1130
	result[13]=1140
	result[14]=1150
	result[15]=1160
*/
}
#endif
