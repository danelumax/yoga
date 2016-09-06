#!/usr/bin/env python
import subprocess, sys, re, os, time
import logging, logging.config
import util
from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")

class ConfigCrm:

    def __init__(self) :
        pass

    def configCrm(self, conf_file) :
        logger.debug(">> conf_file = " + conf_file)
        proc = subprocess.Popen(["crm", "configuration"], stdin=subprocess.PIPE)
        context = util.readfile(conf_file)
        proc.stdin.write("erase\n")
        proc.stdin.flush()
        proc.stdin.write(context)
        proc.stdin.write("\ncommit\n")
        proc.stdin.flush()
        proc.stdin.write("exit\n")
        proc.stdin.flush()
        proc.communicate()
        logger.debug("<<")


    def resetCrm(self):
        logger.debug(">> Reset crm configuration")
        proc = subprocess.Popen(["crm", "configuration"], stdin=subprocess.PIPE)
        proc.stdin.write("erase\n")
        proc.stdin.flush()
        proc.stdin.write("\ncommit\n")
        proc.stdin.flush()
        proc.stdin.write("exit\n")
        proc.stdin.flush()
        proc.communicate()
        logger.debug("<<")


def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="config_crm, reset_crm",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--conf_file",
        help="the CRM configuration file.",
        action="store",
        dest="conf_file",
        default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.conf_file: " + str(options.conf_file))
    
    logger.debug(">> Remote Call Start")
    task = ConfigCrm()
    if options.command == "config_crm":
        task.configCrm(options.conf_file)
    elif options.command == "reset_crm":
        task.resetCrm()
    logger.debug("<< Remote Call End")
    return 0
 
 

if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)

