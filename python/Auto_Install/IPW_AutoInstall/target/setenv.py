#!/usr/bin/env python
import subprocess, sys, re, os
import logging, logging.config
import util
from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class SetEnv:

    def __init__(self) :
        self._file = "/root/.bashrc"

    def write(self) :
        if os.path.exists(self._file) == False:
            proc = subprocess.Popen(['touch', self._file])
            proc.wait()
        fc = util.readfile(self._file)
        if not re.search("setup_env\.sh", fc) :
            fc += "\nsource /opt/ipworks/IPWcommon/env/setup_env.sh >/dev/null 2 >&1\n"
        if not re.search('IPWjre/java/bin', fc) :
            fc += '\nexport PATH=/opt/ipworks/IPWjre/java/bin/:${PATH}\n'
        util.writefile(self._file, fc)

    def clean(self) :
        if os.path.exists(self._file) == False:
            return
        fc = util.readfile(self._file)
        lines = fc.splitlines()
        context = ""
        for line in lines:
            if re.search("^source /opt/ipworks/IPWcommon/env/setup_env\.sh", line) :
                continue
            if re.search('^export PATH=/opt/ipworks/IPWjre/java/bin/', line) :
                continue
            context += line
        util.writefile(self._file, context)
	

def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="write_bashrc.",
        action="store",
        dest="command",
        default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    
    logger.debug(">> Remote Call Start")
    task = SetEnv()
    if "write_bashrc" == options.command:
        task.write()
    elif "clean_bashrc" == options.command:
        task.clean()
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
