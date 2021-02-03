############################################################
# This script is to save the functions used by SourceFile.py
############################################################
import os,sys
import re,subprocess
import shutil

##############################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join( ROOT_DIR, 'template' )
GOLDEN_PATH = os.path.join( ROOT_DIR, 'golden' )

OPERATOR_1= {# for arithmetic
             '-' : 'vs?neg_v_[iu][13][62]_?m?$',
             # for logic
             '~' : 'vnot_v[vx]?_[iu][13][62]_?m?$',
}

OPERATOR_2= {# for arithmetic
             '+': 'vw?s?add_[vw][vxw]_[iu][136][624]_?m?$',
             '-': 'vw?s?sub_[vw][vxw]_[iu][136][624]_?m?$',
             '*': 'vw?s?mulh?q?_v[vx]_[iu][13][62]_?m?$',
             'min,<': 'vmin_v[vx]_[iu][13][62]_?m?$',
             'max,>': 'vmax_v[vx]_[iu][13][62]_?m?$',
             # for logic
             '&': 'vand_v[vx]_[iu][13][62]_?m?$',
             '|': 'vor_v[vx]_[iu][13][62]_?m?$',
             '^': 'vxor_v[vx]_[iu][13][62]_?m?$',
             # for shfit
             '<<': 'vc?w?s?sll?_a?[vwi][vxisw]?_[iu][136][624]_?m?$',
             '>>': 'vc?w?srl?a?_a?[vwi][vxisw]?_[iu][136][624]_?m?$',
             # for compare
             '==': 'vcmpeq_v[vx]_[iu][13][62]_?m?$',
             '!=': 'vcmpne_v[vx]_[iu][13][62]_?m?$',
             '<' : 'vcmplt_v[vx]_[iu][13][62]_?m?$',
             '<=': 'vcmple_v[vx]_[iu][13][62]_?m?$',
             '>' : 'vcmpgt_v[vx]_[iu][13][62]_?m?$',
             '>=': 'vcmpge_v[vx]_[iu][13][62]_?m?$',
}
OPERATOR_3= {# for mac
             '*,+'  : 'vw?s?maccq?_vv_[iu][13][62]_?h?l?p?_?m?$',
             '*,-'  : 'vw?s?msubq?_vv_[iu][13][62]_?h?l?p?_?m?$',
             '-,*,+': 'vw?s?nmsacq?_vv_[iu][13][62]_?h?l?p?_?m?$',
             '-,*,-': 'vw?s?nmsubq?_vv_[iu][13][62]_?h?l?p?_?m?$',
             
}

def arithmetic(node, variable):
    lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
    oper = 'TODO'
    if len(variable)==1:
        for item in OPERATOR_1.items():
            ret = re.match(item[1],node['Intrinsic_Name'])
            if ret:
                operator = item[0]
                oper = operator + variable[0] + '[i]'
            
    if len(variable)==2:
        for item in OPERATOR_2.items():
            ret = re.match(item[1],node['Intrinsic_Name'])
            if ret:
                operator = item[0]
                if 'vx' in node['Intrinsic_Name'].split('_')[1]:
                    oper = variable[0] + '[i]' + operator + variable[1]
                else:
                    oper = variable[0] + '[i]' + operator + variable[1] + '[i]'
                if 'max' in node['Intrinsic_Name'] or 'min' in node['Intrinsic_Name']:
                    if 'vx' in node['Intrinsic_Name'].split('_')[1]:
                        oper = variable[0] + '[i]' + operator.split(',')[1] + variable[1] + ' ? a[i]:b'
                    else:
                        oper = variable[0] + '[i]' + operator.split(',')[1] + variable[1] + '[i]' + ' ? a[i]:b[i]'

    lines += '        exp_result[i] = ' + oper + ';\n'
    lines += '  }\n'
    return lines

