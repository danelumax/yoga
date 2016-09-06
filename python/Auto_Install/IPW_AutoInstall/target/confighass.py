#!/usr/bin/env python

import os, re, subprocess, traceback, sys, time, shutil
import pexpect, util
import logging, logging.config
from optparse import OptionParser



logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigHaSsTask :

    def __init__(self) :
        pass

    def addHost(self, hostname, ip) :
        logger.debug(">> hostname = " + str(hostname) + ', ip = ' + str(ip))
        file_name = '/etc/hosts'
        lines = util.readfilelines(file_name)
        context = ''
        for line in lines :
            if not re.search('\s' + hostname + '\s', line) :
                context = context + line
        context = context + ip + ' ' + hostname + '\n'
        util.writefile(context)
        logger.debug("<<")
 
    def modifyTomcatStartTimeout(self) :
        logger.debug(">>")
        proc = subprocess.Popen(['cibadmin', '-Q', '--scope', 'resources'], stdout=subprocess.PIPE)
        proc.wait()
        tmp_cib_file_path = '/tmp/cibtomcat.xml'
        fd = open(tmp_cib_file_path, 'w')
        line = proc.stdout.readline()
        while line :
            fd.write(line)
            if re.search('<operations id="res-ipwss-tomcat-operations">', line) :
                fd.write('<op id="res-ipwss-tomcat-op-start-0" interval="0" name="start" timeout="120s"/>')
            line = proc.stdout.readline()
        fd.close()
        proc = subprocess.Popen(['cibadmin', '--replace', '--scope', 'resources', '--xml-file', tmp_cib_file_path])
        proc.wait()
        logger.debug("<<")




def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="add_host, modify_tomcat_start_timeout",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--hostname",
        help="hostname",
        action="store",
        dest="hostname",
        default=None)
    parser.add_option("--ip",
        help="IP address to the hostname",
        action="store",
        dest="ip",
        default=None)



    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.hostname: " + str(options.hostname))
    logger.info("options.ip: " + str(options.ip))
    
    logger.debug(">> Remote Call Start")
    task = ConfigHaSsTask()
    if options.command == "add_host" :
        task.addHost(options.hostname, options.ip)
    elif options.command == 'modify_tomcat_start_timeout' :
        task.modifyTomcatStartTimeout()
    else :
        pass
    logger.debug("<< Remote Call End")
    return 0
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print  str(e)
        sys.exit(2)
