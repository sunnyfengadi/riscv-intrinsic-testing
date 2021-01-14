####################################################################################
#TestRunner.py 
####################################################################################
import os,sys
import re,subprocess
import platform
import datetime,time
import shutil
import json
import csv
from optparse import OptionParser
from subprocess import Popen, PIPE
from easyprocess import EasyProcess
from source.typeMap import TYPE_MAP

#####################################################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join( ROOT_DIR, 'test','log' )
ELF_PATH = os.path.join( ROOT_DIR,'test', 'elf' )
BIN_PATH = os.path.join(ROOT_DIR, 'bin', 'test')
TEST_PATH = os.path.join(ROOT_DIR, 'test')

JSON_PATH = os.path.join( ROOT_DIR, 'scripts', 'intrinsic_table.json' )
RESULT_CSV = os.path.join( ROOT_DIR, 'scripts', 'intrinsic_testing.csv' )

sys.path.append(ROOT_DIR)

def cleanWorkspace(path):
    for file in os.listdir(path):
        if '.c' in file:
            os.remove(os.path.join(path, file))

def copyAction( src, dst, filename ):
    srcFile = os.path.join( src, filename )
    if os.path.isfile(srcFile):
        shutil.copy( srcFile , os.path.normpath( dst ) )
    else:
        raise Exception("No this source file")

def writeResult(file, result, apitype):
    with open(file, 'a+') as f:
        f.write("Test API=%s" %apitype + '\n')
        f.write('-'*20 + '\n')
        f.write("Total test api: %d" %result['total'] +'\n')
        f.write("Pass number: %d" %result['pass'] +'\n')
        f.write("Fail number: %d" %result['fail'] +'\n')
        if result['fail_api_name']:
            f.write("Fail API name: %s" %result['fail_api_name'] +'\n') 
        f.write('\n')
    f.close()
        
def runTest(apitype, apiname):
    testResult = ''
    # create folder and clean the older file of log and elf
    if not os.path.exists(os.path.join( LOG_PATH, apitype ) ): 
        os.mkdir( os.path.join( LOG_PATH, apitype ) )
    testLog = os.path.join(LOG_PATH, apitype, apiname+'.txt')
    if os.path.exists(testLog): os.remove(testLog)

    if not os.path.exists(os.path.join( ELF_PATH, apitype) ): 
        os.mkdir( os.path.join( ELF_PATH, apitype ) )
    elfFile = os.path.join(BIN_PATH, apiname+'.elf')
    if os.path.exists(elfFile): os.remove(elfFile)

    # run source and make
    os.system("sh scripts/env.sh")
    p = EasyProcess(['make', 'app='+apiname]).call(timeout=10)
    
    if 'PASSED' in p.stderr: 
        if os.path.exists(os.path.join(BIN_PATH, apiname +'.elf')):
            copyAction(BIN_PATH, os.path.join( ELF_PATH, apitype), apiname +'.elf')
        if 'result={' in p.stdout:
            testResult = 'test pass'
            stdout=p.stderr+'\n'+ '='*70 + '\n' +p.stdout
            f= open(testLog, 'w')
            f.write(stdout)
            f.close()
        else:
            testResult = 'build pass'
    else:
        testResult = 'build fail'
    
    return testResult

def getResult(file):
    data = ''
    result = ''
    with open(file, 'r') as f:
        lines= f.readlines()
        for line in lines:
            if 'result={' in line:
                data = line.split('=',1)[1].replace('\n', '').replace('\r', '')
        status = lines[-1].replace('\n', '').replace('\r', '').replace('!', '')
    return data, status
           
