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

def accumwriteFile (sourceFile, goldenlines, lines):
    with open(sourceFile, 'a+') as f:
        for line in goldenlines:
            if line == '': f.write('\n')
            else: f.write(line + '\n' )
        for line in lines:
            if line == '': f.write('\n')
            else: f.write( '    ' + line + '\n' )

    f.close()

def writeFile (sourceFile, goldenlines, lines, tailfile):
    with open(sourceFile, 'a+') as f:
        for line in goldenlines:
            if line == '': f.write('\n')
            else: f.write(line + '\n' )
        for line in lines:
            if line == '': f.write('\n')
            else: f.write( '    ' + line + '\n' )

    # Write the file tail
    with open(os.path.join(TEMPLATE_PATH, tailfile),'r') as f:
        tailLines=f.readlines()
    with open(sourceFile,'a') as f:
            for line in tailLines:
                f.writelines(line)
    f.close()

def getLoadStoreInputParameters(ldstApis, typeBit, elementnum, combonum):
    inputList = ['int error = 0;']

    api0 = ldstApis[0].split( '_' )
    if (len(api0) == 3): #normal_test
        dataTypeSymbol = api0[-1]
    elif (len(api0) == 4): # mask_test
        dataTypeSymbol = api0[-2]

    if 'i' in dataTypeSymbol: dataType = 'int'
    elif 'u' in dataTypeSymbol: dataType = 'uint'

    scalar_dataType = dataType + str(typeBit) + '_t'
    index_scalar_dataType = 'int' + str(typeBit) + '_t'
    index_combo1_dataType = 'int'+ str(typeBit) + 'x' + str(elementnum) + '_t'
    combo1_dataType = dataType + str(typeBit) + 'x' + str(elementnum) + '_t'
    comboX_dataType = dataType + str(typeBit) + 'x' + str(elementnum) + 'x' + str(combonum) + '_t'

    inputList.append(scalar_dataType + ' base[PAGE_NUM];')
    inputList.append(scalar_dataType + ' base2[PAGE_NUM];')
    inputList.append(index_combo1_dataType + ' index;')

    if 'm' in ldstApis[0]:
        if (elementnum == 8):
            inputList.append('bool8_t mask = m8(0x100000101000001);\n')
            inputList.append('uint64_t exp_mask[ELE_NUM] ={1,0,0,1,1,0,0,1};')
        elif (elementnum == 16):
            inputList.append('bool16_t mask = m16(0x1101100000011011);\n')
            inputList.append('uint64_t exp_mask[ELE_NUM]={1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};')
        elif (elementnum == 32):
            inputList.append('bool32_t mask = m32(0x5140014551400145);\n')
            inputList.append('uint64_t exp_mask[ELE_NUM]={1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};')

    inputList.append(scalar_dataType + ' exp_base[PAGE_NUM];')
    inputList.append(index_scalar_dataType + ' exp_index[ELE_NUM];')

    inputList.append('\n\
    unsigned int element_stride;\n\
    unsigned int group_stride;')

    if (combonum == '1'):
        inputList.append('\n')
        inputList.append(combo1_dataType + ' result = {0};')
        inputList.append(combo1_dataType + ' tmp_result = {0};')
        inputList.append(combo1_dataType + ' tmp2_result = {0};')
        inputList.append(scalar_dataType + ' exp_result[ELE_NUM] = {0};')
    else:
        inputList.append('unsigned int combo_stride;\n')
        inputList.append(comboX_dataType + ' result = {0};')
        inputList.append(comboX_dataType + ' tmp_result = {0};')
        inputList.append(comboX_dataType + ' tmp2_result = {0};')
        inputList.append(scalar_dataType + ' exp_result[COMBO_NUM][ELE_NUM] = {0};')

    return inputList


