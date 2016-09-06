import sys, os, subprocess, re, time, threading
import random
import json
import log
from scp import Scp
from cfg import cfgInstance
import ConfigParser


g_cfgfile = 'network.json'
g_username = 'root'
g_password = ''
g_sshport = '22'
g_ipw_mode = ''
g_exec_tasklist = {} 
g_exec_file = "exec_tasks.json"
g_healthcheck_file = "HealthCheckReport.tmp"
g_progress_thread = None
g_timer_thread = None
g_install_thread = []
g_task_index = 1
g_stop_running = False
g_shadow_file = ".shadow"
g_env_file = "src/ssh/env.info"
g_cli_file = "src/common/cli.info"
g_upgrade_path_file = "src/common/upgrade_path.info"

C_IPv4_PREFIX_LEN = 24
C_IPv6_PREFIX_LEN = 64

C_IPW_APP_AAA = 'AAA'
C_IPW_APP_DNS = 'DNS'
C_IPW_APP_ENUM = 'ENUM'
C_IPW_APP_DHCP = 'DHCP'
C_IPW_APP_CLF = 'CLF'
C_TASK_PREFIX_LENGTH = 3
C_SECTION_DELAY_TIME = 3 

g_isInstall_AAA = False
g_isInstall_DNS = False
g_isInstall_ENUM = False
g_isInstall_DHCP = False
g_isInstall_CLF = False

#upgrade mode, can be either of 'DNS','ENUM','DHCP','AAA',or 'CLF'
g_upgrade_app = '' 
#upgrade service, a list consist of 'DNS','ENUM','DHCP','AAA',or 'CLF'
g_upgrade_service = []
g_isChangeRoot = False
g_ndbSyncSimpleCheck = False
#the time wait for every section when execute task,measured by second
g_section_wait_time = 300 
g_need_shorting_failover_time = False 

C_IPW_MODE_SINGLE = 'SINGLE'
C_IPW_MODE_ENTRY1 = 'ENTRY1'
C_IPW_MODE_ENTRY2 = 'ENTRY2'
C_IPW_MODE_MEDIUM1 = 'MEDIUM1'
C_IPW_MODE_MEDIUM2 = 'MEDIUM2'

C_EMC_MODE_NFS = 'nfs'
C_EMC_MODE_DISKARRAY = 'diskarray'

C_EMC_MOUNT_MODE_DOUBLE = True

C_PRETASK_JSON_PATH = "src/tasks/pretasks.json"
C_POSTTASK_JSON_PATH = "src/tasks/posttasks.json"
C_SINGLE_JSON_PATH = "src/tasks/singletasks.json"
C_ENTRY1_JSON_PATH = "src/tasks/entry1tasks.json"
C_ENTRY2_JSON_PATH = "src/tasks/entry2tasks.json"
C_MEDIUM1_JSON_PATH = "src/tasks/medium1tasks.json"
C_MEDIUM2_JSON_PATH = "src/tasks/medium2tasks.json"

#dict that mode(either one of single,entry1,entry2,medium1,medium2) to json file  
g_mode_jsonfile_dict = {C_IPW_MODE_SINGLE:C_SINGLE_JSON_PATH,
                        C_IPW_MODE_ENTRY1:C_ENTRY1_JSON_PATH,
                        C_IPW_MODE_ENTRY2:C_ENTRY2_JSON_PATH,
                        C_IPW_MODE_MEDIUM1:C_MEDIUM1_JSON_PATH,
                        C_IPW_MODE_MEDIUM2:C_MEDIUM2_JSON_PATH}

