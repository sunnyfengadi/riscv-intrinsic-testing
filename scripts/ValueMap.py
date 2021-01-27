# The map of all api type for templates
import random

def gen_num(bitnum,totalnum):
    output = '{'
    for i in range(0,totalnum-1):
        output = output + str(random.randint(0,pow(2,bitnum))) + ','
    output += str(random.randint(0,pow(2,bitnum))) + '}'
    return output

def gen_mask(totalnum):
    output = '{'
    for i in range(0,totalnum-1):
        output = output + str(random.randint(0,1)) + ','
    output += str(random.randint(0,1)) + '}'
    return output


# base[] is set in python script
VALUE_MAP={
    'int':                    {'value':gen_num(16,16)},
    'int8_t':                 {'base[]':'','a':gen_num(8,1),'b':gen_num(8,1),'imm':'0'},
    'int16_t':                {'base[]':'','a':gen_num(16,1),'b':gen_num(16,1),'imm':'0'},
    'int32_t':                {'base[]':'','a':gen_num(32,1),'b':gen_num(32,1),'imm':'0'},
    'int64_t':                {'base[]':'','a':gen_num(64,1),'b':gen_num(64,1),'imm':'0'},
    'uint8_t':                {'base[]':'','a':gen_num(8,1),'b':gen_num(8,1),'imm':'0'},
    'uint16_t':               {'base[]':'','a':gen_num(16,1),'b':gen_num(16,1),'imm':'0'},
    'uint32_t':               {'base[]':'','a':gen_num(32,1),'b':gen_num(32,1),'imm':'0'},
    'uint64_t':               {'base[]':'','a':gen_num(64,1),'b':gen_num(64,1),'imm':'0'},
    'bool8_t':                {'mask':gen_mask(8),'src_mask':gen_mask(8),'dst_mask':gen_mask(8),'a':gen_mask(8),'b':gen_mask(8),'maskoff':gen_mask(8)},
    'bool8x2_t':              {'mask':gen_mask(16),'src_mask':gen_mask(16),'dst_mask':gen_mask(16),'a':gen_mask(8*2),'b':gen_mask(8*2),'maskoff':gen_mask(8*2)},
    'bool16_t':               {'mask':gen_mask(16),'src_mask':gen_mask(16),'dst_mask':gen_mask(16),'a':gen_mask(16),'b':gen_mask(16),'maskoff':gen_mask(16)},
    'bool16x2_t':             {'mask':gen_mask(32),'src_mask':gen_mask(32),'dst_mask':gen_mask(32),'a':gen_mask(16*2),'b':gen_mask(16*2),'maskoff':gen_mask(16*2)},
    'bool32_t':               {'mask':gen_mask(32),'src_mask':gen_mask(32),'dst_mask':gen_mask(32),'a':gen_mask(32),'b':gen_mask(32),'maskoff':gen_mask(32)},
    'bool32x2_t':             {'mask':gen_mask(64),'src_mask':gen_mask(64),'dst_mask':gen_mask(64),'a':gen_mask(32*2),'b':gen_mask(32*2),'maskoff':gen_mask(32*2)},
    'int16x32_t':             {'a':gen_num(16,32),'b':gen_num(16,32),'c':gen_num(16,32),'value':gen_num(16,32),'maskoff':gen_num(16,32),'index':gen_num(16,32)},
    'int16x32x2_t':           {'a':gen_num(16,32*2),'b':gen_num(16,32*2),'c':gen_num(16,32*2),'value':gen_num(16,32*2),'maskoff':gen_num(16,32*2),'index':gen_num(16,32*2)},
    'int16x32x3_t':           {'a':gen_num(16,32*3),'b':gen_num(16,32*3),'c':gen_num(16,32*3),'value':gen_num(16,32*3),'maskoff':gen_num(16,32*3),'index':gen_num(16,32*3)},
    'int16x32x4_t':           {'a':gen_num(16,32*4),'b':gen_num(16,32*4),'c':gen_num(16,32*4),'value':gen_num(16,32*4),'maskoff':gen_num(16,32*4),'index':gen_num(16,32*4)},
    'int16x32x5_t':           {'a':gen_num(16,32*5),'b':gen_num(16,32*5),'c':gen_num(16,32*5),'value':gen_num(16,32*5),'maskoff':gen_num(16,32*5),'index':gen_num(16,32*5)},
    'int16x32x6_t':           {'a':gen_num(16,32*6),'b':gen_num(16,32*6),'c':gen_num(16,32*6),'value':gen_num(16,32*6),'maskoff':gen_num(16,32*6),'index':gen_num(16,32*6)},
    'int16x32x7_t':           {'a':gen_num(16,32*7),'b':gen_num(16,32*7),'c':gen_num(16,32*7),'value':gen_num(16,32*7),'maskoff':gen_num(16,32*7),'index':gen_num(16,32*7)},
    'int16x32x8_t':           {'a':gen_num(16,32*8),'b':gen_num(16,32*8),'c':gen_num(16,32*8),'value':gen_num(16,32*8),'maskoff':gen_num(16,32*8),'index':gen_num(16,32*8)},
    'int32x16_t':             {'a':gen_num(32,16*1),'b':gen_num(32,16*1),'c':gen_num(32,16),'value':gen_num(32,16),'maskoff':gen_num(32,16*1),'index':gen_num(32,16*1)},
    'int32x16x2_t':           {'a':gen_num(32,16*2),'b':gen_num(32,16*2),'c':gen_num(32,16*2),'value':gen_num(32,16*2),'maskoff':gen_num(32,16*2),'index':gen_num(32,16*2)},
    'int32x16x3_t':           {'a':gen_num(32,16*3),'b':gen_num(32,16*3),'c':gen_num(32,16*3),'value':gen_num(32,16*3),'maskoff':gen_num(32,16*3),'index':gen_num(32,16*3)},
    'int32x16x4_t':           {'a':gen_num(32,16*4),'b':gen_num(32,16*4),'c':gen_num(32,16*4),'value':gen_num(32,16*4),'maskoff':gen_num(32,16*4),'index':gen_num(32,16*4)},
    'int32x16x5_t':           {'a':gen_num(32,16*5),'b':gen_num(32,16*5),'c':gen_num(32,16*5),'value':gen_num(32,16*5),'maskoff':gen_num(32,16*5),'index':gen_num(32,16*5)},
    'int32x16x6_t':           {'a':gen_num(32,16*6),'b':gen_num(32,16*6),'c':gen_num(32,16*6),'value':gen_num(32,16*6),'maskoff':gen_num(32,16*6),'index':gen_num(32,16*6)},
    'int32x16x7_t':           {'a':gen_num(32,16*7),'b':gen_num(32,16*7),'c':gen_num(32,16*7),'value':gen_num(32,16*7),'maskoff':gen_num(32,16*7),'index':gen_num(32,16*7)},
    'int32x16x8_t':           {'a':gen_num(32,16*8),'b':gen_num(32,16*8),'c':gen_num(32,16*8),'value':gen_num(32,16*8),'maskoff':gen_num(32,16*8),'index':gen_num(32,16*8)},
    'int64x8_t':              {'a':gen_num(64,8*1),'b':gen_num(64,8*1),'c':gen_num(64,8),'value':gen_num(64,8),'maskoff':gen_num(64,8*1),'index':gen_num(64,8*1)},
    'int64x8x2_t':            {'a':gen_num(64,8*2),'b':gen_num(64,8*2),'c':gen_num(64,8*2),'value':gen_num(64,8*2),'maskoff':gen_num(64,8*2),'index':gen_num(64,8*2)},
    'int64x8x3_t':            {'a':gen_num(64,8*3),'b':gen_num(64,8*3),'c':gen_num(64,8*3),'value':gen_num(64,8*3),'maskoff':gen_num(64,8*3),'index':gen_num(64,8*3)},
    'int64x8x4_t':            {'a':gen_num(64,8*4),'b':gen_num(64,8*4),'c':gen_num(64,8*4),'value':gen_num(64,8*4),'maskoff':gen_num(64,8*4),'index':gen_num(64,8*4)},
    'int64x8x5_t':            {'a':gen_num(64,8*5),'b':gen_num(64,8*5),'c':gen_num(64,8*5),'value':gen_num(64,8*5),'maskoff':gen_num(64,8*5),'index':gen_num(64,8*5)},
    'int64x8x6_t':            {'a':gen_num(64,8*6),'b':gen_num(64,8*6),'c':gen_num(64,8*6),'value':gen_num(64,8*6),'maskoff':gen_num(64,8*6),'index':gen_num(64,8*6)},
    'int64x8x7_t':            {'a':gen_num(64,8*7),'b':gen_num(64,8*7),'c':gen_num(64,8*7),'value':gen_num(64,8*7),'maskoff':gen_num(64,8*7),'index':gen_num(64,8*7)},
    'int64x8x8_t':            {'a':gen_num(16,8*8),'b':gen_num(16,8*8),'c':gen_num(16,8*8),'value':gen_num(16,8*8),'maskoff':gen_num(64,8*8),'index':gen_num(16,8*8)},
    'uint16x32_t':             {'a':gen_num(16,32),'b':gen_num(16,32),'c':gen_num(16,32),'value':gen_num(16,32),'maskoff':gen_num(16,32),'index':gen_num(16,32)},
    'uint16x32x2_t':           {'a':gen_num(16,32*2),'b':gen_num(16,32*2),'c':gen_num(16,32*2),'value':gen_num(16,32*2),'maskoff':gen_num(16,32*2)},'index':gen_num(16,32*2),
    'uint16x32x3_t':           {'a':gen_num(16,32*3),'b':gen_num(16,32*3),'c':gen_num(16,32*3),'value':gen_num(16,32*3),'maskoff':gen_num(16,32*3),'index':gen_num(16,32*3)},
    'uint16x32x4_t':           {'a':gen_num(16,32*4),'b':gen_num(16,32*4),'c':gen_num(16,32*4),'value':gen_num(16,32*4),'maskoff':gen_num(16,32*4),'index':gen_num(16,32*4)},
    'uint16x32x5_t':           {'a':gen_num(16,32*5),'b':gen_num(16,32*5),'c':gen_num(16,32*5),'value':gen_num(16,32*5),'maskoff':gen_num(16,32*5),'index':gen_num(16,32*5)},
    'uint16x32x6_t':           {'a':gen_num(16,32*6),'b':gen_num(16,32*6),'c':gen_num(16,32*6),'value':gen_num(16,32*6),'maskoff':gen_num(16,32*6),'index':gen_num(16,32*6)},
    'uint16x32x7_t':           {'a':gen_num(16,32*7),'b':gen_num(16,32*7),'c':gen_num(16,32*7),'value':gen_num(16,32*7),'maskoff':gen_num(16,32*7),'index':gen_num(16,32*7)},
    'uint16x32x8_t':           {'a':gen_num(16,32*8),'b':gen_num(16,32*8),'c':gen_num(16,32*8),'value':gen_num(16,32*8),'maskoff':gen_num(16,32*8),'index':gen_num(16,32*8)},
    'uint32x16_t':             {'a':gen_num(32,16*1),'b':gen_num(32,16*1),'c':gen_num(32,16),'value':gen_num(32,16),'maskoff':gen_num(32,16*1),'index':gen_num(32,16)},
    'uint32x16x2_t':           {'a':gen_num(32,16*2),'b':gen_num(32,16*2),'c':gen_num(32,16*2),'value':gen_num(32,16*2),'maskoff':gen_num(32,16*2),'index':gen_num(32,16*2)},
    'uint32x16x3_t':           {'a':gen_num(32,16*3),'b':gen_num(32,16*3),'c':gen_num(32,16*3),'value':gen_num(32,16*3),'maskoff':gen_num(32,16*3),'index':gen_num(32,16*3)},
    'uint32x16x4_t':           {'a':gen_num(32,16*4),'b':gen_num(32,16*4),'c':gen_num(32,16*4),'value':gen_num(32,16*4),'maskoff':gen_num(32,16*4),'index':gen_num(32,16*4)},
    'uint32x16x5_t':           {'a':gen_num(32,16*5),'b':gen_num(32,16*5),'c':gen_num(32,16*5),'value':gen_num(32,16*5),'maskoff':gen_num(32,16*5),'index':gen_num(32,16*5)},
    'uint32x16x6_t':           {'a':gen_num(32,16*6),'b':gen_num(32,16*6),'c':gen_num(32,16*6),'value':gen_num(32,16*6),'maskoff':gen_num(32,16*6),'index':gen_num(32,16*6)},
    'uint32x16x7_t':           {'a':gen_num(32,16*7),'b':gen_num(32,16*7),'c':gen_num(32,16*7),'value':gen_num(32,16*7),'maskoff':gen_num(32,16*7),'index':gen_num(32,16*7)},
    'uint32x16x8_t':           {'a':gen_num(32,16*8),'b':gen_num(32,16*8),'c':gen_num(32,16*8),'value':gen_num(32,16*8),'maskoff':gen_num(32,16*8),'index':gen_num(32,16*8)},
    'uint64x8_t':              {'a':gen_num(64,8*1),'b':gen_num(64,8*1),'c':gen_num(64,8),'value':gen_num(64,8),'maskoff':gen_num(64,8*1),'index':gen_num(64,8)},
    'uint64x8x2_t':            {'a':gen_num(64,8*2),'b':gen_num(64,8*2),'c':gen_num(64,8*2),'value':gen_num(64,8*2),'maskoff':gen_num(64,8*2),'index':gen_num(64,8*2)},
    'uint64x8x3_t':            {'a':gen_num(64,8*3),'b':gen_num(64,8*3),'c':gen_num(64,8*3),'value':gen_num(64,8*3),'maskoff':gen_num(64,8*3),'index':gen_num(64,8*3)},
    'uint64x8x4_t':            {'a':gen_num(64,8*4),'b':gen_num(64,8*4),'c':gen_num(64,8*4),'value':gen_num(64,8*4),'maskoff':gen_num(64,8*4),'index':gen_num(64,8*4)},
    'uint64x8x5_t':            {'a':gen_num(64,8*5),'b':gen_num(64,8*5),'c':gen_num(64,8*5),'value':gen_num(64,8*5),'maskoff':gen_num(64,8*5),'index':gen_num(64,8*5)},
    'uint64x8x6_t':            {'a':gen_num(64,8*6),'b':gen_num(64,8*6),'c':gen_num(64,8*6),'value':gen_num(64,8*6),'maskoff':gen_num(64,8*6),'index':gen_num(64,8*6)},
    'uint64x8x7_t':            {'a':gen_num(64,8*7),'b':gen_num(64,8*7),'c':gen_num(64,8*7),'value':gen_num(64,8*7),'maskoff':gen_num(64,8*7),'index':gen_num(64,8*7)},
    'uint64x8x8_t':            {'a':gen_num(64,8*8),'b':gen_num(64,8*8),'c':gen_num(64,8*8),'value':gen_num(64,8*8),'maskoff':gen_num(64,8*8),'index':gen_num(64,8*8)},
    'enum ACCUM':              {'accum':'','dst_accum':'','src1_accum':'','src2_accum':'',}
}