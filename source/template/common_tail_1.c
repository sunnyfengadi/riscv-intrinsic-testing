
    //compare result
    for(i=0;i<ELE_NUM;i++) {
        if(exp_result[i] != result[i]) {
            printf("fail at %d, result = %x, exp_result = %x\n", i, result[i], exp_result[i]); 
            abort(); 
        }
    }

    return 0;
}