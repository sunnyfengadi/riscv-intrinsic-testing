#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "rivai_rugrats.h"
extern void abort(void);
#define ELE_NUM 16
#define COMBO_NUM 1
#define VLEN 64
#define BYTE_NUM 2
#define PAGE_NUM 4096
#define ELE_WIDTH 4
#define GROUP_NUM 4
#define GROUP_DEPTH 16
#define ELE_STRIDE 4
#define COMBO_STRIDE 4
#define GROUP_STRIDE 8

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
void vldstcb1_v_i32_m_golden(uint64_t *mask, int32_t *base,int32_t*index,int32_t *exp_result) {
    for (int i = 0; i < ELE_NUM; i++) {
        if (mask[i])
            exp_result[i] = base[index[i]];
        else
            exp_result[i] = 0;
    }

}
#pragma GCC pop_options

int main(void) {
    int error = 0;
    int32_t base[PAGE_NUM];
    int32_t base2[PAGE_NUM];
    int32x16_t index;
    bool16_t mask = m16(0x1101100000011011);

    uint64_t exp_mask[ELE_NUM]={1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};
    int32_t exp_base[PAGE_NUM];
    int32_t exp_index[ELE_NUM];
    
    unsigned int element_stride;
    unsigned int group_stride;
    

    int32x16_t result = {0};
    int32x16_t tmp_result = {0};
    int32x16_t tmp2_result = {0};
    int32_t exp_result[ELE_NUM] = {0};

    data_init(exp_base, exp_base, PAGE_NUM, 0xffffffff);
    data_init(index, exp_index, ELE_NUM, PAGE_NUM / 2);
    for (int i = 0; i < ELE_NUM; i++)
        index[i] = index[i] * BYTE_NUM;

    //Get golden result
    vldstcb1_v_i32_m_golden(exp_mask,exp_base, exp_index, exp_result);

    //Get Intrinsic result
    tmp_result = vgldcb1_v_i32_m(mask,exp_base,index);
    
    data_init_scalar(element_stride, element_stride, PAGE_NUM / BYTE_NUM / 2);
    data_init_scalar(group_stride, group_stride, PAGE_NUM / BYTE_NUM / 2);
    vwr_csr(RUGRATS_VMELEMENTSTRIDE, BYTE_NUM*element_stride);
    vwr_csr(RUGRATS_VMGROUPSTRIDE, BYTE_NUM*group_stride);
    vwr_csr(RUGRATS_VMGROUPNUMBER, VLEN / GROUP_DEPTH);
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);

    vstcb1in0_v_i32_m(mask, base, tmp_result, NORMAL);
    tmp2_result = vldcb1in0_v_i32_m(mask, base, NORMAL);
    vsstcb1_v_i32_m(mask, base2, index, tmp2_result);
    result = vgldcb1_v_i32_m(mask, base2,index);

    //compare result
    for(int i = 0; i < ELE_NUM; i++) {
        if(exp_result[i] != result[i]) {
            printf("Failed: result[%d] = %x, exp_result[%d] = %x\n", i, result[i], i, exp_result[i]);
            abort();
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