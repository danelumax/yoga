#!/usr/bin/env python

import os, re, subprocess, traceback, sys, time, shutil
import logging, logging.config
from optparse import OptionParser
from ndb import Ndb


logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigNdb:

    def __init__(self) :
        self._ndb = Ndb(logger)

    def addMip(self, hostname, ip) :
        self._ndb.addMip(hostname, ip)


    def cleanDataNode(self) :
        self._ndb.cleanDataNode()

    def addDataNode(self, datanode_id, datanode_ip) :
        self._ndb.addDataNode(datanode_id, datanode_ip)

    def configMgmd(self, mgm_mip, data_size, index_size, replicas_no) :
        self._ndb.configMgmd(mgm_mip, data_size, index_size, replicas_no)

    def startMgmd(self) :
        self._ndb.startMgmd()


    def configDataNode(self, mgm_mip) :
        self._ndb.configDataNode(mgm_mip)

    def startDataNode(self) :
        self._ndb.startDataNode()

    def checkDataNode(self) :
        self._ndb.checkDataNode()


    def configSqlNode(self, ss_vip, master_ip, server_id) :
        self._ndb.configSqlNode(ss_vip, master_ip, server_id) 

    def configMasterInfo(self, ss_vip) :
        self._ndb.configMasterInfo(ss_vip)

    def startSqlNode(self, master_ip) :
        self._ndb.startSqlNode(master_ip)
 



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="clean_datanode, add_datanode, config_sqlnode, start_mgmd, start_ndbd, start_sqlnode, config_mgm, config_mgm_ha, config_datanode, grant_innodb_previlege",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--id",
        help="id of datanode",
        action="store",
        dest="id",
        default=None)
    parser.add_option("--ip",
        help="IP address to the mgmnode/datanode/sqlnode",
        action="store",
        dest="ip",
        default=None)
    parser.add_option("--mip_name",
        help="the name to the moveable IP, dbcluster_vip/ipwsql_vip",
        action="store",
        dest="mip_name",
        default=None)
    parser.add_option("--data_mem",
        help="Data node parameters, Data Memory Size",
        action="store",
        dest="data_mem",
        default=None)
    parser.add_option("--index_mem",
        help="Data node parameters, Index Memory Size",
        action="store",
        dest="index_mem",
        default=None)
    parser.add_option("--ss_vip",
        help="clustered SS virtual ip address",
        action="store",
        dest="ss_vip",
        default=None)
    parser.add_option("--data_num",
        help="Number of datanode",
        action="store",
        dest="data_num",
        default=None)


    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.id: " + str(options.id))
    logger.info("options.ip: " + str(options.ip))
    logger.info("options.mip_name: " + str(options.mip_name))
    logger.info("options.data_mem: " + str(options.data_mem))
    logger.info("options.index_mem: " + str(options.index_mem))
    logger.info("options.ss_vip: " + str(options.ss_vip))
    logger.info("options.data_num: " + str(options.data_num))
    
    logger.debug(">> Remote Call Start")
    task = ConfigNdb()
    if options.command == 'clean_datanode' :
        task.cleanDataNode()
    elif options.command == 'add_datanode' :
        task.addDataNode(options.id, options.ip)
    elif options.command == 'start_mgmd' :
        task.startMgmd()
    elif options.command == 'start_ndbd' : 
        task.startDataNode()
    elif options.command == 'check_ndbd' : 
        task.checkDataNode()
    elif options.command == 'start_sqlnode' : 
        task.startSqlNode(options.ss_vip)
    elif options.command == 'config_mgmd' :
        task.configMgmd(options.ip, options.data_mem, options.index_mem, options.data_num)
    elif options.command == 'config_ndbd' :
        task.configDataNode(options.ip)
    elif options.command == 'config_sqlnode' : 
        task.configSqlNode(options.ss_vip, options.ip, options.id)
    elif options.command == 'config_masterinfo' : 
        task.configMasterInfo(options.ss_vip)
    elif options.command == 'add_mip' :
        task.addMip(options.mip_name, options.ip)
    elif options.command == 'grant_innodb_previlege' :
        task.grantInnodbPrivilege(options.ip, options.ss_vip)
    else :
        raise Exception("unknow command")
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)