def logic(node, variable):
    lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
    oper = 'TODO'
    if len(variable)==1:
        for item in OPERATOR_1.items():
            ret = re.match(item[1],node['Intrinsic_Name'])
            if ret:
                operator = item[0]
                oper = operator + variable[0] + '[i]'
            
    if len(variable)==2:
        for item in OPERATOR_2.items():
            ret = re.match(item[1],node['Intrinsic_Name'])
            if ret:
                operator = item[0]
                if 'vx' in node['Intrinsic_Name'].split('_')[1]:
                    oper = variable[0] + '[i]' + operator + variable[1]
                else:
                    oper = variable[0] + '[i]' + operator + variable[1] + '[i]'
            
    lines += '        exp_result[i] = ' + oper + ';\n'
    lines += '  }\n'
    return lines

def shift(node, variable):
    lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
    oper = 'TODO'
    for item in OPERATOR_2.items():
        ret = re.match(item[1],node['Intrinsic_Name'])
        if ret:
            operator = item[0]
            split_type = node['Intrinsic_Name'].split('_')[1]
            
            if 'x' in split_type:
                oper = variable[0] + '[i]' + operator + variable[1]
            elif 'vv' in split_type or 'ww' in split_type:
                oper = variable[0] + '[i]' + operator + variable[1] + '[i]'
            elif 'i' in split_type:   # i is imm in variable
                oper = variable[0] + '[i]' + operator + 'imm'   # fix imm as 3

    lines += '        exp_result[i] = ' + oper + ';\n'
    lines += '  }\n'
    return lines

def mac(node, variable): # a+b*c
    oper = 'TODO'
    for item in OPERATOR_3.items():
        ret = re.match(item[1],node['Intrinsic_Name'])
        if ret:
            operator = item[0].split(',')
            if 'vw' in node['Intrinsic_Name']:
                lines = '//widden to do '
                pass
                # print('vw2: match:',node['Intrinsic_Name'],item)
                # lines = '     for (int i = 0; i < COMBO_NUM; i++) {\n'
                # lines += '        for (int j = 0; j < ELE_NUM; j++) {\n'
                # oper = operator[0]+ '(' + variable[1] + '[i*ELE_NUM+j]' + operator[1] + variable[2]+'[i*ELE_NUM+j])'+ operator[2] + variable[0] + '[i][j]'
                # lines += '        exp_result[i] = ' + oper + ';\n'
                # lines += '      }\n'
                # lines += '  }\n'
            else:
                lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
                if re.match('vs?nm(sac)?(sub)?q?_vv_[iu][13][62]_?h?l?p?',node['Intrinsic_Name']): #Neg
                    oper = operator[0]+ '(' + variable[1] + '[i]' + operator[1] + variable[2]+'[i])'+ operator[2] + variable[0] + '[i]'
                else:
                    oper = variable[1]+'[i]'+ operator[0] + variable[2] + '[i]' + operator[1]  + variable[0] + '[i]'
            
                lines += '        exp_result[i] = ' + oper + ';\n'
                lines += '  }\n'
    return lines

def compare(node, variable):
    lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
    oper = 'TODO'
    if len(variable)==2:
        for item in OPERATOR_2.items():
            ret = re.match(item[1],node['Intrinsic_Name'])
            if ret:
                operator = item[0]
                if 'vx' in node['Intrinsic_Name'].split('_')[1]:
                    oper = '('+ variable[0] + '[i]' + operator + variable[1] + ')'
                else:
                    oper = '('+ variable[0] + '[i]' + operator + variable[1] + '[i]' + ')'
            
    lines += '        exp_result[i] = ' + oper + ';\n'
    lines += '  }\n'
    return lines

def move(node, variable):
    lines = '     for (int i = 0; i < ELE_NUM; i++) {\n'
    oper = 'TODO'
    split_type = node['Intrinsic_Name'].split('_')
    
    if '_m' not in node['Intrinsic_Name']:
        if split_type[1] == 'v' and split_type[2] == 'x':
            oper = variable[0]
        if split_type[1] == 'v' and split_type[2] == 'i':  # imm: fix it as 3
            oper = '3'
        if split_type[1] == 'x' and split_type[2] == 'v': 
            oper = variable[0] + '[' + variable[1] + ']'

    lines += '        exp_result[i] = ' + oper + ';\n'
    lines += '  }\n'
    return lines

