#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 32
#define COMBO_NUM 7
#define VLEN 64
#define BYTE_NUM 2
#define PAGE_NUM 4096
#define ELE_WIDTH 2
#define GROUP_NUM 4
#define GROUP_DEPTH 8
#define ELE_STRIDE 14
#define COMBO_STRIDE 2
#define GROUP_STRIDE 28

#define random(threshold) rand()%threshold
//#define data_init_bool(a, b, n, threshold) \
//	a = b = 1;
#define data_init_scalar(a, b, threshold) \
  a = b = random(threshold);
#define data_init(a, b, n, threshold) \
  for(int i = 0; i < n; i++) { \
    a[i] = random(threshold); \
    b[i] = a[i]; \
  }

#pragma GCC push_options
#pragma GCC optimize("O0")
__attribute__((noinline, noclone))
void vldstcb7_v_i16_golden(unsigned int combo_stride,int16_t *base, int16_t *index, int16_t exp_result[COMBO_NUM][ELE_NUM]) {
    for (int j = 0; j < COMBO_NUM; j++)
        for (int i = 0; i < ELE_NUM; i++)
            exp_result[j][i] = base[index[i] + combo_stride*j];
}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int16_t base[PAGE_NUM];
    int16_t base2[PAGE_NUM];
    int16x32_t index;
    int16_t exp_base[PAGE_NUM];
    int16_t exp_index[ELE_NUM];
    
    unsigned int element_stride;
    unsigned int group_stride;
    unsigned int combo_stride;

    int16x32x7_t result = {0};
    int16x32x7_t tmp_result = {0};
    int16x32x7_t tmp2_result = {0};
    int16_t exp_result[COMBO_NUM][ELE_NUM] = {0};

    data_init(exp_base, exp_base, PAGE_NUM, 0xffff);
    data_init(index, exp_index, ELE_NUM, PAGE_NUM / BYTE_NUM / 2);
	data_init_scalar(combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);
    for (int i = 0; i < ELE_NUM; i++)
        index[i] = index[i] * BYTE_NUM;
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);

    //Get golden result
    vldstcb7_v_i16_golden((combo_stride * BYTE_NUM + VLEN) / BYTE_NUM,exp_base, exp_index, exp_result);

    //Get Intrinsic result
    tmp_result = vgldcb7_v_i16(exp_base,index);
    
    data_init_scalar(element_stride, element_stride, PAGE_NUM / BYTE_NUM / 2);
    data_init_scalar(group_stride, group_stride, PAGE_NUM / BYTE_NUM / 2);
    data_init_scalar (combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);
    vwr_csr(RUGRATS_VMELEMENTSTRIDE, BYTE_NUM*element_stride);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, BYTE_NUM*group_stride);
    vwr_csr(RUGRATS_VMGROUPNUMBER, VLEN / GROUP_DEPTH);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);
    vstcb7in0_v_i16(base, tmp_result, NORMAL);
    tmp2_result = vldcb7in0_v_i16(base, NORMAL);
    data_init_scalar (combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);
    vsstcb7_v_i16(base2, index, tmp2_result);
    result = vgldcb7_v_i16(base2,index);

    // Compare Result
    for(int i = 0; i < COMBO_NUM; i++) {
        for(int j = 0; j < ELE_NUM; j++) {
            if(exp_result[i][j] != result.val[i][j]) {
                printf("Failed: result.val[%d][%d] = %llx, exp_result[%d][%d] = %llx\n", i,j, result.val[i][j], i,j, exp_result[i][j]);
                abort();
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