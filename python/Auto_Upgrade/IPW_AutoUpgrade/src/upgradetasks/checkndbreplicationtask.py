import os,re,subprocess,sys
import log, common
import ipwutils
import time

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

from hautil import hautilInstance

class CheckNDBReplicationTask(object) :
    """
    Check NDB Replication
    """

    def __init__(self) :
        self._mysql_bin = '/usr/local/mysql/bin/mysql'

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> StartMgmNodeTask Begin")
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode):
            self._checkNDBReplication(cfg, cfg, '', '')
        elif not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) :
            ss1 = cfgInstance().getSsCfg(0)
            ss2 = cfgInstance().getSsCfg(1)
            innodb = self._getInnodbCfg(ss1, ss2)
            if common.g_isInstall_AAA:
                sqlnode = self._getSqlnodeCfg(ss1, ss2)
            else:
                sqlnode = cfg
            self._checkNDBReplication(innodb, sqlnode, '', '')
        else:
            innodb = cfgInstance().getSsCfg(0)
            self._checkNDBReplication(innodb, cfg, '', '')
        log._file.debug("<< StartMgmNodeTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to check NDB replication manually:")
        helpinfo='''
        # /usr/local/mysql/bin/mysql -P 3307 --protocol=tcp
        mysql> show slave status\G
        
        If error appears, refer to '5.15.2.7 Replication Failure' in 'IPWorks Troubleshooting Guideline'

	If no error, but the value of Seconds_Behind_Master is greater than 0, the replication process is running. Wait for it to complete.
        '''
        log._print.info(helpinfo)
        pass

    def _getInnodbCfg(self, ss1_cfg, ss2_cfg) :
        ssh = sshManagerInstance().getSsh(ss1_cfg.getHostName())
        hostname = hautilInstance().ssStartOn(ssh)
        if hostname == ss1_cfg.getHostName():
            cfg = ss1_cfg
        elif hostname == ss2_cfg.getHostName():
            cfg = ss2_cfg
        else:
            raise Exception("group-ipwss started on unknown host: " + hostname)
        return cfg

    def _getSqlnodeCfg(self, ss1_cfg, ss2_cfg) :
        ssh = sshManagerInstance().getSsh(ss1_cfg.getHostName())
        hostname = hautilInstance().sqlStartOn(ssh)
        if hostname == ss1_cfg.getHostName():
            cfg = ss1_cfg
        elif hostname == ss2_cfg.getHostName():
            cfg = ss2_cfg
        else:
            raise Exception("group-sqlnode started on unknown host: " + hostname)
        return cfg

    def _checkNDBReplication(self, ss_cfg, sql_cfg, innodb_ip, sql_ip) :
        log._file.debug(">>> Check SYNC between Innodb and Ndb")
        replicate_done = False
        # TR HI38883 start
        max_retry = 3 # retry three times
        while not replicate_done and max_retry > 0 :
            slave_bin_log_file, slave_bin_log_pos, seconds_behind_master = self._getSlaveBinLog(sql_cfg, sql_ip)
            while seconds_behind_master > 0 :
                slave_bin_log_file, slave_bin_log_pos, seconds_behind_master = self._getSlaveBinLog(sql_cfg, sql_ip)
                log._file.debug("Seconds behind Master: " + str(seconds_behind_master))
                log._file.debug("The NDB Replication may take at least %d seconds: " % seconds_behind_master)
                time.sleep(3)

            master_bin_log_file, master_bin_log_pos = self._getMasterBinLog(ss_cfg, innodb_ip)
            if master_bin_log_file == slave_bin_log_file and master_bin_log_pos == slave_bin_log_pos :
                replicate_done = True
                break
            else :
                time.sleep(3)
                max_retry -= 1
        # TR HI38883 end

        if not replicate_done :
            raise Exception("replication timeout!!!")
        log._file.debug("<<<")

    def _getMasterBinLog(self, cfg, innodb_ip) :
        log._file.debug(">>> Fetch Master status on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if innodb_ip :
            command = self._mysql_bin + ' -h ' + innodb_ip + ' -u ipworks -pipworks -e "show master status\G"'        
        else :
            command = self._mysql_bin + ' -e "show master status\G"'
        res, r_code = ssh_util.remote_exec(command)
        bin_log_file = ""
        bin_log_pos = 0
        lines = res.split('\n')
        for line in lines:
            toks = line.strip().split(':')
            if len(toks) == 2 :
                if toks[0] == "File" :
                    bin_log_file = toks[1].strip()
                elif toks[0] == "Position" :
                    bin_log_pos = int(toks[1].strip())
        log._file.debug("Master status: file = " + bin_log_file + ', pos = ' + str(bin_log_pos))
        return bin_log_file, bin_log_pos

    def _getSlaveBinLog(self, cfg, sql_ip):
        log._file.debug(">>> Fetch Slave status on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if sql_ip :
            command = self._mysql_bin + ' -h ' + sql_ip + ' -P 3307 --protocol=tcp -e "show slave status\G"'
        else :
            command = self._mysql_bin + ' -P 3307 --protocol=tcp -e "show slave status\G"'
        res, r_code = ssh_util.remote_exec(command)
        bin_log_file = ""
        bin_log_pos = 0
        seconds_behind_master = -1
        lines = res.split('\n')
        for line in lines :
            toks = line.strip().split(':')
            if len(toks) == 2 :
                if toks[0] == "Master_Log_File" :
                    bin_log_file = toks[1].strip()
                elif toks[0] == "Read_Master_Log_Pos" :
                    bin_log_pos = int(toks[1].strip())
                elif toks[0] == "Seconds_Behind_Master" :
                    tmp = toks[1].strip()
                    if tmp.isdigit():
                        seconds_behind_master = int(tmp)
                    elif 'NULL' == tmp:
                        seconds_behind_master = -1
        if not bin_log_file :
            ipwutils.changeMaster(cfg)
        else :
            log._file.debug("Slave status: file = " + bin_log_file + ', pos = ' + str(bin_log_pos) + ', behind = ' + str(seconds_behind_master))
        return bin_log_file, bin_log_pos, seconds_behind_master