def getAccumInputParameters(nodes):
    inputList = ['int error = 0;']
    for node in nodes:
        for i in range(1,8):
            inputType = node['Input_'+str(i)+'_Type']
            inputVariable = node['Input_'+str(i)+'_Variable']
            if inputType:
                if inputType == 'bool8_t':
                    inputStr = 'bool8_t ' + inputVariable +' = m8(0x100000101000001);'
                elif inputType == 'bool16_t':
                    inputStr = 'bool16_t ' + inputVariable +' = m16(0x1101100000011011);'
                elif inputType == 'bool32_t':
                    inputStr = 'bool32_t ' + inputVariable +' = m32(0x5140014551400145);'
                elif inputType == 'enum ACCUM': pass
                else:
                    inputStr = inputType +' '+ inputVariable +';'

                if inputStr not in inputList:
                    inputList.append(inputStr)

    return inputList

def getAccumExpInputParameters(nodes):
    expInput = ['']
    for node in nodes:
        for i in range(1,8):
            inputType = node['Input_'+str(i)+'_Type']
            inputVariable = node['Input_'+str(i)+'_Variable']
            if inputType:
                if 'bool' in inputType: pass
                elif 'enum' in inputType: pass
                else:
                    split_input = inputType.split('x')
                    if (len(split_input) == 1): ## int16_t
                        typebit = re.sub("\D", "", split_input[0])
                        expInputLine = inputType +' exp_'+ inputVariable.rstrip()+';'
                    else:
                        typebit = re.sub("\D", "", split_input[0])
                        eleNum = re.sub("\D", "", split_input[1])
                        expinputType = split_input[0] + '_t'
                        expInputLine = expinputType +' exp_'+inputVariable.rstrip()
                        if (len(split_input) == 2): # int16x32_t int16x32_t
                            expInputLine += '[' + str(eleNum)+'];'
                        elif(len(split_input) == 3): # int16x32x2_t int16x32x2_t
                            comboNum = re.sub("\D", "", split_input[2])
                            expInputLine += '[' + str(comboNum) +'][' + str(eleNum)+ '];'
                if expInputLine not in expInput:
                    expInput.append(expInputLine)
    return expInput

