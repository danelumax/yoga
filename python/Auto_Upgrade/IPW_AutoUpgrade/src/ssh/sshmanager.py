import pxssh
import log
from sshutil import SshUtil

def sshManagerInstance() :
    try :
        inst = SshManager()
    except SshManager as conn:
        inst = conn
    return inst

def obfuscate(password):
    length = len(password)
    if length < 2:
        return password+'*'
    else:
        return password[0]+'*'*(length-1)

class SshManager :

    __instance = None


    def __init__(self) :
        if SshManager.__instance :
            raise SshManager.__instance
        self._ssh_list = {}
        SshManager.__instance = self


    def connect(self, name, ssh_ip, ssh_port, username, password) :
        if name not in self._ssh_list : 
            s = pxssh.pxssh(timeout=6000)
            log._file.debug("host_name = " + name)
            log._file.debug("ssh_ip = " + ssh_ip)
            log._file.debug("ssh_port = " + str(ssh_port))
            log._file.debug("ssh_username = " + username)
            log._file.debug("ssh_password = " + obfuscate(password))
            if not s.login(server=ssh_ip, port=ssh_port, username=username, password=password):
                log._file.error('login failed on ' + ssh_ip)
                raise Exception("Exception: cannot ssh to the node (" + ssh_ip + ":" + str(ssh_port) + ")")

            self._ssh_list[name] = {'conn' : s, 'ip' : ssh_ip, 'port' : ssh_port, 'username' : username, 'password' : password}

            log._file.debug("connect to " + name + "(" + ssh_ip + ") successfully")
            return s
        else :
            return self._ssh_list[name]['conn']



    def reconnect(self, ssh) :
        ssh['conn'] = pxssh.pxssh(timeout=6000)
        log._file.debug("Try to Relogin " + ssh['ip'])
        if not ssh['conn'].login(server=ssh['ip'], port=ssh['port'], username=ssh['username'], password=ssh['password']):
            log._file.error('relogin failed:' + str(ssh['conn']))
            raise Exception("Exception: cannot ressh to the node (" + ssh['ip'] + ":" + int(ssh['port']) + ")")



    def destory(self) :
        for name in self._ssh_list :
            self._ssh_list[name]['conn'].logout()
            log._file.debug("Disconnect with host [%s:%s]" %(name, self._ssh_list[name]['ip']))
        self._ssh_list = {}


    def getSsh(self, name) :
        if name in self._ssh_list :
            ssh = self._ssh_list[name]
            ssh_util = SshUtil(ssh['conn'])
            try : 
                res, r_code = ssh_util.remote_exec("id", p_out=False, p_err=False) 
            except Exception as e:
                log._file.warning("Need to relogin " + ssh['ip'])
                self.reconnect(ssh)
            return self._ssh_list[name]['conn']
        raise Exception("Exception: cannot find ssh (" + name + ")")


    def trySsh(self, name) :
        if name in self._ssh_list :
            log._file.debug("Try to SSH on " + name)
            ssh = self._ssh_list[name]
            try : 
                ssh['conn'] = pxssh.pxssh(timeout=6000)
                if not ssh['conn'].login(server=ssh['ip'], port=ssh['port'], username=ssh['username'], password=ssh['password']):
                    log._file.debug("Can't SSH on " + name)
                    return False
                else :
                    ssh_util = SshUtil(ssh['conn'])
                    ssh_util.remote_exec("id", p_err=False)
                    log._file.debug("Can Successfully SSH on " + name) 
                    return True
            except Exception as e:
                log._file.warning("Try to SSH login " + ssh['ip'] + " Failed")
                return False




