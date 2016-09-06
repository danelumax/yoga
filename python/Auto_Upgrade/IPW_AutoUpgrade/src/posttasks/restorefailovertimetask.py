import os,re,subprocess
import log, common

from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil

class RestoreFailoverTimeTask(object) :
    """
    Restore Failover Time
    """

    def __init__(self) :
        self._ss_host   = None
        self._ipwss_vip = None
        self._admin     = None
        self._password  = None
        self._snapshot  = None
        pass

    def _initial(self, node):
        assert node != None

        self._ss_host, self._ipwss_vip = self._GetSsIP(node)
        self._admin = cfgInstance().getCliUserName()
        self._password = cfgInstance().getCliPassword()
        self._snapshot = "list_dhcpv4server.tmp"
        assert os.path.exists(self._snapshot)

    def precheck(self) :
        pass


    def execute(self, node):
        log._file.debug(">> Restore Failover Time Begin")
        if (common.C_IPW_APP_DHCP not in common.g_upgrade_service) \
           and (common.g_upgrade_app != common.C_IPW_APP_CLF):
            log._file.debug("Not installed dhcp service, ignore this task!")
        else:
            if not common.g_need_shorting_failover_time:
                log._file.debug("'need shorting failover time' is False, skip this task.")
                return

            self._initial(node)
            # 1. list the dhcpv4server
            cmd = "list dhcpv4server"
            res = self._ExecuteIPWcli(cmd)

            # 2. get the primary and failover-mclt
            primary = None
            failover_mclt = None
            lines = res.split("\n")
            for line in lines:
                if re.search("Primary:", line):
                    primary = line.split(":")[1]
                    primary = primary.strip()
                    log._file.debug("Get the primary dhcp server %s" %primary)
                elif re.search("V4Option:", line):
                    value_list = line.split(":")[1]
                    if not re.search("failover-mclt", value_list):
                        log._file.debug("No V4Option with 'failover-mclt'")
                        continue
                    value_list = value_list.strip()
                    items = value_list.split(",")
                    for i in range(len(items)):
                        item = items[i].strip()
                        name = item.split()[0]
                        if name == "failover-mclt":
                            failover_mclt = item.split()[1]
                            log._file.debug("Get the value of V4Optoin 'failover-mclt %s'" %failover_mclt)
                            break

            # 3. modify the failover-mctl to default value for primary
            # 3.1 Remove the 'failover-mclt 60'
            # 3.2 Change it back, if previous value exist
            if primary == None:
                log._file.warning("Didn't find any primary dhcp server! They're NOT failover mode, skip this task!")
            else:
                if failover_mclt != None:
                    log._file.debug("Modify the V4Option to remove the 'failover-mclt %s', which added by shortening failover time task!" %failover_mclt)
                    cmd = "modify dhcpv4server %s -remove V4Option='failover-mclt %s'" %(primary, failover_mclt)
                    self._ExecuteIPWcli(cmd)

                # Get previous value for failover-mclt
                previous = self._GetPrevious()
                if previous != None:
                    log._file.debug("Modify the V4Option to add the pevious 'failover-mclt %s'" %previous)
                    cmd = "modify dhcpv4server %s -add V4Option='failover-mclt %s'" %(primary, previous)
                    self._ExecuteIPWcli(cmd)

                cmd = "update dhcpv4server %s" %primary
                self._ExecuteIPWcli(cmd)
        log._file.debug("<< Restore Failover Time End")


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        assert os.path.exists(self._snapshot)

        fd = open(self._snapshot, 'r')
        content = fd.read()
        fd.close()
        log._file.debug("Content of " + self._snapshot + ":\n" + content)

        log._file.debug("Remove the snapshot file, which record the dhcpv4server status")
        os.remove(self._snapshot)
        pass

    def help(self):
        log._print.info("Login the Active SS:")
        log._print.info("IPWorks> modify dhcpv4server -remove V4Option='failover-mclt 60'")
        log._print.info("IPWorks> update")
        log._print.info("If previous value configured for it, please change it back!")
        pass

    def _GetPrevious(self):
        fd = open(self._snapshot, 'r')
        content = fd.read()
        fd.close()

        failover_mclt = None
        lines = content.split("\n")
        for line in lines:
            if re.search("V4Option:", line):
                value_list = line.split(":")[1]
                if not re.search("failover-mclt", value_list):
                    log._file.debug("No V4Option with 'failover-mclt'")
                    break
                else:
                    value_list = value_list.strip()
                    items = value_list.split(",")
                    for i in range(len(items)):
                        item = items[i].strip()
                        name = item.split()[0]
                        if name == "failover-mclt":
                            failover_mclt = item.split()[1]
                            log._file.debug("Get the previous value of V4Optoin 'failover-mclt %s'" %failover_mclt)
                            break
        return failover_mclt

    def _GetSsIP(self, node):
        cfg = cfgInstance()
        if common.C_IPW_MODE_SINGLE == common.g_ipw_mode:
            ss_host = self._hostname
            ipwss_vip = self._hostip
        elif common.C_IPW_MODE_MEDIUM1 == common.g_ipw_mode \
        or common.C_IPW_MODE_MEDIUM2 == common.g_ipw_mode:
            ss_host = cfg.getSsCfg(0).getHostName()
            ipwss_vip = cfg.getHaCfg().getSsVip()
        elif common.C_IPW_MODE_ENTRY1 == common.g_ipw_mode \
        or common.C_IPW_MODE_ENTRY2 == common.g_ipw_mode:
            ss_host = cfg.getSsCfg(0).getHostName()
            ipwss_vip = cfg.getSsCfg(0).getOamIp()

        return ss_host, ipwss_vip

    def _RemoteExec(self, hostname, command):
        ssh = sshManagerInstance().getSsh(hostname)
        ssh_util = SshUtil(ssh)
        res, _rcode = ssh_util.remote_exec(command, p_err=False, throw=False)
        return res

    def _ExecuteIPWcli(self, cmd, expect=None):
        self._RemoteExec(self._ss_host, "cd " + cfgInstance().getUpgradePath())
        res = self._RemoteExec(self._ss_host, "python ssipwcli.py --ipwss_vip=%s --user=%s --password=%s --command=\"%s\" --expect=%s" %(self._ipwss_vip, self._admin, self._password, cmd, expect))
        return res
