import subprocess
import pexpect
import log


class Scp :

    def __init__(self, ip, port=22, username="root", password="root000") :
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password


    def copy_to(self, src, dst) :
        command = "scp -P " + str(self._port) + " " + src + " " + self._username + "@" + self._ip + ":" + dst
        log._file.debug("Exec cmd: \n%s" %command)    
        console = pexpect.spawn(command, timeout=300) 
        ret = console.expect(["assword: ", "Are you sure you want to continue connecting (yes/no)?", pexpect.EOF, pexpect.TIMEOUT])
        if ret == 1 : 
            console.sendline("yes")
            ret = console.expect(["Password: ", pexpect.EOF, pexpect.TIMEOUT])
        if ret == 0 :
            console.sendline(self._password)
            console.expect([pexpect.EOF])
            log._file.debug("return info: %s" %console.before)
            proc = subprocess.Popen(["echo $?"], stdout=subprocess.PIPE, shell=True)
            proc.wait()
            ret = int(proc.stdout.read())
            log._file.debug("return code: " + str(ret))
            if ret != 0:
                raise Exception("Exception -- failed execute Command: " + command)
        else :
            raise Exception("Exception -- can not copy file with the command: " + command)
     
        console.close()