#dict that mode(either one of single,entry1,entry2,medium1,medium2) to app(either one of dns,dhcp,enum,dhcp,clf)
g_mode_app_dict = {C_IPW_MODE_SINGLE:[C_IPW_APP_DNS],
                   C_IPW_MODE_ENTRY1:[C_IPW_APP_DNS,C_IPW_APP_ENUM,C_IPW_APP_DHCP,C_IPW_APP_AAA],
                   C_IPW_MODE_ENTRY2:[C_IPW_APP_DNS,C_IPW_APP_ENUM,C_IPW_APP_DHCP],
                   C_IPW_MODE_MEDIUM1:[C_IPW_APP_DNS,C_IPW_APP_ENUM,C_IPW_APP_DHCP,C_IPW_APP_AAA],
                   C_IPW_MODE_MEDIUM2:[C_IPW_APP_CLF]}

#dict that app(either on of dns,dhcp,enum,dhcp) to service(list consist of dns,dhcp,enum,dhcp,clf)
g_app_service_dict = {C_IPW_APP_DNS:[C_IPW_APP_DNS],
                      C_IPW_APP_ENUM:[C_IPW_APP_DNS,C_IPW_APP_ENUM],
                      C_IPW_APP_DHCP:[C_IPW_APP_DHCP],
                      C_IPW_APP_AAA:[C_IPW_APP_AAA,C_IPW_APP_DHCP,C_IPW_APP_DNS],
                      C_IPW_APP_CLF:[C_IPW_APP_DHCP,C_IPW_APP_CLF]} 

C_IPW_HOSTROLE_SS = 'SS'
C_IPW_HOSTROLE_PS = 'PS'

#g_key_cfg_dict = {}
####################################################################

def open_file(file_path) :
    log._file.debug(">>> Open file \"%s\"" % file_path)
    fd = open(file_path, "r")
    content = fd.read()
    fd.close()
    log._file.debug("<<<")
    return content

####################################################################

def getNodeList(cfg):
    cfg_list = []
    if not cmp(C_IPW_MODE_SINGLE, g_ipw_mode) : #single
        cfg_list.append(cfg.getPsCfg(0))
    if not cmp(C_IPW_MODE_ENTRY1, g_ipw_mode) : #entry1
        cfg_list.append(cfg.getSsCfg(0))
        cfg_list.append(cfg.getPsCfg(0))
        cfg_list.append(cfg.getPsCfg(1))
    if not cmp(C_IPW_MODE_ENTRY2, g_ipw_mode) : #entry2
        cfg_list.append(cfg.getSsCfg(0))
        cfg_list.append(cfg.getPsCfg(0))
    if not cmp(C_IPW_MODE_MEDIUM1, g_ipw_mode) :#medium1
        cfg_list.append(cfg.getSsCfg(0))
        cfg_list.append(cfg.getSsCfg(1))
        cfg_list.append(cfg.getPsCfg(0))
        cfg_list.append(cfg.getPsCfg(1))
    if not cmp(C_IPW_MODE_MEDIUM2, g_ipw_mode) :#medium2
        cfg_list.append(cfg.getSsCfg(0))
        cfg_list.append(cfg.getSsCfg(1))
        cfg_list.append(cfg.getPsCfg(0))
        cfg_list.append(cfg.getPsCfg(1))
    return cfg_list


####################################################################

display_width = 93
display_item = ' Item: '
display_expvalue  = '   Expect Value: '
display_realvalue = '   Real   Value: '
display_summary   = '   Summary: '

def print_red(s) :
    return "%s[31;5m%s%s[0m" %(chr(27), s, chr(27))

def print_green(s) :
    return "%s[32;1m%s%s[0m" %(chr(27), s, chr(27))

def print_violet(s) :
    return "%s[35;1m%s%s[0m" %(chr(27), s, chr(27))

