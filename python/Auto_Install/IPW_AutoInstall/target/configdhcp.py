#!/usr/bin/env python

import os, re, subprocess, traceback, sys, time, shutil
import pexpect
import logging, logging.config
from optparse import OptionParser
from ipwcli import IpworksCli
from sm import Sm
import util

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigDhcpTask :

    def __init__(self, cli_username, cli_password, ipwss_vip='127.0.0.1') :
        self._ss_vip = ipwss_vip
        self._cli = IpworksCli(cli_username, cli_password, logger, server_ip=ipwss_vip)
        self._sm = Sm(logger)
        self._retry = 10


    def config_dhcp_sm(self, ipwss_vip):
        logger.debug(">>> config dhcp4 server manager")
        dhcp_sm_file = "/etc/ipworks/ipworks_dhcpv4sm.conf"
        tmp = util.readfilelines(dhcp_sm_file)
        fcontext = ""
        for s in tmp:
            if re.search("Server=", s):
                index = s.find("Server=")
                ss = s[0:index] + "Server=" + ipwss_vip + "\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Password=", s):
                index = s.find("Password=")
                # "Admin123" => "DJEgnJ4kZwZ="
                ss = s[0:index] + self._cli.getEncryptPassword+ "\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            else:
                fcontext += s
        util.writefile(dhcp_sm_file, fcontext)
        logger.debug("<<<")


    def _send_cli_command(self, cli, command, debug_print=True) :
        logger.debug("cli cmd: " + command)
        cli.sendline(command)
        cli.expect("IPWorks>")
        if debug_print :
             logger.debug("cli < " + cli.before)


    def create_dhcp_normal(self, ps1):
        logger.debug(">>> create dhcpv4 server in normal mode")
        self._cli.login()
        command = "create dhcpv4server dhcp1 -set address=" + str(ps1)
        self._cli.execute(command)
        self._cli.logout()
        logger.debug("<<<")


    def create_dhcp_failover(self, ps1, ps2):
        logger.debug(">>> create dhcpv4 server in failover mode")
        self._cli.login()
        cmd = "create dhcpv4server dhcp1 -set address=" + str(ps1)
        self._cli.execute(cmd)
        cmd = "create dhcpv4server dhcp2 -set address=" + str(ps2) + ";primary=dhcp1"
        self._cli.execute(cmd)
        self._cli.logout()
        logger.debug("<<<")


    def createSubnet(self):
        logger.debug(">>> create subnet & pool")
        self._cli.login()
        cmd = 'create subnet -set name="10.5Net" -set address=10.5.0.0 -set masklength=16 -set server=dhcp1'
        self._cli.execute(cmd)
        cmd = 'modify -add option="allow-unknown-clients true"'
        self._cli.execute(cmd)
        cmd = 'create pool -set name=poolA -set subnet="10.5Net" -set addressrange=10.5.0.1-10.5.0.10 -set allowedclient=unknown -set server=dhcp1'
        self._cli.execute(cmd)
        self._cli.logout()
        logger.debug("<<<")


    def deleteSubnet(self):
        logger.debug(">>> delete subnet & pool")
        self._cli.login()
        self._cli.execute('delete pool poolA')
        self._cli.execute('delete subnet 10.5Net')
        self._cli.logout()
        logger.debug("<<<")


    def verifyDhcp(self) :
        logger.debug(">>> verify dhcp server in Normal")
        self._cli.login()
        self.startServer("update dhcpv4server") 
        self.checkState("show status dhcpv4server")
        self._cli.logout()
        logger.debug("<<<")


    def verifyDhcpFailOver(self) :
        logger.debug(">>> verify dhcp server in FailOver")
        self._cli.login()
        self.startServer("update dhcpv4server") 
        self.checkState2("show status dhcpv4server dhcp1")
        self.checkState2("show status dhcpv4server dhcp2")
        self._cli.logout()
        logger.debug("<<<")


    def startServer(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            if re.search("is not currently available\. Operation update is interrupted\.", out) == None :
                logger.debug("server has started")
                break
            logger.debug("sleep 10 seconds to wait for SM ready.")
            time.sleep(10)
            retry += 1
        if retry == self._retry :
            raise Exception("Update DHCP server failed")
        logger.debug("<<")


    def checkState(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            logger.debug("searching 'running ' status")
            if re.search("\'running\s*\'", out):
                logger.debug("server has running")
                break
            logger.debug("sleep 10 seconds to wait for Server ready.")
            time.sleep(10)
            retry += 1
        if retry == self._retry :
            raise Exception("DHCP server not running")
        logger.debug("<<")


    def checkState2(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            logger.debug("searching 'running normal' status")
            if re.search("\'running normal\'", out):
                logger.debug("server has running")
                break
            logger.debug("sleep 10 seconds to wait for Server ready.")
            time.sleep(10)
            retry += 1
        if retry == self._retry :
            raise Exception("DHCP server not running")
        logger.debug("<<")


    def checkStopState(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            logger.debug("searching 'down' status")
            if re.search("\'down\'", out):
                logger.debug("server has down")
                break
            logger.debug("sleep 10 seconds to wait for Server down.")
            time.sleep(10)
            retry += 1
        if retry == self._retry :
            raise Exception("DHCP server not stopped")
        logger.debug("<<")


    def stopDhcpNormal(self) :
        logger.debug(">>> stop dhcpv4 server in Normal")
        self._cli.login()
        self._cli.execute("stop dhcpv4server")
        self.checkStopState("show status dhcpv4server")
        self._cli.logout()
        logger.debug("<<<")


    def stopDhcpFailOver(self) :
        logger.debug(">>> stop dhcpv4 server in FailOver")
        self._cli.login()
        self._cli.execute("stop dhcpv4server")
        self.checkStopState("show status dhcpv4server dhcp1")
        self.checkStopState("show status dhcpv4server dhcp2")
        self._cli.logout()
        logger.debug("<<<")


    def deleteDhcpNormal(self) :
        logger.debug(">>> delete dhcpv4 server in Normal")
        self._cli.login()
        self._cli.execute("delete dhcpv4server dhcp1")
        self._cli.execute("list dhcpv4server")
        self._cli.logout()
        logger.debug("<<<")


    def deleteDhcpFailOver(self) :
        logger.debug(">>> delete dhcpv4 server in FailOver")
        self._cli.login()
        self._cli.execute("delete dhcpv4server dhcp2")
        self._cli.execute("delete dhcpv4server dhcp1")
        self._cli.execute("list dhcpv4server")
        self._cli.logout()
        logger.debug("<<<")


    def enbaleLog(self) :
        logger.debug(">>> enable dhcpv4 server log")
        dhcp_cfgfile = "/etc/ipworks/ipworks_dhcpv4.conf"
        tmp = util.readfile(dhcp_cfgfile)
        tmp = re.sub("DHCPV4_ENABLE_LOG=\d*", "DHCPV4_ENABLE_LOG=1", tmp)
        logger.debug("replace: DHCPV4_ENABLE_LOG=1")
        tmp = re.sub("DHCPV4_LOG_LEVEL=\d*", "DHCPV4_LOG_LEVEL=2", tmp)
        logger.debug("replace: DHCPV4_LOG_LEVEL=2")
        util.writefile(dhcp_cfgfile, tmp)
        logger.debug("<<<")



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="config_dhcp, config_dhcp",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--ipwss_vip",
        help="IP address to the ipwss",
        action="store",
        dest="ipwss_vip",
        default=None)
    parser.add_option("--primary",
        help="IP address of the primary ip",
        action="store",
        dest="primary_ip",
        default=None)
    parser.add_option("--secondary",
        help="IP address of the secondary ip",
        action="store",
        dest="secondary_ip",
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
    logger.info("options.primary_ip: " + str(options.primary_ip))
    logger.info("options.secondary_ip: " + str(options.secondary_ip))
    
    logger.debug(">> Remote Call Start")
    if options.ipwss_vip :
        task = ConfigDhcpTask(options.username, options.password, options.ipwss_vip)
    else :
        task = ConfigDhcpTask(options.username, options.password)

    if options.command == "confDhcpSM" :
        task.config_dhcp_sm(options.ipwss_vip)
    elif options.command == "createDhcpNormal" :
        task.create_dhcp_normal(options.primary_ip)
    elif options.command == "createDhcpFailover" :
        task.create_dhcp_failover(options.primary_ip, options.secondary_ip)
    elif options.command == "verifyDhcp" :
        task.verifyDhcp()
    elif options.command == "verifyDhcpFailover" :
        task.verifyDhcpFailOver()
    elif options.command == "stopDhcpNormal" :
        task.stopDhcpNormal()
    elif options.command == "stopDhcpFailover" :
        task.stopDhcpFailOver()
    elif options.command == "deleteDhcpNormal" :
        task.deleteDhcpNormal()
    elif options.command == "deleteDhcpFailover" :
        task.deleteDhcpFailOver()
    elif options.command == "createSubnet" :
        task.createSubnet()
    elif options.command == "deleteSubnet" :
        task.deleteSubnet()
    elif options.command == "enableLog" :
        task.enbaleLog()
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

