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
    
    if comboNum != '1':
        tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][1]
        elementWidth = 'int element_width = ' + typeBit + '/8;'
        paraLines.extend([elementWidth, ''])
        # combo_num = 2,3,...,8 it has vwr_csr() to register the memory
        vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
        paraLines.extend(vwrcsrLines)
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
    
    if comboNum != '1':
        tailFile = TEMPLATE_TYPE[node['Intrinsic_Type']][1]
        elementWidth = 'int element_width = ' + typeBit + '/8;'
        paraLines.extend([elementWidth, ''])
        # combo_num = 2,3,...,8 it has vwr_csr() to register the memory
        vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
        paraLines.extend(vwrcsrLines)
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

###########################################################################################
# usage: python3 
# python SourceFile.py -d "C:\Analog Devices\Risc-v\source-file" -n "intrinsic_table.json"
###########################################################################################
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
        if 'CSR' in nodes['Intrinsic_Type']:                                                         pass #All apis in CSR type are tested together by another files
        elif 'Contiguous Load:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']:  loadFile(nodes)
        elif 'Contiguous Store:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']: storeFile(nodes)
        elif 'Arithmetic:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']:       arithmeticFile(nodes)
        elif 'Logic:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']:             logicalFile(nodes) 
        else: pass
        
if __name__ == "__main__":  
    main() 