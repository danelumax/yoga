import pexpect

IPWCLI = "/opt/ipworks/IPWcli/scripts/ipwcli"

class IpworksCli :

    def __init__(self, logger, server_ip='127.0.0.1') :
        self._cli = None
        self._logger = logger
        self._ipwcli = IPWCLI
        self._server_ip = server_ip


    def login(self, user="admin", password="Admin123") :
        cmd = self._ipwcli + " -server=" + self._server_ip
        self._logger.debug("login CLI cmd: \n" + cmd)
        self._cli = pexpect.spawn(cmd, timeout=600)
        self._cli.expect("IPWorks> Login:")
        self._cli.sendline(user)
        self._cli.expect("IPWorks> Password:")
        self._cli.sendline(password)
        self._cli.expect("IPWorks>")


    def logout(self) :
        self._cli.sendline("exit")


    def execute(self, command, debug_print=True) :
        self._logger.debug("cli exec cmd: " + command)
        self._cli.sendline(command)
        expect_list = ["IPWorks>"]
        self._logger.debug("Blocked to wait for %s" %expect_list)
        ret = self._cli.expect(expect_list, timeout=None) # ignore a timeout and block indefinitely
        self._logger.debug("cli return info:\n#%d#%s" %(ret, self._cli.before))
        return self._cli.before

