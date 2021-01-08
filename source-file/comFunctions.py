##########################################################
# This script is to generate source file accoding to JSON 
##########################################################
import os,sys
import re,subprocess
import shutil

from optparse import OptionParser
from subprocess import Popen, PIPE

##############################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join( ROOT_DIR, 'template' )
TARGETFILE_PATH = os.path.join( ROOT_DIR, 'lib' )

def copyFile( templateFile, apitype, dstName ):
    dst = os.path.join( TARGETFILE_PATH, apitype )
    src= os.path.join( ROOT_DIR, 'template' )
    srcFile = os.path.join( src, templateFile )
    dstFile = os.path.join( dst, dstName + '.c' )
    if os.path.isfile(srcFile):
        shutil.copy( srcFile , os.path.normpath( dstFile ) )
    else:
        raise Exception("No this file as template")
        
    return dstFile
    
def getInputParameters(inputDict, elementnum, combonum, apitype):
    inputList = []
    
    if apitype == 'load':
        totalnum = int(elementnum)* int(combonum)
        if 'base' in inputDict['Input_1_Variable']:
            Input_1_Variable = inputDict['Input_1_Variable'].strip( ']' ) + str(totalnum) + ']'
        else: Input_1_Variable = inputDict['Input_1_Variable'].rstrip()
            
        if 'maskoff' in inputDict['Input_2_Variable']:
            # int16x32x2_t maskoff = {.val[0]={11,22,33,44,55,66,77,88},.val[1]={11,22,33,44,55,66,77,88}};
            valueList = '{' + '.val[0]=' + inputDict['Input_2_Value'] + ', .val[1]=' + inputDict['Input_2_Value'] + '}'
        else: valueList = inputDict['Input_2_Variable'].rstrip()
            
        if inputDict['Input_1_Type']: 
            inputList.append(inputDict['Input_1_Type'] + ' ' + Input_1_Variable + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: 
            inputList.append(inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' + valueList + ';')
        if inputDict['Input_3_Type']:
            Input_3_Variable = inputDict['Input_3_Variable'].strip( ']' ) + str(totalnum) + ']'
            inputList.append(inputDict['Input_3_Type'] + ' ' + Input_3_Variable + ' = ' + str(inputDict['Input_3_Value']) + ';')
        if inputDict['Input_4_Type']: inputList.append(inputDict['Input_4_Type'] + ' ' + inputDict['Input_4_Variable'] + ' = ' + str(inputDict['Input_4_Value']) + ';')
    
    elif apitype == 'arithmetic' or apitype == 'logic' or apitype == 'shift':
        if inputDict['Input_1_Type']: inputList.append(inputDict['Input_1_Type'] + ' ' + inputDict['Input_1_Variable'].rstrip() + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: inputList.append(inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' + str(inputDict['Input_2_Value']) + ';')
        if inputDict['Input_3_Type']: inputList.append(inputDict['Input_3_Type'] + ' ' + inputDict['Input_3_Variable'].rstrip() + ' = ' + str(inputDict['Input_3_Value']) + ';')
        if inputDict['Input_4_Type']: inputList.append(inputDict['Input_4_Type'] + ' ' + inputDict['Input_4_Variable'].rstrip() + ' = ' + str(inputDict['Input_4_Value']) + ';')
    
    elif apitype == 'store':
        if 'base' in inputDict['Input_1_Variable']:Input_1_Variable = inputDict['Input_1_Variable'].strip( ']' ) + str(elementnum) + ']'
        else:Input_1_Variable = inputDict['Input_1_Variable'].rstrip()
        if 'base' in inputDict['Input_2_Variable']:Input_2_Variable = inputDict['Input_2_Variable'].strip( ']' ) + str(elementnum) + ']'
        else:Input_2_Variable = inputDict['Input_2_Variable'].rstrip()
        if inputDict['Input_1_Type']: inputList.append(inputDict['Input_1_Type'] + ' ' + Input_1_Variable + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: inputList.append(inputDict['Input_2_Type'] + ' ' + Input_2_Variable + ' = ' + str(inputDict['Input_2_Value']) + ';')
        if inputDict['Input_3_Type']: inputList.append(inputDict['Input_3_Type'] + ' ' + inputDict['Input_3_Variable'].rstrip() + ' = ' + str(inputDict['Input_3_Value']) + ';')
        if inputDict['Input_4_Type']: inputList.append(inputDict['Input_4_Type'] + ' ' + inputDict['Input_4_Variable'].rstrip() + ' = ' + str(inputDict['Input_4_Value']) + ';')
        
    else: pass
    
    return inputList
    
def getRunlines(inputDict, functionName, apitype):
    variableList = []
    apiInput = ''
    
    for item in inputDict.items():
        if item[0].split( '_' )[2] == 'Variable' and item[1]:
            variableList.append(str(''.join(re.findall(r'[A-Za-z]', item[1]))))
            
    for variable in variableList:
        if 'imm' == variable: variable = '0'  #now imm is fixed as 0 since Risc-v bug
        apiInput += variable + ','
    if apitype == 'store':
        apiTest = functionName + '(' + apiInput.strip( ',' ) + ');'
        run = [ '', apiTest]
    else:
        apiTest = 'result = ' + functionName + '(' + apiInput.strip( ',' ) + ');'
        run = [ '', 'start = cycles();', apiTest, 'stop = cycles();']
    
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
    
def writeFile (sourceFile, lines, tailfile):
    with open(sourceFile, 'a+') as f:
        for line in lines:
            if line == '': f.write('\n')
            else: f.write( '    ' + line + '\n' )
    # Write the file tail
    with open(os.path.join(TEMPLATE_PATH,tailfile),'r') as f:
        tailLines=f.readlines()
    with open(os.path.join(TARGETFILE_PATH,sourceFile),'a') as f:
            for line in tailLines:
                f.writelines(line)
    f.close()
    