####################################################################################
# This script is to generate c source file accoding to JSON for all apis 
####################################################################################
import os,sys
import re,subprocess
import platform
import datetime,time
import shutil
import json
from optparse import OptionParser
from subprocess import Popen, PIPE

from typeMap import TEMPLATE_TYPE
from comFunctions import copyFile,getInputParameters,getRunlines,getVwrCsr,writeFile
#####################################################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

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
    
    paraLines = getInputParameters(parameters, elementNum, comboNum, 'load')
    runLines = getRunlines(parameters, apiName,'load')
    
    comboLine = 'int combo_num = ' + comboNum + ';'
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([comboLine, elementLine, resultLine, expectResult])
    
    elementWidth = 'int element_width = ' + typeBit + '/8;'
    paraLines.extend([elementWidth, ''])
    vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
    paraLines.extend(vwrcsrLines)
    
    if comboNum != '1':
        tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][1]
    else: tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][0]
        
    writeFile(apiFile, paraLines + runLines, tailFile)

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
    
    paraLines = getInputParameters(parameters, elementNum, '1', 'arithmetic')
    runLines = getRunlines(parameters, apiName, 'arithmetic' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([elementLine, resultLine, expectResult])

    writeFile(apiFile, paraLines + runLines, TEMPLATE_TYPE[node['Intrinsic_Type']][0])

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

    paraLines = getInputParameters(parameters, elementNum, comboNum, 'store')
    runLines = getRunlines(parameters, apiName, 'store')

    comboLine = 'int combo_num = ' + comboNum + ';'
    elementLine = 'int element_num = ' + elementNum + ';'
    for line in paraLines: 
        if 'base' in line: expType = line.split( ' ' )[0]
    if node['Expect_Result']:
        expectResult = expType + ' exp_result[' + elementNum + '] = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = expType + ' exp_result[' + elementNum + '] = {0};'
    paraLines.extend([comboLine, elementLine, expectResult])
    
    elementWidth = 'int element_width = ' + typeBit + '/8;'
    paraLines.extend([elementWidth, ''])
    vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
    paraLines.extend(vwrcsrLines)
    
    if comboNum != '1':
        tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][1]
    else: tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][0]
    
    writeFile(apiFile, paraLines + runLines, tailFile)

def logicalFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', 'logic', apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, elementNum, '1', 'logic')
    runLines = getRunlines(parameters, apiName, 'logic' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([elementLine, resultLine, expectResult])

    writeFile(apiFile, paraLines + runLines, TEMPLATE_TYPE[node['Intrinsic_Type']][0])

def shiftFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', 'shift', apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, elementNum, '1', 'shift')
    runLines = getRunlines(parameters, apiName, 'shift' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
    paraLines.extend([elementLine, resultLine, expectResult])

    writeFile(apiFile, paraLines + runLines, TEMPLATE_TYPE[node['Intrinsic_Type']][0])
    
###########################################################################################
# usage: python3 
# python SourceFile.py -d "C:\Analog Devices\Risc-v\source-file" -n "intrinsic_table.json"
###########################################################################################
def main():
    jsonDir = os.path.join(os.path.abspath(os.path.join(ROOT_DIR, "..")), 'scripts' )

    rootNode={}
    lines = []
    file = os.path.join( jsonDir, 'intrinsic_table.json' )
    with open(file, 'r') as f:
        rootNode = json.loads(f.read())
    for nodes in rootNode:
        if 'CSR' in nodes['Intrinsic_Type']:  pass #All apis in CSR type are tested together by another files
        elif 'Contiguous Load:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']:  loadFile(nodes)
        elif 'Contiguous Store:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']: pass #storeFile(nodes)
        elif 'Arithmetic:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']:       pass #arithmeticFile(nodes)
        elif 'Logic:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']:             pass #logicalFile(nodes) #pass
        elif 'Shift:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']:             pass #shiftFile(nodes)
        else: pass
        
if __name__ == "__main__":  
    main() 