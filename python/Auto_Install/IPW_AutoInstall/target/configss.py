#!/usr/bin/env python

import os, re, subprocess, traceback, sys, time, shutil
import pexpect
import logging, logging.config
from optparse import OptionParser



logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigSs:
    def __init__(self,cli_username, cli_password) :
        '''
        Constractor
        '''
        self._cli_username = cli_username
        self._cli_password = cli_password

    def initMysqlDb(self) :
        logger.debug(">> start to init the database ipworks")
        command = "/opt/ipworks/IPWss/db/init_mysql_db"
        while True :
            proc = pexpect.spawn(command, timeout=300)
            index = proc.expect(["Storage Server Username:", "Network I/O Error"])
            logger.debug("index = " + str(index))        
            logger.debug("get the prompt 'Storage Server Username:'")
            logger.debug("return info: \n" + proc.before)
            if index == 0 :
                break
            time.sleep(1)
        proc.sendline(self._cli_username)
        proc.expect("Password:")
        logger.debug("get the prompt 'Password:'")
        logger.debug("return info: \n" + proc.before)
        proc.sendline(self._cli_password)
        proc.expect("Password \(again\):")
        logger.debug("get the prompt 'Password (again):'")
        logger.debug("return info: \n" + proc.before)
        proc.sendline(self._cli_password)
        proc.expect("Exiting.")
        logger.debug("return info: \n" + proc.before)
        logger.debug("<<")
 



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="init_mysql_db",
        action="store",
        dest="command",
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

    
    logger.debug(">> Remote Call Start")
    task = ConfigSs(options.username, options.password)
    if options.command == "init_mysql_db" :
        task.initMysqlDb()
    logger.debug("<< Remote Call End")
    return 0
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
