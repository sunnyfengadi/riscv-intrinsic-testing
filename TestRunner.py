####################################################################################
#TestRunner.py 
####################################################################################
import os,sys
import re,subprocess
import platform
import datetime,time
import shutil
import json
from optparse import OptionParser
from subprocess import Popen, PIPE
from easyprocess import EasyProcess

#####################################################################################
ROOT_DIR=os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join( ROOT_DIR, 'test','log' )
ELF_PATH = os.path.join( ROOT_DIR,'test', 'elf' )
#UPPER_LEVEL = os.path.abspath(os.path.join(ROOT_DIR, ".."))
BIN_PATH = os.path.join(ROOT_DIR, 'bin', 'test')
TEST_PATH = os.path.join(ROOT_DIR, 'test')

sys.path.append(ROOT_DIR)
#sys.path.append(UPPER_LEVEL)

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
        
def TestRunner(type, path, apitype):
    # run shell scripts to get the test logs
    if type == 'test':
        totalNum = 0
        passNum = 0
        failNum = 0
        failApi = []
        subResult = {}

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
        subResult['total']= totalNum
        subResult['pass'] = passNum
        subResult['fail'] = failNum
        subResult['fail_api_name'] = failApi
        return subResult
        
    # parse test results from logs into Json 
    if type == 'parse':
        pass
        


###########################################################################################
# Main
# python3 TestRunner.py -t load   # or -t all that is for all apis 
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
        logPath = os.path.join(ROOT_DIR, 'test', 'log')
        if parseApi == 'all':
            folder = os.listdir(logPath)
            for apiType in folder:
                TestRunner('parse', logPath, apiType)
        else:
            TestRunner('parse', logPath, parseApi)
    else: pass
    
if __name__ == "__main__":  
    main() 