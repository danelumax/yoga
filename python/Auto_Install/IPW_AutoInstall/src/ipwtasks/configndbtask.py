import re, time, random, os
import log, common
from sshutil import SshUtil
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from hautil import hautilInstance



class ConfigNdbTask(object):
    '''
    Config NDB Cluster
    '''


    def __init__(self):
        self._mysql_bin = '/usr/local/mysql/bin/mysql'
        self._datanode_id = 27
        self._server_id = 2
        self._datanode_iplist = []
        self._sqlnode_iplist = []

        
    def precheck(self):
        #TODO: check the ISO file exist 
        #TODO: check the mount point exist and free to use
        pass
    
    def execute(self):
        log._file.debug(">> Config NDB Begin")
        cfg = cfgInstance()

        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode):  # single
            log._file.debug(">> Config NDB in Single Mode")
            if common.g_isInstall_AAA or common.g_isInstall_ENUM :
                ps1 = cfg.getPsCfg(0)
                # grant privileges to sqlnode
                self._sqlnode_iplist.append(ps1.getInternalIp())
                self._grantPrivilegesToSqlnode(ps1)
                # config ndb
                self._datanode_iplist.append(ps1.getInternalIp())
                self._configNDBSingle(ps1, ps1.getInternalIp(), self._server_id)
                if common.g_isInstall_AAA:
                    # grant privileges to ps
                    self._grantPrivilegesToPs(ps1)
                # grant privileges to ss for ndbcluster alarm
                self._grantPrivilegesToSs(ps1, ps1.getInternalIp())
            else :
                log._file.debug("No need to Config NDB")          

        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode):  # entry1
            log._file.debug(">> Config NDB in Entry1 Mode")
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            ps2 = cfg.getPsCfg(1)
            if common.g_isInstall_AAA :
                log._file.debug("Config NDB with AAA")
                # grant privileges to sqlnode
                self._sqlnode_iplist.append(ss1.getInternalIp())
                self._grantPrivilegesToSqlnode(ss1)
                # config ndb
                self._datanode_iplist.append(ps1.getInternalIp())
                self._datanode_iplist.append(ps2.getInternalIp())
                self._configNDBDataNodeHA(ss1)
            elif common.g_isInstall_ENUM :
                log._file.debug("Config NDB with ENUM")
                # grant privileges to sqlnode
                self._sqlnode_iplist.append(ps1.getInternalIp())
                self._sqlnode_iplist.append(ps2.getInternalIp())
                self._grantPrivilegesToSqlnode(ss1)
                # config ndb
                self._datanode_iplist.append(ps1.getInternalIp())
                self._configNDBSingle(ps1, ss1.getInternalIp(), self._server_id)
                self._datanode_iplist = []
                self._datanode_iplist.append(ps2.getInternalIp())
                self._configNDBSingle(ps2, ss1.getInternalIp(), self._server_id+1)
                # grant privileges to ss for ndbcluster alarm
                self._grantPrivilegesToSs(ps1, ss1.getInternalIp())
                self._grantPrivilegesToSs(ps2, ss1.getInternalIp())
            else :
                log._file.debug("No need to Config NDB")
             
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode):  #entry2
            log._file.debug(">> Config NDB in Entry2 Mode")
            ss1 = cfg.getSsCfg(0)
            ps1 = cfg.getPsCfg(0)
            if common.g_isInstall_ENUM :
                log._file.debug("Config NDB with ENUM")
                # grant privileges to sqlnode
                self._sqlnode_iplist.append(ss1.getInternalIp())
                self._sqlnode_iplist.append(ps1.getInternalIp())
                self._grantPrivilegesToSqlnode(ss1)
                # config ndb
                self._datanode_iplist.append(ss1.getInternalIp())
                self._configNDBSingle(ss1, ss1.getInternalIp(), self._server_id)
                self._datanode_iplist = []
                self._datanode_iplist.append(ps1.getInternalIp())
                self._configNDBSingle(ps1, ss1.getInternalIp(), self._server_id+1)
                # grant privileges to ss for ndbcluster alarm
                self._grantPrivilegesToSs(ps1, ss1.getInternalIp())
                self._grantPrivilegesToSs(ss1, ss1.getInternalIp())
            else :
                log._file.debug("No need to Config NDB")

        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode):  # medium1
            log._file.debug(">> Config NDB in Medium1 Mode")
            ss1 = cfg.getSsCfg(0)
            ss2 = cfg.getSsCfg(1)
            ps1 = cfg.getPsCfg(0)
            ps2 = cfg.getPsCfg(1)
            if common.g_isInstall_AAA :
                log._file.debug("Config NDB with AAA")
                # config ndb
                self._datanode_iplist.append(ps1.getInternalIp())
                self._datanode_iplist.append(ps2.getInternalIp())
                self._configNDBMultipleNodesHA()
            elif common.g_isInstall_ENUM :
                log._file.debug("Config NDB with ENUM")
                # grant privileges to sqlnode
                self._sqlnode_iplist.append(ps1.getInternalIp())
                self._sqlnode_iplist.append(ps2.getInternalIp())
                self._grantPrivilegesToSqlnode(ss1, cfg.getHaCfg().getSsVip())
                # config ndb
                self._datanode_iplist.append(ps1.getInternalIp())
                self._configNDBSingle(ps1, cfg.getHaCfg().getSsVip(), self._server_id)
                self._datanode_iplist = []
                self._datanode_iplist.append(ps2.getInternalIp())
                self._configNDBSingle(ps2, cfg.getHaCfg().getSsVip(), self._server_id+1)
                # grant privileges to ss for ndbcluster alarm
                self._grantPrivilegesToSs(ps1, ss1.getInternalIp())
                self._grantPrivilegesToSs(ps2, ss1.getInternalIp())
                self._grantPrivilegesToSs(ps1, ss2.getInternalIp())
                self._grantPrivilegesToSs(ps2, ss2.getInternalIp())
            else :
                log._file.debug("No need to Config NDB")

        elif not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):  # medium2
            log._file.debug(">> Config NDB in Medium2 Mode")
            log._file.debug("No need to Config NDB")

        log._file.debug(">> Config NDB End")


    
    def verify(self):
        log._file.debug(">> Check Innodb & NDB Begin")
        if common.g_isInstall_AAA or common.g_isInstall_ENUM :
            common.save_healthcheck_info("INNODB & NDB Status", 'Sync', 'Sync', "OK")
        else :
            log._file.debug("No need to Check NDB status")
        log._file.debug(">> Check Innodb & NDB End")
    
    def cleanup(self):
        pass
    
    def updateProgress(self):
        pass




    def _configNDBSingle(self, cfg, innodb_ip, serverId):
        log._file.debug(">>> Config NDB Single on " + cfg.getHostName())
        # mgmnode config
        self._configMgmd(cfg, cfg.getInternalIp(), self._datanode_iplist)
        self._startMgmd(cfg)
        # datanode config
        self._configNdbd(cfg, cfg.getInternalIp())
        self._startNdbd(cfg)
        self._checkNdbd(cfg)
        # sqlnode config
        self._configSqlNode(cfg, cfg.getInternalIp(), innodb_ip, serverId)
        self._configMasterInfo(cfg, innodb_ip)
        self._startSqlNode(cfg, innodb_ip)
        time.sleep(5)
        # wait innodb & ndb sync
        #self._waitReplication(cfg, innodb_ip, cfg.getInternalIp())
        self._waitReplication(cfg, innodb_ip, '')
        log._file.debug("<<<")



    def _configNDBDataNodeHA(self, ss_cfg) :
        log._file.debug(">>> ConfigNDB in Data Node HA on" + ss_cfg.getHostName())
        # mgmnode config
        self._configMgmd(ss_cfg, ss_cfg.getInternalIp(), self._datanode_iplist) 
        self._startMgmd(ss_cfg)
        # datanode config
        for ps_cfg in cfgInstance().getPsCfgList():
            self._configNdbd(ps_cfg, ss_cfg.getInternalIp())
        for ps_cfg in cfgInstance().getPsCfgList():
            self._startNdbd(ps_cfg)
        self._checkNdbd(ss_cfg)
        # sqlnode config
        self._configSqlNode(ss_cfg, ss_cfg.getInternalIp(), ss_cfg.getInternalIp(), self._server_id)
        self._configMasterInfo(ss_cfg, ss_cfg.getInternalIp())
        self._startSqlNode(ss_cfg, ss_cfg.getInternalIp())
        time.sleep(5)
        # wait innodb & ndb sync
        #self._waitReplication(ss_cfg, ss_cfg.getInternalIp(), ss_cfg.getInternalIp())
        self._waitReplication(ss_cfg, '', '')
        # grant privileges to ps
        self._grantPrivilegesToPs(ss_cfg)
        # grant privileges to ss for ndbcluster alarm
        self._grantPrivilegesToSs(ss_cfg, ss_cfg.getInternalIp())
        log._file.debug("<<<")




    def _configNDBMultipleNodesHA(self) :
        log._file.debug(">>> ConifgNDB in Multiple Nodes HA ")
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        # ndbcluster must register on node which SS running
        ss_cfg = self._getInnodbCfg(ss1, ss2)
        # mgmnode config
        self._configMgmd(ss_cfg, cfgInstance().getHaCfg().getMgmVip(), self._datanode_iplist)
        # register ndb resource group
        self._register_ha_resource(ss_cfg)
        # wait for fs clone start
        ssh = sshManagerInstance().getSsh(ss_cfg.getHostName())
        if common.C_EMC_MOUNT_MODE_DOUBLE:
            hautilInstance().waitMgmCloneStart(ssh)
            hautilInstance().waitSqlCloneStart(ssh)
            self._configMasterInfo(ss1, cfgInstance().getHaCfg().getSsVip())
            self._configMasterInfo(ss2, cfgInstance().getHaCfg().getSsVip())
        # start mgmnode resource group
        hautilInstance().startMgmnodeResGrp(ssh)
        hautilInstance().waitMgmnodeResGrpStart(ssh)
        time.sleep(5)
        # start sqlnode resource group
        hautilInstance().startSqlnodeResGrp(ssh)
        hautilInstance().waitSqlnodeResGrpStart(ssh)
        time.sleep(5)
        # after register ndbcluster, group-ipwss and group-sqlnode maybe change node to run
        ss_cfg = self._getInnodbCfg(ss1, ss2)
        sql_cfg = self._getSqlnodeCfg(ss1, ss2)
        # wait innodb & ndb sync
        self._waitReplication2(ss_cfg, sql_cfg, '', '')
        # grant privileges to ps
        self._grantPrivilegesToPs(sql_cfg)
        # grant privileges to ss for ndbcluster alarm
        self._grantPrivilegesToSs(sql_cfg, ss1.getInternalIp())
        self._grantPrivilegesToSs(sql_cfg, ss2.getInternalIp())
        log._file.debug("<<<")



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



