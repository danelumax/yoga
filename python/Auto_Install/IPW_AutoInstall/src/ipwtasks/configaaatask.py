import re, time, random, os, traceback, sys
import log, common
from scp import Scp
from sshutil import SshUtil
from cfg import cfgInstance
from hautil import hautilInstance
from sshmanager import sshManagerInstance
import errutil


class ConfigAAATask(object) :
    """
    Config AAA Server
    """

    def __init__(self) :
        pass

    def precheck(self) :
        pass


    def execute(self):
        log._file.debug(">> Config AAA Server Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :  # single
            self._configAAASingle()
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) : # entry1
            self._configAAAEntry()
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :  # medium1
            self._configAAAMedium()
        else :
            log._file.debug("No need to config AAA")
        log._file.debug("<< Config AAA Server End")
    

    def verify(self):
        log._file.debug(">> Check AAA Server Status Begin")
        common.save_healthcheck_info("AAA Server Status", 'normal', 'normal', "OK")
        log._file.debug("<< Check AAA Server Status End")
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass


    def _configAAASingle(self) :
        log._file.debug(">> Config AAA Server in Single mode Begin")
        ps1 = cfgInstance().getPsCfg(0)
        self._configCoreServer(ps1, ps1.getInternalIp(), ps1.getInternalIp())
        self._configRadiusStack(ps1)
        self._configPlugins(ps1, ps1.getInternalIp(), ps1.getInternalIp())
        self._configDiameter(ps1, ps1.getInternalIp(), ps1.getInternalIp())
        self._configCSV(ps1, ps1.getOamIp())
        self._startCsvengine(ps1)
        try :
            # verify
            srv_ip = "%s,%s" %(ps1.getOamIp(), ps1.getTrafficIp())
            self._createAAAServer(ps1, ps1.getInternalIp(), srv_ip)
            self._startSm(ps1)
            self._verifyAAA(ps1, ps1, ps1.getInternalIp())
        except Exception, e :
            log._file.error("Exception in _configAAASingle : " + str(e))
            raise
        finally :
            # cleanup
            self._stopSm(ps1)
            self._deleteAAAServer(ps1, ps1.getInternalIp())
            self._removeFile(ps1)
        log._file.debug("<< Config AAA Server in Single mode End")


    def _configAAAEntry(self) :
        log._file.debug(">> Config AAA Server in Entry1 mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
        for ps_cfg in cfg.getPsCfgList() :
            self._configCoreServer(ps_cfg, ss1.getInternalIp(), ss1.getInternalIp())
            self._configRadiusStack(ps_cfg)
            self._configPlugins(ps_cfg, ss1.getInternalIp(), ss1.getInternalIp())
            self._configDiameter(ps_cfg, ss1.getInternalIp(), ss1.getInternalIp())
        self._configCSV(ss1, ss1.getOamIp())
        self._startCsvengine(ss1)
        try :
            # verify
            srv_ip = "%s,%s" %(ps1.getOamIp(), ps1.getTrafficIp())
            self._createAAAServer(ss1, ss1.getInternalIp(), srv_ip)
            self._startSm(ps1)
            self._verifyAAA(ss1, ps1, ss1.getInternalIp())
        except Exception, e :
            log._file.error("Exception in _configAAAEntry : " + str(e))
            raise
        finally :
            self._stopSm(ps1)
            self._deleteAAAServer(ss1, ss1.getInternalIp())
            self._removeFile(ps1)
            self._removeFile(ps2)
        log._file.debug("<< Config AAA Server in Entry1 mode End")


    def _configAAAMedium(self) :
        log._file.debug(">> Config AAA Server in Medium1 mode Begin")
        cfg = cfgInstance()
        ss1 = cfg.getSsCfg(0)
        ss2 = cfg.getSsCfg(1)
        ps1 = cfg.getPsCfg(0)
        ps2 = cfg.getPsCfg(1)
  
        for ps_cfg in cfg.getPsCfgList() :
            self._configCoreServer(ps_cfg, cfg.getHaCfg().getMgmVip(), cfg.getHaCfg().getSqlVip())
            self._configRadiusStack(ps_cfg)
            self._configPlugins(ps_cfg, cfg.getHaCfg().getMgmVip(), cfg.getHaCfg().getCsvVip())
            self._configDiameter(ps_cfg, cfg.getHaCfg().getMgmVip(), cfg.getHaCfg().getSqlVip())

        self._configCSV(ss1, cfg.getHaCfg().getMgmVip(), cfg.getHaCfg().getSsVip())
        self._registerHaCsvengine(ss1, ss2, cfg.getHaCfg().getMgmVip())
        self._startHaCsvengine(ss1)

        try :
            # verify
            srv_ip = "%s,%s" %(ps1.getOamIp(), ps1.getTrafficIp())
            self._createAAAServer(ss1, cfg.getHaCfg().getSsVip(), srv_ip)
            self._startSm(ps1)
            self._verifyAAA(ss1, ps1, cfg.getHaCfg().getSsVip())
        except Exception, e :
            log._file.error("Exception in _configAAAMedium : " + str(e))
            raise
        finally :
            self._stopSm(ps1)
            self._deleteAAAServer(ss1, cfg.getHaCfg().getSsVip())
            self._removeFile(ps1)
            self._removeFile(ps2)
        log._file.debug("<< Config AAA Server in Medium1 mode End")


#########################################################################################
  

    def _configCoreServer(self, cfg, mgm_vip, sql_vip):
        log._file.debug(">> Config Core Server on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_core_server --mgm_vip=' + mgm_vip + ' --sql_vip=' + sql_vip + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")

    
    def _configRadiusStack(self, cfg):
        log._file.debug(">> Config Radius Stack on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_radius_stack' + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _configPlugins(self, cfg, mgm_vip, csv_vip):
        log._file.debug(">> Config Plugins on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_plugins --mgm_vip=%s --csv_vip=%s --aaasrv_ip=%s --username=%s --password=%s ' %(mgm_vip, csv_vip, cfg.getOamIp(), common.g_cli_username, common.g_cli_password)
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _configCSV(self, cfg, mgm_vip, ss_vip=''):
        log._file.debug(">> Config CSV on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_csv --mgm_vip=' + mgm_vip + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        if ss_vip :
            command = 'python configaaa.py --command=enable_sessionrecord --ipwss_vip=' + ss_vip + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        else :
            ssh_util.remote_exec('chkconfig -s ipworks.aaa_csv_engine on', p_err=False, throw=False)
            ssh_util.remote_exec('chkconfig -s ipworks.aaa_csv_engine_monitor on', p_err=False, throw=False)
            command = 'python configaaa.py --command=enable_sessionrecord' + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _configDiameter(self, cfg, mgm_vip, sql_vip):
        log._file.debug(">> Config Diameter on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_diameter --mgm_vip=' + mgm_vip + ' --sql_vip=' + sql_vip + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")
 

    def _configServerManager(self, cfg, ss_vip):
        log._file.debug(">> Config Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        res, r_code = ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=config_aaa_sm --ipwss_vip=' + ss_vip + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        res, r_code = ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _registerHaCsvengine(self, ss1_cfg, ss2_cfg, mgm_vip):
        log._file.debug(">> Register CSV engine resource on " + ss1_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss1_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if not cmp(ss1_cfg.getPassword(), ss2_cfg.getPassword()) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --diskarray --ndb-mgm-vip " + mgm_vip + " --all-password=" + ss1_cfg.getPassword()
            else:
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_csvengine.pl --nfs --ndb-mgm-vip " + mgm_vip + " --all-password=" + ss1_cfg.getPassword()
        else :
            passwd = '%s,%s' %(ss1_cfg.getPassword(), ss2_cfg.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=csvengine --password=%s --mgm_vip=%s --mode=diskarray' %(passwd, mgm_vip)
            else:
                command = 'python register_cluster.py --command=csvengine --password=%s --mgm_vip=%s --mode=nfs' %(passwd, mgm_vip)
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        # wait for fs clone start
        if common.C_EMC_MOUNT_MODE_DOUBLE:
            hautilInstance().waitCsvCloneStart(ssh)
        log._file.debug("<<")


    def _startHaCsvengine(self, cfg):
        log._file.debug(">> Start CSV engine HA resource group on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        hautilInstance().startCsvResGrp(ssh)
        hautilInstance().waitCsvResGrpStart(ssh)
        log._file.debug("<<")


    def _startCsvengine(self, cfg):
        log._file.debug(">> Start CSV engine on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("/etc/init.d/ipworks.aaa_csv_engine start")
        log._file.debug("<<")


    def _createAAAServer(self, ss_cfg, ss_vip, srv_ip) :
        log._file.debug(">> Create AAA server on " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=create_aaa --ipwss_vip=%s --aaasrv_ip=%s' %(ss_vip, srv_ip) + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _deleteAAAServer(self, ss_cfg, ss_vip) :
        log._file.debug(">> Delete AAA server on " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=delete_aaa --ipwss_vip=%s' %(ss_vip) + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _verifyAAA(self, ss_cfg, ps_cfg, ss_vip) :
        log._file.debug(">> Verify AAA server on " + ss_cfg.getHostName())
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_ps = sshManagerInstance().getSsh(ps_cfg.getHostName())
        ssh_util_ps = SshUtil(ssh_ps)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        # update aaaserver on ss
        command = 'python configaaa.py --command=update_aaa --ipwss_vip=%s' %(ss_vip) + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        # start aaaserver process on ps
        ssh_util_ps.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configaaa.py --command=start_aaa' + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util_ps.remote_exec(command)
        # check aaaserver process status on ss
        command = 'python configaaa.py --command=verify_aaa --ipwss_vip=%s' %(ss_vip) + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        # check aaaserver alarm on ps
        command = common.getAlarmCmd('ipworksAAA')
        res,code = ssh_util_ps.remote_exec(command, p_err=False, throw=False)
        alarm = common.parseAlarmInfo(res)
        if alarm :
            item = "Alarm %s On %s" %('ipworksAAA', ps_cfg.getHostName())
            common.save_healthcheck_info(item, alarm, "", "--")
        # check error log
        errutil.checkAAAErrorLog(ps_cfg)
        # stop aaaserver on ss
        command = 'python configaaa.py --command=stop_aaa --ipwss_vip=%s' %(ss_vip) + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<")


    def _startSm(self, cfg) :
        log._file.debug(">>> Start Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=start_aaasm' + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _stopSm(self, cfg) :
        log._file.debug(">>> Stop Server Manager on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configsm.py --command=stop_aaasm' + " --password=" +common.g_cli_password \
                  + ' --username=' + common.g_cli_username
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

    
    def _removeFile(self, cfg):
        log._file.debug(">>> Remove Files on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("rm /etc/ipworks/aaa/ca_cert_path/ca.pem", p_err=False, throw=False)
        ssh_util.remote_exec("rm /etc/ipworks/aaa/serv_key/server.key", p_err=False, throw=False)
        ssh_util.remote_exec("rm /etc/ipworks/aaa/serv_cert/server.pem", p_err=False, throw=False)
        log._file.debug("<<<")



