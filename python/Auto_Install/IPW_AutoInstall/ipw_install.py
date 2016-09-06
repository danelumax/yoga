#!/usr/bin/env python

import os, sys, traceback, signal
tool_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.sep.join((tool_path, "src")))

import log
log.Init()

import common
from optparse import OptionParser
from cfg import cfgInstance
from healthcheckinfo import healthcheckInstance
from taskgenerate import TaskGenerate
from tasksuite import TaskSuite
from sshmanager import sshManagerInstance




def parseParameter() :
    log._file.debug(">>> enter parse Parameter")
    parser = OptionParser()
    parser.add_option("-c",
                      "--cfg",
                      help = "Optional, cfg file path",
                      action = "store",
                      dest = "cfg",
                      default = None)
    (options, args) = parser.parse_args(args = sys.argv)

    if options.cfg :
        common.g_cfgfile = str(options.cfg)

    if not os.path.exists(common.g_cfgfile) :
        raise Exception("file \"%s\" does not exist" %common.g_cfgfile)

    log._file.debug("load cfg file: " + common.g_cfgfile)
    log._file.debug("<<< outer parse Parameter")



def onsignal_int(signum, frame) :
    log._file.debug("Receive SIGINT[Ctrl+C] to stop process: %s\n" %str(signum))
    if not common.g_stop_running :
        common.stop_progress()
        common.stop_install()
        sshManagerInstance().destory()
        common.save_tasks()
        common.g_stop_running = True
        log._file.debug("========= Force Exit Main Thread =========")
        sys.exit(-1)
    

def register_signal() :
    signal.signal(signal.SIGINT, onsignal_int)


def main() :
    register_signal()
    parseParameter()

    cfg = cfgInstance()
    cfg.parse(common.g_cfgfile)

    healthcheckInstance().parse()

    task_generate = TaskGenerate()
    task_suite = TaskSuite()

    if not common.is_have_tasks() :
        task_generate.getPrepareTasks()
        task_generate.getTasks()
        
    common.LOG("Starting IPWorks Installation (total %d):" %(common.get_tasks_num()))
    task_suite.execute()
    common.LOG("IPWorks has been successfully Installed !")

    common.display_healthcheck_info()

    return 0



if __name__ == "__main__" :
    try :
        sys.exit(main())
    except Exception as e :
        log._all.error("Exit: " + str(e))
        log._all.error("Please find trace info in file \"log/install.log\"")
        traceback.print_exc(file = sys.stderr)
        sys.exit(-1)





