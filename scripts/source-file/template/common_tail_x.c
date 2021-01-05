    
    printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
    printf("result={");
    for(i=0;i<combo_num;i++) {
        for(j=0;j<element_num;j++) {
            if(j==element_num-1 && i==combo_num-1)
            printf("%d}\n",result.val[i][j]);
        else
            printf("%d,",result.val[i][j]);
            if(exp_result.val[i][j] != result.val[i][j]) error = 1;
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