def print_info(n, r, e, s) :
    info = ''
    info += '|' + display_item + n.ljust(display_width - len(display_item)) + '|\n'
    info += '|' + display_expvalue + e.ljust(display_width - len(display_expvalue))+ '|\n'
    if len(r) > (display_width - len(display_realvalue)):
        w = display_width - len(display_realvalue) - 1
        info += '|' + display_realvalue + r[:w]+ ' |\n'
        r = r[w:]
        while len(r) > (display_width-1) :
            w = display_width - 2
            info += '| ' + r[:w] + ' |\n'
            r = r[w:]
        info += '| ' + r.ljust(display_width-1) + '|\n'
    else :
        info += '|' + display_realvalue + r.ljust(display_width - len(display_realvalue))+ '|\n'
    if "NOK" == s :
        info += '|' + display_summary + print_red(s.ljust(display_width - len(display_summary)))+ '|\n'
    elif "OK" == s :
        info += '|' + display_summary + print_green(s.ljust(display_width - len(display_summary)))+ '|\n'
    else :
        info += '|' + display_summary + print_violet(s.ljust(display_width - len(display_summary)))+ '|\n'
    return info


def display_healthcheck_info() :
    info = ''
    if os.path.exists(g_healthcheck_file) :
        check_list = parse_file(g_healthcheck_file)
        os.popen('mv %s %s' %(g_healthcheck_file, g_healthcheck_file.split('.')[0]))
        info += '|'+ '='.center(display_width,'=')+ '|\n'
        info += '|'+ 'IPWorks Environment Validation Summary'.center(display_width,' ')+ '|\n'
        info += '|'+ '='.center(display_width,'=')+ '|\n'
        for item in check_list :
            info += print_info(item["Item"], item["Real_value"], item["Exp_value"], item["Summary"])
        info += '|'+ '='.center(display_width,'=')+ '|\n'
    else :
        log._file.warning("Doesn't Exist " + g_healthcheck_file)
    if info :
        log._print.debug("\nIPWorks Health Check Report:\n%s" %(info))


def save_healthcheck_info(P_name, P_real, P_exp, P_summary) :
    log._file.debug(">>> Save health check info begin")
    check_list = []
    if os.path.exists(g_healthcheck_file) :
        tmp = parse_file(g_healthcheck_file)
        if tmp :
            check_list = tmp
    is_exist = False
    if check_list:
        for item in check_list:
            if not cmp(P_name, item['Item']):
                item["Real_value"] = P_real
                item["Exp_value"] = P_exp
                item["Summary"] = P_summary
                is_exist = True
                break
    if not check_list or not is_exist:
        check_item = {}
        check_item["Item"] = P_name
        check_item["Real_value"] = P_real
        check_item["Exp_value"] = P_exp
        check_item["Summary"] = P_summary
        check_list.append(check_item)            
    save_checklist(check_list)
    log._file.debug("<<< Save health check info end")


def save_checklist(check_list) :
    msg = "[\n"
    m = len(check_list)
    for i in range(m) :
        encodejson = json.dumps(check_list[i])
        if i == (m-1) :
            msg += "  %s\n" %encodejson
        else :
            msg += "  %s,\n" %encodejson
    msg += "]\n"
    log._file.debug('Update Health Check info:\n%s' %(msg))
    fd = open(g_healthcheck_file, 'w')
    fd.write(msg)
    fd.close()

####################################################################
def get_tasks_num() :
    task_num = 0
    for key in g_exec_tasklist.keys():
        tasklist = g_exec_tasklist[key]
        for i in tasklist:
            for j in i :
                log._file.debug("name = "+j['name'])
                log._file.debug("status = "+j['status'])
                if cmp('done',j['status']):
                    task_num += 1 
    return task_num

def is_have_tasks() :
    result = False
    #num = 0
    cfg = cfgInstance()
    if os.path.exists(g_exec_file) :
        task_root = parse_file(g_exec_file)
        for key in task_root.keys():
            templist = []
            templist.append(task_root[key])
            #host = cfg.getCfgFromKey(key)
            #savekey = str(num)+key
            #log._file.debug("savekey ="+savekey)
            #num = num+1 
            g_exec_tasklist[key] = templist
            #g_key_cfg_dict[host] = key 
      
            if not result :
                result = haveReadyTask(templist)
       
    if(result):
       log._file.debug("The task in tasklist has not finished yet,continue to execute it!")  
    else:
       log._file.debug("Need to generate new tasklist!")  

    return result

