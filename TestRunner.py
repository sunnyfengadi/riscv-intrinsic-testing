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
from source.SourceFile import *
from scripts.parseHtmlJson import *

#####################################################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join( ROOT_DIR, 'test','log' )
ELF_PATH = os.path.join( ROOT_DIR,'test', 'elf' )
BIN_PATH = os.path.join( ROOT_DIR, 'bin', 'test')
TEST_PATH = os.path.join( ROOT_DIR, 'test')

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
        f.write("Test Pass number: %d" %result['test_passed'] +'\n')
        f.write("Test Fail number: %d" %result['test_failed'] +'\n')
        f.write("Build Pass number: %d" %result['build_passed'] +'\n')
        f.write("Build Fail number: %d" %result['build_failed'] +'\n')
        if result['test_pass_api_name']:
            f.write("\nTest Passed API name: \n \t%s" %result['test_pass_api_name'] +'\n')
        if result['test_fail_api_name']:
            f.write("\nTest Failed API name: \n \t%s" %result['test_fail_api_name'] +'\n')
        if result['build_pass_api_name']:
            f.write("\nBuild Passed API name: \n \t%s" %result['build_pass_api_name'] +'\n')
        if result['build_fail_api_name']:
            f.write("\nBuild Failed API name: \n \t%s" %result['build_fail_api_name'] +'\n')
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

    stdout=p.stderr+'\n'+ '='*70 + '\n' +p.stdout
    f= open(testLog, 'w')
    f.write(stdout)
    f.close()
    if 'PASSED' in p.stderr: 
        if os.path.exists(os.path.join(BIN_PATH, apiname +'.elf')):
            copyAction(BIN_PATH, os.path.join( ELF_PATH, apitype), apiname +'.elf')
        if 'TEST PASSED' in p.stdout:
            testResult = 'test_passed'
        elif 'TEST FAILED' in p.stdout:
            testResult = 'test_failed'
        else:
            testResult = 'build_passed'
    else:
        testResult = 'build_failed'
    
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
           
def testRunner(type, path, apitype):
    totalNum = 0
    testpassNum = 0
    testfailNum = 0
    buildpassNum = 0
    buildfailNum = 0
    testpassApi = []
    testfailApi = []
    buildpassApi = []
    buildfailApi = []
    subResult = {}
    # run shell scripts to get the test logs
    if type == 'test':
        srcDir = os.path.join(path, apitype)
        for file in os.listdir(srcDir):
            totalNum += 1 
            cleanWorkspace(TEST_PATH)
            copyAction(srcDir, TEST_PATH, file)
            result = runTest(apitype, file.split('.')[0])
            if 'test_passed' in result:
                testpassNum += 1
                testpassApi.append(file)
            elif 'test_failed' in result:
                testfailNum += 1
                testfailApi.append(file)
            elif 'build_passed' in result:
                buildpassNum += 1
                buildpassApi.append(file)
            else:
                buildfailNum += 1
                buildfailApi.append(file)
            os.remove(os.path.join(TEST_PATH, file))

    if type == 'golden':
        pass

    # parse test results from logs into Json 
    if type == 'parser':
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
    subResult['test_passed'] = testpassNum
    subResult['test_failed'] = testfailNum
    subResult['build_passed'] = buildpassNum
    subResult['build_failed'] = buildfailNum
    subResult['test_pass_api_name'] = testpassApi
    subResult['test_fail_api_name'] = testfailApi
    subResult['build_pass_api_name'] = buildpassApi
    subResult['build_fail_api_name'] = buildfailApi

    return subResult
    
###########################################################################################
# Main
###########################################################################################
def main():
    parser=OptionParser()
    
    # options only for parse html and generate json used by source scripts
    parser.add_option('-f', '--function', dest='function', default='',
        help= "functions to parse html and generate json. it has four options: "
              " -f h2c, to transiton from html to csv "
              " -f c2j, to transiton from csv to json "
              " -f j2c, to transiton from json to csv "
              " -f fcsv, to formalize csv to insert ID and type ")
    
    # options only for source c file generation
    parser.add_option('-s', '--source', action='store_true', dest='source', default=False, 
        help="generate the source c file according to json. e.g. --source")
        
    # options only for both build/test and parse result
    parser.add_option('-t', '--test', dest='test', default='', 
        help="test api file with vector core. e.g. -t load, -t all")
    parser.add_option('-g', '--golden', dest='golden', default='',
        help="test api in golden file with scalar core. e.g. -g store, -g all")
    parser.add_option('-p', '--parser', dest='parser', default='',
        help="parse the expect result from golden and fill json. e.g. -p store, -p all")
        
    (options,args)=parser.parse_args()

    if options.function: functionHandler(options.function)
    if options.source: sourceHandler(options.source)
    if options.test:
        resultAll = {'total': 0, 'test_passed':0, 'test_failed':0, 'build_passed':0, 'build_failed':0}
        libPath = os.path.join(ROOT_DIR, 'source', 'lib')
        resultFile = os.path.join(TEST_PATH,'test_result.txt')
        if os.path.exists(resultFile): os.remove(resultFile)
        if options.test == 'all':
            folder = os.listdir(libPath)
            for apiType in folder: 
                result = testRunner('test', libPath, apiType)
                writeResult(resultFile, result, apiType)
                for key,value in result.items():
                    if key in resultAll: resultAll[key]+=value
            resultAll['test_pass_api_name'] = ''
            resultAll['test_fail_api_name'] = ''
            resultAll['build_pass_api_name'] = ''
            resultAll['build_fail_api_name'] = ''
            writeResult(resultFile, resultAll, "Summary of all")
        else: 
            result = testRunner('test', libPath, options.test)
            writeResult(resultFile, result, options.test)
    else: pass
    
    if options.golden:
        filePath = os.path.join(ROOT_DIR, 'golden')
        testRunner(golden, filePath, 'all')
        pass

    if options.parser:
        resultAll = {'total': 0, 'pass':0, 'fail':0}
        logPath = os.path.join(ROOT_DIR, 'test', 'log')
        resultFile = os.path.join(TEST_PATH,'parse_result.txt')
        if os.path.exists(resultFile): os.remove(resultFile)
        result = testRunner('parse', logPath, options.parse)
        writeResult(resultFile, result, options.parse)
    else: pass
    
if __name__ == "__main__":  
    main() 