##########################################################################################



    def _register_ha_resource(self, cfg) :
        log._file.debug(">>> Register NDB cluster resource on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        if not cmp(ss1.getPassword(), ss2.getPassword()) \
          and not cmp(ss1.getPassword(), ps1.getPassword()) \
          and not cmp(ss1.getPassword(), ps2.getPassword()) :
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --diskarray --all-password=" + cfg.getPassword()
            else:
                command = "echo 'Y' | /opt/ipworks/IPWhaagents/scripts/register_ndbcluster.pl --nfs --all-password=" + cfg.getPassword()
        else :
            passwd = '%s,%s,%s,%s' %(ss1.getPassword(), ss2.getPassword(), ps1.getPassword(), ps2.getPassword())
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()) :
                command = 'python register_cluster.py --command=ndbcluster --password=%s --mode=diskarray' %(passwd)
            else:
                command = 'python register_cluster.py --command=ndbcluster --password=%s --mode=nfs' %(passwd)
            ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


##########################################################################################


    def _grantPrivilegesToSqlnode(self, cfg, innodb_ip=''):
        log._file.debug(">>> Grant Privileges to SQL node for data replication on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        for ip in self._sqlnode_iplist:
            if innodb_ip :
                command = self._mysql_bin + ' -h ' + innodb_ip + ' -e "grant all privileges on *.* to \'ipworks\'@\'' + ip + '\' identified by \'ipworks\';"'
            else :
                command = self._mysql_bin + ' -e "grant all privileges on *.* to \'ipworks\'@\'' + ip + '\' identified by \'ipworks\';"'
            ssh_util.remote_exec(command)
        log._file.debug("<<<")



    def _grantPrivilegesToPs(self, cfg, sql_ip='') :
        log._file.debug(">>> Grant Privileges to PS to access SQL node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        for ip in self._datanode_iplist:
            if sql_ip :
                command = self._mysql_bin + ' -h ' + sql_ip + ' -P 3307 --protocol=tcp -e "grant all privileges on *.* to \'\'@\'' + ip + '\' identified by \'\';"'
            else :
                command = self._mysql_bin + ' -P 3307 --protocol=tcp -e "grant all privileges on *.* to \'\'@\'' + ip + '\' identified by \'\';"'
            ssh_util.remote_exec(command)
        log._file.debug("<<<")


    # for check ndbcluster alarm, ss node should be able to access sqlnode with username(ipworks) and password(ipworks)
    def _grantPrivilegesToSs(self, cfg, ip, sql_ip='') :
        log._file.debug(">>> Grant Privileges to SS to access SQL node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if sql_ip :
            command = self._mysql_bin + ' -h ' + sql_ip + ' -P 3307 --protocol=tcp -e "grant all privileges on *.* to \'ipworks\'@\'' + ip + '\' identified by \'ipworks\';"'
        else :
            command = self._mysql_bin + ' -P 3307 --protocol=tcp -e "grant all privileges on *.* to \'ipworks\'@\'' + ip + '\' identified by \'ipworks\';"'
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


##########################################################################################

    def _configMgmd(self, cfg, mgm_ip, datanode_ip_list) :
        log._file.debug(">>> Config Mgm node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        datanode_num = len(datanode_ip_list)

        command = 'python configndb.py --command=config_mgmd --ip=%s --data_mem=%s --index_mem=%s --data_num=%d' %(mgm_ip, cfgInstance().getDataMemSize(), cfgInstance().getIndexMemSize(), datanode_num)
        ssh_util.remote_exec(command)

        command = 'python configndb.py --command=clean_datanode'
        ssh_util.remote_exec(command)

        datanode_id = self._datanode_id
        for datanode_ip in datanode_ip_list :
            command = 'python configndb.py --command=add_datanode --id=' + str(datanode_id) + ' --ip=' + datanode_ip
            datanode_id += 1
            ssh_util.remote_exec(command)
        log._file.debug("<<<")



    def _startMgmd(self, cfg) :
        log._file.debug(">>> Start Mgm node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=start_mgmd'
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


##########################################################################################

    def _configNdbd(self, cfg, mgm_ip):
        log._file.debug(">>> Config Data node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=config_ndbd --ip=' + mgm_ip
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

   
    def _startNdbd(self, cfg) :
        log._file.debug(">>> Start Data node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=start_ndbd'
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _checkNdbd(self, cfg) :
        log._file.debug(">>> Check Data node status on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=check_ndbd'
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


##########################################################################################

    def _configSqlNode(self, cfg, mgm_ip, innodb_ip, server_id) :
        log._file.debug(">>> Config Sql node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=config_sqlnode --ss_vip=' + innodb_ip + ' --ip=' + mgm_ip + ' --id=' + str(server_id)
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


    def _configMasterInfo(self, cfg, innodb_ip) :
        log._file.debug(">>> Config Sql node MasterInfo on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=config_masterinfo --ss_vip=' + innodb_ip
        ssh_util.remote_exec(command)
        log._file.debug("<<<")

 
    def _startSqlNode(self, cfg, innodb_ip) :
        log._file.debug(">>> Start Sql node on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = 'python configndb.py --command=start_sqlnode --ss_vip=' + innodb_ip
        ssh_util.remote_exec(command)
        log._file.debug("<<<")


##########################################################################################

    def _getMasterBinLog(self, cfg, innodb_ip) :
        log._file.debug(">>> Fetch Master status on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        if innodb_ip :
            command = self._mysql_bin + ' -h ' + innodb_ip + ' -u ipworks -pipworks -e "show master status\G"'        
            #command = self._mysql_bin + ' -h ' + innodb_ip + ' -e "show master status\G"'
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
        log._file.debug("Slave status: file = " + bin_log_file + ', pos = ' + str(bin_log_pos) + ', behind = ' + str(seconds_behind_master))
        return bin_log_file, bin_log_pos, seconds_behind_master



    def _waitReplication(self, cfg, innodb_ip, sql_ip) :
        """ check slave status """
        log._file.debug(">>> Check SYNC between Innodb and Ndb on " + cfg.getHostName())
        replicate_done = False
        max_retry = 60
        seconds_behind_master = -1
        while not replicate_done and max_retry > 0 :
            seconds_behind_master = -1
            while seconds_behind_master != 0 and max_retry > 0 :
                slave_bin_log_file, slave_bin_log_pos, seconds_behind_master = self._getSlaveBinLog(cfg, sql_ip)
                log._file.debug("Seconds behind Master: " + str(seconds_behind_master))
                max_retry -= 1
                time.sleep(2)
            master_bin_log_file, master_bin_log_pos = self._getMasterBinLog(cfg, innodb_ip)
            
            if master_bin_log_file == slave_bin_log_file and master_bin_log_pos == slave_bin_log_pos :
                replicate_done = True
            else :
                time.sleep(1)
                max_retry -= 1

        if not replicate_done :
            raise Exception("replication timeout!!!")
        log._file.debug("<<<")


    def _waitReplication2(self, ss_cfg, sql_cfg, innodb_ip, sql_ip) :
        log._file.debug(">>> Check SYNC between Innodb and Ndb")
        replicate_done = False
        max_retry = 60
        while not replicate_done and max_retry > 0 :
            seconds_behind_master = -1
            while seconds_behind_master != 0 and max_retry > 0 :
                slave_bin_log_file, slave_bin_log_pos, seconds_behind_master = self._getSlaveBinLog(sql_cfg, sql_ip)
                log._file.debug("Seconds behind Master: " + str(seconds_behind_master))
                max_retry -= 1
                time.sleep(2)
            master_bin_log_file, master_bin_log_pos = self._getMasterBinLog(ss_cfg, innodb_ip)
            
            if master_bin_log_file == slave_bin_log_file and master_bin_log_pos == slave_bin_log_pos :
                replicate_done = True
            else :
                time.sleep(1)
                max_retry -= 1

        if not replicate_done :
            raise Exception("replication timeout!!!")
        log._file.debug("<<<")

   

 