def getInputParameters(inputDict, elementnum, combonum, apiType):
    inputList = ['int error = 0;']
    expInput = []
    for i in range(1,8):
        if inputDict['Input_'+str(i)+'_Type']:
            if (apiType == 'compare'):
                if (inputDict['Input_'+ str(i)+'_Variable'] == 'a'):
                    compare_in_datatype = inputDict['Input_'+str(i)+'_Type']
                    compare_exp_datatype = inputDict['Input_'+str(i)+'_Type'].split('x')[0] + '_t'
                    compare_exp_eleNum = re.sub("\D", "", inputDict['Input_'+str(i)+'_Type'].split('x')[1])
    for i in range(1,8):
        if inputDict['Input_'+str(i)+'_Type']:
            if 'base' in inputDict['Input_'+str(i)+'_Variable']:
                Input_Variable = inputDict['Input_'+ str(i)+'_Variable'].strip( ']' ) +'ELE_NUM*COMBO_NUM];' #base[ELE_NUM]
                inputList.append(inputDict['Input_'+str(i)+'_Type'] + ' ' + Input_Variable)
            else:
                if 'mask' in inputDict['Input_'+str(i)+'_Variable']:
                    if (elementnum == '8'):
                        inputList.append('bool8_t mask = m8(0x100000101000001);')
                    elif (elementnum == '16'):
                        inputList.append('bool16_t mask = m16(0x1101100000011011);')
                    elif (elementnum == '32'):
                        inputList.append('bool32_t mask = m32(0x5140014551400145);')
                else:
                    inputList.append(inputDict['Input_'+str(i)+'_Type'] +\
                            ' '+ inputDict['Input_'+ str(i)+'_Variable'].rstrip()+';')
                if (apiType == 'compare'):
                    if (inputDict['Input_'+ str(i)+'_Variable'] == 'b'):
                        inputList.append(compare_in_datatype + ' c;')
                        inputList.append(compare_in_datatype + ' d;')
            split_input = inputDict['Input_'+str(i)+'_Type'].split('x')
            if 'bool' in inputDict['Input_'+str(i)+'_Type']: #bool8_t bool8x2_t
                eleNum = re.sub("\D", "", split_input[0])
                if (inputDict['Input_'+str(i)+'_Variable'] == 'mask') and (apiType == 'compare'):
                    if (elementnum == '8'):
                        expInputLine = 'uint64_t exp_mask[ELE_NUM] = {1,0,0,1,1,0,0,1};'
                    elif (elementnum == '16'):
                        expInputLine = 'uint64_t exp_mask[ELE_NUM] = {1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};'
                    elif (elementnum == '32'):
                        expInputLine = 'uint64_t exp_mask[ELE_NUM] = {1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,1,1};'
                else:
                    expInputLine = 'uint64_t exp_'+ inputDict['Input_'+str(i)+'_Variable']
                    if (len(split_input) == 1): #bool8_t
                        expInputLine += '[' + str(eleNum)+'];'
                    elif (len(split_input) == 2): #bool8x2_t
                        comboNum = re.sub("\D", "", split_input[1])
                        expInputLine += '[' + str(eleNum)+'*'+str(comboNum)+'];'
            else:
                if (len(split_input) == 1): ## int16_t
                    typebit = re.sub("\D", "", split_input[0])
                    inputType = inputDict['Input_'+str(i)+'_Type']

                    if 'base' in inputDict['Input_'+str(i)+'_Variable']:
                        Input_Variable = inputDict['Input_'+ str(i)+'_Variable'].strip( ']' ) +'ELE_NUM*COMBO_NUM];' #base[ELE_NUM]
                        expInputLine = inputType +' exp_'+ Input_Variable
                    else:
                        expInputLine = inputType +' exp_'+ inputDict['Input_'+ str(i)+'_Variable'].rstrip()+';'
                else:
                    typebit = re.sub("\D", "", split_input[0])
                    eleNum = re.sub("\D", "", split_input[1])
                    inputType = split_input[0] + '_t'
                    expInputLine = inputType +' exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip()
                    if (len(split_input) == 2): # int16x32_t int16x32_t
                        expInputLine += '[' + str(eleNum)+'];'
                    elif(len(split_input) == 3): # int16x32x2_t int16x32x2_t
                        comboNum = re.sub("\D", "", split_input[2])
                        expInputLine += '[' + str(comboNum) +'][' + str(eleNum)+ '];'
            expInput.append(expInputLine)
            if (apiType == 'compare'):
                if (inputDict['Input_'+ str(i)+'_Variable'] == 'b'):
                    expInput.append(compare_exp_datatype + ' exp_c[' + str(compare_exp_eleNum)+'];')
                    expInput.append(compare_exp_datatype + ' exp_d[' + str(compare_exp_eleNum)+'];')
    return inputList + expInput

