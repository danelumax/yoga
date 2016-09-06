import re, sys, time, traceback
from optparse import OptionParser


from ipwcli import IpworksCli

import log
log.Init(True)

class checkipwcliserver(object):
    """
    Login SS(ipwcli) and execute the command
    """

    def __init__(self, ipwss_ip="127.0.0.1", user="admin", password="Admin123"):
        self._retry = 10
        self._cli = IpworksCli(log._file, server_ip=ipwss_ip)
        self._cli.login(user, password)

    def execute(self, cmd, oamip,flag):
        log._file.debug(">>")
        out = self._cli.execute(cmd)
        result1 = re.search(oamip, out)
        if (not result1) and (flag == "NO"):
            raise Exception("Execute the command failed :" + cmd)
        elif (result1) and (flag == "YES"):
            log._all.error("ps name exists in cli,please configure it")
            sys.exit(1)

        log._all.debug("Execute the command succeed!:" + cmd)
        log._file.debug("<<")

    def cleanup(self):
        self._cli.logout()
        pass

def main() :
    log._all.debug(">> Remote Call begin")

    parser = OptionParser()
    parser.add_option("--ipwss_ip",
                      help="IPWorks SS  IP.",
                      action="store",
                      dest="ipwss_ip",
                      default=None)
    parser.add_option("--user",
                      help="admin user to login ipwcli.",
                      action="store",
                      dest="user",
                      default=None)
    parser.add_option("--password",
                      help="password for admin user to login ipwcli.",
                      action="store",
                      dest="password",
                      default=None)
    parser.add_option("--oamip",
                      help="oamip for server",
                      action="store",
                      dest="oamip",
                      default=None)
    parser.add_option("--flag",
                      help="oamip for server",
                      action="store",
                      dest="flag",
                      default=None)
    parser.add_option("--command",
                      help="command list to execute.",
                      action="store",
                      dest="command",
                      default=None)

    (options, _args) = parser.parse_args(args=sys.argv)
    log._all.info("Parse options.ipwss_ip:%s options.user:%s options.password:%s options.oamip:%s options.flag:%s options.command:%s" %(options.ipwss_ip, options.user, "********",options.oamip,options.flag,options.command))

    task = checkipwcliserver(options.ipwss_ip, options.user, options.password)
    task.execute(options.command,options.oamip,options.flag)
    task.cleanup()
    log._all.debug(">> Remote Call 'SS ipwcli execute' END")
    return 0



if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        log._cons.error(e)
        sys.exit(2)
