import os, re
import log, common
import nodecfg
import hacfg
import getpass

def cfgInstance() :
    try :
        inst = Cfg()
    except Cfg as cfg:
        inst = cfg
    return inst


class Cfg :
    '''
    class Cfg
    '''

    __instance = None


    def __init__(self) :
        if Cfg.__instance :
            raise Cfg.__instance
        Cfg.__instance = self
            
        self._ss_cfg_list = []
        self._ps_cfg_list = []
        self._client_cfg_list = []
        self._ha_cfg = None
        self._clf_cfg = None
        
        self._data_mem = 0
        self._index_mem = 0
        
        self._ipw_iso = ""
        self._ipw_name = ""
        self._os_iso = ""
        self._os_name = ""
        self._mount_point = ""
        self._upgrade_path = ""
        
        self._ss_mapping = None
        self._ps_mapping = None
        self._default_gw = ""
        self._ntp_server = ""
        self._cli_username = ""
        self._cli_password = ""
        self._upgrade_patch_cmds = []
        self._upgrade_patch_rpms = []

        

    def parse(self, network_cfg_file):
        log._file.debug(">> enter parse cfg file: " + network_cfg_file)
        json_root = common.parse_file(network_cfg_file)
        # config common
        self._setCommon(json_root)
        # config ha optional
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self._ha_cfg = hacfg.HaCfg()
            self._ha_cfg.setCommon(json_root["ha"])
        # config node
        self._network = json_root["network"]
        self._setNodes()
        # config ndb optional
        self.getCliInfo()
        log._file.debug("<< outer parse cfg file")


    def _setCommon(self, json_root) :
        # mandatory
        self.isValideType(json_root["type"].upper().strip())
        self.isValideApp(json_root["mode"].upper().strip())
        self.isValideService(json_root["service"].upper().strip())
        self.commercialCheck()
        self.checkmodeAndservice()
        self.setIpwIsoPath(json_root["ipw_iso_path"].strip())
        self.checkfile(self._ipw_iso)
        self.setMountPoint(json_root["mount_point"].strip())
        self.setUpgradePath(json_root["upgrade_path"].strip())

        if((json_root["chroot"].lower().strip()) == "yes"):
            common.g_isChangeRoot = True
        if((json_root["ndb_sync_simple_check"].lower().strip()) == "yes"):
            common.g_ndbSyncSimpleCheck = True
        common.g_section_wait_time = int(json_root["section_wait_time"].strip())
        if(common.g_section_wait_time <=0 ):
            raise Exception("Section wait time must be larger than 0")
        if((json_root["need_shorting_failover_time"].lower().strip()) == "yes"):
            common.g_need_shorting_failover_time = True

        # optional
        if common.getOptionValue(json_root["network"], "username") :
            common.g_username = json_root["network"]["username"]
        if common.getOptionValue(json_root["network"], "password") :
            common.g_password = json_root["network"]["password"]
        if common.getOptionValue(json_root["network"], "ssh_port") :
            common.g_sshport = json_root["network"]["ssh_port"]
        if common.getOptionValue(json_root["network"], "default_gateway") :
            self._default_gw = json_root["network"]["default_gateway"]
        if common.getOptionValue(json_root["network"], "ntp_server") :
            self._ntp_server = json_root["network"]["ntp_server"]
        if common.getOptionValue(json_root["network"], "mapping") :
            if common.getOptionValue(json_root["network"]["mapping"], "ss") :
                self._ss_mapping = self._setMapping(json_root["network"]["mapping"]["ss"])
            if common.getOptionValue(json_root["network"]["mapping"], "ps") :
                self._ps_mapping = self._setMapping(json_root["network"]["mapping"]["ps"])

        '''set update patch commands'''
        self.setUpdatePatchCommands(json_root)
        for item in self._upgrade_patch_rpms:
            self.checkfile(item)
        
        
    def _setMapping(self, node) :
        mapping = MappingCfg()
        if common.getOptionValue(node, "oam_mapping") :
            mapping._oam_mapping = node["oam_mapping"]
        if common.getOptionValue(node, "traffic_mapping") :
            mapping._traffic_mapping = node["traffic_mapping"]
        if common.getOptionValue(node, "heartbeat_mapping") :
            mapping._heartbeat_mapping = node["heartbeat_mapping"]
        if common.getOptionValue(node, "internal_mapping") :
            mapping._internal_mapping = node["internal_mapping"]
        return mapping


    def _setNodes(self) :
        if common.getOptionValue(self._network["ss"], "nodes") :
            if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
              or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                  if len(self._network["ss"]["nodes"]) < 2 :
                      raise Exception("SS Should have 2 nodes")
            for node in self._network["ss"]["nodes"] :
                ss = nodecfg.SsCfg()
                ss.setCommon(node)
                if not ss.validateCfg() :
                    raise Exception("SS node Parameters are incorrect")
                self._ss_cfg_list.append(ss)

        else:
            if cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
                raise Exception("SS nodes can't be empty")
        if common.getOptionValue(self._network["ps"], "nodes") :
            if not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) \
              or not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
              or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                  if len(self._network["ps"]["nodes"]) < 2 :
                      raise Exception("PS Should have 2 nodes")
            for node in self._network["ps"]["nodes"] :
                ps = nodecfg.PsCfg()
                ps.setCommon(node)
                if not ps.validateCfg() :
                    raise Exception("PS node Parameters are incorrect")
                self._ps_cfg_list.append(ps)

        else:
            raise Exception("PS nodes can't be empty")

    def setCliUserName(self,username):
        self._cli_username = username

    def setCliPassword(self,password):
        self._cli_password = password

    def setUpdatePatchCommands(self,json_node):
        if(common.getOptionValue(json_node, "sles_patch_update")):
            if len(json_node["sles_patch_update"]) > 0 :
                patchpath = self._update_path = json_node["sles_patch_update"]["path"]
                if(len(patchpath) > 0):
                    if cmp('/', patchpath[-1]) :
                        patchpath += '/'
                else:
                    return None

            for x in json_node["sles_patch_update"]["update_rpms"] :
                if len(x.strip()) <= 0: continue 
                
                self._upgrade_patch_rpms.append(patchpath+x)
                if (re.search('kernel-', x)):
                    self._upgrade_patch_cmds.append("rpm -i " +x)
                else:
                    self._upgrade_patch_cmds.append("rpm -U " +x)

    def getDefaultGw(self) :
        return self._default_gw


    def getNtpServer(self) :
        return self._ntp_server

    
    def getSsCfg(self, index):
        if index < len(self._ss_cfg_list):
            return self._ss_cfg_list[index]
        else:
            return None


    def getSsCfgList(self) :
        return self._ss_cfg_list
    
    
    def getPsCfg(self, index):
        if index < len(self._ps_cfg_list):
            return self._ps_cfg_list[index]
        else:
            return None


    def getPsCfgList(self) :
        return self._ps_cfg_list


    def getHaCfg(self) :
        return self._ha_cfg

    def getClfCfg(self) :
        return self._clf_cfg

    def getClientCfgList(self):
        return self._client_cfg_list


    def isValideApp(self, mode):
        if not cmp(common.C_IPW_APP_AAA, mode) :
            log._file.debug("Upgrade Mode: AAA")
        elif not cmp(common.C_IPW_APP_DNS, mode) :
            log._file.debug("Upgrade Mode: DNS")
        elif not cmp(common.C_IPW_APP_ENUM, mode) :
            log._file.debug("Upgrade Mode: ENUM")
        elif not cmp(common.C_IPW_APP_DHCP, mode) :
            log._file.debug("Upgrade Mode: DHCP")
        elif not cmp(common.C_IPW_APP_CLF, mode) :
            log._file.debug("Upgrade Mode: CLF")
        else :
            raise Exception("Unknown Mode: " + Mode)
        common.g_upgrade_app = mode 

    def isValideService(self,service):
        serviceList = service.split(',')
        for item in serviceList:
            if not cmp(common.C_IPW_APP_AAA, item) :
                log._file.debug("Upgrade Service: AAA")
                common.g_isInstall_AAA = True
                self.addService(common.C_IPW_APP_AAA)
            elif not cmp(common.C_IPW_APP_DNS, item) :
                log._file.debug("Upgrade Service: DNS")
                common.g_isInstall_DNS = True
                self.addService(common.C_IPW_APP_DNS)
            elif not cmp(common.C_IPW_APP_ENUM, item) :
                log._file.debug("Upgrade Service: ENUM")
                common.g_isInstall_DNS = True
                common.g_isInstall_ENUM = True
                self.addService(common.C_IPW_APP_DNS)
                self.addService(common.C_IPW_APP_ENUM)
            elif not cmp(common.C_IPW_APP_DHCP, item) :
                log._file.debug("Upgrade Service: DHCP")
                self.addService(common.C_IPW_APP_DHCP)
            elif not cmp(common.C_IPW_APP_CLF, item) :
                log._file.debug("Upgrade Service: CLF")
                common.g_isInstall_CLF = True
                common.g_isInstall_DHCP = True
                self.addService(common.C_IPW_APP_DHCP)
                self.addService(common.C_IPW_APP_CLF)
            else :
                raise Exception("Unknown Service: " + item)

    def addService(self,service):
            if(service not in common.g_upgrade_service): 
                common.g_upgrade_service.append(service)
        

    def isValideType(self, ipw_type):
        if not cmp(common.C_IPW_MODE_SINGLE, ipw_type) \
          or not cmp(common.C_IPW_MODE_ENTRY1, ipw_type) \
          or not cmp(common.C_IPW_MODE_ENTRY2, ipw_type) \
          or not cmp(common.C_IPW_MODE_MEDIUM1, ipw_type) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, ipw_type) :
            log._file.debug("IPWorks Type: %s" %ipw_type)
            common.g_ipw_mode = ipw_type
        else:
            raise Exception("Unknown Type: " + ipw_type)


    def commercialCheck(self):
        applist = common.g_mode_app_dict[common.g_ipw_mode]
        for item in applist:
            if not cmp(item,common.g_upgrade_app):
                return 
        
        raise Exception("Do not support app : " + common.g_upgrade_app + " in type : "+common.g_ipw_mode)

    def checkmodeAndservice(self):
        serviceList = common.g_app_service_dict[common.g_upgrade_app]
        for item in common.g_upgrade_service:
            if item not in serviceList:
                raise Exception("Do not support service : " + item + " in upgrade mode : "+common.g_upgrade_app)
        

    def getIpwIsoPath(self) :
        return self._ipw_iso

    def setIpwIsoPath(self, iso_path) :
        self._ipw_iso = iso_path
        tmp = iso_path.split('/')
        self.setIpwIsoName(tmp[-1])

    def getIpwIsoName(self) :
        return self._ipw_name

    def setIpwIsoName(self, iso_name) :
        self._ipw_name = iso_name

    def setHaeIsoPath(self, hae_iso_path) :
        self._hae_iso = hae_iso_path
        tmp = hae_iso_path.split('/')
        self.setHaeIsoName(tmp[-1])

    def getHaeIsoName(self) :
        return self._hae_name

    def setHaeIsoName(self, hae_iso_name) :
        self._hae_name = hae_iso_name



    def getOsIsoPath(self) :
        return self._os_iso

    def setOsIsoPath(self, os_path) :
        self._os_iso = os_path
        tmp = os_path.split('/')
        self.setOsIsoName(tmp[-1])

    def getOsIsoName(self) :
        return self._os_name

    def setOsIsoName(self, os_name) :
        self._os_name = os_name

    def getMountPoint(self) :
        return self._mount_point

    def setMountPoint(self, mount_point) :
        if mount_point[-1] == '/':
            mount_point = mount_point[0:-1]
        self._mount_point = mount_point


    def checkfile(self, filepath):
        if not os.path.exists(filepath) :
            raise Exception("%s Doesn't Exist !!!" %(filepath))

    def getUpgradePath(self) :
        return self._upgrade_path

    def setUpgradePath(self, upgrade_path) :
        if upgrade_path[-1] != '/':
            upgrade_path += '/' 
        self._upgrade_path = upgrade_path

    def getCfgFromKey(self,key):
        key = key[common.C_TASK_PREFIX_LENGTH:]
        if(key == "PS&SS"):
            if(common.g_ipw_mode == common.C_IPW_MODE_SINGLE):
                return self.getPsCfg(0)
            else:
                return self.getSsCfg(0)
        elif(key == "SS"):
            return self.getSsCfg(0)
        elif(key == "Active-SS") :
            #return self.getSsCfg(0)
             return self.getActiveSS()
        elif(key == "Standby-SS"):
             return self.getStandBySS()
            #return self.getSsCfg(1)
        elif(key == "PS1"):
            return self.getPsCfg(0)
        elif(key == "PS2"):
            return self.getPsCfg(1)

        return None


    def getActiveSS(self):
        log._file.debug(">>> getActiveSS")
        for ss in self.getSsCfgList():
            if(ss._isActiveSs):
                log._file.debug("Get Active SS : "+ss.getHostName())
                return ss

    def getStandBySS(self):
        log._file.debug(">>> getStandBySS")
        for ss in self.getSsCfgList():
            if not (ss._isActiveSs):
                log._file.debug("Get StandBy SS : "+ss.getHostName())
                return ss


    def getCliUserName(self):
        return self._cli_username

    def getCliPassword(self):
        return self._cli_password

    def print_red(self, s) :
        print "%s[31;5m%s%s[0m" %(chr(27), s, chr(27))

    def getCliInfo(self):
        context = common.getCliInfo()
        if(context):
            for x in context :
                tmp = x.split(';')
                self.setCliUserName(common.decrypt(tmp[0]))
                self.setCliPassword(common.decrypt(tmp[1].strip()))
        else:
            self.inputCliInfo()
        log._file.debug("<<<")

    def inputCliInfo(self):
        print 'Please Input CLI Information:'
        username = raw_input('  Enter CLI Username: ')
        self.setCliUserName(username)
        while 1 :
            p1 = getpass.getpass('  Enter CLI Password: ')
            p2 = getpass.getpass('  Enter CLI Password (Confirm): ')
            if cmp(p1, p2) :
                self.print_red("Password doesn't Match !!!")
                continue
            break
        self.setCliPassword(p1)
        common.saveCliInfo(common.encrypt(username),common.encrypt(p1)) 

    def getUpdateRPMS(self):
        return self._upgrade_patch_rpms

    def getUpdateCmds(self):
        return self._upgrade_patch_cmds
  

class MappingCfg :
    '''
    classdoc
    '''

    def __init__(self) :
        self._oam_mapping = []
        self._traffic_mapping = []
        self._heartbeat_mapping = []
        self._internal_mapping = []