def getAccumRunlines(nodes, apiTotalNum, accumNum, accumNum1, accumNum2):
    apiRun = ['','//Get Intrinsic result']

    for i,node in enumerate(nodes):
        Variables = ''

        if 'accum' in node['Intrinsic_Name']:
            functionName = node['Intrinsic_Name'].replace('[07][07][07]',str(accumNum)+str(accumNum1)+str(accumNum2))
        else:
            functionName = node['Intrinsic_Name']

        apiRunStr = ''
        if i == apiTotalNum-1:
            apiRunStr += 'final_'
        apiRunStr += 'result' + str(accumNum)
        if 'accum' in node['Intrinsic_Name']:
            apiRunStr += str(accumNum1) + str(accumNum2)
        apiRunStr += ' = ' + functionName + '('
        for i in range(1,8):
            inputType = node['Input_'+str(i)+'_Type']
            inputVar = node['Input_'+str(i)+'_Variable']
            if inputType:
                if 'accum' in node['Intrinsic_Name']:
                    Variables += inputVar + ', '
                else:
                    if 'accum' in inputVar:
                        Variables += 'ACCUM' + str(accumNum)
                    else: 
                        if 'Shift' in node['Intrinsic_Type']:
                            if '_ax_' in node['Intrinsic_Name']:
                                if inputVar == 'b':
                                    inputVar = 'b1'
                            elif '_ai_' in node['Intrinsic_Name'] or '_i_' in node['Intrinsic_Name']:
                                if inputVar == 'imm':
                                    inputVar = '8'

                        Variables += inputVar + ', '

        apiRunStr += Variables.strip( ', ' ) + ');'
        apiRun.append(apiRunStr)
    newapiRun = '*'.join(apiRun)
    if 'accum' in node['Intrinsic_Name']:
        newapiRun2 = newapiRun.replace('a,','bak,',1).replace('a,','result'+ str(accumNum) +str(accumNum1) + str(accumNum2)+',').replace('bak,','a,')
    else:
        newapiRun2 = newapiRun.replace('a,','bak,',1).replace('a,','result'+ str(accumNum) +',').replace('bak,','a,')
    apiRun = newapiRun2.split('*')
    return apiRun

def getRunlines(inputDict, functionName, eleNum, apitype):
    variableList = []
    apiInput = ''
    expInput = ''
    
    for item in inputDict.items():
        if item[0].split( '_' )[2] == 'Variable' and item[1]:
            variableList.append(item[1].strip( '[]' ))  #need remove the '[]' in 'base[]'
    for variable in variableList:
        expInput += 'exp_' + variable + ','
        if 'imm' == variable:
            if apitype == 'load':
                variable = '8'  #now imm is fixed as 8 since Risc-v issue
            else:
                variable = '0'  #now imm is fixed as 0 since Risc-v issue
        apiInput += variable + ','
    if (apitype == 'compare'):
        expInput += ' exp_c, exp_d, '
    expRun = ['','//Get golden result']
    expRun.append(functionName + '_golden(' + expInput + 'exp_result);')

    apiRun = ['','//Get Intrinsic result']
    if apitype == 'store':
        apiRun.append(functionName + '(' + apiInput.strip( ',' ) + ');')
    elif (apitype == 'compare'):
        apiRun.append('bool' + str(eleNum) + '_t compare_result = ' + functionName + '(' + apiInput.strip( ',' ) + ');')
        ret = re.match('vcmp(eq)?(ge)?(gt)?(le)?(lt)?(ne)?_v[vx]_[iu][13][62]_m$',functionName)
        if ret:
            mergefunction = 'vmerge_vv_' + functionName.split('_')[-2]
        else:
            mergefunction = 'vmerge_vv_' + functionName.split('_')[-1]
        apiRun.append('result = ' + mergefunction + '(compare_result, c, d);')
    else:
        apiRun.append('result = ' + functionName + '(' + apiInput.strip( ',' ) + ');')
    
    return expRun + apiRun
    
def getVwrCsr ():
    lines = ['']

    lines.append('vwr_csr(RUGRATS_VMELEMENTSTRIDE, ELE_STRIDE);') #element_stride = combo_num * element_width
    lines.append('vwr_csr(RUGRATS_VMCOMBOSTRIDE, COMBO_STRIDE);')     #combo_stride = element_width
    lines.append('vwr_csr(RUGRATS_VMGROUPSTRIDE, GROUP_STRIDE);')     #group_stride = element_stride *N( N = 1,2,3... && N <= element_num_per_group), N=2
    lines.append('vwr_csr(RUGRATS_VMGROUPNUMBER, GROUP_NUM);')
    lines.append('vwr_csr(RUGRATS_VMGROUPDEPTH, GROUP_DEPTH);')       #group_depth = element_width *element_num_per_group (element_num_per_group = 4)
    
    return lines 

