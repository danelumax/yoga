#!/usr/bin/env python

import os, sys, subprocess, time
import pexpect
import logging, logging.config
from optparse import OptionParser

import util

import log
log.Init(True)


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

    def register_ss(self, option) :
        log._file.debug(">> Register SS Resource Group")
        log._file.info("Exec cmd: /opt/ipworks/IPWhaagents/scripts/register_cluster.pl --%s %s" %(self._mode, option))
        proc = subprocess.Popen(['/opt/ipworks/IPWhaagents/scripts/register_cluster.pl', '--%s' %(self._mode), option], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        log._file.debug("<<")
      
    def register_ndbcluster(self, option) :
        log._file.debug(">> Register ndbcluster Resource Group")
        log._file.info("Exec cmd: /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --%s %s" %(self._mode, option))
        proc = subprocess.Popen(['/opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl', '--%s' %(self._mode), option], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('%s\n' %(self._ps1_pwd))
        proc.stdin.write('%s\n' %(self._ps2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        log._file.debug("<<")

    def register_csvengine2(self, mgm_vip) :
        log._file.debug(">> Register csvengine Resource Group")
        cmd = '/opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --%s --ndb-mgm-vip %s' %(self._mode, mgm_vip)
        log._file.info('Exec cmd: ' + cmd)
        cli = pexpect.spawn(cmd)
        ret = cli.expect(['(?i)root password:', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        print(cli.before)
        cli.sendline(self._ss1_pwd)
        ret = cli.expect(['(?i)root password:', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        print(cli.before)
        cli.sendline(self._ss2_pwd)
        ret = cli.expect(['(?i)Do you want to continue[Y|N]', pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)
        print(cli.before)
        cli.sendline('Y')
        ret = cli.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=60.0)
        print(cli.before)
        log._file.info('#################################')
        cli.close()
        log._file.debug("<<")

    def register_csvengine(self, mgm_vip) :
        log._file.debug(">> Register csvengine Resource Group")
        log._file.info("Exec cmd: /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --%s --ndb-mgm-vip %s" %(self._mode, mgm_vip))
        proc = subprocess.Popen(['/opt/ipworks/IPWhaagents/scripts/register_csvengine.pl', '--%s' %(self._mode), '--ndb-mgm-vip', mgm_vip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('%s\n' %(self._ss1_pwd))
        proc.stdin.write('%s\n' %(self._ss2_pwd))
        proc.stdin.write('Y\n')
        proc.wait()
        print proc.stdout.read()
        log._file.debug("<<")

    def register_clf(self, slm_ip, clf_dev) :
        log._file.debug(">> Register CLF Resource Group")
        self.parse_slm_ip(slm_ip)
        if not cmp('nfs', self._mode) :
            cmd = "/opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --%s" %(self._mode)
        else :
            cmd = "/opt/ipworks/IPWhaagents/scripts/agent_clf/ipw_reg_clfcluster --CLFdevice=%s" %(clf_dev)
        log._file.info("Exec cmd: " + cmd)
        cli = pexpect.spawn(cmd)
        ret = cli.expect(['(?i)(?:are) you sure you want to continue connecting', "(?i)(?:password): ", pexpect.TIMEOUT, pexpect.EOF], timeout=5.0)

        if 0 == ret :
            log._file.info(cli.before)
            cli.sendline('yes')
            ret = cli.expect(['(?i)(?:are) you sure you want to continue connecting', "(?i)(?:password): ", pexpect.TIMEOUT, pexpect.EOF])
        if 1 == ret :
            log._file.info(cli.before)
            cli.sendline(self._ps2_pwd)
            ret = cli.expect(['(?i)Primary License Server Address', pexpect.TIMEOUT, pexpect.EOF])
        else :
            raise Exception("Failed to login PS2 while register clf resource")
        
        if 0 == ret :
            log._file.info(cli.before)
            cli.sendline(self._slm_prim)
            ret = cli.expect(["(?i)Secondary License Server Address", pexpect.TIMEOUT, pexpect.EOF])
        else :
            raise Exception("Failed to input Primery License Server IP while register clf resource")
        
        if 0 == ret :
            log._file.info(cli.before)
            cli.sendline(self._slm_seco)
            ret = cli.expect([pexpect.TIMEOUT, pexpect.EOF])
        else :
            raise Exception("Failed to input Secondry License Server IP while register clf resource")

        log._file.info(cli.before)
        cli.close()
        log._file.debug("<<")


    def parse_slm_ip(self, ip) :
        log._file.debug(">> Parse License Server IP")
        tmp = ip.split(',')
        self._slm_prim = tmp[0]
        print self._slm_prim
        self._slm_seco = tmp[1]
        print self._slm_seco
        log._file.debug("<<")


    def parse_password(self, passwd) :
        log._file.debug(">> Parse Password")
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
        log._file.debug("<<")


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
    parser.add_option("--option",
        help="makelink-only",
        action="store",
        dest="option",
        default=None)

    (options, args) = parser.parse_args(args=sys.argv)
    log._file.info("options.password: " + util.obfuscate(options.password))
    log._file.info("options.command: " + str(options.command))
    log._file.info("options.mode: " + str(options.mode))
    log._file.info("options.mgm_vip: " + str(options.mgm_vip))
    log._file.info("options.slm_ip: " + str(options.slm_ip))
    log._file.info("options.clf_dev: " + str(options.clf_dev))
    log._file.info("options.option: " + str(options.option))
    
    log._file.debug(">> Remote Call Start")
    task = RegisterCluster(options.mode, options.password)
    if options.command == "ss" :
        task.register_ss(options.option)
    elif options.command == "ndbcluster" :
        task.register_ndbcluster(options.option)
    elif options.command == "csvengine" :
        task.register_csvengine(options.mgm_vip)
    elif options.command == "clf" :
        task.register_clf(options.slm_ip, options.clf_dev)
    else :
        raise Exception("Unknown command: " + options.command)
    log._file.debug("<< Remote Call End")
    return 0
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        log._cons.error(e)
        print str(e)
        sys.exit(2)

