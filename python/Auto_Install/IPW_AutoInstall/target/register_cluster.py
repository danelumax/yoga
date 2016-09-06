#!/usr/bin/env python

import os, sys, subprocess, time
import pexpect
import logging, logging.config
from optparse import OptionParser
from sm import Sm

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class RegisterCluster :

    def __init__(self, mode, passwd) :
        self._mode = mode
        self._ss1_pwd = ''
        self._ss2_pwd = ''
        self._ps1_pwd = ''
        self._ps2_pwd = ''
        self._slm_prim = ''
        self._slm_seco = ''
        self.parse_password(passwd)

    def register_ss(self, has_prov_vip=False) :
        logger.debug(">> Register SS Resource Group")
       
        cmd = '/opt/ipworks/IPWhaagents/scripts/register_cluster.pl'        

        args = [ cmd, '--%s'%(self._mode) ]        
        if has_prov_vip: args += ['--pro']

        logger.info("Exec cmd: %s" %(' '.join(args)))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        logger.debug("<<")
      
    def register_ndbcluster(self) :
        logger.debug(">> Register ndbcluster Resource Group")
        logger.info("Exec cmd: /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --%s" %(self._mode))
        proc = subprocess.Popen(['/opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl', '--%s' %(self._mode)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('%s\n' %(self._ps1_pwd))
        proc.stdin.write('%s\n' %(self._ps2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        logger.debug("<<")

    def register_csvengine2(self, mgm_vip) :
        logger.debug(">> Register csvengine Resource Group")
        cmd = '/opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --%s --ndb-mgm-vip %s' %(self._mode, mgm_vip)
        logger.info('Exec cmd: ' + cmd)
        cli = pexpect.spawn(cmd)
        ret = cli.expect(['(?i)root password:', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        #logger.info('-------111 ret = %d-------' %(ret))
        print(cli.before)
        cli.sendline(self._ss1_pwd)
        ret = cli.expect(['(?i)root password:', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        #logger.info('-------222 ret = %d-------' %(ret))
        print(cli.before)
        cli.sendline(self._ss2_pwd)
        ret = cli.expect(['(?i)Do you want to continue[Y|N]', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        #logger.info('-------333 ret = %d-------' %(ret))
        print(cli.before)
        cli.sendline('Y')
        ret = cli.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=60.0)
        #logger.info('-------444 ret = %d-------' %(ret))
        print(cli.before)
        logger.info('#################################')
        cli.close()
        logger.debug("<<")

    def register_csvengine(self, mgm_vip) :
        logger.debug(">> Register csvengine Resource Group")
        logger.info("Exec cmd: /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --%s --ndb-mgm-vip %s" %(self._mode, mgm_vip))
        proc = subprocess.Popen(['/opt/ipworks/IPWhaagents/scripts/register_csvengine.pl', '--%s' %(self._mode), '--ndb-mgm-vip', mgm_vip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        logger.debug("<<")

    def register_clf(self, slm_ip, clf_dev) :
        logger.debug(">> Register CLF Resource Group")
        self.parse_slm_ip(slm_ip)
        if not cmp('nfs', self._mode) :
            cmd = "/opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --%s" %(self._mode)
        else :
            cmd = "/opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --CLFdevice=%s" %(clf_dev)
        logger.info("Exec cmd: " + cmd)
        cli = pexpect.spawn(cmd)
        ret = cli.expect(['(?i)(?:are) you sure you want to continue connecting', "(?i)(?:password): ", pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        #logger.info('-------111 ret = %d-------' %(ret))

        if 0 == ret :
            logger.info(cli.before)
            cli.sendline('yes')
            ret = cli.expect(['(?i)(?:are) you sure you want to continue connecting', "(?i)(?:password): ", pexpect.TIMEOUT, pexpect.EOF])
            #logger.info('-------222 ret = %d-------' %(ret))
        if 1 == ret :
            logger.info(cli.before)
            cli.sendline(self._ps2_pwd)
            ret = cli.expect(['(?i)Primary License Server Address', pexpect.TIMEOUT, pexpect.EOF])
            #logger.info('-------333 ret = %d-------' %(ret))
        else :
            raise Exception("Failed to login PS2 while register clf resource")
        
        if 0 == ret :
            logger.info(cli.before)
            cli.sendline(self._slm_prim)
            ret = cli.expect(["(?i)Secondary License Server Address", pexpect.TIMEOUT, pexpect.EOF])
            #logger.info('-------444 ret = %d-------' %(ret))
        else :
            raise Exception("Failed to input Primery License Server IP while register clf resource")
        
        if 0 == ret :
            logger.info(cli.before)
            cli.sendline(self._slm_seco)
            ret = cli.expect([pexpect.TIMEOUT, pexpect.EOF])
            #logger.info('-------555 ret = %d-------' %(ret))
        else :
            raise Exception("Failed to input Secondry License Server IP while register clf resource")

        logger.info(cli.before)
        cli.close()
        logger.debug("<<")


    def parse_slm_ip(self, ip) :
        logger.debug(">> Parse License Server IP")
        tmp = ip.split(',')
        self._slm_prim = tmp[0]
        print self._slm_prim
        self._slm_seco = tmp[1]
        print self._slm_seco
        logger.debug("<<")


    def parse_password(self, passwd) :
        logger.debug(">> Parse Password")
        tmp = passwd.split(',')
        print str(tmp)
        if 2 == len(tmp) :
            self._ss1_pwd = tmp[0]
            self._ss2_pwd = tmp[1]
        elif 4 == len(tmp) :
            self._ss1_pwd = tmp[0]
            self._ss2_pwd = tmp[1]
            self._ps1_pwd = tmp[2]
            self._ps2_pwd = tmp[3]
        elif 1 == len(tmp) :
            self._ps2_pwd = tmp[0]
        else :
            raise Exception("Password is incorrect: " + passwd)
        logger.debug("<<")




def main() :

    parser = OptionParser()
    parser.add_option("--password",
        help="SS & PS password",
        action="store",
        dest="password",
        default=None)
    parser.add_option("--command",
        help="ss, ndbcluster, csvengine",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--mode",
        help="nfs, diskarray",
        action="store",
        dest="mode",
        default=None)
    parser.add_option("--mgm_vip",
        help="ndb mgm vip",
        action="store",
        dest="mgm_vip",
        default=None)
    parser.add_option("--slm_ip",
        help="license server ip",
        action="store",
        dest="slm_ip",
        default=None)
    parser.add_option("--clf_dev",
        help="CLF Device",
        action="store",
        dest="clf_dev",
        default=None)
    parser.add_option("--has_prov_vip",
        help="add HA primitive  res-ipwprov-vip",
        action="store_true",
        dest="has_prov_vip",
        default=False)

    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.password: " + str(options.password))
    logger.info("options.command: " + str(options.command))
    logger.info("options.mode: " + str(options.mode))
    logger.info("options.mgm_vip: " + str(options.mgm_vip))
    logger.info("options.slm_ip: " + str(options.slm_ip))
    logger.info("options.clf_dev: " + str(options.clf_dev))
    logger.info("options.has_prov_vip: %s" %(options.has_prov_vip))
    
    logger.debug(">> Remote Call Start")
    task = RegisterCluster(options.mode, options.password)
    if options.command == "ss" :
        task.register_ss(has_prov_vip=options.has_prov_vip)
    elif options.command == "ndbcluster" :
        task.register_ndbcluster()
    elif options.command == "csvengine" :
        task.register_csvengine(options.mgm_vip)
    elif options.command == "clf" :
        task.register_clf(options.slm_ip, options.clf_dev)
    else :
        raise Exception("Unknown command: " + options.command)
    logger.debug("<< Remote Call End")
    return 0
 
 
 
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)


