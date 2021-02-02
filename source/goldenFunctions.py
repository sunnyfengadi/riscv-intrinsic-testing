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
             '!' : 'vnot_v[vx]?_[iu][13][62]_?m?$',
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

    return '        exp_result[i] = ' + oper + ';'

def logic(node, variable):
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
            
    return '        exp_result[i] = ' + oper + ';'

def shift(node, variable):
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
                oper = variable[0] + '[i]' + operator + '3'   # fix imm as 3
            
    return '        exp_result[i] = ' + oper + ';'

def mac(node, variable):
    oper = 'TODO'
    for item in OPERATOR_3.items():
        ret = re.match(item[1],node['Intrinsic_Name'])
        if ret:
            operator = item[0].split(',')
            if 'Neg' in node['Intrinsic_Type']:
                oper = operator[0]+ '(' + variable[0] + '[i]' + operator[1] + variable[1]+'[i])'+ operator[2] + variable[2] + '[i]'
            else:
                oper = '('+ variable[0] + '[i]' + operator[0] + variable[1]+'[i])'+ operator[1] + variable[2] + '[i]'
            
    return '        exp_result[i] = ' + oper + ';'

def compare(node, variable):
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
            
    return '        exp_result[i] = ' + oper + ';'

def move(node, variable):
    oper = 'TODO'
    split_type = node['Intrinsic_Name'].split('_')
    
    if '_m' not in node['Intrinsic_Name']:
        if split_type[1] == 'v' and split_type[2] == 'x':
            oper = variable[0]
        if split_type[1] == 'v' and split_type[2] == 'i':  # imm: fix it as 3
            oper = '3'
        if split_type[1] == 'x' and split_type[2] == 'v': 
            oper = variable[0] + '[' + variable[1] + ']'

    return '        exp_result[i] = ' + oper + ';'

def SetGoldenFunction(node, elenum, typebit, apitype):
    variableList = []
    expInput = ''
    
    operator = 'Operator Line --- TODO'
    line1 = ['#pragma GCC push_options', 
             '#pragma GCC optimize("O0")',
             '__attribute__((noinline, noclone))']
    line3 = ['#pragma GCC pop_options', '', 
             'int main(void) {' ]
    
    # get exp input list
    for i in range(1,8):
        if node['Input_'+str(i)+'_Type'] and 'accum' not in node['Input_'+str(i)+'_Variable']: 
            variableList.append(node['Input_'+str(i)+'_Variable'])
            
            if 'x' in node['Input_'+str(i)+'_Type']:
                inputType = node['Input_'+str(i)+'_Type'].split('x')[0]+'_t'
                expInput+= inputType + ' *' + node['Input_'+str(i)+'_Variable'] + ','
            else:
                inputType = node['Input_'+str(i)+'_Type']
                expInput+= inputType + ' ' + node['Input_'+str(i)+'_Variable'] + ','

    if 'x' in node['Output_Type']: expType = node['Output_Type'].split('x')[0] + '_t'
    elif 'bool' in node['Output_Type']: expType = 'uint'+ typebit + '_t'
    else: expType = node['Output_Type']
    expInput += expType + ' *exp_result'
    
    # get exp operator 
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
             '    for (int i = 0; i < ELE_NUM; i++)',
             operator,
             '}']
            
    return line1+line2+line3
    
    