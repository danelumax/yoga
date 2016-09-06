import sys, os, subprocess, re, time, threading
import random
import json
import log
import base64
from scp import Scp


g_cfgfile = 'network.json'
g_username = 'root'
g_password = ''
g_sshport = '22'
g_ipw_mode = ''
g_cli_password = ''
g_cli_username = ''
g_exec_tasklist = []
g_exec_file = "exec_tasks.json"
g_healthcheck_file = "HealthCheckReport.tmp"
g_progress_thread = None
g_install_thread = []
g_task_index = 1
g_stop_running = False
g_shadow_file = ".shadow"


C_IPv4_PREFIX_LEN = 24
C_IPv6_PREFIX_LEN = 64

C_IPW_APP_AAA = 'aaa'
C_IPW_APP_DNS = 'dns'
C_IPW_APP_ENUM = 'enum'
C_IPW_APP_DHCP = 'dhcp'
C_IPW_APP_CLF = 'clf'

g_isInstall_AAA = False
g_isInstall_DNS = False
g_isInstall_ENUM = False
g_isInstall_DHCP = False
g_isInstall_CLF = False

C_IPW_MODE_SINGLE = 'single'
C_IPW_MODE_ENTRY1 = 'entry1'
C_IPW_MODE_ENTRY2 = 'entry2'
C_IPW_MODE_MEDIUM1 = 'medium1'
C_IPW_MODE_MEDIUM2 = 'medium2'

C_EMC_MODE_NFS = 'nfs'
C_EMC_MODE_DISKARRAY = 'diskarray'

C_EMC_MOUNT_MODE_DOUBLE = False

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
    for i in g_exec_tasklist :
        for j in i :
            if cmp('done', j['status']) :
                task_num += 1
    return task_num

def is_have_tasks() :
    if os.path.exists(g_exec_file) :
        task_root = parse_file(g_exec_file)
        for task_list in task_root :
            for x in task_list :
                if cmp("done", x["status"]) and cmp("always", x["status"]) :
                     log._file.debug("%s hasn't finished" %x["name"])
                     global g_exec_tasklist
                     g_exec_tasklist = task_root
                     #log._file.debug("g_exec_tasklist:\n%s" %g_exec_tasklist)
                     return True
    log._file.debug("All pre-exec tasks have finished, need to generate new tasks")
    return False
    

def save_tasks() :
    msg = "[\n"
    m = len(g_exec_tasklist)
    for i in range(m) :
        msg += "  [\n"
        n = len(g_exec_tasklist[i])
        for j in range(n) :
            encodejson = json.dumps(g_exec_tasklist[i][j])
            if j == (n-1) :
                msg += "    %s\n" %encodejson
            else :
                msg += "    %s,\n" %encodejson
        if i == (m-1) :
            msg += "  ]\n"
        else :
            msg += "  ],\n"
    msg += "]\n"
    #print msg
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
spec_width = 30

class ProgressThread(threading.Thread) :

    def __init__(self, threadname, prefix) :
        threading.Thread.__init__(self, name=threadname)
        self.running = True
        self.prefix = prefix
        log._file.debug("start %s progress thread, running: %s" %(self.name, str(self.running)))

    def stop(self) :
        self.running = False
        log._file.debug("stop %s progress thread, running: %s" %(self.name, str(self.running)))

    def run(self) :
        i = 0
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




def start_progress(name, prefix) :
    log._file.debug(">> ##### Start Progress thread begin #####")
    global g_progress_thread
    g_progress_thread = ProgressThread(name, prefix)
    g_progress_thread.setDaemon(True)
    g_progress_thread.start()
    log._file.debug("<< ##### Start Progress thread end ##### ")

def finish_progress() :
    log._file.debug(">> $$$$$ Finish Progress thread begin $$$$$")
    global g_progress_thread, g_task_index
    g_progress_thread.stop()
    g_progress_thread.join()
    print '%s %s: %s [Done]' %(g_progress_thread.prefix, g_progress_thread.name.ljust(spec_width, ' '), "%s"%(wait_width * '.'))
    g_task_index += 1
    g_progress_thread = None
    log._file.debug("<< $$$$$ Finish Progress thread end $$$$$")

def stop_progress() :
    log._file.debug(">> !!!!! Force stop Progress thread begin !!!!!")
    global g_progress_thread
    if g_progress_thread :
        g_progress_thread.stop()
        g_progress_thread.join()
        print
        g_progress_thread = None
    else :
        log._file.debug("Progress thread is None")
    log._file.debug("<< !!!!! Force stop Progress thread end !!!!!")


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

def saveCliPassword():
    global g_cli_password
    global g_cli_username
    saveNodeInfo("ipwcli","ipwcli",g_cli_username,g_cli_password)


def checkPassword(password):
    lower = 0
    upper = 0
    digit = 0
    special = 0
    special_character_array = list("`~!@#$%^&*()_-+={[]}|\\':;\"<,>.?/")
    for ch in list(password):
        if ch in special_character_array:
            special = 1
        elif ch.isdigit():
            digit = 1
        elif ch.islower():
            lower = 1
        elif ch.isupper():
            upper = 1
        else:
            return False, "error password, contain invalid characters"
    if(special + digit + lower + upper < 3):
        return False, """For security reasons, it is recommended that your password include at least 3 of the following 4 items: Lower case characters, Upper case characters, Numbers, Special Characters"""

    pwd_len = len(password) - 1
    if pwd_len < 7 and pwd_len > 62:
        return False, "Have minimum 8 characters and maximum 63 characters."
    for i in xrange(pwd_len):
        if i + 2 <= pwd_len:
            if password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit():
                first = int(password[i])
                second = int(password[i+1])
                third = int(password[i+2])
                if(first == second and second == third):
                    return False, "error password, three repetitive numbers"

                if i + 3 <= pwd_len and password[i + 3].isdigit():
                    fourth = int(password[i+3])
                    if(second == first + 1 and third == second + 1 and fourth == third +1):
                        return False, "error password, four consecutive numbers"
    return True, ""

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


def checkIPFormat(ip_str, isvip = False):
    if ip_str is None or ip_str == "":
        return True
    print "check ip {%r}" % ip_str
    if ip_str.find(".") != -1:
        if isValidIPv4(ip_str) is False:
            raise Exception("IP format is Error: %r" %ip_str)
    else:
        if isValidIPv6(ip_str) is False:
            raise Exception("IP format is Error: %r" %ip_str)
    if isvip:
        pass
        
    return True

def isValidIPv4(ip_str):
    if ip_str.startswith(".") or ip_str.endswith("."):
        return False
    dig_list = ip_str.split(".")
    if len(dig_list) != 4:
        return False
    for dig in dig_list:
        if not dig.isdigit():
            return False
        if int(dig) < 0 or int(dig) > 255:
            return False
    return True

def isValidIPv6(ip_str):
    hex_char = ['0','1','2','3','4','5','6','7','8','9','0','a','A','b','B','c','C','e','E','f','F']
    dig_list = ip_str.split(":")
    if ip_str.startswith(":"):
        dig_list = dig_list[1:]
    if ip_str.endswith(":"):
        dig_list = dig_list[:-1]
    isOmit = 0
    for dig in dig_list:
        if len(dig) > 4:
            return False
        if len(dig) == 0:
            if isOmit > 0:
                return False
            isOmit += 1
        for cha in dig:
            if cha not in hex_char:
                return False
    if (isOmit == 0):
        if (len(dig_list) != 8) or ip_str.startswith(":") or ip_str.endswith(":"):
            return False

    return True


