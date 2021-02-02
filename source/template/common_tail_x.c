
    //Compare Result
    for(int i = 0; i < COMBO_NUM; i++) {
        for(int j = 0; j < ELE_NUM; j++) {
            if(exp_result[i*ELE_NUM+j] != result.val[i][j]) {
                printf("Failed: result.val[%d][%d] = %x, exp_result[%d] = %x\n", i,j, result.val[i][j], i*ELE_NUM+j, exp_result[i*ELE_NUM+j]);
                //abort();
                error = 1;
            }
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