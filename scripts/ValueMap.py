# The map of all api type for templates
src_mask_8 ='{1,1,0,1,0,0,1,1}'
src_mask_16 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'
src_mask_32 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'
src_mask_64 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'

dst_mask_8 ='{1,0,0,0,0,1,1,0}'
dst_mask_16 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'
dst_mask_32 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'
dst_mask_64 = '{1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1,0,0,1,1}'

def generate_num(start_num,total_num):
    output = '{'
    for i in range(start_num,start_num + total_num):
        output = output + str(i) + ','
    output += str(start_num + total_num) + '}'
    return output

def generate_maskoff(num):
    output = '{'
    for i in range(1,num):
        output = output + str(10*i) + ','
    output += str(10*num) + '}'
    return output

VALUE_MAP={
    'int':                    {'value':generate_num(1,11)},
    'int8_t':                 {'base[]':'','a':'','b':'6','imm':'0'},
    'int16_t':                {'base[]':'','a':'','b':'6','imm':'0'},
    'int32_t':                {'base[]':'','a':'','b':'6','imm':'0'},
    'int64_t':                {'base[]':'','a':'','b':'6','imm':'0'},
    'uint8_t':                {'base[]':'','a':'','b':'6','imm':'0'},
    'uint16_t':               {'base[]':'','a':'','b':'6','imm':'0'},
    'uint32_t':               {'base[]':'','a':'','b':'6','imm':'0'},
    'uint64_t':               {'base[]':'','a':'','b':'6','imm':'0'},
    'bool8_t':                {'mask':src_mask_8,'src_mask':src_mask_8,'dst_mask':dst_mask_8,'a':generate_num(1,8),'b':generate_num(2,8),'maskoff':generate_maskoff(8)},
    'bool8x2_t':              {'mask':src_mask_16,'src_mask':src_mask_16,'dst_mask':dst_mask_16,'a':generate_num(1,8*2),'b':generate_num(2,8*2),'maskoff':generate_maskoff(8*2)},
    'bool16_t':               {'mask':src_mask_16,'src_mask':src_mask_16,'dst_mask':dst_mask_16,'a':generate_num(1,16),'b':generate_num(2,16),'maskoff':generate_maskoff(16)},
    'bool16x2_t':             {'mask':src_mask_32,'src_mask':src_mask_32,'dst_mask':dst_mask_32,'a':generate_num(1,16*2),'b':generate_num(2,16*2),'maskoff':generate_maskoff(16*2)},
    'bool32_t':               {'mask':src_mask_32,'src_mask':src_mask_32,'dst_mask':dst_mask_32,'a':generate_num(1,32),'b':generate_num(2,32),'maskoff':generate_maskoff(32)},
    'bool32x2_t':             {'mask':src_mask_64,'src_mask':src_mask_64,'dst_mask':dst_mask_64,'a':generate_num(1,32*2),'b':generate_num(2,32*2),'maskoff':generate_maskoff(32*2)},
    'int16x32_t':             {'a':generate_num(1,32),'b':generate_num(2,32),'c':generate_num(3,32),'value':generate_num(1,32),
                            'maskoff':generate_maskoff(32),'index':generate_num(4,32)},
    'int16x32x2_t':           {'a':generate_num(1,32*2),'b':generate_num(2,32*2),'c':generate_num(3,32*2),'value':generate_num(1,32*2),
                            'maskoff':generate_maskoff(32*2),'index':generate_num(4,32*2)},
    'int16x32x3_t':           {'a':generate_num(1,32*3),'b':generate_num(2,32*3),'c':generate_num(3,32*3),'value':generate_num(1,32*3),
                            'maskoff':generate_maskoff(32*3),'index':generate_num(4,32*3)},
    'int16x32x4_t':           {'a':generate_num(1,32*4),'b':generate_num(2,32*4),'c':generate_num(3,32*4),'value':generate_num(1,32*4),
                            'maskoff':generate_maskoff(32*4),'index':generate_num(4,32*4)},
    'int16x32x5_t':           {'a':generate_num(1,32*5),'b':generate_num(2,32*5),'c':generate_num(3,32*5),'value':generate_num(1,32*5),
                            'maskoff':generate_maskoff(32*5),'index':generate_num(4,32*5)},
    'int16x32x6_t':           {'a':generate_num(1,32*6),'b':generate_num(2,32*6),'c':generate_num(3,32*6),'value':generate_num(1,32*6),
                            'maskoff':generate_maskoff(32*6),'index':generate_num(4,32*6)},
    'int16x32x7_t':           {'a':generate_num(1,32*7),'b':generate_num(2,32*7),'c':generate_num(3,32*7),'value':generate_num(1,32*7),
                            'maskoff':generate_maskoff(32*7),'index':generate_num(4,32*7)},
    'int16x32x8_t':           {'a':generate_num(1,32*8),'b':generate_num(2,32*8),'c':generate_num(3,32*8),'value':generate_num(1,32*8),
                            'maskoff':generate_maskoff(32*8),'index':generate_num(4,32*8)},
    'int32x16_t':             {'a':generate_num(1,16*1),'b':generate_num(2,16*1),'c':generate_num(3,16),'value':generate_num(1,16),
                            'maskoff':generate_maskoff(16*1),'index':generate_num(4,16*1)},
    'int32x16x2_t':           {'a':generate_num(1,16*2),'b':generate_num(2,16*2),'c':generate_num(3,16*2),'value':generate_num(1,16*2),
                            'maskoff':generate_maskoff(16*2),'index':generate_num(4,16*2)},
    'int32x16x3_t':           {'a':generate_num(1,16*3),'b':generate_num(2,16*3),'c':generate_num(3,16*3),'value':generate_num(1,16*3),
                            'maskoff':generate_maskoff(16*3),'index':generate_num(4,16*3)},
    'int32x16x4_t':           {'a':generate_num(1,16*4),'b':generate_num(2,16*4),'c':generate_num(3,16*4),'value':generate_num(1,16*4),
                            'maskoff':generate_maskoff(16*4),'index':generate_num(4,16*4)},
    'int32x16x5_t':           {'a':generate_num(1,16*5),'b':generate_num(2,16*5),'c':generate_num(3,16*5),'value':generate_num(1,16*5),
                            'maskoff':generate_maskoff(16*5),'index':generate_num(4,16*5)},
    'int32x16x6_t':           {'a':generate_num(1,16*6),'b':generate_num(2,16*6),'c':generate_num(3,16*6),'value':generate_num(1,16*6),
                            'maskoff':generate_maskoff(16*6),'index':generate_num(4,16*6)},
    'int32x16x7_t':           {'a':generate_num(1,16*7),'b':generate_num(2,16*7),'c':generate_num(3,16*7),'value':generate_num(1,16*7),
                            'maskoff':generate_maskoff(16*7),'index':generate_num(4,16*7)},
    'int32x16x8_t':           {'a':generate_num(1,16*8),'b':generate_num(2,16*8),'c':generate_num(3,16*8),'value':generate_num(1,16*8),
                            'maskoff':generate_maskoff(16*8),'index':generate_num(4,16*8)},
    'int64x8_t':              {'a':generate_num(1,8*1),'b':generate_num(2,8*1),'c':generate_num(3,8),'value':generate_num(1,8),
                            'maskoff':generate_maskoff(8*1),'index':generate_num(4,8*1)},
    'int64x8x2_t':            {'a':generate_num(1,8*2),'b':generate_num(2,8*2),'c':generate_num(3,8*2),'value':generate_num(1,8*2),
                            'maskoff':generate_maskoff(8*2),'index':generate_num(4,8*2)},
    'int64x8x3_t':            {'a':generate_num(1,8*3),'b':generate_num(2,8*3),'c':generate_num(3,8*3),'value':generate_num(1,8*3),
                            'maskoff':generate_maskoff(8*3),'index':generate_num(4,8*3)},
    'int64x8x4_t':            {'a':generate_num(1,8*4),'b':generate_num(2,8*4),'c':generate_num(3,8*4),'value':generate_num(1,8*4),
                            'maskoff':generate_maskoff(8*4),'index':generate_num(4,8*4)},
    'int64x8x5_t':            {'a':generate_num(1,8*5),'b':generate_num(2,8*5),'c':generate_num(3,8*5),'value':generate_num(1,8*5),
                            'maskoff':generate_maskoff(8*5),'index':generate_num(4,8*5)},
    'int64x8x6_t':            {'a':generate_num(1,8*6),'b':generate_num(2,8*6),'c':generate_num(3,8*6),'value':generate_num(1,8*6),
                            'maskoff':generate_maskoff(8*6),'index':generate_num(4,8*6)},
    'int64x8x7_t':            {'a':generate_num(1,8*7),'b':generate_num(2,8*7),'c':generate_num(3,8*7),'value':generate_num(1,8*7),
                            'maskoff':generate_maskoff(8*7),'index':generate_num(4,8*7)},
    'int64x8x8_t':            {'a':generate_num(1,8*8),'b':generate_num(2,8*8),'c':generate_num(3,8*8),'value':generate_num(1,8*8),
                            'maskoff':generate_maskoff(8*8),'index':generate_num(4,8*8)},
    'uint16x32_t':             {'a':generate_num(1,32),'b':generate_num(2,32),'c':generate_num(3,32),'value':generate_num(1,32),
                            'maskoff':generate_maskoff(32),'index':generate_num(4,32)},
    'uint16x32x2_t':           {'a':generate_num(1,32*2),'b':generate_num(2,32*2),'c':generate_num(3,32*2),'value':generate_num(1,32*2),
                            'maskoff':generate_maskoff(32*2)},'index':generate_num(4,32*2),
    'uint16x32x3_t':           {'a':generate_num(1,32*3),'b':generate_num(2,32*3),'c':generate_num(3,32*3),'value':generate_num(1,32*3),
                            'maskoff':generate_maskoff(32*3),'index':generate_num(4,32*3)},
    'uint16x32x4_t':           {'a':generate_num(1,32*4),'b':generate_num(2,32*4),'c':generate_num(3,32*4),'value':generate_num(1,32*4),
                            'maskoff':generate_maskoff(32*4),'index':generate_num(4,32*4)},
    'uint16x32x5_t':           {'a':generate_num(1,32*5),'b':generate_num(2,32*5),'c':generate_num(3,32*5),'value':generate_num(1,32*5),
                            'maskoff':generate_maskoff(32*5),'index':generate_num(4,32*5)},
    'uint16x32x6_t':           {'a':generate_num(1,32*6),'b':generate_num(2,32*6),'c':generate_num(3,32*6),'value':generate_num(1,32*6),
                            'maskoff':generate_maskoff(32*6),'index':generate_num(4,32*6)},
    'uint16x32x7_t':           {'a':generate_num(1,32*7),'b':generate_num(2,32*7),'c':generate_num(3,32*7),'value':generate_num(1,32*7),
                            'maskoff':generate_maskoff(32*7),'index':generate_num(4,32*7)},
    'uint16x32x8_t':           {'a':generate_num(1,32*8),'b':generate_num(2,32*8),'c':generate_num(3,32*8),'value':generate_num(1,32*8),
                            'maskoff':generate_maskoff(32*8),'index':generate_num(4,32*8)},
    'uint32x16_t':             {'a':generate_num(1,16*1),'b':generate_num(2,16*1),'c':generate_num(3,16),'value':generate_num(1,16),
                            'maskoff':generate_maskoff(16*1),'index':generate_num(4,16)},
    'uint32x16x2_t':           {'a':generate_num(1,16*2),'b':generate_num(2,16*2),'c':generate_num(3,16*2),'value':generate_num(1,16*2),
                            'maskoff':generate_maskoff(16*2),'index':generate_num(4,16*2)},
    'uint32x16x3_t':           {'a':generate_num(1,16*3),'b':generate_num(2,16*3),'c':generate_num(3,16*3),'value':generate_num(1,16*3),
                            'maskoff':generate_maskoff(16*3),'index':generate_num(4,16*3)},
    'uint32x16x4_t':           {'a':generate_num(1,16*4),'b':generate_num(2,16*4),'c':generate_num(3,16*4),'value':generate_num(1,16*4),
                            'maskoff':generate_maskoff(16*4),'index':generate_num(4,16*4)},
    'uint32x16x5_t':           {'a':generate_num(1,16*5),'b':generate_num(2,16*5),'c':generate_num(3,16*5),'value':generate_num(1,16*5),
                            'maskoff':generate_maskoff(16*5),'index':generate_num(4,16*5)},
    'uint32x16x6_t':           {'a':generate_num(1,16*6),'b':generate_num(2,16*6),'c':generate_num(3,16*6),'value':generate_num(1,16*6),
                            'maskoff':generate_maskoff(16*6),'index':generate_num(4,16*6)},
    'uint32x16x7_t':           {'a':generate_num(1,16*7),'b':generate_num(2,16*7),'c':generate_num(3,16*7),'value':generate_num(1,16*7),
                            'maskoff':generate_maskoff(16*7),'index':generate_num(4,16*7)},
    'uint32x16x8_t':           {'a':generate_num(1,16*8),'b':generate_num(2,16*8),'c':generate_num(3,16*8),'value':generate_num(1,16*8),
                            'maskoff':generate_maskoff(16*8),'index':generate_num(4,16*8)},
    'uint64x8_t':              {'a':generate_num(1,8*1),'b':generate_num(2,8*1),'c':generate_num(3,8),'value':generate_num(1,8),
                            'maskoff':generate_maskoff(8*1),'index':generate_num(4,8)},
    'uint64x8x2_t':            {'a':generate_num(1,8*2),'b':generate_num(2,8*2),'c':generate_num(3,8*2),'value':generate_num(1,8*2),
                            'maskoff':generate_maskoff(8*2),'index':generate_num(4,8*2)},
    'uint64x8x3_t':            {'a':generate_num(1,8*3),'b':generate_num(2,8*3),'c':generate_num(3,8*3),'value':generate_num(1,8*3),
                            'maskoff':generate_maskoff(8*3),'index':generate_num(4,8*3)},
    'uint64x8x4_t':            {'a':generate_num(1,8*4),'b':generate_num(2,8*4),'c':generate_num(3,8*4),'value':generate_num(1,8*4),
                            'maskoff':generate_maskoff(8*4),'index':generate_num(4,8*4)},
    'uint64x8x5_t':            {'a':generate_num(1,8*5),'b':generate_num(2,8*5),'c':generate_num(3,8*5),'value':generate_num(1,8*5),
                            'maskoff':generate_maskoff(8*5),'index':generate_num(4,8*5)},
    'uint64x8x6_t':            {'a':generate_num(1,8*6),'b':generate_num(2,8*6),'c':generate_num(3,8*6),'value':generate_num(1,8*6),
                            'maskoff':generate_maskoff(8*6),'index':generate_num(4,8*6)},
    'uint64x8x7_t':            {'a':generate_num(1,8*7),'b':generate_num(2,8*7),'c':generate_num(3,8*7),'value':generate_num(1,8*7),
                            'maskoff':generate_maskoff(8*7),'index':generate_num(4,8*7)},
    'uint64x8x8_t':            {'a':generate_num(1,8*8),'b':generate_num(2,8*8),'c':generate_num(3,8*8),'value':generate_num(1,8*8),
                            'maskoff':generate_maskoff(8*8),'index':generate_num(4,8*8)},
}