def save_tasks():
    msg = "{\n"
    index = 0
    length = len(g_exec_tasklist.keys())
    for key in sorted(g_exec_tasklist.keys()):
        #printkey = key[1:]
        index += 1
        tasklist = g_exec_tasklist[key]
        #tempkey = g_key_cfg_dict[key]
        #msg += '"'+printkey+'"'+ ": [\n"
        msg += '"'+key+'"'+ ": [\n"
        m = len(tasklist)
        for i in range(m):
            n = len(tasklist[i])
            for j in range(n):
                encodejson = json.dumps(tasklist[i][j])
                if j == (n-1):
                    msg += "    %s\n" %encodejson
                else :
                    msg += "    %s,\n" %encodejson
        if(index == length):
            msg += "  ]\n"
        else:
            msg += "  ],\n"

    msg += "}\n"

    fd = open(g_exec_file, 'w')
    fd.write(msg)
    fd.close()

####################################################################

def create_file(cfg, context, path, name) :
    log._file.debug(">>> Create file \"%s\" on %s:%s"  % (name, cfg.getHostName(), path))
    file_name = None
    do_loop = True
    while do_loop :
        ran = random.randint(1, 999999)
        file_name = "/tmp/" + name + "." + str(ran)
        if not os.path.exists(file_name):
            do_loop = False
    fd = open(file_name, "w")
    fd.write(context)
    fd.close()
    scp = Scp(cfg.getOamIp(), cfg.getSshPort(), cfg.getUserName(), cfg.getPassword())
    scp.copy_to(file_name, path+name)
    if file_name != None :
        os.remove(file_name)
    log._file.debug("<<<")


def parse_file(file_path):
    log._file.debug(">>> Parse file \"%s\"" % file_path)
    json_root = None
    fd = open(file_path, 'r')
    context = fd.read()
    fd.close()
    if context :
        json_root = json.loads(context)
    log._file.debug("File context :\n%s" % context)
    #log._file.debug("File context :\n%s" % json_root)
    log._file.debug("<<<")
    return json_root


def check_down_status(cfg):
    log._file.debug(">>> Check whether remote machine \"%s\" is down status" % cfg.getHostName())
    peer_ip = cfg.getOamIp()
    ret = 0
    while ret == 0 :
        proc = subprocess.Popen(["ping", "-c", "1", peer_ip], stdout=subprocess.PIPE)
        ret = proc.wait()
    logger.debug("remote machine \"%s\" is down" % cfg.getHostName())
    log._file.debug("<<<")


def check_up_status(cfg):
    log._file.debug(">>> Check whether remote machine \"%s\" is up status" % cfg.getHostName())
    peer_ip = cfg.getOamIp()
    ret = -1
    while ret != 0 :
        time.sleep(30)
        proc = subprocess.Popen(["ping", "-c", "1", peer_ip], stdout=subprocess.PIPE)
        ret = proc.wait()
        log._file.debug("wait for remote(%s) up ..." % peer_ip)
    log._file.debug("remote machine \"%s\" is up" % cfg.getHostName())
    log._file.debug("<<<")


def getOptionValue(node, name) :
    value = None
    try :
        value = node[name]
    except Exception :
        pass
    return value


def getHostName() :
    sys_type = os.name
    if not cmp('nt', sys_type) :
        hostname = os.getenv('computername')
        log._file.debug("Get Local hostname: " + hostname)
        return hostname
    elif not cmp('posix', sys_type) :
        host = os.popen('echo $HOSTNAME')
        try :
            hostname = host.read().strip()
            log._file.debug("Get Local hostname: " + hostname)
            return hostname
        finally :
            host.close()
    else :
        raise Exception("Unknown hostname")


##########################################################

tag = ['/', '-', '\\', '|']
tag_len = len(tag)
wait_width = 40
spec_width = 40

