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

def getInputParameters(inputDict, elementnum, combonum):
    inputList = ['int error = 0;']
    expInput = []
    for i in range(1,8):
        if inputDict['Input_'+str(i)+'_Type']:
            if 'base' in inputDict['Input_'+str(i)+'_Variable']:
                Input_Variable = inputDict['Input_'+ str(i)+'_Variable'].strip( ']' ) +'ELE_NUM*COMBO_NUM];' #base[ELE_NUM]
                inputList.append(inputDict['Input_'+str(i)+'_Type'] + ' ' + Input_Variable)
            else:
                inputList.append(inputDict['Input_'+str(i)+'_Type'] +\
                            ' '+ inputDict['Input_'+ str(i)+'_Variable'].rstrip()+';')

            split_input = inputDict['Input_'+str(i)+'_Type'].split('x')
            if 'bool' in inputDict['Input_'+str(i)+'_Type']: #bool8_t bool8x2_t
                eleNum = re.sub("\D", "", split_input[0])
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
                        expInputLine += '[' + str(eleNum)+'*'+str(comboNum) +'];'
            expInput.append(expInputLine)

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
        if 'imm' == variable:
            if apitype == 'load':
                variable = '8'  #now imm is fixed as 8 since Risc-v issue
            else:
                variable = '0'  #now imm is fixed as 0 since Risc-v issue
        apiInput += variable + ','

    expRun = ['','//Get golden result']
    expRun.append(functionName + '_golden(' + expInput + 'exp_result);')

    apiRun = ['','//Get Intrinsic result']
    if apitype == 'store':
        apiRun.append(functionName + '(' + apiInput.strip( ',' ) + ');')
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

    lines.append('#define ELE_NUM ' + elenum)
    if (combonum != 1):
        lines.append('#define COMBO_NUM ' + str(combonum))

    if apitype == 'load' or apitype == 'store' or apitype == 'iir':
        lines.append('#define ELE_WIDTH ' + str(element_width))
        lines.append('#define GROUP_NUM ' + str(group_num))
        lines.append('#define GROUP_DEPTH ' + str(group_depth))
        lines.append('#define ELE_STRIDE ' + str(element_stride))
        lines.append('#define COMBO_STRIDE ' + str(combo_stride))
        lines.append('#define GROUP_STRIDE ' + str(group_stride))

    lines.append('')

    return lines

def SetDataInitDefinition():
    lines = []
    lines.append(' \
#define random(threshold) rand()%threshold \n \
//#define data_init_bool(a, b, n, threshold) \\ \n \
    //	a = b = 1; \n \
#define data_init_scalar(a, b, threshold) \\ \n \
    a = b = random(threshold); \n \
#define data_init(a, b, n, threshold) \\ \n \
    for(int i = 0; i < n; i++) { \\ \n \
            a[i] = random(threshold); \\ \n \
            b[i] = a[i]; \\ \n \
        }')
    
    lines.append('')

    return lines

def SetResultLine(node,typebit):
    lines = ['']

    #int16_t exp_result[ELE_NUM] = {0};
    split_output = node['Output_Type'].split('x')
    if 'void' in node['Output_Type']: pass #void
    else:
        if 'bool' in node['Output_Type']: #bool8_t bool8x2_t
            eleNum = re.sub("\D", "", split_output[0])
            if (len(split_output) == 1): #bool8_t
                expResultLine = 'uint'+ typebit + '_t' + ' exp_result['+str(eleNum)+'] = {0};'
            elif (len(split_output) == 2): #bool8x2_t
                comboNum = re.sub("\D", "", split_output[1])
                expResultLine = 'uint'+ typebit + '_t' + ' exp_result['+str(eleNum)+'*'+str(comboNum) +'] = {0};'
        else:
            if (len(split_output) == 1): # int16_t int32_t
                expResultLine = node['Output_Type'] + ' exp_result;'
            elif (len(split_output) == 2): # int16x32_t int16x32_t
                eleNum = re.sub("\D", "", split_output[1])
                expResultLine = split_output[0] + '_t' + ' exp_result['+str(eleNum)+'] = {0};'
            elif (len(split_output) == 3): # int16x32x2_t int16x32x3_t
                eleNum = re.sub("\D", "", split_output[1])
                comboNum = re.sub("\D", "", split_output[2])
                expResultLine = split_output[0] + '_t' + ' exp_result['+str(eleNum)+'*'+str(comboNum) +'] = {0};'

        lines.append(node['Output_Type'] + ' result = {0};')
        lines.append(expResultLine)

    return lines

