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

OPERATOR_1= {'-' : 'neg',
}

OPERATOR_2= {'+': 'add',
             '-': 'sub',
             '*': 'mul',
}
OPERATOR_3= {}

def arithmetic(node, variable):
    oper = 'TODO'
    if '_m' in node['Intrinsic_Name']: 
        return oper
    else:
        if len(variable)==1:
            for item in OPERATOR_2.items():
                if item[1] in node['Intrinsic_Name']:
                    operator  = item[0]
                    oper = operator + variable[1] + '[i]'
                
        if len(variable)==2:
            for item in OPERATOR_2.items():
                if item[1] in node['Intrinsic_Name']:
                    operator  = item[0]
                    print(operator)
                else:
                    operator = 'Todo'
                    
            if 'vx' in node['Intrinsic_Name'].split('_')[1]:
                print("sssssssssssssssssssssssssss")
                oper = variable[0] + '[i]' + operator + variable[1]
            else:
                oper = variable[0] + '[i]' + operator + variable[1] + '[i]'
            
    return '        exp_result[i] = ' + oper + ';'

def getExpResult(node, elenum, typebit, apitype):
    expLines = []
    variableList = []
    expInput = ''
    
    operator = 'TODO'
    line1 = ['#define ELE_NUM ' + elenum, ' ', 
             '#pragma GCC push_options', 
             '#pragma GCC optimize("O0")'
             '__attribute__((noinline, noclone))']
    line3 = ['#pragma GCC pop_options', '', 
             'int main(void) {' ]
    
    # get exp input list
    for i in range(1,8):
        if node['Input_'+str(i)+'_Type'] and 'accum' not in node['Input_'+str(i)+'_Variable']: 
            variableList.append(node['Input_'+str(i)+'_Variable'])
            
            if 'x' in node['Input_'+str(i)+'_Type']:
                inputType = node['Input_'+str(i)+'_Type'].split('x')[0]+'_t'
            else: inputType = node['Input_'+str(i)+'_Type']
            expInput+= inputType + ' *' + node['Input_'+str(i)+'_Variable'] + ','

    if 'x' in node['Output_Type']: expType = node['Output_Type'].split('x')[0] + '_t'
    elif 'bool' in node['Output_Type']: expType = 'uint'+ typebit + '_t'
    else: expType = node['Output_Type']
    expInput += expType + ' *exp_result'
    
    # get exp operator 
    if apitype == 'arithmetic':
        operator = arithmetic(node, variableList)
    else:
        pass
            
    line2 = ['void '+ node['Intrinsic_Name'].rstrip() + '_golden(' + expInput + ') {',
             '    for (int i = 0; i < ELE_NUM; i++)',
             operator,
             '}']
            
    expLines = line1+line2+line3
    return expLines 