def SetMacro(typebit, elenum, combonum, apitype):
    lines = []
    #if 'Load:' in node
    element_width = int(typebit)//8
    element_stride = int(combonum) * element_width
    combo_stride = element_width
    group_stride = element_stride *2
    group_num = 4
    group_depth = element_width *group_num

    lines.append('#define ELE_NUM ' + str(elenum))
    if (combonum != 1):
        lines.append('#define COMBO_NUM ' + str(combonum))

    if apitype == 'load_store':
        lines.append('#define VLEN 64')
        lines.append('#define BYTE_NUM '+ str(element_width))
        lines.append('#define PAGE_NUM 4096')
        lines.append('#define ELE_WIDTH ' + str(element_width))
        lines.append('#define GROUP_NUM ' + str(group_num))
        lines.append('#define GROUP_DEPTH ' + str(group_depth))
        lines.append('#define ELE_STRIDE ' + str(element_stride))
        lines.append('#define COMBO_STRIDE ' + str(combo_stride))
        lines.append('#define GROUP_STRIDE ' + str(group_stride))

    lines.append('')

    return lines

def SetAccumDataInitDefinition():
    lines = []
    lines.append('\
#define random(threshold) rand()%threshold\n\
#define data_init_scalar(a, threshold) \\\n\
  a = random(threshold);\n\
#define data_init(a, n, threshold) \\\n\
  for(int i = 0; i < n; i++) { \\\n\
    a[i] = random(threshold); \\\n\
  }\n\
#define data_init_matrix(a, n, m, threshold) \\\n\
  for(int i = 0; i < m; i++) { \\\n\
    for(int j = 0; j < n; j++) { \\\n\
      a.val[i][j] = random(threshold); \\\n\
    } \\\n\
  }\n')

    return lines

def SetDataInitDefinition(apitype):
    lines = []
    lines.append('\
#define random(threshold) rand()%threshold\n\
//#define data_init_bool(a, b, n, threshold) \\\n\
//	a = b = 1;\n\
#define data_init_scalar(a, b, threshold) \\\n\
  a = b = random(threshold);\n\
#define data_init(a, b, n, threshold) \\\n\
  for(int i = 0; i < n; i++) { \\\n\
    a[i] = random(threshold); \\\n\
    b[i] = a[i]; \\\n\
  }\n')
    if apitype != 'load_store':
        lines.append('\
#define data_init_matrix(a, b, n, m, threshold) \\\n\
  for(int i = 0; i < m; i++) { \\\n\
    for(int j = 0; j < n; j++) { \\\n\
      a.val[i][j] = random(threshold); \\\n\
      b[i][j] = a.val[i][j]; \\\n\
    } \\\n\
  }\n')
    
    #lines.append('')

    return lines

def SetAccumResultLine(nodes, apiTotalNum, accumNum, accumNum1, accumNum2):
    lines = []

    for node in nodes:
        tmpResult = node['Output_Type'] + ' result' + str(accumNum)
        if 'accum' in node['Intrinsic_Name']:
                tmpResult += str(accumNum1) + str(accumNum2)
        tmpResult += ' = {0};'

        if tmpResult not in str(lines):
            lines.append(tmpResult)

    return lines

def SetResultLine(node,typebit, apitype):
    lines = ['']

    #int16_t exp_result[ELE_NUM] = {0};
    split_output = node['Output_Type'].split('x')
    if 'void' in node['Output_Type']: pass #void
    else:
        if 'bool' in node['Output_Type']: #bool8_t bool8x2_t
            eleNum = re.sub("\D", "", split_output[0])
            if (len(split_output) == 1): #bool8_t
                expResultLine = 'uint64_t' + ' exp_result['+str(eleNum)+'] = {0};'
            elif (len(split_output) == 2): #bool8x2_t
                comboNum = re.sub("\D", "", split_output[1])
                expResultLine = 'uint64_t' + ' exp_result['+str(comboNum)+']['+str(eleNum) +'] = {0};'
        else:
            if (len(split_output) == 1): # int16_t int32_t
                expResultLine = node['Output_Type'] + ' exp_result;'
            elif (len(split_output) == 2): # int16x32_t int16x32_t
                eleNum = re.sub("\D", "", split_output[1])
                expResultLine = split_output[0] + '_t' + ' exp_result['+str(eleNum)+'] = {0};'
            elif (len(split_output) == 3): # int16x32x2_t int16x32x3_t
                eleNum = re.sub("\D", "", split_output[1])
                comboNum = re.sub("\D", "", split_output[2])
                expResultLine = split_output[0] + '_t' + ' exp_result['+str(comboNum)+']['+str(eleNum) +'] = {0};'

        lines.append(node['Output_Type'] + ' result = {0};')
        lines.append(expResultLine)

    return lines

