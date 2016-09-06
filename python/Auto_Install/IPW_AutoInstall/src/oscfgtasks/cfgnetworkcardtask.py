import re
import log, common
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil


class CfgNetworkCardTask(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._ifcfg_file = "src/template/ifcfg.tmp"
        self._bond_file = "src/template/bond.tmp"
        self._bond_index = 0
        
        
    def precheck(self):
        pass
    
    
    def execute(self):
        log._all.debug(">>> Config Network Card Begin")
        self._cfg = cfgInstance()
        for ss_cfg in cfgInstance().getSsCfgList() :
            self._bond_index = 0
            is_restart = False
            mapping = cfgInstance()._ss_mapping
            # OAM IP
            if mapping._oam_mapping :
                is_restart = True
                self._configOam(ss_cfg, mapping._oam_mapping)
            # Heartbeat IP
            if mapping._heartbeat_mapping :
                if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
                   or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                    is_restart = True
                    self._configHeartbeat(ss_cfg, mapping._heartbeat_mapping)
            # Traffic IP
            if mapping._traffic_mapping :
                if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) \
                   or not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
                    is_restart = True
                    self._configTraffic(ss_cfg, mapping._traffic_mapping)
            # Internal IP
            if mapping._internal_mapping :
                is_restart = True
                self._configInternal(ss_cfg, mapping._internal_mapping)
            # Bond config
            if self._bond_index > 0 :
                self._configBindfile(ss_cfg)
            # service network restart
            #if is_restart :
            #    self._restartNetwork(ss_cfg)
                
                
        #for ps_cfg in cfgInstance().getPsCfgList() :
        #    self._bond_index = 0
        #    is_restart = False
        #    mapping = cfgInstance()._ps_mapping
            # OAM IP
        #    if mapping._oam_mapping :
        #        is_restart = True
        #        self._configOam(ps_cfg, mapping._oam_mapping)
            # Traffic IP
        #    if mapping._traffic_mapping :
        #        is_restart = True
        #        self._configTraffic(ps_cfg, mapping._traffic_mapping)
            # Heartbeat IP
        #    if mapping._heartbeat_mapping :
        #        if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
        #            is_restart = True
        #            self._configHeartbeat(ps_cfg, mapping._heartbeat_mapping)
            # Internal IP
        #    if mapping._internal_mapping :
        #        is_restart = True
        #        self._configInternal(ps_cfg, mapping._internal_mapping) 
            # Bond Config
        #    if self._bond_index > 0 :
        #        self._configBindfile(ps_cfg)
            # service network restart
        #    if is_restart :
        #        self._restartNetwork(ps_cfg)
            
        log._all.debug("<<< Config Network Card End")
    

    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def _configOam(self, cfg, mapping) :
        log._all.debug("Config OAM IP on " + cfg.getHostName())
        if len(mapping) > 1 :
            self._configBind(cfg, mapping, cfg.getOamIp(), cfg.getOamPrefix())
        else :
            self._configSinglePort(cfg, mapping, cfg.getOamIp(), cfg.getOamPrefix())

    
    
    
    def _configHeartbeat(self, cfg, mapping) :
        log._all.debug("Config Heartbeat IP on " + cfg.getHostName())
        if len(mapping) > 1 :
            self._configBind(cfg, mapping, cfg.getHeartbeatIp(), cfg.getHeartbeatPrefix())
        else :
            self._configSinglePort(cfg, mapping, cfg.getHeartbeatIp(), cfg.getHeartbeatPrefix())
        
        
        
    def _configTraffic(self, cfg, mapping) :
        log._all.debug("Config Traffic IP on " + cfg.getHostName())
        if len(mapping) > 1 :
            self._configBind(cfg, mapping, cfg.getTrafficIp(), cfg.getTrafficPrefix(), cfg.getTrafficIpv6(), cfg.getTrafficIpv6Prefix())
        else :
            self._configSinglePort(cfg, mapping, cfg.getTrafficIp(), cfg.getTrafficPrefix(), cfg.getTrafficIpv6(), cfg.getTrafficIpv6Prefix())
    
    
    
    def _configInternal(self, cfg, mapping) :
        log._all.debug("Config Internal IP on " + cfg.getHostName())
        if len(mapping) > 1 :
            self._configBind(cfg, mapping, cfg.getInternalIp(), cfg.getInternalPrefix())
        else :
            self._configSinglePort(cfg, mapping, cfg.getInternalIp(), cfg.getInternalPrefix())

    


    def _configSinglePort(self, cfg, mapping, ip, prefix, ipv6="", ipv6_prefix="") :
        log._all.debug("Config Single Port IP")
        device = mapping[0]
        content = common.open_file(self._ifcfg_file)
        tmp = "%s/%d" %(ip, prefix)
        content = content.replace("<IP Address>", tmp)
        if ipv6 :
            content += "IPADDR_1=\'%s/%d\'\n" %(ipv6, ipv6_prefix)
        #log._all.debug("content:\n" + content)
        filename = "ifcfg-%s" %device
        #common.create_file(cfg, content, '/etc/sysconfig/network/', filename)
        common.create_file(cfg, content, '/', filename)
        
    
    
    def _configBind(self, cfg, mapping, ip, prefix, ipv6="", ipv6_prefix="") :
        log._all.debug("Config Bind IP")
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("rm -f /etc/sysconfig/network/ifcfg-" + str(mapping[0]), throw=False)
        ssh_util.remote_exec("rm -f /etc/sysconfig/network/ifcfg-" + str(mapping[1]), throw=False)
        device = 'bond' + str(self._bond_index)
        self._bond_index += 1
        content = common.open_file(self._bond_file)
        content = content.replace("<Device Name>", device)
        content = content.replace("<Slave0>", mapping[0])
        content = content.replace("<Slave1>", mapping[1])
        tmp = "%s/%d" %(ip, prefix)
        content = content.replace("<IP Address>", tmp)
        if ipv6 :
            content += "IPADDR_1=\'%s/%d\'\n" %(ipv6, ipv6_prefix)
        #log._all.debug("content:\n" + content)
        filename = "ifcfg-%s" %device
        #common.create_file(cfg, content, '/etc/sysconfig/network/', filename)
        common.create_file(cfg, content, '/', filename)
        
        
        

    def _configBindfile(self, cfg) :
        content = ''
        if self._bond_index > 1 :
            log._all.debug("has more than one bond")
            for x in range(self._bond_index) :
                content += "alias bond" + str(x) + " bonding\n"
            content += "options bonding max_bonds=" + str(self._bond_index) + " mode=active-backup miimon=100 use_carrier=0"
        else :
            log._all.debug("has only one bond")    
            content = "alias bond0 bonding\noptions bond0 mode=active-backup miimon=100 use_carrier=0"
        #log._all.debug("content:\n" + content)
        #common.create_file(cfg, content, '/etc/', 'modprobe.conf.local')
        common.create_file(cfg, content, '/', 'modprobe.conf.local')

        

    def _restartNetwork(self, cfg) :
        log._all.debug("restart network on " + cfg.getHostName())
        ssh = sshManagerInstance().getSsh(cfg.getHostName())
        ssh_util = SshUtil(ssh)
        ssh_util.remote_exec("service network restart")







