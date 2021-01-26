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
from .comFunctions import *

sys.path.append('..') 
from scripts.Intrinsic_Type_List import INTRINSIC_TYPE_MAP
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
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = {0};'
        #print("please add the expect result for %s" %node['Intrinsic_Name'])
    paraLines.extend([comboLine, elementLine, resultLine, expectResult])
    
    elementWidth = 'int element_width = ' + typeBit + '/8;'
    paraLines.extend([elementWidth, ''])
    vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
    paraLines.extend(vwrcsrLines)
    
    if comboNum != '1':
        tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][2]
    else: tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1]
        
    writeFile(apiFile, paraLines + runLines, tailFile)

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
        tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][2]
    else: tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1]
    
    writeFile(apiFile, paraLines + runLines, tailFile)

def compareFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', 'compare', apiName)
    
    for item in node.items():
        if item[0] == 'Intrinsic_Name':                             # get the type bit number 16/32/64 bit
            for i in item[1].split('_'):
                if re.match('[iu][136][624]$',i):
                    typeBit = re.sub("\D", "", i)
        
        if item[0] == 'Output_Type':                                # get the number of element that is 8 or 16 or 32
            elementNum = re.sub("\D", "", item[1])
            
        if item[0].split( '_' )[0] == 'Input':                      # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, elementNum, '1', 'common')
    runLines = getRunlines(parameters, apiName, 'common' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'] + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'] + ' exp_result = {0};'
        #print("please add the expect result for %s" %node['Intrinsic_Name'])
    
    paraLines.extend([elementLine, resultLine, expectResult])
    writeFile(apiFile, paraLines + runLines, INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1])
    
def iirFile(node):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    comboNum = re.findall(r"\d+\.?\d*", apiName.split('_')[-1])[0]
    apiFile = copyFile('template_head.c', 'iir', apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, elementNum, comboNum, 'iir')
    runLines = getRunlines(parameters, apiName,'iir')
    
    comboLine = 'int combo_num = ' + comboNum + ';'
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = {0};'
        #print("please add the expect result for %s" %node['Intrinsic_Name'])
    paraLines.extend([comboLine, elementLine, resultLine, expectResult])
    
    elementWidth = 'int element_width = ' + typeBit + '/8;'
    paraLines.extend([elementWidth, ''])
    vwrcsrLines = getVwrCsr(int (comboNum), int (typeBit))
    paraLines.extend(vwrcsrLines)
    
    if comboNum != '1':
        tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][2]
    else: tailFile = INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1]
        
    writeFile(apiFile, paraLines + runLines, tailFile)
    
def generalFile(node, apitype):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', apitype, apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':
            typeBit = re.sub("\D", "", item[1].split( 'x' )[0])    # get the type bit number 16/32/64 bit
            elementNum = re.sub("\D", "", item[1].split( 'x' )[1]) # get the number of element that is 16 or 32 
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
    
    paraLines = getInputParameters(parameters, elementNum, '1', 'common')
    runLines = getRunlines(parameters, apiName, 'common' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    if node['Expect_Result']:
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = node['Output_Type'].split('x')[0] + '_t exp_result = {0};'
        #print("please add the expect result for %s" %node['Intrinsic_Name'])
    
    paraLines.extend([elementLine, resultLine, expectResult])
    writeFile(apiFile, paraLines + runLines, INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1])
    
def commonFile(node, apitype):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', apitype, apiName)
    
    for item in node.items():
        if item[0] == 'Intrinsic_Name':                             # get the type bit number 16/32/64 bit
            for i in item[1].split('_'):
                if re.match('[iu][136][624]$',i):
                    typeBit = re.sub("\D", "", i)
                    elementNum = str(512// int(typeBit))
                if 'bool' in i:
                    elementNum = re.sub("\D", "", i)               # get the number of element that is 8 or 16 or 32
        if item[0].split( '_' )[0] == 'Input':                     # get the list of variables
            parameters[item[0]] = item[1]
        
    paraLines = getInputParameters(parameters, elementNum, '1', 'common')
    runLines = getRunlines(parameters, apiName, 'common' )
    
    elementLine = 'int element_num = ' + elementNum + ';'
    resultLine = node['Output_Type'] + ' result = {0};'
    
    if 'x' in node['Output_Type']: expType = node['Output_Type'].split('x')[0] + '_t'
    else: expType = node['Output_Type']
    if node['Expect_Result']:
        expectResult = expType + ' exp_result = ' + str(node['Expect_Result']) + ';'
    else:
        expectResult = expType + ' exp_result = {0};'
        #print("please add the expect result for %s" %node['Intrinsic_Name'])

    paraLines.extend([elementLine, resultLine, expectResult])
    writeFile(apiFile, paraLines + runLines, INTRINSIC_TYPE_MAP[node['Intrinsic_Type']][1])
    
###########################################################################################
# usage: python3 
# python SourceFile.py -d "C:\Analog Devices\Risc-v\source-file" -n "intrinsic_table.json"
###########################################################################################
def sourceHandler(typeList):
    jsonDir = os.path.join(os.path.abspath(os.path.join(ROOT_DIR, "..")), 'scripts' )
    rootNode={}
    file = os.path.join( jsonDir, 'intrinsic_table.json' )
    with open(file, 'r') as f:
        rootNode = json.loads(f.read())
    for nodes in rootNode:
        #for apis that have combo num: 1-8, others is 1 
        if 'Load:' in nodes['Intrinsic_Type']: loadFile(nodes)
        if 'Store:' in nodes['Intrinsic_Type']: storeFile(nodes)
        if 'IIR:' in nodes['Intrinsic_Type']: iirFile(nodes)
            
        #out_type is all bool, maybe merged into commonFile() later 
        if 'Compare:' in nodes['Intrinsic_Type']: compareFile(nodes)
        
        #for logic, shift, move that have bool type
        if 'Logic:' in nodes['Intrinsic_Type']: commonFile(nodes, 'logic')
        if 'Shift:' in nodes['Intrinsic_Type']: commonFile(nodes, 'shift')
        if 'Move:' in nodes['Intrinsic_Type']: commonFile(nodes, 'move')
        
        #for arithmetic, mac, reduction, permutation, conversion
        if 'Arithmetic:' in nodes['Intrinsic_Type']: generalFile(nodes, 'arithmetic')
        if 'Mac:' in nodes['Intrinsic_Type']: generalFile(nodes, 'mac')
        if 'Reduction:' in nodes['Intrinsic_Type']: generalFile(nodes, 'reduction')
        if 'Permutation:' in nodes['Intrinsic_Type']: generalFile(nodes, 'permutation')
        if 'Conversion:' in nodes['Intrinsic_Type']: generalFile(nodes, 'conversion')
    