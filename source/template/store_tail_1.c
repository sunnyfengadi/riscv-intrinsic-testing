
    //compare result
    for(i=0;i<ELE_NUM;i++) {
        if(exp_base[i] != base[i]) {
            printf("Failed: result[%d] = %x, exp_result[%d] = %x\n", i, base[i], i, exp_base[i]);
            error = 1;
        }
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