def AccumDataInit(nodes,typebit, eleNum, comboNum):
    dataInit = ['']
    for node in nodes:
        for i in range(1,8):
            inputType = node['Input_'+str(i)+'_Type']
            inputVariable = node['Input_'+ str(i)+'_Variable']
            if inputType:
                split_input = inputType.split('x')
                if 'bool' in inputType: pass #bool8_t bool8x2_t
                elif 'enum ACCUM' in inputType: pass
                else:
                    if (len(split_input) == 1): #int8_t
                        typebit = re.sub("\D", "", split_input[0])
                        if 'imm' in inputVariable:
                            if 'Load' in node['Intrinsic_Type']:
                                data_init_str = 'imm = 8; // imm do not need to call data_init'
                            elif 'Shift' in node['Intrinsic_Type']:
                                data_init_str = 'imm = rand()%' + str(eleNum)+'; // imm do not need to call data_init'
                            else:
                                data_init_str = 'imm = 0; // imm do not need to call data_init'
                        else:
                            data_init_str = 'data_init_scalar(' + \
                                        inputVariable.strip( ',' )
                    else: #int32x16_t int32x16x2_t
                        typebit = re.sub("\D", "", split_input[0])
                        eleNum = re.sub("\D", "", split_input[1])

                        if (len(split_input) == 2): # int16x32_t int16x32_t
                            data_init_str = 'data_init(' + \
                                            inputVariable + \
                                            ', ' + str(eleNum)
                        elif(len(split_input) == 3): # int16x32x2_t int16x32x2_t
                            comboNum = re.sub("\D", "", split_input[2])
                            data_init_str = 'data_init_matrix(' + \
                                            inputVariable + \
                                            ', ' + str(eleNum) +', '+str(comboNum)

                    if (typebit == '8'):  data_init_str += ', 0xff);'
                    elif (typebit == '16'):  data_init_str += ', 0xffff);'
                    elif (typebit == '32'):  data_init_str += ', 0xffffffff);'
                    elif (typebit == '64'):  data_init_str += ', 0xffffffffffffffff);'
                    else: data_init_str += ');'
                if data_init_str not in dataInit:
                    dataInit.append(data_init_str)

    return dataInit


