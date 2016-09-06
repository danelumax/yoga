#!/usr/bin/env python

import os, sys 
import logging, logging.config
from optparse import OptionParser
from sm import Sm

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigSmTask :
    def __init__(self, cli_username, cli_password) :
        self._sm = Sm(logger)
        self._cli_username = cli_username
        self._cli_password = cli_password


    def config(self, ipwss_vip) :
        logger.debug(">>")
        self._sm.config(self._cli_username,self._cli_password, ipwss_vip)
        logger.debug("<<")
      
    def start(self) :
        logger.debug(">>")
        self._sm.start()
        logger.debug("<<")

    def stop(self) :
        logger.debug(">>")
        self._sm.stop()
        logger.debug("<<")


    def start_dnssm(self) :
        logger.debug(">>")
        self._sm.start_sm("DNS")
        logger.debug("<<")

    def stop_dnssm(self) :
        logger.debug(">>")
        self._sm.stop_sm("DNS")
        logger.debug("<<")


    def start_enumsm(self) :
        logger.debug(">>")
        self._sm.start_sm("ENUMSERVER")
        logger.debug("<<")

    def stop_enumsm(self) :
        logger.debug(">>")
        self._sm.stop_sm("ENUMSERVER")
        logger.debug("<<")


    def start_dhcpv4sm(self) :
        logger.debug(">>")
        self._sm.start_sm("DHCPv4")
        logger.debug("<<")

    def stop_dhcpv4sm(self) :
        logger.debug(">>")
        self._sm.stop_sm("DHCPv4")
        logger.debug("<<")


    def start_aaasm(self) :
        logger.debug(">>")
        self._sm.start_sm("AAA")
        logger.debug("<<")

    def stop_aaasm(self) :
        logger.debug(">>")
        self._sm.stop_sm("AAA")
        logger.debug("<<")



def main() :

    parser = OptionParser()
    parser.add_option("--command",
        help="config, start",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--ipwss_vip",
        help="IP address of storage server",
        action="store",
        dest="ipwss_vip",
        default=None)
    parser.add_option("--password",
        help="ipwcli password, necessary",
        action="store",
        dest="password",
        default=None)
    parser.add_option("--username",
        help="ipwcli username, necessary",
        action="store",
        dest="username",
        default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.ipwss_vip: " + str(options.ipwss_vip))
    
    logger.debug(">> Remote Call Start")
    task = ConfigSmTask(options.username, options.password)
    if options.command == "config" :
        task.config(options.ipwss_vip)
    elif options.command == "start" :
        task.start()
    elif options.command == "stop" :
        task.stop()
    elif options.command == "start_dnssm" :
        task.start_dnssm()
    elif options.command == "stop_dnssm" :
        task.stop_dnssm()
    elif options.command == "start_enumsm" :
        task.start_enumsm()
    elif options.command == "stop_enumsm" :
        task.stop_enumsm()
    elif options.command == "start_dhcpv4sm" :
        task.start_dhcpv4sm()
    elif options.command == "stop_dhcpv4sm" :
        task.stop_dhcpv4sm()
    elif options.command == "start_aaasm" :
        task.start_aaasm()
    elif options.command == "stop_aaasm" :
        task.stop_aaasm()
    logger.debug("<< Remote Call End")
    return 0
 
 
 
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