def DataInit(node,inputDict,typebit,apitype):
    dataInit = ['']
    for i in range(1,8):
        if inputDict['Input_'+str(i)+'_Type']:
            split_input = inputDict['Input_'+str(i)+'_Type'].split('x')
            if 'bool' in inputDict['Input_'+str(i)+'_Type']: #bool8_t bool8x2_t
                eleNum = re.sub("\D", "", split_input[0])
                data_init_str = 'data_init_bool('+ \
                                inputDict['Input_'+str(i)+'_Variable']+ \
                                ', exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip()
                if (len(split_input) == 1): #bool8_t
                    data_init_str += ', '+ str(eleNum)
                elif (len(split_input) == 2): #bool8x2_t
                    comboNum = re.sub("\D", "", split_input[1])
                    data_init_str += ', '+ str(eleNum)+'*'+str(comboNum)
            else:
                if (len(split_input) == 1): #int8_t
                    typebit = re.sub("\D", "", split_input[0])
                    if 'imm' in inputDict['Input_'+str(i)+'_Variable']:
                        if apitype == 'load':
                            data_init_str = 'imm = exp_imm = 8; // imm and exp_imm do not need to call data_init'
                        else:
                            data_init_str = 'imm = exp_imm = 0; // imm and exp_imm do not need to call data_init'
                    elif 'base' in inputDict['Input_'+str(i)+'_Variable']:
                        if apitype == 'store':
                            data_init_str = '//base here is output, do not need to call data_init'
                        else: data_init_str = 'data_init(base, exp_base, ELE_NUM*COMBO_NUM'
                    else:
                        ret = re.match('vmv_x_v_[iu][13][62]_?m?',node['Intrinsic_Name'])
                        if ret:
                            data_init_str = 'b = exp_b = rand()%16 // b and exp_b should be in the range[0,16)'
                        else:
                            data_init_str = 'data_init_scalar(' + \
                                    inputDict['Input_'+str(i)+'_Variable'] + \
                                    ', exp_'+ inputDict['Input_'+ str(i)+'_Variable'].rstrip()
                else: #int32x16_t int32x16x2_t
                    typebit = re.sub("\D", "", split_input[0])
                    eleNum = re.sub("\D", "", split_input[1])
                    data_init_str = 'data_init(' + \
                                    inputDict['Input_'+str(i)+'_Variable']+ \
                                    ', exp_'+inputDict['Input_'+ str(i)+'_Variable'].rstrip()
                    if (len(split_input) == 2): # int16x32_t int16x32_t
                        data_init_str += ', '+ str(eleNum)
                    elif(len(split_input) == 3): # int16x32x2_t int16x32x2_t
                        comboNum = re.sub("\D", "", split_input[2])
                        data_init_str += ', '+ str(eleNum)+'*'+str(comboNum)

            if (typebit == '8'):  data_init_str += ', 0xff);'
            elif (typebit == '16'):  data_init_str += ', 0xffff);'
            elif (typebit == '32'):  data_init_str += ', 0xffffffff);'
            elif (typebit == '64'):  data_init_str += ', 0xffffffffffffffff);'
            else: data_init_str += ');'

            dataInit.append(data_init_str)

    return dataInit