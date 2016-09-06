#!/usr/bin/env python
import subprocess, sys
import logging, logging.config

from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class SetHacluserPasswd(object):

    def __init__(self) :
        pass

    def execute(self, password) :
        proc = subprocess.Popen(["passwd", "hacluster"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(password + "\n")
        proc.stdin.write(password + "\n")
        proc.stdin.flush()
        proc.communicate()
        proc.wait()
        return 0



def main() :
    parser = OptionParser()
    parser.add_option("--passwd",
                      help="the password of the ha cluster user",
                      action="store",
                      dest="password",
                      default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.password: " + str(options.password))
    
    logger.debug(">>> Remote Call Start")
    task = SetHacluserPasswd()
    task.execute(options.password)
    logger.debug("<<< Remote Call End")
    return 0
 
 
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)

