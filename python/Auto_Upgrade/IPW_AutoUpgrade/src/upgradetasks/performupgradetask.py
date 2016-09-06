import log, common
import ipwutils
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class PerformUpgradeTask(object) :
    """
    Perform Upgrade
    """

    def __init__(self) :
        self._hostname     = None
        self._upgrade_path = None
        self._mount_point  = None
        pass

    def _initial(self, node):
        assert node != None

        self._hostname     = node.getHostName()
        self._upgrade_path = cfgInstance().getUpgradePath()
        self._mount_point  = cfgInstance().getMountPoint()

    def precheck(self) :
        pass


    def execute(self, node = None):
        log._file.debug(">> PerforemUpgradeTask Begin")

        self._initial(node)

        log._file.debug(">>> PerforemUpgradeTask on " + self._hostname)

        ipwutils.mountShareDir(node)

        ssh = sshManagerInstance().getSsh(self._hostname)
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("cd " + self._upgrade_path)
        command = "python upgrade.py --mount_point=%s" %self._mount_point
        res, rcode = ssh_util.remote_exec(command, p_err=False, throw=False)

        ipwutils.unmountShareDir(node)
        if rcode != 0:
            log._file.error("Perform Upgrade IPWorks failed!"+res)
            raise Exception("Perform Upgrade IPWorks failed!")

        log._file.debug("<< PerforemUpgradeTask End on " + self._hostname)


    def verify(self):
        pass

    def cleanup(self):
        pass

    def updateProgress(self):
        pass

    def help(self):
        """
        Login to the target server:
        1. Check is there any running IPWorks process?
           # ps -ef | grep ipw
           If yes, please kill them, try auto upgrade again.
           else, please manually upgrade it.

        2. Check the target version installed the same components as current version
           # ls /opt/IPWorks/*/*
           /opt/IPWorks/14.b/AVA_901_16_4_R3B02:
           IPWasdnsmon  IPWbackup  IPWcli  IPWcnoss  IPWcommon  IPWdns  IPWjre  IPWmysql  IPWslm  IPWsm  IPWss  IPWtomcat  IPWwebui  version.txt

           /opt/IPWorks/15.b/AVA_901_16_5_R1A03:
           IPWasdnsmon  IPWbackup  IPWcli  IPWcnoss  IPWcommon  IPWdns  IPWjre  IPWmysql  IPWslm  IPWsm  IPWss  IPWtomcat  IPWwebui  version.txt

           If not, manually install the absent component via 'ipwsetup'.

        3. Ensure target system time is correct.
           If it's older than real time, please correct it manually.

        4. Check the mount point on target server is correct, no reboot in the whole upgrade.
           a) Use 'mount' to show all the mount point, and check IPWorks ISO is mounted correctly.
           # mount
           /Auto_upgrade/AVA90116_5_R1A05_buildxxxx.iso on /mnt type iso9660 (ro)

           b) If it's NOT mounted, use the following command to mount it manually.
           # mount -o loop AVA90116_5_R1A05_buildxxxx.iso /mnt
        """
        log._print.info("Please ensure all IPWorks processes are stoppped.")
        log._print.info("If upgrade fail, please check messages in log file: /var/ipworks/logs/ipworks_ipwsetup_%s.log" %(self._hostname))
        log._print.info("Please use the following steps to manually fix it on host '%s':" %(self._hostname))
        log._print.info(self.help.__doc__)
        pass

