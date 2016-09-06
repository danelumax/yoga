'''
Created on 2015/04/17

@author: eyotang
'''

import re, sys, time, traceback
from optparse import OptionParser


from ipwcli import IpworksCli

import log
log.Init(True)

class ssipwcli(object):
    """
    Login SS(ipwcli) and execute the command
    """

    def __init__(self, ipwss_vip="127.0.0.1", user="admin", password="Admin123"):
        self._retry = 10
        self._cli = IpworksCli(log._file, server_ip=ipwss_vip)
        self._cli.login(user, password)
        self._fib = generatefib(self._retry)
        time.sleep(3) # wait for 3s to login

    def execute(self, cmd, expect=None):
        log._file.debug(">> ssipwcli execute Begin")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            print out
            if expect is None:
                if re.search("is not currently available\. Operation update is interrupted\.", out) == None :
                    log._file.debug("server has started")
                    break
                log._file.debug("sleep 10 seconds to wait for SM ready.")
                time.sleep(10)
            else:
                hitcount = 0
                for expect_item in expect:
                    count = None
                    if type(expect_item) is list:
                        item = expect_item[0]
                        count = expect_item[1]
                    if count is None and len(re.findall(expect_item, out)) == 0:
                        log._file.debug("Haven't found expected item:[%s] in output:[%s]" %(expect_item, out))
                        log._file.debug("sleep %s seconds to wait the result." %str(60*self._fib[retry]))
                        time.sleep(60*self._fib[retry])
                        break
                    elif count != None and len(re.findall(item, out)) != count:
                        log._file.debug("Haven't found expected item:[%s] in output:[%s], or doesn't match the count [%d]" %(item, out, int(count)))
                        log._file.debug("sleep %s seconds to wait the result." %str(60*self._fib[retry]))
                        time.sleep(60*self._fib[retry])
                        break
                    else:
                        hitcount += 1
                if hitcount == len(expect):
                    break

            retry += 1
        if self._retry == retry :
            raise Exception("Execute IPWcli command failed: " + cmd)
        log._file.debug("<< ssipwcli execute End")

    def cleanup(self):
        self._cli.logout()
        pass

def fib():
    "unbounded generator, creates Fibonacci sequence"
    x = 0
    y = 1
    while 1:
        x, y = y, x + y
        yield x

def generatefib(retry):
    g = fib()
    sequence = []
    for i in range(retry):
        sequence.append(g.next())
    return sequence

def main() :
    log._file.debug(">> Remote Call 'SS ipwcli execute' BEGIN")

    parser = OptionParser()
    parser.add_option("--ipwss_vip",
                      help="IPWorks SS virtual IP.",
                      action="store",
                      dest="ipwss_vip",
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
    parser.add_option("--command",
                      help="command list to execute.",
                      action="store",
                      dest="command",
                      default=None)

    parser.add_option("--expect",
                      help="expected result, after execute the command.",
                      action="store",
                      dest="expect",
                      default=None)


    (options, _args) = parser.parse_args(args=sys.argv)
    log._file.info("options.ipwss_vip : %s" %options.ipwss_vip)
    log._file.info("options.user      : %s" %options.user)
    log._file.info("options.command   : %s" %options.command)
    log._file.info("options.expect    : %s" %options.expect)

    task = ssipwcli(options.ipwss_vip, options.user, options.password)
    task.execute(options.command, eval(options.expect))
    task.cleanup()
    log._file.debug(">> Remote Call 'SS ipwcli execute' END")
    return 0



if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        log._cons.error(e)
        sys.exit(2)
