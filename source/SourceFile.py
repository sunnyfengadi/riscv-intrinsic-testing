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

def loadStoreFile(node, apiName, ldstApis):
    parameters={}
    apiFile = copyFile('template_head.c', 'load_store', apiName)
    DataInitLines = ['']
    runLines = []

    comboNum = re.findall(r"\d+\.?\d*", apiName)[0]
    ret = re.match('vg?(ld)?s?(st)?cb[1-8](in0)?_v_[iu][136][624]_m$',apiName)
    if ret:
        typeBit = re.sub("\D", "", apiName.split( '_' )[-2])
    else:
        typeBit = re.sub("\D", "", apiName.split( '_' )[-1])

    elementNum = 512//int(typeBit)

    MacroLines = SetMacro(typeBit, elementNum, comboNum, 'load_store')
    DataInitDefinitionLines = SetDataInitDefinition('load_store')
    goldenLines = SetLoadStoreGoldenFunction(apiName, typeBit, elementNum, comboNum, 'load_store')
    paraLines = getLoadStoreInputParameters(ldstApis, typeBit, elementNum, comboNum)
    data_init_str = 'data_init(exp_base, exp_base, PAGE_NUM, '
    if (typeBit == '8'):  data_init_str += '0xff);'
    elif (typeBit == '16'):  data_init_str += '0xffff);'
    elif (typeBit == '32'):  data_init_str += '0xffffffff);'
    elif (typeBit == '64'):  data_init_str += '0xffffffffffffffff);'
    else: data_init_str += ');'
    DataInitLines.append(data_init_str)

    data_init_str = 'data_init(index, exp_index, ELE_NUM, '
    if (comboNum == '1'):
        data_init_str += 'PAGE_NUM / 2);'
    else:
        data_init_str += 'PAGE_NUM / BYTE_NUM / 2);\n'
        data_init_str += '\tdata_init_scalar(combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);'
    DataInitLines.append(data_init_str)

    DataInitLines.append('for (int i = 0; i < ELE_NUM; i++)\n\
        index[i] = index[i] * BYTE_NUM;')

    if (comboNum != '1'):
        DataInitLines.append('vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);')

    rungoldenLines = ['','//Get golden result']
    runIntrinsicLines = ['','//Get Intrinsic result']
    goldenStr = ''

    # Get golden result
    if (comboNum != '1'):
        goldenStr += apiName + '_golden((combo_stride * BYTE_NUM + VLEN) / BYTE_NUM,'
    else:
        goldenStr += apiName + '_golden('

    IntrinsicStr = 'tmp_result = ' + ldstApis[2] + '('
    if 'm' in ldstApis[0]:
        goldenStr += 'exp_mask,'
        IntrinsicStr += 'mask,'

    goldenStr += 'exp_base, exp_index, exp_result);'
    IntrinsicStr += 'exp_base,index);'

    rungoldenLines.append(goldenStr)
    runIntrinsicLines.append(IntrinsicStr)

    # Get Intrinsic result
    runIntrinsicLines.append('\n\
    data_init_scalar(element_stride, element_stride, PAGE_NUM / BYTE_NUM / 2);\n\
    data_init_scalar(group_stride, group_stride, PAGE_NUM / BYTE_NUM / 2);')

    if (comboNum != '1'):
        runIntrinsicLines.append('data_init_scalar (combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);')

    runIntrinsicLines.append('vwr_csr(RUGRATS_VMELEMENTSTRIDE, BYTE_NUM*element_stride);\n\
    vwr_csr(RUGRATS_VMGROUPSTRIDE, BYTE_NUM*group_stride);\n\
    vwr_csr(RUGRATS_VMGROUPNUMBER, VLEN / GROUP_DEPTH);\n\
    vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);\n')

    if (comboNum != '1'):
        runIntrinsicLines.append('vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);')

    # tmp2_result = vldcb1in0_v_i16(base,NORMAL);
    storetmp_result = ldstApis[1] + '('
    ldtmp2_result = 'tmp2_result = ' + ldstApis[0] + '('
    storetmp2_result = ldstApis[3] + '('
    ldbase2 = 'result = ' + ldstApis[2] + '('

    if 'm' in ldstApis[0]:
        storetmp_result += 'mask, '
        ldtmp2_result += 'mask, '
        storetmp2_result += 'mask, '
        ldbase2 += 'mask, '

    runIntrinsicLines.append(storetmp_result + 'base, tmp_result, NORMAL);')
    runIntrinsicLines.append(ldtmp2_result + 'base, NORMAL);')
    if (comboNum != '1'):
        runIntrinsicLines.append('data_init_scalar (combo_stride, combo_stride, PAGE_NUM / BYTE_NUM / 2);\n\
    vwr_csr(RUGRATS_VMCOMBOSTRIDE, combo_stride * BYTE_NUM + VLEN);')

    runIntrinsicLines.append(storetmp2_result + 'base2, index, tmp2_result);')
    runIntrinsicLines.append(ldbase2 + 'base2,index);')

    goldenLines = MacroLines + DataInitDefinitionLines + goldenLines
    paraLines += DataInitLines + rungoldenLines + runIntrinsicLines

    # for item in INTRINSIC_TYPE_MAP.items():
    #     ret = re.match(item[0],node['Intrinsic_Name'])
    #     if ret:
    if comboNum != '1':
        tailFile = 'common_tail_x.c'
    else: tailFile = 'common_tail_1.c'

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
    
    MacroLines = SetMacro(typeBit, elementNum, comboNum, 'iir')
    DataInitDefinitionLines = SetDataInitDefinition('iir')
    goldenLines = SetGoldenFunction(node, '', elementNum, typeBit, 'iir')
    paraLines = getInputParameters(parameters, elementNum, comboNum, 'iir')
    resultLine = SetResultLine(node,typeBit,'iir')
    DataInitLines = DataInit(node,parameters,'',typeBit, elementNum, 'iir')
    vwrcsrLines = getVwrCsr()
    runLines = getRunlines(parameters, apiName, elementNum, 'iir')

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
    DataInitDefinitionLines = SetDataInitDefinition(apitype)
    paraLines = getInputParameters(parameters, elementNum, comboNum, apitype)
    if (apitype == 'compare'):
        for i in range(1,8):
            if parameters['Input_'+str(i)+'_Type']:
                if (parameters['Input_'+ str(i)+'_Variable'] == 'a'):
                    out_datatype = parameters['Input_'+str(i)+'_Type']
                    out_exp_datatype = parameters['Input_'+str(i)+'_Type'].split('x')[0] + '_t'
        resultLine = [out_datatype + ' result = {0};']
        resultLine += [out_exp_datatype + ' exp_result[ELE_NUM] = {0};']

        DataInitLines = DataInit(node,parameters,'',typeBit,elementNum, apitype)
        if (typeBit == '16'):
            DataInitLines += ['data_init(c, exp_c, 32, 0xffff);']
            DataInitLines += ['data_init(d, exp_d, 32, 0xffff);']
        elif (typeBit == '32'):
            DataInitLines += ['data_init(c, exp_c, 16, 0xffffffff);']
            DataInitLines += ['data_init(d, exp_d, 16, 0xffffffff);']
        elif (typeBit == '64'):
            DataInitLines += ['data_init(c, exp_c, 8, 0xffffffffffffffff);']
            DataInitLines += ['data_init(d, exp_d, 8, 0xffffffffffffffff);']

        goldenLines = SetCompareGoldenFunction(node, apiName, elementNum, typeBit, apitype)

    else:
        goldenLines = SetGoldenFunction(node, '', elementNum, typeBit, apitype)
        resultLine = SetResultLine(node,typeBit,apitype)
        DataInitLines = DataInit(node,parameters,'',typeBit,elementNum, apitype)
    
    runLines = getRunlines(parameters, apiName, elementNum, apitype)
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

    relist = getrelist(rootNode)
    for nodes in rootNode:
        #for apis that have combo num: 1-8, others is 1 
        if 'Load:' in nodes['Intrinsic_Type'] or 'Store:' in nodes['Intrinsic_Type']:
            for fileName,ldstApis in relist.items():
                loadStoreFile(nodes, fileName, ldstApis)
        # if 'Store:' in nodes['Intrinsic_Type'] and 'Interleave' not in nodes['Intrinsic_Type']: storeFile(nodes)
        if 'IIR:' in nodes['Intrinsic_Type']: iirFile(nodes)
            
        #for logic, shift, move, compare that have bool type
        if 'Compare:' in nodes['Intrinsic_Type']: commonFile(nodes, 'compare')
        if 'Logic:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']: commonFile(nodes, 'logic')
        if 'Shift:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type'] and '64' not in nodes['Intrinsic_Name']: commonFile(nodes, 'shift')
        if 'Move:' in nodes['Intrinsic_Type'] and 'bool' not in nodes['Output_Type']: commonFile(nodes, 'move')
        
        #for arithmetic, mac, reduction, permutation, conversion
        if 'Arithmetic:' in nodes['Intrinsic_Type'] and '64' not in nodes['Intrinsic_Name']: commonFile(nodes, 'arithmetic')
        if 'Mac:' in nodes['Intrinsic_Type'] and '64' not in nodes['Output_Type']: commonFile(nodes, 'mac')
        if 'Reduction:' in nodes['Intrinsic_Type']: commonFile(nodes, 'reduction')
        if 'Permutation:' in nodes['Intrinsic_Type']: commonFile(nodes, 'permutation')
        if 'Conversion:' in nodes['Intrinsic_Type']: commonFile(nodes, 'conversion')