def load(node, variable):
    oper = ' \
    for(int i=0; i<COMBO_NUM; i++){\n \
        for(int j=0; j<GROUP_NUM; j++){\n \
            for(int k=0; k<GROUP_DEPTH/ELE_WIDTH; k++){\n \
                exp_result[i][j*GROUP_DEPTH/ELE_WIDTH+k] = base[i*COMBO_STRIDE/ELE_WIDTH+ j*GROUP_STRIDE/ELE_WIDTH + k*ELE_STRIDE/ELE_WIDTH];\n \
            }\n \
        }\n \
    }'
    return oper

def SetGoldenFunction(node, elenum, typebit, apitype):
    variableList = []
    expInput = ''
    
    operator = 'Operator Line --- TODO'
    line1 = ['#pragma GCC push_options', 
             '#pragma GCC optimize("O0")',
             '__attribute__((noinline, noclone))']
    line3 = ['#pragma GCC pop_options', '', 
             'int main(void) {' ]

    for i in range(1,8):
        if node['Input_'+str(i)+'_Type'] and 'accum' not in node['Input_'+str(i)+'_Variable']:
            split_input = node['Input_'+str(i)+'_Type'].split('x')
            if 'bool' in node['Input_'+str(i)+'_Type']: #bool8_t bool8x2_t
                variableList.append(node['Input_'+str(i)+'_Variable'])
                if (len(split_input) == 1): #bool8_t
                    expInput += 'uint64_t *' + node['Input_'+str(i)+'_Variable'] +','
                else: #bool8x2_t
                    comboNum = re.sub("\D", "", split_input[1])
                    eleNum = re.sub("\D", "", split_input[0])
                    expInput += 'uint64_t *' + node['Input_'+str(i)+'_Variable'] + \
                            '[' + str(comboNum)+']['+str(eleNum)+'],'
            else:
                if (len(split_input) == 1): ## int16_t void
                    inputType = node['Input_'+str(i)+'_Type']
                    if 'base' in node['Input_'+str(i)+'_Variable']:
                        variableList.append('base')
                        expInput += inputType + ' *base,'
                    else:
                        variableList.append(node['Input_'+str(i)+'_Variable'])
                        expInput += inputType + ' ' + node['Input_'+str(i)+'_Variable'] + ','
                else:
                    inputType = split_input[0]+'_t'
                    variableList.append(node['Input_'+str(i)+'_Variable'])

                    if (len(split_input) == 2): ## int16x32_t bool8x2_t
                        expInput+= inputType + ' *' + node['Input_'+str(i)+'_Variable'] + ','
                    elif (len(split_input) == 3): ## int16x32x2_t
                        comboNum = re.sub("\D", "", split_input[2])
                        eleNum = re.sub("\D", "", split_input[1])
                        expInput += inputType + ' ' + node['Input_'+str(i)+'_Variable'] + \
                                    '[' + str(comboNum) + '][' + str(eleNum) + '],'

    split_output = node['Output_Type'].split('x')
    if 'void' in node['Output_Type']: pass #void
    else:
        if 'bool' in node['Output_Type']:
            if (len(split_output) == 1): # bool8_t bool8x2_t
                expInput = 'uint64_t *exp_result'
            else:  # bool8x2_t
                expInput += 'uint64_t exp_result[][ELE_NUM]'
        else:
            if (len(split_output) == 1): #int16_t int32_t void
                expInput += node['Output_Type'] + ' exp_result;'
            else:
                if (len(split_output) == 2): #int16x32_t
                    expInput += split_output[0] + '_t' + ' *exp_result'
                elif (len(split_output) == 3): #int16x32x3_t
                    expInput += split_output[0] + '_t' + ' exp_result[][ELE_NUM]'

    # get exp operator 
    if apitype == 'load':
        operator = load(node, variableList)
    if apitype == 'arithmetic':
        operator = arithmetic(node, variableList)
    if apitype == 'logic':
        operator = logic(node, variableList)
    if apitype == 'shift':
        operator = shift(node, variableList)
    if apitype == 'mac':
        operator = mac(node, variableList)
    if apitype == 'compare':
        operator = compare(node, variableList)
    if apitype == 'move':
        operator = move(node, variableList)
    else:
        pass

    line2 = ['void '+ node['Intrinsic_Name'].rstrip() + '_golden(' + expInput + ') {',
            operator,
            '}']
            
    return line1+line2+line3
    
    