import pexpect
import util


class IpworksCli :

    def __init__(self,username,password, logger, server_ip='127.0.0.1') :
        self._cli = None
        self._logger = logger
        self._server_ip = server_ip
        self._cli_username = username
        self._cli_password = password


    def login(self) :
        cmd = "/opt/ipworks/IPWcli/scripts/ipwcli -server=" + self._server_ip
        self._logger.debug("login CLI cmd: \n" + cmd)
        self._cli = pexpect.spawn(cmd, timeout=600)
        self._cli.expect("IPWorks> Login:")
        self._cli.sendline(self._cli_username)
        self._cli.expect("IPWorks> Password:")
        self._cli.sendline(self._cli_password)
        self._cli.expect("IPWorks>")


    def logout(self) :
        self._cli.sendline("exit")


    def execute(self, command, debug_print=True) :
        self._logger.debug("cli exec cmd: " + command)
        self._cli.sendline(command)
        expect_list = ["IPWorks>"]
        ret = self._cli.expect(expect_list)
        self._logger.debug("cli return info:\n#%d#%s" %(ret, self._cli.before))
        return self._cli.before
    def getEncryptPassword(self):
        util.ipworksEncryptPassword(self._cli_password)
