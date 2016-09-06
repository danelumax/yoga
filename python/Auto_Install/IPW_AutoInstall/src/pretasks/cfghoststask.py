import log, common
from cfg import cfgInstance



class CfgHostsTask(object) :
    """
    Config Hosts File
    """

    def __init__(self) :
        self._hosts_file = "src/template/hosts.tmp"
        self._cfg_list = []

    def precheck(self) :
        pass


    def execute(self) :
        log._file.debug(">> Config Hosts file Begin")
        content = common.open_file(self._hosts_file)
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            self._createSingleHosts(content)
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            self._createEntry1Hosts(content)
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            self._createEntry2Hosts(content)
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            self._createMedium1Hosts(content)
        elif not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._createMedium2Hosts(content)
        log._file.debug(">> Config Hosts file End")
        

    def verify(self) :
        pass

    def updateProgress(self) :
        pass


    def _createSingleHosts(self, content) :
        log._file.debug(">>> Config Hosts file in Single Mode")
        ps1 = cfgInstance().getPsCfg(0)
        self._cfg_list.append(ps1)
        oam_ip = self._getOamIp()
        traf_ip = self._getTrafficIp()
        hosts = "%s\n%s\n%s" %(content, oam_ip, traf_ip)
        log._file.debug("hosts content: \n" + hosts)
        common.create_file(ps1, hosts, '/etc/', 'hosts')
        log._file.debug("<<<")


    def _createEntry1Hosts(self, content) :
        log._file.debug(">>> Config Hosts file in Entry1 Mode")
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._cfg_list.append(ss1)
        self._cfg_list.append(ps1)
        self._cfg_list.append(ps2)
        oam_ip = self._getOamIp()
        traf_ip = self._getTrafficIp("ps")
        inte_ip = self._getInternalIp()
        prov_ip = self._getProvisionIp()
        #vip = self._getEntryVip(ss1)
        vip = ''
        ss_hosts = "%s\n%s\n%s\n%s" %(content, oam_ip, inte_ip, prov_ip)
        log._file.debug("SS hosts content: \n" + ss_hosts)
        ps_hosts = "%s\n%s\n%s\n%s\n%s" %(content, oam_ip, traf_ip, inte_ip, vip)
        log._file.debug("PS hosts content: \n" + ps_hosts)
        common.create_file(ss1, ss_hosts, '/etc/', 'hosts')
        common.create_file(ps1, ps_hosts, '/etc/', 'hosts')
        common.create_file(ps2, ps_hosts, '/etc/', 'hosts')
        log._file.debug("<<<")


    def _createEntry2Hosts(self, content) :
        log._file.debug(">>> Config Hosts file in Entry2 Mode")
        ss1 = cfgInstance().getSsCfg(0)
        ps1 = cfgInstance().getPsCfg(0)
        self._cfg_list.append(ss1)
        self._cfg_list.append(ps1)
        oam_ip = self._getOamIp()
        traf_ip = self._getTrafficIp()
        inte_ip = self._getInternalIp()
        prov_ip = self._getProvisionIp()
        
        ss_hosts = "%s\n%s\n%s\n%s" %(content, oam_ip, inte_ip, prov_ip)
        log._file.debug("SS hosts content: \n" + ss_hosts)
        ps_hosts = "%s\n%s\n%s\n%s" %(content, oam_ip, traf_ip, inte_ip)
        log._file.debug("PS hosts content: \n" + ps_hosts)
        common.create_file(ss1, ss_hosts, '/etc/', 'hosts')
        common.create_file(ps1, ps_hosts, '/etc/', 'hosts')
        log._file.debug("<<<")


    def _createMedium1Hosts(self, content) :
        log._file.debug(">>> Config Hosts file in Medium1 Mode")
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._cfg_list.append(ss1)
        self._cfg_list.append(ss2)
        self._cfg_list.append(ps1)
        self._cfg_list.append(ps2)
        ht_ip1 = self._getHeartbeatIp1("ss")
        ht_ip2 = self._getHeartbeatIp2("ss")
        oam_ip = self._getOamIp()
        traf_ip = self._getTrafficIp("ps")
        inte_ip = self._getInternalIp()
        prov_ip = self._getProvisionIp()
        vip_ip = self._getVip()
        ss_hosts = "%s\n%s\n%s\n%s\n%s\n%s\n%s" %(content, ht_ip1,ht_ip2, oam_ip, inte_ip, prov_ip, vip_ip)
        log._file.debug("SS hosts content: \n" + ss_hosts)
        ps_hosts = "%s\n%s\n%s\n%s\n%s" %(content, oam_ip, traf_ip, inte_ip, vip_ip)
        log._file.debug("PS hosts content: \n" + ps_hosts)
        common.create_file(ss1, ss_hosts, '/etc/', 'hosts')
        common.create_file(ss2, ss_hosts, '/etc/', 'hosts')
        common.create_file(ps1, ps_hosts, '/etc/', 'hosts')
        common.create_file(ps2, ps_hosts, '/etc/', 'hosts')
        log._file.debug("<<<")


    def _createMedium2Hosts(self, content) :
        log._file.debug(">>> Config Hosts file in Medium2 Mode")
        ss1 = cfgInstance().getSsCfg(0)
        ss2 = cfgInstance().getSsCfg(1)
        ps1 = cfgInstance().getPsCfg(0)
        ps2 = cfgInstance().getPsCfg(1)
        self._cfg_list.append(ss1)
        self._cfg_list.append(ss2)
        self._cfg_list.append(ps1)
        self._cfg_list.append(ps2)
        ss_ht_ip1 = self._getHeartbeatIp1("ss")
        ps_ht_ip1 = self._getHeartbeatIp1("ps")
        ss_ht_ip2 = self._getHeartbeatIp2("ss")
        ps_ht_ip2 = self._getHeartbeatIp2("ps")
        oam_ip = self._getOamIp()
        traf_ip = self._getTrafficIp("ps")
        inte_ip = self._getInternalIp()
        prov_ip = self._getProvisionIp()
        vip_ip = self._getVip()
        ss_hosts = "%s\n%s\n%s\n%s\n%s\n%s\n%s" %(content, ss_ht_ip1,ss_ht_ip2, oam_ip, inte_ip, prov_ip, vip_ip)
        log._file.debug("SS hosts content: \n" + ss_hosts)
        ps_hosts = "%s\n%s\n%s\n%s\n%s\n%s\n%s" %(content, ps_ht_ip1,ps_ht_ip2, oam_ip, traf_ip, inte_ip, vip_ip)
        log._file.debug("PS hosts content: \n" + ps_hosts)
        common.create_file(ss1, ss_hosts, '/etc/', 'hosts')
        common.create_file(ss2, ss_hosts, '/etc/', 'hosts')
        common.create_file(ps1, ps_hosts, '/etc/', 'hosts')
        common.create_file(ps2, ps_hosts, '/etc/', 'hosts')
        log._file.debug("<<<")


    def _getOamIp(self) :
        tmp = ''
        for cfg in self._cfg_list :
            tmp += "%-16s      %s #OAM newtowrk IP\n" %(cfg.getOamIp(), cfg.getHostName())
        log._file.debug("OAM IP: \n" + tmp)
        return tmp


    def _getTrafficIp(self, node_type='') :
        tmp = ""
        if not cmp('ps', node_type) :
            for cfg in cfgInstance().getPsCfgList() :
                if cfg.getTrafficIp() :
                    tmp += "%-16s      %s\n" %(cfg.getTrafficIp(), cfg.getHostName())
                if cfg.getTrafficIpv6() :
                    tmp += "%s        %s\n" %(cfg.getTrafficIpv6(), cfg.getHostName())
        else :
            for cfg in self._cfg_list :
                #log._file.debug("%s: %s, %s" %(cfg.getHostName(),cfg.getTrafficIp(),cfg.getTrafficIpv6()))
                if cfg.getTrafficIp() :
                    tmp += "%-16s      %s\n" %(cfg.getTrafficIp(), cfg.getHostName())
                if cfg.getTrafficIpv6() :
                    tmp += "%s        %s\n" %(cfg.getTrafficIpv6(), cfg.getHostName())
        log._file.debug("Traffic IP: \n" + tmp)
        return tmp


    def _getInternalIp(self) :
        tmp = ''
        for cfg in self._cfg_list :
            if cmp(cfg.getInternalIp(), cfg.getOamIp()) :
                tmp += "%-16s      %s\n" %(cfg.getInternalIp(), cfg.getHostName())
        log._file.debug("Internal IP: \n" + tmp)
        return tmp


    def _getHeartbeatIp1(self, node_type) :
        tmp = ""
        if not cmp('ss', node_type) :
            for cfg in cfgInstance().getSsCfgList() :
                tmp += "%-16s      %s #heartbeat IP\n" %(cfg.getHeartbeatIp1(), cfg.getHostName())
        else :
            for cfg in cfgInstance().getPsCfgList() :
                tmp += "%-16s      %s #heartbeat IP\n" %(cfg.getHeartbeatIp1(), cfg.getHostName())
        log._file.debug("Heartbeat IP: \n" + tmp)
        return tmp

    def _getHeartbeatIp2(self, node_type) :
        tmp = ""
        if not cmp('ss', node_type) :
            for cfg in cfgInstance().getSsCfgList() :
                tmp += "%-16s      %s #heartbeat IP 2\n" %(cfg.getHeartbeatIp2(), cfg.getHostName())
        else :
            for cfg in cfgInstance().getPsCfgList() :
                tmp += "%-16s      %s #heartbeat IP 2\n" %(cfg.getHeartbeatIp2(), cfg.getHostName())
        log._file.debug("Heartbeat IP: \n" + tmp)
        return tmp

    def _getVip(self) :
        tmp = "%-16s      ipwss_vip #ipworks SS virtual IP\n" %cfgInstance()._ha_cfg.getSsVip()
        
        prov_vip = cfgInstance()._ha_cfg.getProvisionVip()
        if  prov_vip:
            tmp += "%-16s      ipwprov_vip #ipworks provision virtual IP\n" %prov_vip

        if common.g_isInstall_AAA :
            tmp += "%-16s      dbcluster_vip \n" %cfgInstance()._ha_cfg.getMgmVip()
            tmp += "%-16s      ipwsql_vip\n" %cfgInstance()._ha_cfg.getSqlVip()
            tmp += "%-16s      csvengine_vip\n" %cfgInstance()._ha_cfg.getCsvVip()
        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) and common.g_isInstall_CLF :
            tmp += "%-16s      clf_cmi_nacf_pmi_racfe4_umi_vip\n" %cfgInstance()._ha_cfg.getA2Vip()
            tmp += "%-16s      ipw_clf_sbccops_sbce2_vip\n" %cfgInstance()._ha_cfg.getE2Vip()
            tmp += "%-16s      ipw_pmal_cmipmi_soap_vip\n" %cfgInstance()._ha_cfg.getPmalVip()
        
        nfs_ip = cfgInstance()._ha_cfg.getNfsIp()
        if nfs_ip : tmp += "%-16s      emc_nfs_ip #EMC NFS server IP\n" %nfs_ip
        
        log._file.debug("VIP: \n" + tmp)
        return tmp
    
    
    def _getEntryVip(self, cfg) :
        tmp = ""
        if common.g_isInstall_AAA :
            tmp = "%-16s      dbcluster_vip\n" %cfg.getInternalIp()
        log._file.debug("VIP: \n" + tmp)
        return tmp

    def _getProvisionIp(self) :
        tmp = ""
        for cfg in cfgInstance().getSsCfgList() :
            if cfg.getProvisionIp() : 
                tmp += "%-16s      %s-prov #Provision network IP\n" %(cfg.getProvisionIp(), cfg.getHostName())
        log._file.debug("Provision IP: \n" + tmp)
        return tmp


    
    
