#!/usr/bin/env python

import os, re, subprocess, sys, time, shutil
import util


class Sm :

    def __init__(self, logger) :
        self._logger = logger
        self._sm_cmd1 = "/etc/init.d/ipworks.sm"
        self._sm_cmd2 = "/opt/ipworks/IPWsm/scripts/ipwsm"
        self._sm_cmd3 = "/opt/ipworks/IPWsm/scripts/ipwsmctl"


    def config(self, cli_username, cli_password, ipwss_vip='127.0.0.1') :
        self._logger.debug(">> config sm")
        config_path = "/etc/ipworks/"
        file_list = ["ipworks_aaasm.conf", "ipworks_asdnsmonsm.conf", "ipworks_dhcpv4sm.conf",
                     "ipworks_dhcpv6sm.conf", "ipworks_dnsalgsm.conf", "ipworks_dnssm.conf",
                     "ipworks_enumsm.conf"]
        for file_name in file_list :
            if os.path.exists(config_path + file_name) :
                self._logger.debug("config file: " + file_name)
                fd = open(config_path + file_name, "r+w")
                context = fd.read()
                context = re.sub("Server=\w+", "Server=" + ipwss_vip, context)
                context = re.sub("UserName=\w+", "UserName=" + cli_username, context)
                context = re.sub("Password=\w*", "Password=" + util.ipworksEncryptPassword(cli_password), context)  # password: Admin123e
                #TODO: temporary remove it because of the TR
                #context = context.replace("#Sm.LocalAddress=\n", "Sm.LocalAddress=127.0.0.1\n")
                fd.seek(os.SEEK_SET)
                fd.write(context)
                fd.close()
        self._logger.debug("<<")


    def start(self) :
        self._logger.debug(">> start server manager")
        proc = subprocess.Popen([self._sm_cmd1, "start"])
        proc.wait()
        self._logger.debug("please wait for a while...")
        time.sleep(20)	#TODO: waiting for sm startup
        self._logger.debug("<<")

    
    def stop(self) :
        self._logger.debug(">> stop server manager")
        proc = subprocess.Popen([self._sm_cmd1, "stop"])
        proc.wait()
        self._logger.debug("please wait for a while...")
        time.sleep(20)	#TODO: waiting for sm stopdown
        self._logger.debug("<<")


    def start_sm(self, sm_type) :
        self._logger.debug(">> start server manager: " + sm_type)
        cmd = "%s ServerType=%s &" %(self._sm_cmd2, sm_type)
        self._logger.debug("exec cmd: %s" %cmd)
        proc = subprocess.Popen([cmd], shell=True)
        ret = proc.wait()
        self._logger.debug("return code: %s" %ret)
        time.sleep(20)	#TODO: waiting for sm start
        if not util.check_process('java -DApp=ipw%ssm' %(sm_type.lower()), "start"):
            raise Exception("Server Manager Doesn't Started !")
        self._logger.debug("<<")


    def stop_sm(self, sm_type) :
        self._logger.debug(">> stop server manager: " + sm_type)
        cmd = "%s ServerType=%s Shutdown=yes &" %(self._sm_cmd3, sm_type)
        self._logger.debug("exec cmd: %s" %cmd)
        proc = subprocess.Popen([cmd], shell=True)
        ret = proc.wait()
        self._logger.debug("return code: %s" %ret)
        time.sleep(20)	#TODO: waiting for sm stop
        if not util.check_process('java -DApp=ipw%ssm' %(sm_type.lower()), "stop"):
            raise Exception("Server Manager Doesn't Stopped !")
        self._logger.debug("<<")


    def set_log_level(self, conf_path, level=5) :
        replace_pair_list = [ ["Log.Level=\d+", "Log.Level=" + str(level)] ]
        util.replace_context(conf_path, replace_pair_list)



