
    printf("cycles \t= stop-start \t= %u - %u = %u\n",stop,start,stop-start);
    printf("result={");
    for(i=0;i<element_num;i++) {
        if(i==element_num-1)
            printf("%d}\n",result[i]);
        else
            printf("%d,",result[i]);

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