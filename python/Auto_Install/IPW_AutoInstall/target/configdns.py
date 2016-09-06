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



class ConfigDnsTask :

    def __init__(self,username,cli_pwd, ipwss_vip='127.0.0.1') :
        self._ss_vip = ipwss_vip
        self._cli = IpworksCli(username, cli_pwd,logger, server_ip=ipwss_vip)
        self._sm = Sm(logger)
        self._arecord = {"hostname" : "host.iptelco.com", "ip" : "10.0.0.1"}
        self._naptr_record = {"dnsched" : "4.3.2.1.4.3.2.1.0.1.4.4.e164.iptelco.com", "sipaor" : "sip:441012341234@iptelco.com"}
        self._cli_username = username
        self._cli_pwd = cli_pwd
        self._cli_cmd = "/opt/ipworks/IPWcli/scripts/ipwcli -server=%s -user=%s -password=%s " %(self._ss_vip, self._cli_username, self._cli_pwd)
        self._retry = 10


    def prepareDns(self) :
        logger.debug(">> Prepare DNS Server")
        conf_file = open("/etc/resolv.conf", "w")
        conf_file.write("nameserver 127.0.0.1\n")
        conf_file.write("domain localhost\n")
        conf_file.close()
        port_file_path = "/var/run/dnssm.port"
        if os.path.exists(port_file_path) :
            os.remove(port_file_path)
        logger.debug("<<")


    def prepareEnum(self, ip):
        logger.debug(">> Prepare Enum Server")
        port_file_path = "/var/run/enumsm.port"
        if os.path.exists(port_file_path) :
            os.remove(port_file_path)
        conf_file = "/etc/ipworks/ipworks_enum.conf"
        lines = util.readfilelines(conf_file)
        context = ''
        for line in lines:
            if re.search("^Enum.Ndb.Connection.Management.Node=", line):
                context += "Enum.Ndb.Connection.Management.Node=" + ip + ":1186\n"
            elif re.search("^Enum.Log.Level=", line) :
                context += "Enum.Log.Level=warning\n"
            else:
                context += line
        util.writefile(conf_file, context)
        logger.debug("<<")


    def createDnsEnum(self, hostname, oam_ip, server_id) : 
        logger.debug(">> create dns & enum")
        self._cli.login()
        self._cli.execute("create dnsserver " + hostname + " -set dnsname=" + hostname + ".iptelco.com;address=" + oam_ip)
        self._cli.execute('modify dnsserver ' + hostname + ' -set option="listen-on port 5300{any;}","listen-on-v6 port 5300{any;}"')
        self._cli.execute("create enumserver -set defaultmtu=1500;address=" + oam_ip + ";enumserverid=" + server_id)
        self._cli.logout()
        logger.debug("<<")


    def deleteDnsEnum(self, hostname, server_id) : 
        logger.debug(">> delete dns & enum")
        server = "/opt/ipworks/IPWcli/scripts/ipwcli -server=%s -user=%s -password=%s" %(self._ss_vip,self._cli_username, self._cli_pwd)
        cmd = '"delete enumserver ' + server_id + '"'
        #proc = subprocess.Popen([server + cmd], stdout=subprocess.PIPE, shell=True)
        #proc.wait()
        #ret = proc.stdout.read()
        #logger.debug(ret)
        tmp = 'No object(s) were updated.'
        while True :
            proc = subprocess.Popen([server + cmd], stdout=subprocess.PIPE, shell=True)
            proc.wait()
            ret = proc.stdout.read()
            logger.debug(ret)
            if re.search(tmp, ret):
                time.sleep(10)
            else:
                break
        server2 = 'echo "yes" |' + server
        cmd = '"delete dnsserver ' + hostname + '"'
        #proc = subprocess.Popen([server2 + cmd], shell=True)
        #proc.wait()
        #ret = proc.stdout.read()
        while True :
            proc = subprocess.Popen([server2 + cmd], stdout=subprocess.PIPE, shell=True)
            proc.wait()
            ret = proc.stdout.read()
            logger.debug(ret)
            if re.search(tmp, ret):
                time.sleep(10)
            else:
                break
        logger.debug("<<")


    def createDns(self, hostname, oam_ip) :
        logger.debug(">> create a dns server")
        self._cli.login()
        self._cli.execute("create dnsserver " + hostname + " -set dnsname=" + hostname + ".iptelco.com;address=" + oam_ip)
        self._cli.logout()
        logger.debug("<<")


    def deleteDns(self, hostname) : 
        logger.debug(">> delete dns")
        server = "/opt/ipworks/IPWcli/scripts/ipwcli -server=" + self._ss_vip + " -user=" +self._cli_username + " -password=" + self._cli_pwd
        server2 = 'echo "yes" |' + server
        cmd = '"delete dnsserver ' + hostname + '"'
        #proc = subprocess.Popen([server2 + cmd], shell=True)
        #proc.wait()
        tmp = 'No object(s) were updated.'
        while True :
            proc = subprocess.Popen([server2 + cmd], stdout=subprocess.PIPE, shell=True)
            proc.wait()
            ret = proc.stdout.read()
            logger.debug(ret)
            if re.search(tmp, ret):
                time.sleep(10)
            else:
                break
        logger.debug("<<")


    def startDnsEnum(self, hostname, server_id) :
        logger.debug(">> start dns & enum")
        self._cli.login()
        self.startServer("update dnsserver " + hostname)
        self.checkState("list dnsserver " + hostname)
        self.startServer("start enumserver " + server_id)
        self.checkState("list enumserver " + server_id)
        self._cli.logout()
        logger.debug("<<")

        #check the status of processes