class ProgressThread(threading.Thread) :

    def __init__(self, threadname, prefix,printbar) :
        threading.Thread.__init__(self, name=threadname)
        self.running = True
        self.prefix = prefix
        self.printbar = printbar 
        log._file.debug("start %s progress thread, running: %s" %(self.name, str(self.running)))

    def stop(self) :
        self.running = False
        log._file.debug("stop %s progress thread, running: %s" %(self.name, str(self.running)))

    def run(self) :
        i = 0
        if(self.printbar):
            while self.running :
                print '%s %s: %s %s\r' %(self.prefix, self.name.ljust(spec_width, ' '), "%s"%(i % wait_width * '.'), tag[i%tag_len]),
                sys.stdout.flush()
                i += 1
                i %= wait_width
                if i == 0 :
                    print '%s %s: %s  \r' %(self.prefix, self.name.ljust(spec_width, ' '), "%s"%(wait_width*' ')),
                    sys.stdout.flush()
                time.sleep(0.1)
            log._file.debug("progress thread of %s end" %self.name)
        else:
            print(self.prefix+" "+self.name.ljust(spec_width, ' '))
            



def start_progress(name, prefix,printbar = True) :
    log._file.debug(">> ##### Start Progress thread begin #####")
    global g_progress_thread
    g_progress_thread = ProgressThread(name, prefix,printbar)
    g_progress_thread.setDaemon(True)
    g_progress_thread.start()
    log._file.debug("<< ##### Start Progress thread end ##### ")

def finish_progress() :
    log._file.debug(">> $$$$$ Finish Progress thread begin $$$$$")
    global g_progress_thread, g_task_index
    g_progress_thread.stop()
    g_progress_thread.join()
    if(g_progress_thread.printbar):
        print '%s %s: %s [Done]' %(g_progress_thread.prefix, g_progress_thread.name.ljust(spec_width, ' '), "%s"%(wait_width * '.'))
    g_task_index += 1
    g_progress_thread = None
    log._file.debug("<< $$$$$ Finish Progress thread end $$$$$")

def stop_progress() :
    global g_progress_thread
    if(g_progress_thread.printbar):
        print '%s %s: %s [Failed]' %(g_progress_thread.prefix, g_progress_thread.name.ljust(spec_width, ' '), "%s"%(wait_width * '.'))
    if g_progress_thread :
        g_progress_thread.stop()
        g_progress_thread.join()
        print
        g_progress_thread = None
    else :
        log._file.debug("Progress thread is None")
    log._print.error("Stop the auto upgrade process!")


def LOG(msg) :
    print str(msg)
    sys.stdout.flush()


def stop_install() :
    log._file.debug(">> Force stop Install thread")
    start_progress('Stopping Install threads', 'Please wait for')
    global g_install_thread
    for x in g_install_thread :
        x.stop()
    for x in g_install_thread :
        x.join()
    g_install_thread = []
    finish_progress()
    log._file.debug("<< Force stop Install thread")


snmp_cmd = '/opt/ipworks/IPWcommon/usr/bin/snmpwalk'
def getAlarmCmd(app) :
    command = '(%s -v 2c localhost alarmTable |grep "%s" > /dev/null) ' %(snmp_cmd, app) + \
              '&& (snmpkey=$(%s -v 2c localhost alarmTable | grep "%s" ' %(snmp_cmd, app)+ \
              '| sed -e \'s/\\./ /g\' ' + \
              "| awk '{print $13\" \"$14}' | tr '\\n' ' ' " + \
              "| sed -e 's/ $//g' | sed -e 's#= #=\\|\\\\.#g')" + \
              '&& %s -v 2c localhost alarmTable |grep -E "\\.$snmpkey")' %(snmp_cmd)
    return command

def parseAlarmInfo(info) :
    tmp = info.split('\n')
    r = ''
    for x in tmp :
        x = x.strip()
        if re.search('^.1.3.6.1.4.1.3881.2.1.8', x) :
            r += x + ';'
    return r

##############################################################

def getNodeInfo() :
    log._file.debug(">> Get Node Information(username & password)")
    fd = open(g_shadow_file, "r")
    context = fd.readlines()
    fd.close()
    log._file.debug("<<")
    return context


