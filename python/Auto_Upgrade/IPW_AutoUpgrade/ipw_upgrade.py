#!/usr/bin/env python

import os, sys, traceback, signal
tool_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.sep.join((tool_path, "src/util")))
sys.path.insert(0, os.sep.join((tool_path, "src/logs")))
sys.path.insert(0, os.sep.join((tool_path, "src/ssh")))
sys.path.insert(0, os.sep.join((tool_path, "src/common")))
sys.path.insert(0, os.sep.join((tool_path, "src/tasks")))

import log
log.Init()

from optparse import OptionParser
import common 
import cfg
import taskmanager
from tasksuite import TaskSuite
import time


def onsignal_int(signum, frame) :
    print ("\nReceive SIGINT[Ctrl+C] to stop process by force !")
    common.stopTimer()
    common.save_tasks()
    sys.exit(-1)
    

def register_signal() :
    signal.signal(signal.SIGINT, onsignal_int)


def main() :
    register_signal()
    parser = OptionParser()

    cfgInstance = cfg.cfgInstance()
    cfgInstance.parse(common.g_cfgfile) 
    task_suite = TaskSuite()

    taskManager =  taskmanager.TaskManager()
    if not common.is_have_tasks():
        log._file.debug("Generate new task list")
        taskManager.setExecTaskList()

    common.LOG("Starting IPWorks Upgrade (total %d):" %(common.get_tasks_num()))
    taskManager.startAllTask()
    common.cleanNodeInfo()
    common.cleanEnvInfo()
    common.cleanCliInfo()
    common.LOG("IPWorks has been successfully Upgraded from '%s' to '%s' !" %(common.get_base_version(), common.get_target_version()))
    common.cleanUpgradePath()

    return 0




if __name__ == "__main__" :
    try :
        sys.exit(main())
    except Exception as e :
        log._all.error("Exit: " + str(e))
        log._all.error("Please find trace info in file \"log/auto_upgrade.log\"")
        traceback.print_exc(file = sys.stderr)
        sys.exit(-1)