#        if not self._util.check_process("/opt/ipworks/IPWdns/usr/bin/named") :
#            raise Exception("can't find the process /opt/ipworks/IPWdns/usr/bin/named..... The dns is not started")
#        elif not self._util.check_process("/opt/ipworks/IPWenum/usr/bin/ipwenum") :
#            raise Exception("can't find the process /opt/ipworks/IPWenum/usr/bin/ipwenum ... The enum is not started")
 
    def startDns(self, hostname):
        logger.debug(">> start dns")
        self._cli.login()
        self.startServer("update dnsserver " + hostname) 
        self.checkState("list dnsserver " + hostname)
        self._cli.logout()
        logger.debug("<<")


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
        if self._retry == retry :
            raise Exception("Update/Start Server failed: " + cmd)
        logger.debug("<<")


    def checkState(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            logger.debug("searching 'running' status")
            if re.search("\'running\s*\'", out):
                logger.debug("server has running")
                break
            logger.debug("sleep 10 seconds to wait for Server ready.")
            time.sleep(10)
            retry += 1
        if self._retry == retry :
            raise Exception("Server not running: " + cmd)
        logger.debug("<<")


    def checkStopState(self, cmd) :
        logger.debug(">>")
        retry = 0
        while retry < self._retry :
            out = self._cli.execute(cmd)
            logger.debug("searching 'down' status")
            if re.search("\'down\s*\'", out):
                logger.debug("server has down")
                break
            logger.debug("sleep 10 seconds to wait for Server down.")
            time.sleep(10)
            retry += 1
        if self._retry == retry :
            raise Exception("Server not stop: " + cmd)
        logger.debug("<<")


    def stopDnsEnum(self):
        logger.debug(">> stop dns & enum")
        self._cli.login()
        self._cli.execute("stop enumserver") 
        self.checkStopState("list enumserver")
        self._cli.execute("stop dnsserver")
        self.checkStopState("list dnsserver")
        self._cli.logout()
        logger.debug("<<")


    def stopDns(self):
        logger.debug(">> stop dns")
        self._cli.login()
        self._cli.execute("stop dnsserver")
        self.checkStopState("list dnsserver")
        self._cli.logout()
        logger.debug("<<")


    def configMasterZone(self, hostname) :
        logger.debug(">> create master zone")
        self._cli.login()
        self._cli.execute("create masterzone " + hostname + " iptelco.com")
        self._cli.execute("create arecord " + self._arecord["hostname"] + " " + self._arecord["ip"])
        #self._cli.execute("update dnsserver " + hostname)
        self._cli.logout()
        logger.debug("<<")


    def cleanMasterZone(self) :
        logger.debug(">> clean master zone")
        cmd = self._cli_cmd + '"delete arecord ' + self._arecord['hostname'] + '"'
        logger.debug("exec cli cmd: " + util.obfuscate_passwd(cmd))
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        proc.wait()
        ret = proc.stdout.read()
        logger.debug("ret info: " + ret)
        logger.debug("exec cli cmd: " + util.obfuscate_passwd(cmd))
        cmd = 'echo "yes" |' + self._cli_cmd
        cmd += '"delete masterzone iptelco.com"'
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        proc.wait()
        ret = proc.stdout.read()
        logger.debug("ret info: " + ret)
        logger.debug("exec cli cmd: " + util.obfuscate_passwd(cmd))
        cmd = self._cli_cmd + '"update dnsserver"'
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        proc.wait()
        ret = proc.stdout.read()
        logger.debug("ret info: " + ret)
        logger.debug("<<")


    def configEnumZone(self) :
        logger.debug(">> create enum zone")
        self._cli.login()
        self._cli.execute('create enumzone 1 -set enumzonename="e164.iptelco.com"')
        #logger.info("create enumdnsched: " + self._naptr_record['dnsched'] + " ==> " + self._naptr_record['sipaor'])
        command = "create enumdnsched " + self._naptr_record["dnsched"] \
                + " -set naptrFlags=nu;naptrOrder=100;naptrPreference=10;naptrService=E2U+SIP;naptrTxt=!^.*$!" + self._naptr_record["sipaor"] + "!"
        self._cli.execute(command)
        self._cli.logout()
        logger.debug("<<")
 

    def cleanEnumZone(self) :
        logger.debug(">> clean enum zone")
        self._cli.login()
        self._cli.execute("delete enumdnsched " + self._naptr_record["dnsched"])
        self._cli.execute("delete enumzone 1")
        self._cli.logout()
        logger.debug("<<")


    def verify_dns(self) :
        logger.debug(">> verify dns")
        logger.debug("starting the dns....")
        if self._verify_dns(self._arecord) == False :
            raise Exception("can not dig the hostname: " + self._arecord["hostname"])
        logger.info("dns is started")	
        logger.debug("<<")


    def verify_dns_enum(self) :
        logger.debug(">> verify dns & enum")
        logger.debug("starting the enum....")
        if self._verify_enum(self._naptr_record) == False :
            raise Exception("can not dig the naptr: " + self._naptr_record["dnsched"])
        logger.info("enum is started")
        logger.debug("starting the dns....")
        if self._verify_dns(self._arecord, 5300) == False :
            raise Exception("can not dig the hostname: " + self._arecord["hostname"])
        logger.info("dns is started")	
        logger.debug("<<")
 


    def _verify_dns(self, arecord, port=53) :
        hostname = arecord["hostname"]
        command = 'dig @127.0.0.1 -p ' + str(port) + ' ' + arecord["hostname"]
        logger.info("send the command to verify DNS: " + command)
        proc = subprocess.Popen(["dig",  "@127.0.0.1", "-p", str(port), arecord["hostname"] ], stdout=subprocess.PIPE)
        proc.wait()
        lines = proc.stdout.read()
        logger.info("result:\n%s" %lines)
        lines = lines.splitlines()
        logger.info("to find: %s" %arecord["ip"])
        for line in lines:
            #logger.info("line: " + line)
            if re.search(arecord["ip"], line) :
                logger.info("match line: %s" %line)
                return True
        logger.error("No match")
        return False


    def _verify_enum(self, naptr_record, port=53) :
        hostname = naptr_record["dnsched"]
        command = 'dig @127.0.0.1 -p ' + str(port) + ' ' + naptr_record["dnsched"] + " NAPTR"
        logger.info("send the command to verify ENUM> " + command)
        proc = subprocess.Popen(["dig", "@127.0.0.1", "-p", str(port), naptr_record["dnsched"], "NAPTR"], stdout=subprocess.PIPE)
        proc.wait()
        lines = proc.stdout.read()
        logger.info("result:\n%s" %lines)
        lines = lines.splitlines()
        logger.info("to find: %s" %naptr_record["sipaor"])
        for line in lines:
            #logger.info("line: " + line)
            if re.search(naptr_record["sipaor"], line) :
                logger.info("match line: %s" %line)
                return True
        logger.error("No match")
        return False



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="config_dns, config_dns_enum",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--hostname",
        help="hostname",
        action="store",
        dest="hostname",
        default=None)
    parser.add_option("--oam_ip",
        help="IP address of OAM network",
        action="store",
        dest="oam_ip",
        default=None)
    parser.add_option("--server_id",
        help="ENUM server ID",
        action="store",
        dest="server_id",
        default=None)
    parser.add_option("--ipwss_vip",
        help="IP address to the ipwss",
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
    logger.info("options.hostname: " + str(options.hostname))
    logger.info("options.oam_ip: " + str(options.oam_ip))
    logger.info("options.server_id: " + str(options.server_id))
    logger.info("options.ipwss_vip: " + str(options.ipwss_vip))
    
    logger.debug(">> Remote Call Start")
    if options.password is not None:
        if options.ipwss_vip :
            task = ConfigDnsTask(options.username, options.password, options.ipwss_vip)
        else :
            task = ConfigDnsTask(options.username, options.password)
        
    if options.command == "prepareDns" :
        task.prepareDns()
    elif options.command == "prepareEnum" :
        task.prepareEnum(options.oam_ip)
    elif options.command == "createDnsEnum" :
        task.createDnsEnum(options.hostname, options.oam_ip, options.server_id)
    elif options.command == "createDns" :
        task.createDns(options.hostname, options.oam_ip)
    elif options.command == "deleteDnsEnum" :
        task.deleteDnsEnum(options.hostname, options.server_id)
    elif options.command == "deleteDns" :
        task.deleteDns(options.hostname)
    elif options.command == "startDnsEnum" :
        task.startDnsEnum(options.hostname, options.server_id)
    elif options.command == "startDns" :
        task.startDns(options.hostname)
    elif options.command == "stopDnsEnum" :
        task.stopDnsEnum()
    elif options.command == "stopDns" :
        task.stopDns()
    elif options.command == "configMasterZone" :
        task.configMasterZone(options.hostname)
    elif options.command == "configEnumZone" :
        task.configEnumZone()
    elif options.command == "cleanMasterZone" :
        task.cleanMasterZone()
    elif options.command == "cleanEnumZone" :
        task.cleanEnumZone()
    elif options.command == "verifyDnsEnum" :
        task.verify_dns_enum()
    elif options.command == "verifyDns" :
        task.verify_dns()
    logger.debug("<< Remote Call End")
    return 0
 
if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)
