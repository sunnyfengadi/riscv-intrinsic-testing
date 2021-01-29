############################################################
# This script is to save the functions used by SourceFile.py
############################################################
import os,sys
import re,subprocess
import shutil

from optparse import OptionParser
from subprocess import Popen, PIPE

##############################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join( ROOT_DIR, 'template' )
TARGETFILE_PATH = os.path.join( ROOT_DIR, 'lib' )
GOLDEN_PATH = os.path.join( ROOT_DIR, 'golden' )

def copyFile( templateFile, apitype, dstName ):
    dst = os.path.join( TARGETFILE_PATH, apitype )
    if not os.path.exists(dst):
        os.makedirs(dst)

    src= os.path.join( ROOT_DIR, 'template' )
    srcFile = os.path.join( src, templateFile )
    dstFile = os.path.join( dst, dstName + '.c' )
    if os.path.isfile(srcFile):
        shutil.copy( srcFile , os.path.normpath( dstFile ) )
    else:
        raise Exception("No this file as template")
        
    return dstFile
    
def writeFile (sourceFile,goldenlines, lines, tailfile):
    with open(sourceFile, 'a+') as f:
        for line in goldenlines:
            if line == '': f.write('\n')
            else: f.write(line + '\n' )
            
        for line in lines:
            if line == '': f.write('\n')
            else: f.write( '    ' + line + '\n' )
    # Write the file tail
    with open(os.path.join(TEMPLATE_PATH,tailfile),'r') as f:
        tailLines=f.readlines()
    with open(sourceFile,'a') as f:
            for line in tailLines:
                f.writelines(line)
    f.close()
    
