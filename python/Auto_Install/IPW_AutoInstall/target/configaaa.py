#!/usr/bin/env python

import os, re, sys, subprocess, time
import logging, logging.config
from optparse import OptionParser
from ipwcli import IpworksCli
import util

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class ConfigAaa:

    def __init__(self, cli_username, cli_password, ipwss_vip='127.0.0.1'):
        self._core_conf = "/etc/ipworks/aaa_core_server.conf"
        self._radius_conf = "/etc/ipworks/aaa_radius_stack.conf"
        self._plugin_conf = "/etc/ipworks/aaa_plugins.conf"
        self._sm_conf = "/etc/ipworks/ipworks_aaasm.conf"
        self._csv_conf = "/etc/ipworks/aaa_acct_engine.conf"
        self._diameter_conf = "/etc/ipworks/aaa_server.conf"
        self._cli = IpworksCli(cli_username, cli_password, logger, server_ip=ipwss_vip)
        self._retry = 10


    def config_core_server(self, dbcluster_vip, sqlnode_vip):
        logger.debug(">> config core")
        tmp = util.readfilelines(self._core_conf)
        fcontext = ""
        for s in tmp:
            if re.search("Ndb.Connection.Management.Node=", s):
                index = s.find("Ndb.Connection.Management.Node=")
                ss = s[0:index] + "Ndb.Connection.Management.Node=" + dbcluster_vip + ":1186\n"
                logger.debug("replace as: " + ss)
                fcontext += ss
            elif re.search("Ndb.SQL.Node.IP=", s):
                index = s.find("Ndb.SQL.Node.IP=")
                ss = s[0:index] + "Ndb.SQL.Node.IP=" + sqlnode_vip + "\n"
                logger.debug("replace as: " + ss)
                fcontext += ss
            elif re.search("Log.Level=", s):
                logger.debug("replace as: Log.Level=4")
                fcontext += "Log.Level=4\n"
            else:
                fcontext += s
        util.writefile(self._core_conf, fcontext)
        logger.debug("<<")


    def config_radius_stack(self):
        logger.debug(">> config radius stack")
        tmp = util.readfilelines(self._radius_conf)
        fcontext = ""
        for s in tmp:
            #if re.search("Localhost.Bind.IPType=", s):
                #index = s.find("Localhost.Bind.IPType=")
                #ss = s[0:index] + "Localhost.Bind.IPType=2\n"
                #logger.debug("replace: " + ss)
                #fcontext += ss
            if re.search("Log.Level=", s):
                logger.debug("replace as: Log.Level=4")
                fcontext += "Log.Level=4\n"
            else:
                fcontext += s
        util.writefile(self._radius_conf, fcontext)
        logger.debug("<<")


    def config_plugins(self, dbcluster_vip, csvengine_vip, oam_ip):
        logger.debug(">> config plugin")
        tmp = util.readfilelines(self._plugin_conf)
        fcontext = ""
        for s in tmp:
            if re.search("Ndb.Connection.Management.Node=", s):
                index = s.find("Ndb.Connection.Management.Node=")
                ss = s[0:index] + "Ndb.Connection.Management.Node=" + dbcluster_vip + ":1186\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Acct.To.Session.CSV=", s):
                index = s.find("Acct.To.Session.CSV=")
                ss = s[0:index] + "Acct.To.Session.CSV=1\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Acct.Server.IP=", s):
                index = s.find("Acct.Server.IP=")
                ss = s[0:index] + "Acct.Server.IP=" + csvengine_vip + "\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Cert.ServKeyPassword=", s):
                index = s.find("Cert.ServKeyPassword=")
                ss = s[0:index] + "Cert.ServKeyPassword=q2uuqTI2MKV=\n"  # whatever
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Wlan.ISDN.Number=", s):
                index = s.find("Wlan.ISDN.Number=")
                ss = s[0:index] + "Wlan.ISDN.Number=1234567\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Wlan.SGSN.Address=", s):
                index = s.find("Wlan.SGSN.Address=")
                ss = s[0:index] + "Wlan.SGSN.Address=%s\n" %(oam_ip)
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Log.Level=", s):
                logger.debug("replace as: Log.Level=4")
                fcontext += "Log.Level=4\n"
            else:
                fcontext += s
        util.writefile(self._plugin_conf, fcontext)
        self._exec_cmd("cp ca.pem /etc/ipworks/aaa/ca_cert_path/")
        self._exec_cmd("cp server.key /etc/ipworks/aaa/serv_key/")
        self._exec_cmd("cp server.pem /etc/ipworks/aaa/serv_cert/")
        logger.debug("<<")


    def _exec_cmd(self, cmd, throw=False):
        logger.debug("exec cmd: " + cmd)
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        code = proc.wait()
        logger.debug("return code: " + str(code))
        if 0 != code and throw :
            raise Exception("Failed to exec cmd: " + cmd)
        ret = proc.stdout.read()
        logger.debug("return info: " + ret)


    def config_diameter(self, dbcluster_vip, sqlnode_vip):
        logger.debug(">> config diameter")
        tmp = util.readfilelines(self._diameter_conf)
        fcontext = ""
        for s in tmp:
            if re.search("Ndb.Connection.Management.Node=", s):
                index = s.find("Ndb.Connection.Management.Node=")
                ss = s[0:index] + "Ndb.Connection.Management.Node=" + dbcluster_vip + ":1186\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Ndb.Connection.Sql.Node=", s):
                index = s.find("Ndb.Connection.Sql.Node=")
                ss = s[0:index] + "Ndb.Connection.Sql.Node=" + sqlnode_vip + "\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            elif re.search("Log.Level=", s):
                logger.debug("replace as: Log.Level=4")
                fcontext += "Log.Level=4\n"
            else:
                fcontext += s
        util.writefile(self._diameter_conf, fcontext)
        logger.debug("<<")


    def config_csv(self, dbcluster_vip):
        logger.debug(">> config csv")
        tmp = util.readfilelines(self._csv_conf)
        fcontext = ""
        for s in tmp:
            if re.search("Ndb.Connection.Management.Node=", s):
                index = s.find("Ndb.Connection.Management.Node=")
                ss = s[0:index] + "Ndb.Connection.Management.Node=" + dbcluster_vip + ":1186\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            else:
                fcontext += s
        util.writefile(self._csv_conf, fcontext)
        logger.debug("<<")


    def config_aaa_sm(self, ipwss_vip):
        logger.debug(">>")
        tmp = util.readfilelines(self._sm_conf)
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
                ss = s[0:index] + "Password="+ self._cli.getEncryptPassword() +"\n"
                logger.debug("replace: " + ss)
                fcontext += ss
            else:
                fcontext += s
        util.writefile(self._sm_conf, fcontext)
        logger.debug("<<")


    def create_aaa(self, srv_ip):
        logger.debug(">> create aaa server")
        self._cli.login()
        self._cli.execute("create aaaserver -set name=aaasrv1;address=" + srv_ip)
        res = self._cli.execute("list aaaserver")
        if not re.search('aaasrv1', res) :
            raise Exception("Failed to create aaaserver")
        #self._cli.execute("modify aaacsvrecord -set enable=true")
        #self._cli.execute("modify aaacsvrecord -set Records=\"Acct-Status-Type,NAS-IP-Address,Acct-Session-Id,Acct-Input-Packets,Acct-Output-Packets,Acct-Input-Octets,Acct-Output-Octets,Acct-Session-Time\"")
        #self._cli.execute("list aaacsvrecord")
        self._cli.logout()
        logger.debug("<<")


    def enable_sessionrecord(self):
        logger.debug(">> enable aaasessionrecord")
        self._cli.login()
        self._cli.execute("modify aaacsvrecord -set enable=true")
        self._cli.execute("modify aaacsvrecord -set Records=\"Acct-Status-Type,NAS-IP-Address,Acct-Session-Id,Acct-Input-Packets,Acct-Output-Packets,Acct-Input-Octets,Acct-Output-Octets,Acct-Session-Time\"")
        self._cli.execute("list aaacsvrecord")
        self._cli.execute('modify aaasessionrecord -set enable=true;AcctOnOffCloseAll=false;records="User-Name,NAS-Port,Framed-IP-Address,Called-Station-Id,Calling-Station-Id,Originating-Line-Info,Acct-Multi-Session-Id,NAS-Port-Id,Chargeable-User-Identity,Framed-Interface-Id,Framed-IPv6-Prefix,Class"')
        self._cli.execute("list aaasessionrecord")
        self._cli.logout()
        logger.debug("<<")


    def delete_aaa(self):
        logger.debug(">> delete aaa server")
        self._cli.login()
        self._cli.execute("delete aaaserver")
        #self._cli.execute("modify aaacsvrecord -set enable=false")
        self._cli.execute('modify aaasessionrecord -set enable=false')
        self._cli.logout()
        logger.debug("<<")


    def update_aaa(self):
        logger.debug(">> update aaa server")
        self._cli.login()
        self.startServer("update aaaserver")
        self._cli.logout()
        logger.debug("<<")


    def start_aaa(self):
        logger.debug(">> start aaa server")
        self._exec_cmd("/etc/init.d/ipworks.aaa_core_server start")
        self._exec_cmd("/etc/init.d/ipworks.aaa_radius_stack start")
        self._exec_cmd("/etc/init.d/ipworks.aaa_plugins start")
        logger.debug("<<")


    def stop_aaa(self):
        logger.debug(">> stop aaa server")
        self._cli.login()
        self._cli.execute("stop aaaserver")
        self.checkStopState("list aaaserver")
        self._cli.logout()
        logger.debug("<<")


    def verify_aaa(self):
        logger.debug(">> verify aaa server")
        self._cli.login()
        self.checkState("list aaaserver")
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
            server_running = True
            #check_point = ["radius running", "core running", "aaa running", "'pap_1' running", "'chap_1' running", "'authz_1' running"]
            # 14B FD1 LSV2 changed
            check_point = ["radius running", "core running", "backend running", "aaa running"]
            logger.debug("searching " + str(check_point) + " status")
            for item in check_point :
                if not re.search(item, out) :
                    server_running = False
            if server_running :
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
            server_down = True
            #check_point = ["radius down", "core down", "aaa down", "'pap_1' down", "'chap_1' down", "'authz_1' down"]
            # 14B FD1 LSV2 changed
            check_point = ["radius down", "core down", "backend down", "aaa down"]
            logger.debug("searching " + str(check_point) + " status")
            for item in check_point :
                if not re.search(item, out) :
                    server_down = False
            if server_down :
                logger.debug("server has down")
                break
            logger.debug("sleep 10 seconds to wait for Server down.")
            time.sleep(10)
            retry += 1
        if self._retry == retry :
            raise Exception("Server not stop: " + cmd)
        logger.debug("<<")



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="config_core_server, config_radius_stack, config_plugins, config_csv, config_aaa_sm",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--mgm_vip",
        help="dbcluster vip",
        action="store",
        dest="dbcluster_vip",
        default=None)
    parser.add_option("--sql_vip",
        help="sql node vip",
        action="store",
        dest="sqlnode_vip",
        default=None)
    parser.add_option("--csv_vip",
        help="CSV engine vip",
        action="store",
        dest="csvengine_vip",
        default=None)
    parser.add_option("--ipwss_vip",
        help="IP address to the ipwss",
        action="store",
        dest="ipwss_vip",
        default=None)
    parser.add_option("--aaasrv_ip",
        help="IP address to the aaa server",
        action="store",
        dest="aaasrv_ip",
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
    logger.info("options.dbcluster_vip: " + str(options.dbcluster_vip))
    logger.info("options.sqlnode_vip: " + str(options.sqlnode_vip))
    logger.info("options.csvengine_vip: " + str(options.csvengine_vip))
    logger.info("options.ipwss_vip: " + str(options.ipwss_vip))
    logger.info("options.aaasrv_ip: " + str(options.aaasrv_ip))
    
    logger.debug(">> Remote Call Start")
    if options.ipwss_vip :
        task = ConfigAaa(options.username, options.password,options.ipwss_vip)
    else :
        task = ConfigAaa(options.username, options.password)

    if options.command == "config_core_server" :
        task.config_core_server(options.dbcluster_vip, options.sqlnode_vip)
    elif options.command == "config_radius_stack" :
        task.config_radius_stack()
    elif options.command == "config_plugins" :
        task.config_plugins(options.dbcluster_vip, options.csvengine_vip, options.aaasrv_ip)
    elif options.command == "config_csv" :
        task.config_csv(options.dbcluster_vip)
    elif options.command == "config_aaa_sm" :
        task.config_aaa_sm(options.ipwss_vip)
    elif options.command == "config_diameter" :
        task.config_diameter(options.dbcluster_vip, options.sqlnode_vip)
    elif options.command == "create_aaa" :
        task.create_aaa(options.aaasrv_ip)
    elif options.command == "delete_aaa" :
        task.delete_aaa()
    elif options.command == "update_aaa" :
        task.update_aaa()
    elif options.command == "start_aaa" :
        task.start_aaa()
    elif options.command == "stop_aaa" :
        task.stop_aaa()
    elif options.command == "verify_aaa" :
        task.verify_aaa()
    elif options.command == "enable_sessionrecord" :
        task.enable_sessionrecord()
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)








