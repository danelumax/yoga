import os, sys, traceback,time
import log, common
from src import taskDict
from cfg import cfgInstance
import threading
import time
import signal

class TaskSuite(object) :
    """
    Class TaskSuite
    """

    def __init__(self) :
        pass


    def execute(self,key,task_list) :
        log._file.debug(">> Start to execute tasks :\n%s" %task_list)
        cfg = cfgInstance()
        node = cfg.getCfgFromKey(key)
        key = key[common.C_TASK_PREFIX_LENGTH:]
        taskDiscList = None
        taskDiscList = self.getTaskdiscription(task_list)
        length = len(taskDiscList)
        if(length == 0):
            log._file.debug("No task in sub tasklist,key = "+key)
            return
        if(node):
            print("\nThe below tasks will be executed on host automaticly: "+node.getHostName()+", role : "+key+"\n")
        else:
            print("\nThe below tasks will be executed on all nodes automaticly: \n")
        for item in taskDiscList:
            print("    ."+item)
        while(1):
            promot = '    Continue the auto upgrade progress ? (Please ensure that you environment is ready) Y | N : '
            common.g_timer_thread = timer(common.g_section_wait_time,promot) 
            common.g_timer_thread.start()
            input = nonBockingRawInput("\n"+promot,common.g_section_wait_time+common.C_SECTION_DELAY_TIME)
            common.stopTimer()
            input = input.strip().upper()
            if(input == 'Y'):
                break;
            elif (input == 'N'):
                print("\n    Stop the auto upgrade progress manually!")
                log._file.debug("Stop the auto upgrade progress manually!")
                sys.exit(0)
            else:
                print("\n    Please enter Y or N !")
    
        if task_list :
            i = len(task_list)
            for m in range(i) :
                if task_list[m] :
                    j = len(task_list[m])
                    for n in range(j) :
                        if task_list[m][n] and cmp("done", task_list[m][n]["status"].lower()) \
                          and cmp("manual",task_list[m][n]["status"].lower()):
                            task_name = task_list[m][n]["name"]
                            module_name = taskDict[task_name]
                            try :
                                module = __import__(module_name)
                                clazz = getattr(module, task_name)
                                t = clazz()
                                strindex = ''
                                if(len(str(common.g_task_index)) == 1):
                                    strindex = '    %d .' %(common.g_task_index)
                                else:
                                    strindex = '    %d.' %(common.g_task_index)
                                log._file.debug("class doc: '%s'" % t.__doc__.strip())
                                if not cmp(t.__doc__.strip(),'Stop Other Process'):
                                    common.start_progress(t.__doc__.strip(), strindex,False)
                                else:
                                    common.start_progress(t.__doc__.strip(), strindex)
                                t.precheck()
                                if(node):
                                    t.execute(node)
                                else:
                                    t.execute()
                                t.verify()
                                t.updateProgress()
                                if cmp("always", task_list[m][n]["status"]) \
                                  and cmp("test", task_list[m][n]["status"]) :
                                    task_list[m][n]["status"] = "done"
                                common.finish_progress()
                            except Exception as e :
                                common.stop_progress()
                                common.save_tasks()
                                ###sshManagerInstance().destory()
                                log._all.error("Exception info: " + str(e))
                                self.print_helpInfo(t)
                                traceback.print_exc(file = sys.stderr)
                                raise Exception("Import & Execute Task '%s' Failed" %task_name)
                else : 
                    log._file.debug("task set is empty")
        else :
            log._file.debug("task list is empty")
        common.save_tasks()
        ###sshManagerInstance().destory()
        log._file.debug("<< Task list has finished")



    def getTaskdiscription(self,task_list):
        discriptionList = []
        if task_list :
            i = len(task_list)
            for m in range(i) :
                if task_list[m] :
                    j = len(task_list[m])
                    for n in range(j) :
                        if task_list[m][n] and cmp("done", task_list[m][n]["status"].lower()) \
                          and cmp("manual",task_list[m][n]["status"].lower()):
                            task_name = task_list[m][n]["name"]
                            module_name = taskDict[task_name]
                            module = __import__(module_name)
                            clazz = getattr(module, task_name)
                            t = clazz()
                            log._file.debug("class doc: '%s'" % t.__doc__.strip())
                            discriptionList.append(t.__doc__.strip())

        return discriptionList

    def print_helpInfo(self,task):
        taskdesc = task.__doc__.strip()
        header = " Help info for '%s' task " %taskdesc
        infomsgLength = 100
        msg1 = "*" * 30
        msg2 = "*" * (infomsgLength-30-len(header))
        msg3 = "*" * infomsgLength

        log._print.info("")
        log._print.info(msg1+header+msg2)
        task.help()
        log._print.info(msg3)
        log._print.info("")


class timer(threading.Thread):  
    def __init__(self, waittime,promot):  
        threading.Thread.__init__(self)  
        self.waittime = waittime  
        self.thread_stop = False  
        self.firstTime = True 
        self.promot = promot[:-2]
   
    def run(self):   
        time.sleep(common.C_SECTION_DELAY_TIME)
        while ((not self.thread_stop) and (self.waittime > 0)):  
            time.sleep(1)  
            if(self.thread_stop):
                return
            if(self.firstTime):
                sys.stdout.write('\b'+'\b'+"( "+str(self.waittime)+" ) : ")
                self.firstTime = False 
                sys.stdout.flush()
            else:
                sys.stdout.write('\r')
                sys.stdout.write(self.promot+"( "+str(self.waittime)+" ) : ")
                sys.stdout.flush()

            self.waittime -= 1

        return

    def stop(self):  
        self.thread_stop = True

class TimeOutException(Exception):
    pass

def alarmHandler(signum, frame):
    raise TimeOutException

def nonBockingRawInput(prompt, timeout):
    time.sleep(0.5)
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        length = len(str(timeout))
        text = raw_input(prompt)
        signal.alarm(0)
        return text
    except TimeOutException:
        sys.stdout.write("\n")
        sys.stdout.flush()
    except (IOError,EOFError,KeyboardInterrupt),e:
        common.stopTimer()
        sys.stdout.write("\n")
        print("\nInput Error,auto upgrade progress stopped!")
        sys.exit(-1)
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return 'Y' 



            
    