def cleanNodeInfo() :
    log._file.debug(">> Clean Node Information(username & password)")
    os.system("rm -f %s" %(g_shadow_file))
    log._file.debug("<<")


def saveNodeInfo(host, ip, user, passwd) :
    log._file.debug(">> Save Node Information(username & password)")
    fc = ""
    if os.path.exists(g_shadow_file) :
        fc = open_file(g_shadow_file)
    if not re.search(host, fc) :
        cmd = "%s;%s;%s;%s" %(host, ip, user, encrypt(passwd))
        os.system('echo "%s" >> %s' %(cmd, g_shadow_file))
    log._file.debug("<<")



key = 15
def encrypt(s):
    b = bytearray(str(s).encode("gbk"))
    n = len(b)
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2 : 0-15, ASCII: 15-80
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")


def decrypt(s):
    c = bytearray(str(s).encode("gbk"))
    n = len(c)
    if n % 2 != 0 :
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except:
        raise Exception("Decode password Failed !!!")

def haveReadyTask(list):
    temp = list
    x = len(temp)
    for y in range(x):
            if temp[y]:
                z = len(temp[y])
                n = 0
                while n < z:
                    if (not cmp("ready",temp[y][n]["status"])) :
                        return  True
                    else:
                        n = n+1
 
    return False

def getEnvInfo():
    log._file.debug("getEnvInfo")
    context = None
    if os.path.exists(g_env_file) :
        fd = open(g_env_file, "r")
        context = fd.readlines()
        fd.close()
    return context
    log._file.debug("<<")

def cleanEnvInfo():
    log._file.debug("cleanEnvInfo")
    os.system("rm -f %s" %(g_env_file))
    log._file.debug("<<")

def saveEnvInfo(item1,item2):
    log._file.debug("saveEnvInfo")
    fc = ""
    cmd = "%s;%s" %(item1,item2)
    os.system('echo "%s" >> %s' %(cmd, g_env_file))
    log._file.debug("<<")

def getCliInfo():
    log._file.debug("getCliInfo")
    context = None
    if os.path.exists(g_cli_file) :
        fd = open(g_cli_file, "r")
        context = fd.readlines()
        fd.close()
    return context
    log._file.debug("<<")

def cleanCliInfo():
    log._file.debug("cleanCliInfo")
    os.system("rm -f %s" %(g_cli_file))
    log._file.debug("<<")

def saveCliInfo(item1,item2):
    log._file.debug("saveCliInfo")
    fc = ""
    cmd = "%s;%s" %(item1,item2)
    os.system('echo "%s" >> %s' %(cmd, g_cli_file))
    log._file.debug("<<")

def saveUpgradePath(base, target):
    log._file.debug("saveUpgradePath")
    filename = g_upgrade_path_file
    if os.path.exists(filename):
        log._file.warn("file %s already exist, remove it." % filename)
        os.remove(filename)

    config = ConfigParser.RawConfigParser()
    config.add_section('UpgradePath')
    config.set('UpgradePath', 'base_version', base)
    config.set('UpgradePath', 'target_version', target)

    with open(filename, 'wb') as configfile:
        config.write(configfile)

    log._file.debug("<<")

def cleanUpgradePath():
    log._file.debug("cleanUpgradePath")
    if os.path.exists(g_upgrade_path_file):
        os.remove(g_upgrade_path_file)
    log._file.debug("<<")

def get_version_info(version):
    config = ConfigParser.ConfigParser()
    config.read(g_upgrade_path_file)

    return config.get('UpgradePath', version)

def get_base_version():
    log._file.debug("get_base_version")
    return get_version_info('base_version')

def get_target_version():
    log._file.debug("get_base_version")
    return get_version_info('target_version')


def stopTimer():
    log._file.debug("stopTimer")
    global g_timer_thread
    if  g_timer_thread:
        g_timer_thread.stop()
        g_timer_thread.join()
        g_timer_thread = None
    log._file.debug("<<")

