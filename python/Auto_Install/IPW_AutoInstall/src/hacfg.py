import re
import log, common

class HaCfg :
    """
    Class HaCfg
    """
    
    def __init__(self) :
        self._ss_vip = ""
        self._mgm_vip = ""
        self._sql_vip = ""
        self._csv_vip = ""
        self._a2_vip = ""
        self._e2_vip = ""
        self._pmal_vip = ""
        self._ha_multicast_ip1 = ""
        self._ha_multicast_ip2 = ""
        self._ha_multicast_port1 = ""
        self._ha_multicast_port2 = ""
        self._ha_cluster_password = ""
        self._emc_mode = common.C_EMC_MODE_NFS   #  'nfs' or 'diskarray'
        # for diskarray
        self._fs_ipwvol_size = 0
        self._fs_mgmvol_size = 0
        self._fs_sqlvol_size = 0
        self._fs_csvvol_size = 0
        self._local_disk = "/dev/sda"
        self._ha_disk_01 = ""
        self._ha_disk_02 = ""
        self._ha_disk_03 = ""
        self._ha_disk_04 = ""
        self._md0_size_G = 298
        self._sbd_size_M = 10
        # for nfs
        self._nfs_ip = ''
        # for updates
        self._need_update = False
        self._update_path = ""
        self._update_rpms = []
        self._update_cmds = []
        # for provision vip
        self._provision_vip = ""


    def setCommon(self, json_node) :
        if common.getOptionValue(json_node, "emc_mode") :
            self._emc_mode = json_node["emc_mode"].strip().lower()
            if cmp(common.C_EMC_MODE_NFS, self._emc_mode) and cmp(common.C_EMC_MODE_DISKARRAY, self._emc_mode) :
                raise Exception("Unknown EMC Mode: " + self._emc_mode)
        # common
        self._ss_vip = json_node["ipwss_vip"]
        common.checkIPFormat(self._ss_vip, True)

        if "ipwprov_vip" in json_node:
            self._provision_vip = json_node["ipwprov_vip"].strip()
            common.checkIPFormat(self._provision_vip,True)
        
        if common.g_isInstall_AAA :
            self._mgm_vip = json_node["dbcluster_vip"]
            common.checkIPFormat(self._mgm_vip,True)
            self._sql_vip = json_node["ipwsql_vip"]
            common.checkIPFormat(self._sql_vip,True)
            self._csv_vip = json_node["csvengine_vip"]
            common.checkIPFormat(self._csv_vip,True)
        if common.g_isInstall_CLF :
            self._a2_vip = json_node["clf_cmi_nacf_pmi_racfe4_umi_vip"]
            common.checkIPFormat(self._a2_vip,True)
            self._e2_vip = json_node["ipw_clf_sbccops_sbce2_vip"]
            common.checkIPFormat(self._e2_vip,True)
            self._pmal_vip = json_node["ipw_pmal_cmipmi_soap_vip"]
            common.checkIPFormat(self._pmal_vip,True)
        self._ha_multicast_ip1 = json_node["ha_multicast_ip1"]
        common.checkIPFormat(self._ha_multicast_ip1)
        self._ha_multicast_ip2 = json_node["ha_multicast_ip2"]
        common.checkIPFormat(self._ha_multicast_ip2)
        self._ha_multicast_port1 = int(json_node["ha_multicast_port1"])
        self._ha_multicast_port2 = int(json_node["ha_multicast_port2"])
        self._ha_cluster_password = json_node["ha_cluster_password"]
        # only for diskarray
        if not cmp(common.C_EMC_MODE_DISKARRAY, self._emc_mode) :
            self._fs_ipwvol_size = int(json_node['fs_ipwvol_size'])
            if common.g_isInstall_AAA :
                self._fs_mgmvol_size = int(json_node['fs_mgmvol_size'])
                self._fs_sqlvol_size = int(json_node['fs_sqlvol_size'])
                self._fs_csvvol_size = int(json_node['fs_csvvol_size'])
            self._ha_disk_01 = json_node["emc_disk_01"]
            self._ha_disk_02 = json_node["emc_disk_02"]
            if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
                self._ha_disk_03 = json_node["emc_disk_03"]
                self._ha_disk_04 = json_node["emc_disk_04"]
            self._md0_size_G = int(json_node["md0_size_G"])
            self._sbd_size_M = int(json_node["sbd_size_M"])
        else :
            self._nfs_ip = json_node["emc_nfs_ip"]
            common.checkIPFormat(self._nfs_ip)
        # for ha update
        if common.getOptionValue(json_node, "ha_update") :
            if len(json_node["ha_update"]) > 0 :
                self._update_path = json_node["ha_update"]["path"]
                if self._update_path :
                    if cmp('/', self._update_path[-1]) :
                        self._update_path += '/'
                    self._need_update = True
                    for x in json_node["ha_update"]["rpms"] :
                        self._update_rpms.append(x)
                    for x in json_node["ha_update"]["cmds"] :
                        if re.search("\$\{rpms\}", x) :
                            rpms = " ".join(self._update_rpms)
                            x = x.replace("${rpms}", rpms)
                        log._file.debug("ha update cmd: " + x)
                        self._update_cmds.append(x)
                    


    def validateCfg(self) :
        is_ok = True
        # common validate
        if not self._ss_vip :
            log._file.error("ss_vip can't be empty in Medium Mode")
            is_ok = False
        if not self._ha_multicast_ip1 or not self._ha_multicast_ip2 or not self._ha_multicast_port1 or not self._ha_multicast_port2:
            log._file.error("ha_multicast_ip, ha_multicast_port can't be empty in Medium Mode")
            is_ok = False
        if common.g_isInstall_AAA :
            if not self._mgm_vip or not self._sql_vip or not self._csv_vip :
                log._file.error("mgm_vip, sql_vip, csv_vip can't be empty in Medium AAA")
                is_ok = False
        if common.g_isInstall_CLF :
            if not self._a2_vip or not self._e2_vip or not self._pmal_vip :
                log._file.error("clf_cmi_nacf_pmi_racfe4_umi_vip, ipw_clf_sbccops_sbce2_vip, ipw_pmal_cmipmi_soap_vip can't be empty in Medium CLF")
                is_ok = False
        # diskarray validate
        if not cmp(common.C_EMC_MODE_DISKARRAY, self._emc_mode) :
            if self._fs_ipwvol_size <= 0 :
                log._file.error("fs_ipwvol_size can't be 0 in Medium Mode")
                is_ok = False
            if common.g_isInstall_AAA :
                if not self._fs_mgmvol_size or not self._fs_sqlvol_size or not self._fs_csvvol_size :
                    log._file.error("fs_ipwvol_size, fs_mgmvol_size, fs_sqlvol_size, fs_csvvol_size can't be 0 in Medium AAA")
                    is_ok = False
            if not self._ha_disk_01 :
                log._file.error("emc_disk_01 can't be empty in Medium Mode")
                is_ok = False
            if not self._ha_disk_03 and not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
                log._file.error("emc_disk_03 can't be empty in Medium2 Mode")
                is_ok = False
            if (self._md0_size_G <= 0) or (self._sbd_size_M <= 0):
                log._file.error("md0_size_G, sbd_size_M can't be 0 in Medium Mode")
                is_ok = False
        else :
            if not self._nfs_ip :
                log._file.error("nfs server ip can't be empty when EMC is NFS Mode")
                is_ok = False
        return is_ok



    def getSsVip(self) :
        return self._ss_vip

    def getMgmVip(self) :
        return self._mgm_vip

    def getSqlVip(self) :
        return self._sql_vip

    def getCsvVip(self) :
        return self._csv_vip
    
    def getA2Vip(self) :
        return self._a2_vip
        
    def getE2Vip(self) :
        return self._e2_vip
        
    def getPmalVip(self) :
        return self._pmal_vip    
        
    def getFsIpwvolSize(self) :
        return self._fs_ipwvol_size

    def getFsMgmvolSize(self) :
        return self._fs_mgmvol_size

    def getFsSqlvolSize(self) :
        return self._fs_sqlvol_size

    def getFsCsvvolSize(self) :
        return self._fs_csvvol_size

    def getHaMulticastIp1(self) :
        return self._ha_multicast_ip1

    def getHaMulticastIp2(self) :
        return self._ha_multicast_ip2

    def getHaMulticastPort1(self) :
        return self._ha_multicast_port1

    def getHaMulticastPort2(self) :
        return self._ha_multicast_port2

    def getHaClusterPassword(self) :
        return self._ha_cluster_password

    def getHaDisk01(self) :
        return self._ha_disk_01

    def getHaDisk02(self) :
        return self._ha_disk_02

    def getHaDisk03(self) :
        return self._ha_disk_03

    def getHaDisk04(self) :
        return self._ha_disk_04

    def getMd0Size(self) :
        return self._md0_size_G

    def getSbdSize(self) :
        return self._sbd_size_M

    def getNfsIp(self) :
        return self._nfs_ip

    def getEmcMode(self) :
        return self._emc_mode

    def getNeedUpdate(self) :
        return self._need_update

    def getUpdatePath(self) :
        return self._update_path

    def getUpdateRpms(self) :
        return self._update_rpms

    def getUpdateCmds(self) :
        return self._update_cmds
    
    def getProvisionVip(self) :
        return self._provision_vip




