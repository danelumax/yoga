#!/usr/bin/env python

import os, re, sys, subprocess, time
import logging, logging.config
from optparse import OptionParser
import util

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class ConfigSnmp:

    def __init__(self):
        self._conf = '/etc/ipworks/ipworks_snmp.conf'

    def _config(self, mgm_vip):
        logger.debug(">> config snmp")
        tmp = util.readfilelines(self._conf)
        fcontext = ""
        for s in tmp:
            if re.search("SNMP_MANAGE_NODE_IPLIST=", s):
                index = s.find("SNMP_MANAGE_NODE_IPLIST=")
                ss = s[0:index] + "SNMP_MANAGE_NODE_IPLIST=" + mgm_vip
                logger.debug("replace as: " + ss)
                fcontext += ss
            else:
                fcontext += s
        util.writefile(self._conf, fcontext)
        logger.debug("<<")



def main() :
    parser = OptionParser()
    parser.add_option("--mgm_vip",
        help="dbcluster vip",
        action="store",
        dest="dbcluster_vip",
        default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.dbcluster_vip: " + str(options.dbcluster_vip))

    logger.debug(">> Remote Call Start")
    task = ConfigSnmp()
    task._config(options.dbcluster_vip)
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)




