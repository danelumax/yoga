import os, sys, traceback
import log, common
from src import taskDict
from sshmanager import sshManagerInstance


class TaskSuite(object) :
    """
    Class TaskSuite
    """

    def __init__(self) :
        pass


    def execute(self) :
        log._file.debug(">> Start to execute tasks :\n%s" %common.g_exec_tasklist)
        if common.g_exec_tasklist :
            i = len(common.g_exec_tasklist)
            for m in range(i) :
                if common.g_exec_tasklist[m] :
                    j = len(common.g_exec_tasklist[m])
                    for n in range(j) :
                        if common.g_exec_tasklist[m][n] and cmp("done", common.g_exec_tasklist[m][n]["status"].lower()) :
                            task_name = common.g_exec_tasklist[m][n]["name"]
                            module_name = taskDict[task_name]
                            try :
                                module = __import__(module_name)
                                clazz = getattr(module, task_name)
                                t = clazz()
                                log._file.debug("class doc: '%s'" % t.__doc__.strip())
                                common.start_progress(t.__doc__.strip(), '    %d.' %(common.g_task_index))
                                t.precheck()
                                t.execute()
                                t.verify()
                                t.updateProgress()
                                if cmp("always", common.g_exec_tasklist[m][n]["status"]) \
                                  and cmp("test", common.g_exec_tasklist[m][n]["status"]) :
                                    common.g_exec_tasklist[m][n]["status"] = "done"
                                common.finish_progress()
                            except Exception as e :
                                common.stop_progress()
                                common.save_tasks()
                                sshManagerInstance().destory()
                                log._all.error("Exception info: " + str(e))
                                traceback.print_exc(file = sys.stderr)
                                raise Exception("Import & Execute Task '%s' Failed" %task_name)
                else : 
                    log._file.debug("task set is empty")
        else :
            log._file.debug("task list is empty")
        common.save_tasks()
        sshManagerInstance().destory()
        log._file.debug("<< Task list has finished")




