import log, common
import utils
import ipwutils

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

from hautil import hautilInstance

class SyncNDBSchemaTask(object) :
    """
    Sync NDB Schema
    """

    def __init__(self) :
        self._mysql_bin = '/usr/local/mysql/bin/mysql'
        self._datanode_iplist = []

    def precheck(self) :
        pass


    def execute(self,cfg = None):
        log._file.debug(">> SyncNDBSchemaTask Begin")
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) \
	  or not cmp(common.C_IPW_MODE_ENTRY1,common.g_ipw_mode) :
            self._startSqlNode(cfg)
            self._changeMaster(cfg)
            self._grantPrivileges(cfg)
            self._syncNDBSchema(cfg)
            self._stopSQLNode(cfg)
        log._file.debug("<< SyncNDBSchemaTask End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        log._print.info("")
        log._print.info("    Please refer to the following steps to sync NDB schema manually:")
        helpinfo='''
        1. Start the SQL node.
        Note: Do NOT use the Control Panel to start the SQL node.
        If the disk array is VNXe3200
            # mount /global/sqlnode
        # /etc/init.d/ipworks.mysql start-sqlnode /etc/ipworks/mysql/confs/sqlnode1.conf --skip-slave-start &

        2. Change the master server for the SQL nodes.
        # /usr/local/mysql/bin/mysql -P 3307 --protocol=tcp
        mysql> change master to master_host='<Master_Host>', master_user='<Master_User>', master_password='<Master_Password>';
        mysql> quit
        Note: The <Master_Host>, <Master_User>, and <Master_Password> represent the values of corresponding parameters in /etc/ipworks/mysql/confs/sqlnode_masterinfo.conf.

        3. Grant all privileges to SQL nodes.
        # /usr/local/mysql/bin/mysql -P 3307 --protocol=tcp
        mysql> grant all privileges on *.* to 'ipworks'@'<SS O&M IP Address>' identified by 'ipworks';
        mysql> grant all privileges on *.* to ''@'<Each PS O&M IP Address>' identified by '';
        mysql> quit

        4. Synchronize the MySQL static data between InnoDB and ndb.
        # /opt/ipworks/IPWss/db/ipw-ndb-sync -Innodb h=<ipwss_vip>:P=3306 -sqlnode h=<SS O&M IP Address>:P=3307 -changeschema
        The duration of the synchronization may take time depends on the size of user data. For example, for 2M aaauser, it will take 30 minutes.
        To shorten this time, you can use "-simpleCheck" option. It will only check count, Max & Min id for each table.
        Ensure that the status for each checking item is either done or consistent.

        5. Stop the SQL node.
        # /etc/init.d/ipworks.mysql stop-sqlnode shutdown --protocol=tcp -P 3307
        If the disk array is VNXe3200
            # umount /global/sqlnode
        '''
        log._print.info(helpinfo)
        pass

    def _startSqlNode(self, host):
        log._file.debug(">> Start SqlNode begin on host " + host.getHostName())
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        if not common.C_EMC_MOUNT_MODE_DOUBLE:
            ipwutils.mountDir(host, "/global/sqlnode")
        cmd = "/etc/init.d/ipworks.mysql start-sqlnode /etc/ipworks/mysql/confs/sqlnode1.conf --skip-slave-start"
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "sqlnode", "start"):
            log._file.error("Start SqlNode failed")
            raise Exception("Start SqlNode failed")
        log._file.debug("Start SqlNode Succeed!")

    def _stopSQLNode(self, host):
        log._file.debug(">> Stop SQLNode begin on host " + host.getHostName())
        cmd = "/etc/init.d/ipworks.mysql stop-sqlnode shutdown --protocol=tcp -P 3307"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        if not utils.check_process(ssh, "sqlnode", "stop"):
            log._file.error("Stop SQLNode failed")
            raise Exception("Stop SQLNode failed")
        if not common.C_EMC_MOUNT_MODE_DOUBLE:
            ipwutils.unmountDir(host, "/global/sqlnode")
        log._file.debug("Stop SQLNode Succeed!")

    def _grantPrivileges(self, cfg) :
        ss1 = cfgInstance().getSsCfg(0)
        self._grantPrivilegesToSs(cfg, ss1.getInternalIp())
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode):
            ss2 = cfgInstance().getSsCfg(1)
            self._grantPrivilegesToSs(cfg, ss2.getInternalIp())
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._datanode_iplist.append(ps1.getInternalIp())
        self._datanode_iplist.append(ps2.getInternalIp())
        self._grantPrivilegesToPs(cfg)

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

    def _syncNDBSchema(self, host) :
        log._file.debug(">>> Sync NDB Schema on host " + host.getHostName())
        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode):
            ss_ip = cfgInstance().getHaCfg().getSsVip()
        else:
	    ss_ip = host.getOamIp()
        sql_ip = host.getOamIp()
        cmd = '/opt/ipworks/IPWss/db/ipw-ndb-sync -Innodb h=' + ss_ip + ':P=3306 -sqlnode h=' + sql_ip + ':P=3307 -changeschema'
        if common.g_ndbSyncSimpleCheck :
            cmd = cmd + ' -simpleCheck'
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec(cmd)
        log._file.debug("<<<")
     
    def _changeMaster(self, host) :
        log._file.debug(">>> Change Master on " + host.getHostName())
        cmd = "grep master-host /etc/ipworks/mysql/confs/sqlnode_masterinfo.conf"
        ssh = sshManagerInstance().getSsh(host.getHostName())
        ssh_util = SshUtil(ssh)
        ret, r_code = ssh_util.remote_exec(cmd)
        innodb_ip = ret[ret.find("=")+1:]
        cmd = '/usr/local/mysql/bin/mysql -P 3307 --protocol=tcp -e "stop slave;change master to master_host=\'' + innodb_ip + '\', master_user=\'ipworks\', master_password=\'ipworks\';"'
        ssh_util.remote_exec(cmd)
