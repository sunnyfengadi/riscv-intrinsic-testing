##########################################################
# This script is to generate source file accoding to JSON 
##########################################################
import os,sys
import re,subprocess
import platform
import datetime,time
import shutil
import subprocess
import json
from optparse import OptionParser
from subprocess import Popen, PIPE
from typeMap import TEMPLATE_TYPE
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
    
def getInputParameters(inputDict, totalnum, apitype):
    inputList = []
    if apitype == 'load':
        if 'base' in inputDict['Input_1_Variable']:Input_1_Variable = inputDict['Input_1_Variable'].strip( ']' ) + str(totalnum) + ']'
        else:Input_1_Variable = inputDict['Input_1_Variable'].rstrip()
        if inputDict['Input_1_Type']: inputList.append(inputDict['Input_1_Type'] + ' ' + Input_1_Variable + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: inputList.append(inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' + str(inputDict['Input_2_Value']) + ';')
        if inputDict['Input_3_Type']:
            Input_3_Variable = inputDict['Input_3_Variable'].strip( ']' ) + str(totalnum) + ']'
            inputList.append(inputDict['Input_3_Type'] + ' ' + Input_3_Variable + ' = ' + str(inputDict['Input_3_Value']) + ';')
        if inputDict['Input_4_Type']: inputList.append(inputDict['Input_4_Type'] + ' ' + inputDict['Input_4_Variable'] + ' = ' + str(inputDict['Input_4_Value']) + ';')
    elif apitype == 'arithmetic':
        if inputDict['Input_1_Type']: inputList.append(inputDict['Input_1_Type'] + ' ' + inputDict['Input_1_Variable'].rstrip() + ' = ' + str(inputDict['Input_1_Value']) + ';')
        if inputDict['Input_2_Type']: inputList.append(inputDict['Input_2_Type'] + ' ' + inputDict['Input_2_Variable'].rstrip() + ' = ' + str(inputDict['Input_2_Value']) + ';')
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
    
def writeFile (sourceFile, lines, combo):
    with open(sourceFile, 'a+') as f:
        for line in lines:
            if line == '': f.write('\n')
            else: f.write( '    ' + line + '\n' )
    # Write the file tail
    if combo == '1':
        with open(os.path.join(TEMPLATE_PATH,'common_tail_1.c'),'r') as f:
                commonTailLines=f.readlines()
    else:
        with open(os.path.join(TEMPLATE_PATH,'common_tail_x.c'),'r') as f:
                commonTailLines=f.readlines()
    with open(os.path.join(TARGETFILE_PATH,sourceFile),'a') as f:
            for line in commonTailLines:
                f.writelines(line)
    f.close()
    
def loadFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    comboNum = re.findall(r"\d+\.?\d*", apiName)[0]
    apiFile = copyFile('template_head.c', 'load', apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, int(elementNum)* int(comboNum), 'load')
    runLines = getRunlines(parameters, apiName,'load')
    
    comboLine = 'int combo_num = ' + comboNum + ';'
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([comboLine, elementLine, resultLine, expectResult])
    
    if comboNum != '1':
        elementWidth = 'int element_width = ' + typeBit + '/8;'
        paraLines.extend([elementWidth, ''])
        # combo_num = 2,3,...,8 it has vwr_csr() to register the memory
        vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
        paraLines.extend(vwrcsrLines)
        
    writeFile(apiFile, paraLines + runLines,comboNum)

def arithmeticFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', 'arithmetic', apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, int(elementNum)* 1, 'arithmetic')
    runLines = getRunlines(parameters, apiName, 'arithmetic' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([elementLine, resultLine, expectResult])
        
    writeFile(apiFile, paraLines + runLines,'1')

def storeFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    comboNum = re.findall(r"\d+\.?\d*", apiName)[0]
    apiFile = copyFile('template_head.c', 'store', apiName)
    
    for item in node.items():
        if 'int' in item[1] and 'x' in item[1]:
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])      # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1])   # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                       # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, int(elementNum)* int(comboNum), 'store')
    runLines = getRunlines(parameters, apiName, 'store')
    
    comboLine = 'int combo_num = ' + comboNum + ';'
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([comboLine, elementLine, resultLine, expectResult])
    
    if comboNum != '1':
        elementWidth = 'int element_width = ' + typeBit + '/8;'
        paraLines.extend([elementWidth, ''])
        # combo_num = 2,3,...,8 it has vwr_csr() to register the memory
        vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
        paraLines.extend(vwrcsrLines)
        
    writeFile(apiFile, paraLines + runLines,comboNum)

#########################################################################
# Main
# 
# python SourceFile.py -d "C:\Analog Devices\Risc-v\source-file" -n "intrinsic_table.json"
#########################################################################
def main():
    __version__="1.0" 
    parser=OptionParser(usage="usage: %prog parse exist json and create source C file",version="%prog "+"%s"%(__version__))
    parser.add_option("-d","--dir",help="provide the json path",dest="dir",default='C:\Analog Devices\Risc-v\source-file')
    parser.add_option("-n","--name",help="provide the name of json file",dest="name",default='intrinsic_table.json')
    (options,args)=parser.parse_args()  
    jsonDir = options.dir
    jsonName = options.name

    rootNode={}
    lines = []
    file = os.path.join( jsonDir, jsonName )
    with open(file, 'r') as f:
        rootNode = json.loads(f.read())
    for nodes in rootNode:
        if 'CSR' in nodes['Intrinsic_Type']: pass  # All apis in CSR type are tested together by another files
        elif 'Load' in nodes['Intrinsic_Type']: pass #loadFile(nodes)
        elif 'Store' in nodes['Intrinsic_Type']: storeFile(nodes)
        elif 'Arithmetic' in nodes['Intrinsic_Type']: pass #arithmeticFile(nodes)
        elif 'Logical' in nodes['Intrinsic_Type']:pass
        else: pass
if __name__ == "__main__":  
    main() 