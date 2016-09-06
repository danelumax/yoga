#!/usr/bin/env python
import subprocess, sys, re, os
import logging, logging.config

from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class CheckEMC:
    def __init__(self) :
        pass

    def execute(self,emc_ip) :
        proc = subprocess.Popen(["ping","-c 3",str(emc_ip)], stdout=subprocess.PIPE)
        proc.wait()
        line = proc.stdout.readline()
        while line:
            if(-1 != line.find('0 received')):
                logger.debug("The connection to "+str(emc_ip)+" does not work! Please check it !")
                return -1;
            line = proc.stdout.readline()
        logger.debug("The connection to "+str(emc_ip)+" works well!")
        return 0


def main() :
    parser = OptionParser()
    parser.add_option("--emc_ip",
        help="the emc address",
        action="store",
        dest="emc_ip",
        default=None)
 
    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.emc_ip: " + str(options.emc_ip))
    
    logger.debug(">> Remote Call Start")
    task = CheckEMC()
    result = task.execute(options.emc_ip)
    logger.debug("<< Remote Call End")
    return result
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
