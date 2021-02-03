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
from .goldenFunctions import *

sys.path.append('..') 
from scripts.Intrinsic_Type_List import INTRINSIC_TYPE_MAP
#####################################################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

TYPE_DICT= {
    'Load:'       :'Load',
    'Store:'      :'store',
    'IIR:'        :'iir',
    'Compare:'    :'compare',
    'Logic:'      :'logic',
    'Shift:'      :'shift',
    'Move:'       :'move',
    'Arithmetic:' :'arithmetic',
    'Mac:'        :'mac',
    'Reduction:'  :'reduction',
    'Permutation:':'permutation',
    'Conversion:' :'conversion',
    }

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

    MacroLines = SetMacro(typeBit, elementNum, comboNum, 'load')
    DataInitDefinitionLines = SetDataInitDefinition()
    goldenLines = SetGoldenFunction(node, elementNum, typeBit, 'load')
    paraLines = getInputParameters(parameters, elementNum, comboNum)
    resultLine = SetResultLine(node,typeBit)
    DataInitLines = DataInit(node,parameters,typeBit,elementNum,'load')
    vwrcsrLines = getVwrCsr()
    runLines = getRunlines(parameters, apiName, 'load' )
    
    goldenLines = MacroLines + DataInitDefinitionLines + goldenLines
    paraLines += resultLine + DataInitLines + vwrcsrLines + runLines

    for item in INTRINSIC_TYPE_MAP.items():
        ret = re.match(item[0],node['Intrinsic_Name'])
        if ret:
            if comboNum != '1':
                tailFile = item[1][2]
            else: tailFile = item[1][1]
            
    writeFile(apiFile, goldenLines, paraLines, tailFile)

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

    MacroLines = SetMacro(typeBit, elementNum, comboNum, 'store')
    DataInitDefinitionLines = SetDataInitDefinition()
    goldenLines = SetGoldenFunction(node, elementNum, typeBit, 'store')
    paraLines = getInputParameters(parameters, elementNum, comboNum)
    resultLine = SetResultLine(node,typeBit)
    DataInitLines = DataInit(node,parameters,typeBit,elementNum,'store')
    vwrcsrLines = getVwrCsr()
    runLines = getRunlines(parameters, apiName, 'store')

    goldenLines = MacroLines + DataInitDefinitionLines + goldenLines
    paraLines += resultLine + DataInitLines + vwrcsrLines + runLines
    
    for item in INTRINSIC_TYPE_MAP.items():
        ret = re.match(item[0],node['Intrinsic_Name'])
        if ret:
            if comboNum != '1':
                tailFile = item[1][2]
            else: tailFile = item[1][1]

    writeFile(apiFile, goldenLines, paraLines, tailFile)
    
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
    
    #paraLines = getInputParameters(parameters, elementNum, comboNum)
    #runLines = getRunlines(parameters, apiName,'iir')
    MacroLines = SetMacro(typeBit, elementNum, comboNum, 'iir')
    DataInitDefinitionLines = SetDataInitDefinition()
    goldenLines = SetGoldenFunction(node, elementNum, typeBit, 'iir')
    paraLines = getInputParameters(parameters, elementNum, comboNum)
    resultLine = SetResultLine(node,typeBit)
    DataInitLines = DataInit(node,parameters,typeBit, elementNum, 'iir')
    vwrcsrLines = getVwrCsr()
    runLines = getRunlines(parameters, apiName, 'iir')

    goldenLines = MacroLines + DataInitDefinitionLines + goldenLines
    paraLines += resultLine + DataInitLines + vwrcsrLines + runLines
    
    for item in INTRINSIC_TYPE_MAP.items():
        ret = re.match(item[0],node['Intrinsic_Name'])
        if ret:
            if comboNum != '1':
                tailFile = item[1][2]
            else: tailFile = item[1][1]

    writeFile(apiFile, goldenLines, paraLines, tailFile)
    
def commonFile(node, apitype):
    parameters={}
    apiName = node['Intrinsic_Name'].rstrip()
    apiFile = copyFile('template_head.c', apitype, apiName)
    
    for item in node.items():
        if item[0] == 'Output_Type':                               # get combo_num, 1-8
            if len(item[1].split('x'))== 3:
                comboNum = re.sub("\D", "", item[1].split('x')[2])
            else:
                for i in range(1,8):
                    if node['Input_'+str(i)+'_Type']:
                        if len(item[1].split('x'))== 3:
                            comboNum = re.sub("\D", "", item[1].split('x')[2])
                        else: comboNum = 1
            
        if item[0] == 'Intrinsic_Name':                             # get the type bit number 16/32/64 bit
            for i in item[1].split('_'):                            # get the number of element that is 8 or 16 or 32
                if re.match('[iu][136][624]$',i):
                    typeBit = re.sub("\D", "", i)
                    elementNum = str(512// int(typeBit))
                elif 'bool' in i:
                    elementNum = re.sub("\D", "", i)
                    typeBit = str(512// int(elementNum))
        if item[0].split( '_' )[0] == 'Input':                      # get the list of variables
            parameters[item[0]] = item[1]

    MacroLines = SetMacro(typeBit, elementNum, comboNum, apitype)
    DataInitDefinitionLines = SetDataInitDefinition()
    goldenLines = SetGoldenFunction(node, elementNum, typeBit, apitype)
    paraLines = getInputParameters(parameters, elementNum, comboNum)
    resultLine = SetResultLine(node,typeBit)
    DataInitLines = DataInit(node,parameters,typeBit,elementNum, apitype)
    runLines = getRunlines(parameters, apiName, apitype )
    
    goldenLines = MacroLines + DataInitDefinitionLines + goldenLines
    paraLines += resultLine + DataInitLines + runLines

    for item in INTRINSIC_TYPE_MAP.items():
        ret = re.match(item[0], node['Intrinsic_Name'])
        if ret:
            tailFile = item[1][1]

    writeFile(apiFile, goldenLines, paraLines, tailFile)


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
        if 'Load:' in nodes['Intrinsic_Type'] and 'Interleave' not in nodes['Intrinsic_Type']: loadFile(nodes)
        if 'Store:' in nodes['Intrinsic_Type'] and 'Interleave' not in nodes['Intrinsic_Type']: storeFile(nodes)
        if 'IIR:' in nodes['Intrinsic_Type']: iirFile(nodes)
            
        #for logic, shift, move, compare that have bool type
        if 'Compare:' in nodes['Intrinsic_Type']: commonFile(nodes, 'compare')
        if 'Logic:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']: commonFile(nodes, 'logic')
        if 'Shift:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type'] and '64' not in nodes['Intrinsic_Name']: commonFile(nodes, 'shift')
        if 'Move:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']: commonFile(nodes, 'move')
        
        #for arithmetic, mac, reduction, permutation, conversion
        if 'Arithmetic:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']: commonFile(nodes, 'arithmetic')
        if 'Mac:' in nodes['Intrinsic_Type']: commonFile(nodes, 'mac')
        if 'Reduction:' in nodes['Intrinsic_Type']: commonFile(nodes, 'reduction')
        if 'Permutation:' in nodes['Intrinsic_Type']: commonFile(nodes, 'permutation')
        if 'Conversion:' in nodes['Intrinsic_Type']: commonFile(nodes, 'conversion')
