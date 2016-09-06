import common 
import os
import log
from tasksuite import TaskSuite
from cfg import cfgInstance


def managerInstance() :
    try :
        inst = TaskManager()
    except TaskManager as taskmanager:
        inst = taskmanager 
    return inst


class TaskManager :
    '''
    class TaskManager 
    '''

    __instance = None


    def __init__(self) :
        if TaskManager.__instance :
            raise TaskManager.__instance
        TaskManager.__instance = self

    def setExecTaskList(self):
        log._file.debug("<<< setExecTaskList")
        cfg = cfgInstance()

        common.g_exec_tasklist = {} 
        prelist = []
        templist = []
        postlist = []

        ##add pretask
        task_root = common.parse_file(common.C_PRETASK_JSON_PATH) 
        for key in task_root.keys():
            prelist.append(task_root[key]) 
            common.g_exec_tasklist[key] = prelist 


        ##add upgradetask
        jsonfile = common.g_mode_jsonfile_dict[common.g_ipw_mode]
        task_root = common.parse_file(jsonfile)
        for key in task_root[common.g_upgrade_app].keys():
            log._file.debug("Key = "+key)
            templist = []
            templist.append(task_root[common.g_upgrade_app][key]) 
            common.g_exec_tasklist[key] = templist

       
        #TR HT88501,add shortingfailover and restorefailover task for DHCP,AAA co-located situation 
        if((common.g_upgrade_app != common.C_IPW_APP_DHCP and common.g_upgrade_app != common.C_IPW_APP_CLF) and (common.C_IPW_APP_DHCP in common.g_upgrade_service)):
            ShorteningFailoverTimeTask = {"name" : "ShorteningFailoverTimeTask","status" : "ready"}
            RestoreFailoverTimeTask = {"name" : "RestoreFailoverTimeTask","status" : "ready"}
            for key in sorted(common.g_exec_tasklist.keys()):
                if(key == "2-1Active-SS") or (key == "2-1SS"):
                    common.g_exec_tasklist[key][0].insert(0,ShorteningFailoverTimeTask)
                elif(key.find("PS2") != -1):
                    common.g_exec_tasklist[key][0].append(RestoreFailoverTimeTask)
         
        ##add posttask 
        task_root = common.parse_file(common.C_POSTTASK_JSON_PATH)
        for key in task_root.keys():
            postlist.append(task_root[key]) 
            common.g_exec_tasklist[key] = postlist 

        log._file.debug(">>>")


    def startAllTask(self):
        log._file.debug("<<< startAllTask")
        task_suite = TaskSuite()
        for key in sorted(common.g_exec_tasklist.keys()):
            log._file.debug("key in start All Task = "+key)
            task_suite.execute(key,common.g_exec_tasklist[key])
        log._file.debug(">>>")

    def printTask(self,list,key):
        log._file.debug("<<< printTask")
        log._file.debug("key = "+key)
        for i in list:
            for j in i:
                log._file.debug("name = "+j['name'])
                log._file.debug("status = "+j['status'])
        log._file.debug(">>>")

