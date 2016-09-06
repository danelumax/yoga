#!/usr/bin/env python

import os, re, subprocess, traceback, sys, time, shutil
import logging, logging.config
from optparse import OptionParser
import util


logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigSlm:

    def __init__(self) :
        self._license_file = "trial_license.per"


    def startServer(self, license) :
        logger.debug('>> Start License Server')
        # copy license file
        shutil.copy2(license, "/etc/ipworks/slm/")
        # config license server
        file_name = '/etc/ipworks/ipworks_slm.conf'
        tmp = util.readfilelines(file_name)
        info = ''
        for x in tmp:
            if re.search('License.File=', x):
                info += "License.File=%s\n" %(license)
            else:
                info += x
        util.writefile(file_name, info)
        # start license server
        proc = subprocess.Popen(["/etc/init.d/ipworks.slm", "start"])
        proc.wait()
        time.sleep(5)
        if not util.check_process('/opt/ipworks/IPWslm/usr/bin/lserv_sn', "start"):
            raise Exception("License Server doesn't Started !")
        logger.debug('<<')


    def configClient(self, primary_ip, secondary_ip) :
        logger.debug('>> Config License Client')
        file_name = '/etc/ipworks/ipworks_slm_client.conf'
        tmp = util.readfilelines(file_name)
        info = ''
        for x in tmp:
            if re.search('Primary.Server=', x):
                if primary_ip != None :
                    info += "Primary.Server=%s\n" %(primary_ip)
                else:
                    info += x
            elif re.search('Secondary.Server=', x):
                if secondary_ip != None :
                    info += "Secondary.Server=%s\n" %(secondary_ip)
                else:
                    info += x
            else :
                info += x
        util.writefile(file_name, info)
        logger.debug('<<')
 

def main() :
    parser = OptionParser()
    parser.add_option("--role",
        help="server/client",
        action="store",
        dest="role",
        default=None)
    parser.add_option("--license",
        help="license file",
        action="store",
        dest="license",
        default=None)
    parser.add_option("--primary_ip",
        help="IP address of the primary SLM server",
        action="store",
        dest="primary_ip",
        default=None)
    parser.add_option("--secondary_ip",
        help="IP address of the second SLM server",
        action="store",
        dest="secondary_ip",
        default=None)



    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.role: " + str(options.role))
    logger.info("options.license: " + str(options.license))
    logger.info("options.primary_ip: " + str(options.primary_ip))
    logger.info("options.secondary_ip: " + str(options.secondary_ip))
    
    logger.debug(">> Remote Call Start")
    task = ConfigSlm()
    if options.role == "server" :
        task.startServer(options.license)
    else:
        task.configClient(options.primary_ip, options.secondary_ip)
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