def DataInit(node,inputDict,ldstApis,typebit,eleNum,apitype):
    dataInit = ['']

    for i in range(1,8):
        if inputDict['Input_'+str(i)+'_Type']:
            split_input = inputDict['Input_'+str(i)+'_Type'].split('x')
            if 'bool' in inputDict['Input_'+str(i)+'_Type']: pass#bool8_t bool8x2_t
            else:
                if (len(split_input) == 1): #int8_t
                    typebit = re.sub("\D", "", split_input[0])
                    if 'imm' in inputDict['Input_'+str(i)+'_Variable']:
                        if apitype == 'load':
                            data_init_str = 'imm = exp_imm = 8; // imm and exp_imm do not need to call data_init'
                        elif apitype == 'shift':
                            data_init_str = 'imm = exp_imm = rand()%'+str(eleNum)+'; // imm and exp_imm do not need to call data_init'
                        else:
                            data_init_str = 'imm = exp_imm = 0; // imm and exp_imm do not need to call data_init'
                    elif 'base' in inputDict['Input_'+str(i)+'_Variable']:
                        if apitype == 'store':
                            data_init_str = '//base here is output, do not need to call data_init'
                        else: data_init_str = 'data_init(base, exp_base, ELE_NUM*COMBO_NUM'
                    else:
                        ret = re.match('vmv_x_v_[iu][13][62]_?m?',node['Intrinsic_Name'])
                        if ret:
                            data_init_str = 'b = exp_b = rand()%'+str(eleNum)+' // b and exp_b should be in the range[0,16)'
                        else:
                            data_init_str = 'data_init_scalar(' + \
                                    inputDict['Input_'+str(i)+'_Variable'] + \
                                    ', exp_'+ inputDict['Input_'+ str(i)+'_Variable'].rstrip()
                else: #int32x16_t int32x16x2_t
                    typebit = re.sub("\D", "", split_input[0])
                    eleNum = re.sub("\D", "", split_input[1])

                    if (len(split_input) == 2): # int16x32_t int16x32_t
                        data_init_str = 'data_init(' + \
                                        inputDict['Input_'+str(i)+'_Variable']+ \
                                        ', exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip() + \
                                        ', ' + str(eleNum)
                    elif(len(split_input) == 3): # int16x32x2_t int16x32x2_t
                        comboNum = re.sub("\D", "", split_input[2])
                        data_init_str = 'data_init_matrix(' + \
                                        inputDict['Input_'+str(i)+'_Variable']+ \
                                        ', exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip() + \
                                        ', ' + str(eleNum) +', '+str(comboNum)

                if (typebit == '8'):  data_init_str += ', 0xff);'
                elif (typebit == '16'):  data_init_str += ', 0xffff);'
                elif (typebit == '32'):  data_init_str += ', 0xffffffff);'
                elif (typebit == '64'):  data_init_str += ', 0xffffffffffffffff);'
                else: data_init_str += ');'

                dataInit.append(data_init_str)

    return dataInit


# Map api
# vldstcd1_v_i16 : vldcd1_v_i16, vstcd1_v_i16, vgldcd1_v_i16, vsstcd1_v_i16
# vldstcd1_v_i16_m : vldcd1_v_i16_m, vstcd1_v_i16_m, vgldcd1_v_i16_m, vsstcd1_v_i16_m
def getrelist(rootNode):
    redic = {}
    for node in rootNode:
        if 'Load:' in node['Intrinsic_Type'] or 'Store:' in node['Intrinsic_Type']:
            apiName = node['Intrinsic_Name'].rstrip()
            comboNum = re.findall(r"\d+\.?\d*", apiName)[0]
            split_api = apiName.split( '_' )

            ret = re.match('vg?(ld)?s?(st)?cb[1-8](in0)?_v_[iu][136][624]_m$',apiName)
            if ret:
                restring = 'vldstcb'+ comboNum + '_v_' + split_api[-2] + '_m'
            else:
                restring = 'vldstcb'+ comboNum + '_v_' +  split_api[-1]

            if restring not in redic:
                redic[restring] = []
            redic[restring].append(apiName)

    return redic

# {'Arithmetic': [{'ID': '5', ...}, {...},...],
#'Shift': [{'ID': '0', }, {},...]
#...}
def getaccumApi(rootNode):
    accumApi = []
    apiGroup = {}

    for nodes in rootNode:
        if 'accum' in nodes['Intrinsic_Name']:
            accumApi.append(nodes)
        for i in range(1,8):
            if 'accum' in nodes['Input_'+str(i)+'_Variable']:
                accumApi.append(nodes)

    for node in accumApi:
        apiName = node['Intrinsic_Type'].split(':')[0]
        if 'uint' in node['Output_Type']:
            apiName = str(apiName) + '_uint'
        else: apiName = str(apiName) + '_int'
        if apiName not in apiGroup:
            apiGroup[apiName] = []
        apiGroup[apiName].append(node)

    return apiGroup