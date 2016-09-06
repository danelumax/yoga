#!/usr/bin/env python
import subprocess, sys, re, os
import logging, logging.config

from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")

class RpmInstaller :

    def __init__(self) :
        pass

    def execute(self, mount_point, name, sub_module, is_shell) :
        os.chdir(mount_point + "/x86-linux/" + name + "/")
        ret = 0
        if sub_module :
            command = ["./install", sub_module]
            console = subprocess.Popen(command, shell=is_shell)
        else :
            console = subprocess.Popen(["./install"], shell=is_shell)
        ret = console.wait()
        return ret
 



def main() :
    parser = OptionParser()
    parser.add_option("--mount_point",
        help="the path to the mount point.",
        action="store",
        dest="mount_point",
        default=None)
    parser.add_option("--name",
        help="name of the installation package.",
        action="store",
        dest="name",
        default=None)
    parser.add_option("--sub_module",
        help="name of the sub module.",
        action="store",
        dest="sub_module",
        default=None)
    parser.add_option("--shell",
        help="legacy IPWorks ....",
        action="store_true",
        dest="shell",
        default=False)
 
    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.mount_point: " + str(options.mount_point))
    logger.info("options.name: " + str(options.name))
    logger.info("options.sub_module: " + str(options.sub_module))
    logger.info("options.shell: " + str(options.shell))
    
    logger.debug(">> Remote Call Start")
    task = RpmInstaller()
    ret = task.execute(options.mount_point, options.name, options.sub_module, options.shell)
    logger.debug("<< Remote Call End")
    return ret
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)