def TestRunner(type, path, apitype):
    totalNum = 0
    passNum = 0
    failNum = 0
    failApi = []
    subResult = {}
    # run shell scripts to get the test logs
    if type == 'test':
        srcDir = os.path.join(path, apitype)
        for file in os.listdir(srcDir):
            totalNum += 1 
            cleanWorkspace(TEST_PATH)
            copyAction(srcDir, TEST_PATH, file)
            result = runTest(apitype, file.split('.')[0])
            if 'test pass' in result: 
                passNum += 1
            else: 
                failNum += 1
                failApi.append(file)
            os.remove(os.path.join(TEST_PATH, file))
        
    # parse test results from logs into Json 
    if type == 'parse':
        rootNode={}
        valueList = []
        logDir = os.path.join(path, apitype) 
        
        jsonFile = open(JSON_PATH, "r",encoding='utf-8')
        csvFile = open(RESULT_CSV, "w",encoding='utf-8',newline='')
        rootNode = json.load(jsonFile)
        writer = csv.writer(csvFile)
        
        writer.writerow(rootNode[0].keys())
        for nodes in rootNode:
            if apitype == 'all':  # for all, 遍历文件夹/test/log 找到该api的.txt
                for parent,dirnames,files in os.walk(path):
                    for file in files:
                        if file == nodes['Intrinsic_Name'].strip() + '.txt':
                            totalNum += 1
                            logfile = os.path.join(parent,file)
                            testData, testStatus = getResult( logfile )
                            nodes['Testing_Result'] = testData
                            nodes['Testing_Status'] = testStatus
                        else: 
                            failApi.append(nodes['Intrinsic_Name'])
                
            else: # for apitype, to find this log file under /test/log/apitype
                if nodes['Intrinsic_Type'] in TYPE_MAP[apitype] and '64' not in nodes['Intrinsic_Name']: # big issue for 64bit
                    totalNum += 1
                    logfile = os.path.join( logDir, nodes['Intrinsic_Name'].strip() + '.txt' )
                    if os.path.exists(logfile): 
                        testData, testStatus = getResult( logfile )
                        nodes['Testing_Result'] = testData
                        nodes['Testing_Status'] = testStatus
                        passNum += 1
                    else: 
                        failNum += 1
                        failApi.append(nodes['Intrinsic_Name'])
            
            valueList.append(nodes.values())
            
        writer.writerows(valueList)
        csvFile.close()
        
    subResult['total']= totalNum
    subResult['pass'] = passNum
    subResult['fail'] = failNum
    subResult['fail_api_name'] = failApi
    return subResult
    
###########################################################################################
# Main
# python3 TestRunner.py -t load   # or '-t all' that is for all apis 
# python3 TestRunner.py -p load 
###########################################################################################
def main():
    parser=OptionParser()
    parser.add_option("-t","--test",help="test api file with different type",dest="test",default='')
    parser.add_option("-p","--parse",help="parse result and fill json",dest="parse",default='')
    (options,args)=parser.parse_args()  
    testApi = options.test
    parseApi = options.parse

    if testApi:
        resultAll = {'total': 0, 'pass':0, 'fail':0}
        libPath = os.path.join(ROOT_DIR, 'source-file', 'lib')
        resultFile = os.path.join(TEST_PATH,'test_result.txt')
        if os.path.exists(resultFile): os.remove(resultFile)

        if testApi == 'all':
            folder = os.listdir(libPath)
            for apiType in folder: 
                result = TestRunner('test', libPath, apiType)
                writeResult(resultFile, result, apiType)

                for key,value in result.items():
                    if key in resultAll:
                        resultAll[key]+=value
            resultAll['fail_api_name'] = ''
            writeResult(resultFile, resultAll, "Summary of all")
        else: 
            result = TestRunner('test', libPath, testApi)
            writeResult(resultFile, result, testApi)
    else: pass
    
    if parseApi:
        resultAll = {'total': 0, 'pass':0, 'fail':0}
        logPath = os.path.join(ROOT_DIR, 'test', 'log')
        resultFile = os.path.join(TEST_PATH,'parse_result.txt')
        if os.path.exists(resultFile): os.remove(resultFile)
        
        result = TestRunner('parse', logPath, parseApi)
        writeResult(resultFile, result, parseApi)
    else: pass
    
if __name__ == "__main__":  
    main() 