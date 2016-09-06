'''
This file is used to go through all files and directories/sub-directories,
then automatically import the tasks defined in each python module
'''
import sys
import os
import re
import log


def makeFolderAsPackage(directory) :
    '''
    This function is used to add file __init__.py to sub folders
    '''
    for dirpath, dirnames, filenames in os.walk(directory) :
        pkgRealPath = os.path.join(dirpath, '__init__.py')
        if not os.path.exists(pkgRealPath) :
            log._file.debug('No package found under ' + dirpath + ', create __init__.py automaticlly!')
            f = open(os.path.join(dirpath, '__init__.py'), "w")
            f.write('# This file make the directory to be a module')
            f.close()
            
            
def isTaskModule(filename) :
    '''
    The method is to determine a module is a task module which:
    1. file name should be end with 'task'(not case sensitive)
    2. extension should be '.py'
    '''
    (name, ext) = os.path.splitext(filename)
    if ext != '.py' :
        return False
    if name[-4:].lower() != 'task' :
        return False
    return True
    
    
def getTaskFiles(directory) :
    '''
    Get all task exact path of a given directory and it's sub directories
    Return a list
    '''
    files = []
    for dirpath, dirnames, filenames in os.walk(directory) :
        for filename in filenames:
            if isTaskModule(str(filename)) :
                realPath = os.path.join(dirpath, filename)
                files.append(realPath)
    return files               

    
def getTaskName(taskFile) :
    '''
    Each task defined one and only one class
    we are going to find this class and return the class name in the file
    '''
    fileId = open(taskFile, 'r')
    context = fileId.read().splitlines()
    fileId.close()
    taskName = ""
    for line in context :
        if re.search('^class', line) :
            className = line.split()[1]
            taskName = className.split(':')[0].split(r'(')[0]
            break
    return taskName


def getTaskModule(dirpath, taskFile) :
    moduleName = os.path.splitext(taskFile)[0].replace(dirpath, "")
    moduleName = moduleName.replace("/", ".").replace("\\", ".")[1:]
    return moduleName


def getModuleInTaskFile(taskHomeDir) :
    '''
    The method is used to generate to a dict to describ the task and it's module
    '''
    if not os.path.exists(taskHomeDir):
        raise Exception("Directory '%s' does not exist" %(taskHomeDir))
    taskDict = {}
    taskFiles = getTaskFiles(taskHomeDir)
    task_home_parent = os.path.dirname(taskHomeDir)
    for taskFile in taskFiles:
        moduleName = getTaskModule(task_home_parent, taskFile)
        taskName = getTaskName(taskFile)
        if taskName in taskDict.keys() : 
            raise Exception ("Found duplicated task <" + taskName + "> in module " + taskDict[taskName] + " && " + moduleName)
        if not taskName :
            raise Exception (str(taskFile) + " does not contain a valid task class.")

        taskDict[taskName] = moduleName
         
    return taskDict
    




if __name__ != '__main__':

    curPath = os.path.dirname(os.path.realpath(__file__))
    makeFolderAsPackage(curPath)
    taskDict = getModuleInTaskFile(curPath)

    for item in taskDict :
        cmd = 'from ' + taskDict[item] + ' import ' + item
        log._file.debug(cmd)
        exec(cmd)

 