def getInputParameters(inputDict, elementnum, combonum, apitype):
    inputList = ['int i,j;']
    expInput = []
    
    if apitype=='load' or apitype=='iir':
        totalnum = int(elementnum)* int(combonum)
        value2 = ''
        if 'base' in inputDict['Input_1_Variable']:
            Input_1_Variable = inputDict['Input_1_Variable'].strip( ']' ) + str(totalnum) + ']'
        else: Input_1_Variable = inputDict['Input_1_Variable'].rstrip()
            
        if 'maskoff' in inputDict['Input_2_Variable'] and combonum != '1':
            valueList = inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' + '{'
            for i in range(int(combonum)):
                value = '.val[' + str(i) + '] = ' + inputDict['Input_2_Value'] + ','
                valueList += value + '\n\t\t\t'
            value2 = valueList.rstrip('\n\t\t\t').rstrip(',') + '};'
        else: 
            value2 = inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' +  str(inputDict['Input_2_Value'])+ ';'
            
        if inputDict['Input_1_Type']: 
            inputList.append(inputDict['Input_1_Type'] + ' ' + Input_1_Variable + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: 
            inputList.append(value2)
        if inputDict['Input_3_Type']:
            Input_3_Variable = inputDict['Input_3_Variable'].strip( ']' ) + str(totalnum) + ']'
            inputList.append(inputDict['Input_3_Type'] + ' ' + Input_3_Variable + ' = ' + str(inputDict['Input_3_Value']) + ';')
            
        for i in range(4,8):
            if inputDict['Input_'+str(i)+'_Type']: 
                inputList.append(inputDict['Input_'+str(i)+'_Type'] +' '+inputDict['Input_'+ str(i)+'_Variable'].rstrip()+' = '+ str(inputDict['Input_'+str(i)+'_Value']) + ';')
        
    if apitype == 'store':
        if 'base' in inputDict['Input_1_Variable']:Input_1_Variable = inputDict['Input_1_Variable'].strip( ']' ) + str(elementnum) + ']'
        else:Input_1_Variable = inputDict['Input_1_Variable'].rstrip()
        if 'base' in inputDict['Input_2_Variable']:Input_2_Variable = inputDict['Input_2_Variable'].strip( ']' ) + str(elementnum) + ']'
        else:Input_2_Variable = inputDict['Input_2_Variable'].rstrip()
        
        if inputDict['Input_1_Type']: inputList.append(inputDict['Input_1_Type'] + ' ' + Input_1_Variable + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: inputList.append(inputDict['Input_2_Type'] + ' ' + Input_2_Variable + ' = ' + str(inputDict['Input_2_Value']) + ';')
        for i in range(3,8):
            if inputDict['Input_'+str(i)+'_Type']: 
                inputList.append(inputDict['Input_'+str(i)+'_Type'] +' '+inputDict['Input_'+ str(i)+'_Variable'].rstrip()+' = '+ str(inputDict['Input_'+str(i)+'_Value']) + ';')
        
    if apitype=='common':
        # common type list: logic, shfit, move, mac, arithmetic, reduction, permutation, conversion, compare
        for i in range(1,8):
            if inputDict['Input_'+str(i)+'_Type']: 
                inputList.append(inputDict['Input_'+str(i)+'_Type'] +' '+inputDict['Input_'+ str(i)+'_Variable'].rstrip()+' = '+ str(inputDict['Input_'+str(i)+'_Value']) + ';')
                
                if 'x' in inputDict['Input_'+str(i)+'_Type']: 
                    inputType = inputDict['Input_'+str(i)+'_Type'].split('x')[0] + '_t'
                else: inputType = inputDict['Input_'+str(i)+'_Type']
                
                if ',' in inputDict['Input_'+str(i)+'_Value']:
                    expInput.append(inputType +' exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip()+'['+ elementnum + ']= '+ str(inputDict['Input_'+str(i)+'_Value']) + ';')
                else:
                    expInput.append(inputType +' exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip()+' = '+ str(inputDict['Input_'+str(i)+'_Value']) + ';')
                
    return inputList + expInput

def getRunlines(inputDict, functionName, apitype):
    variableList = []
    apiInput = ''
    expInput = ''
    
    for item in inputDict.items():
        if item[0].split( '_' )[2] == 'Variable' and item[1]:
            variableList.append(item[1].strip( '[]' ))  #need remove the '[]' in 'base[]'
    for variable in variableList:
        expInput += 'exp_' + variable + ','
        if 'imm' == variable: variable = '0'  #now imm is fixed as 0 since Risc-v issue
        apiInput += variable + ','
    
    expRun =  functionName + '_golden(' + expInput + 'exp_result);'
    
    if apitype == 'store':
        apiRun = functionName + '(' + apiInput.strip( ',' ) + ');'
        run = [ '', expRun, apiRun]
    else:
        apiRun = 'result = ' + functionName + '(' + apiInput.strip( ',' ) + ');'
        run = [ '', expRun, apiRun]
    
    return run 
    
def getVwrCsr (combonum,typebit):
    lines = []
    
    element_width = typebit//8
    element_stride = combonum * element_width
    combo_stride = element_width
    group_stride = element_stride *2
    group_depth = element_width *4
    
    lines.append('vwr_csr(' + 'RUGRATS_VMELEMENTSTRIDE,' + str(element_stride) + ');') #element_stride = combo_num * element_width
    lines.append('vwr_csr(' + 'RUGRATS_VMCOMBOSTRIDE,' + str(combo_stride) + ');')     #combo_stride = element_width
    lines.append('vwr_csr(' + 'RUGRATS_VMGROUPSTRIDE,' + str(group_stride) + ');')     #group_stride = element_stride *N( N = 1,2,3... && N <= element_num_per_group), N=2
    lines.append('vwr_csr(' + 'RUGRATS_VMGROUPNUMBER,' + str(4) + ');')
    lines.append('vwr_csr(' + 'RUGRATS_VMGROUPDEPTH,' + str(group_depth) + ');')       #group_depth = element_width *element_num_per_group (element_num_per_group = 4)
    
    return lines 
    

