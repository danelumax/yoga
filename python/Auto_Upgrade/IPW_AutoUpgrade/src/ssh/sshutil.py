import sys
import log
import re


class SshUtil :

    def __init__(self, ssh, ip=None, logger=None) :
        self._conn = ssh
        self._ip = ip
        if logger :
            self._log = logger
        else :
            self._log = log._file

    def obfuscate_passwd(self, command):
        def obfuscate(password):
            length = len(password)
            if length < 2:
                return password+'*'
            else:
                return password[0]+'*'*(length-1)

        def repl(m):
            if m.group(2):
                return "%s=%s" % (m.group(1), obfuscate(m.group(2)))
            return m.group(1)

        keywords = ['password', 'passwd'] # extend it in future, if neccessary.
        return re.sub(r"(%s)=(\S+)" % '|'.join(keywords), repl, command)

    #==============================================================================
    # Execute command in a remote host
    #==============================================================================
    def remote_exec(self, command, p_out=True, p_err=True, throw=True, wait=0):
        if not self._conn :
            self._log.error("ssh connection is not initialized!")
        res = ""
        r_code = 0
        if p_out :
            self._log.debug("Exec cmd: \n" + self.obfuscate_passwd(command))
        try:
            self._conn.prompt(1)   # wait for 1 second
            self._conn.sendline("stty -echo") # don't echo input characters
            self._conn.prompt()
            self._conn.sendline(command)
            self._conn.prompt(-1)  # wait for prompt
            res = self._conn.before.strip()
            if p_out:
                self._log.debug("return info:\n%s" %res)

            if wait > 0 :
                self._conn.prompt(wait)
                res = self._conn.before.strip()
                self._log.debug("retry return info:\n%s" %res)

            self._conn.prompt(1)
            self._conn.sendline("echo $?")
            self._conn.prompt(-1)
            output = self._conn.before.strip()
            lineList = output.split("\n")
            for line in lineList:
                if line.isdigit():
                    r_code = int(line)
        except Exception as e:
            if p_err :
                self._log.error("Execute command: *** " + self.obfuscate_passwd(command) + " *** failed")
                self._log.error("Error info: " + str(e))
            res = None
            r_code = 1
            if throw :
                raise Exception("Failed to execute command: " + self.obfuscate_passwd(command))

        if p_out:
            #self._log.debug("return info:\n%s" %res)
            self._log.debug("return code: %d" %r_code)

        if r_code != 0 and p_err :
            self._log.error("Failed to execute command (on " + str(self._ip) + "): " + self.obfuscate_passwd(command))

        if r_code != 0 and throw :
            raise Exception("Failed to execute command (on " + str(self._ip) + "): " + self.obfuscate_passwd(command))

        return res, r_code



