#!/usr/bin/env python
import subprocess, sys, re, os
import logging, logging.config

from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class MountIso:
    def __init__(self) :
        pass

    def execute(self, mount_point, iso_path) :
        proc = subprocess.Popen(["mount"], stdout=subprocess.PIPE)
        proc.wait()
        line = proc.stdout.readline()
        if '/' == mount_point[-1]:
            mount_point = mount_point[0:-1]
        while line :
            if re.search(mount_point + " type iso9660", line) :
                logger.debug("exec cmd: umount " + mount_point)
                proc = subprocess.Popen(["umount", mount_point], stdout=subprocess.PIPE)
                proc.wait()
                break
            line = proc.stdout.readline()

        if not os.path.exists(mount_point) :
            os.mkdir(mount_point)

        proc = subprocess.Popen(["mount", "-o", "loop", iso_path, mount_point])
        proc.wait()
        return 0


def main() :
    parser = OptionParser()
    parser.add_option("--mount_point",
        help="the path to the mount point.",
        action="store",
        dest="mount_point",
        default=None)
    parser.add_option("--iso_path",
        help="the path to the ISO file.",
        action="store",
        dest="iso_path",
        default=None)
 
    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.mount_point: " + str(options.mount_point))
    logger.info("options.iso_path: " + str(options.iso_path))
    
    logger.debug(">> Remote Call Start")
    task = MountIso()
    task.execute(options.mount_point, options.iso_path)
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
