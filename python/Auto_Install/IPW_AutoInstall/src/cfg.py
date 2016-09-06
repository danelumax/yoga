import os
import re
import getpass
import log, common
import hacfg, nodecfg, clfcfg


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
        self._hae_iso = ""
        self._hae_name = ""
        self._os_iso = ""
        self._os_name = ""
        self._license_path = ""
        self._license_name = ""
        self._mount_point = ""
        self._install_path = ""
        
        self._ss_mapping = None
        self._ps_mapping = None
        self._default_gw = ""
        self._ntp_server = ""
        self._install_ss7 = False

        

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
            if not self._ha_cfg.validateCfg() :
                raise Exception("HA Parameters are incorrect")
            if not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
                self._clf_cfg = clfcfg.ClfCfg()
                self._clf_cfg.setCommon(json_root["clf"])
                if not self._clf_cfg.validateCfg() :
                    raise Exception("CLF Parameters are incorrect")
        # config node
        self._network = json_root["network"]
        self._setNodes()
        # config ndb optional
        if common.g_isInstall_AAA or common.g_isInstall_ENUM:
            self._data_mem = int(json_root['ndb']["data_memory_size"])
            self._index_mem = int(json_root['ndb']["index_memory_size"])
            if (self._data_mem <= 0) or (self._index_mem <= 0):
                raise Exception("data_memory_size, data_memory_size can't be 0")
        log._file.debug("<< outer parse cfg file")


    def _setCommon(self, json_root) :
        # mandatory
        self.isValideType(json_root["type"].lower().strip())
        self.isValideApp(json_root["app"].lower().strip())
        if common.getOptionValue(json_root, "commercial_check") :
            if 'no' == json_root["commercial_check"].strip().lower():
                self.commercialCheck(False)
            else:
                self.commercialCheck()
        else:
            self.commercialCheck()
        self.setIpwIsoPath(json_root["ipw_iso_path"].strip())
        self.checkfile(self._ipw_iso)
        self.setLicensePath(json_root["license_path"].strip())
        self.checkfile(self._license_path)
        self.setInstallPath(json_root["install_path"].strip())
        self.setMountPoint(json_root["mount_point"].strip())
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            self.setHaeIsoPath(json_root["hae_iso_path"])
            self.setOsIsoPath(json_root["os_iso_path"])
            self.checkfile(self._os_iso)
            self.checkfile(self._hae_iso)
        # optional
        if common.getOptionValue(json_root, "install_ss7") :
            self.setInstallSS7(json_root["install_ss7"])
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
        # user input the ipwcli password

        need_input = True
        if os.path.exists(common.g_shadow_file) :
            fc = common.getNodeInfo()
            for x in fc :
                if re.search("ipwcli", x) :
                    log._file.info("Find Node info: " + x)
                    tmp = x.split(';')
                    self.setCliPassword( tmp[2].strip(), common.decrypt(tmp[3].strip()))
                    need_input = False
                    break
        if need_input is True:
            self.setCliPassword()


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


    def isValideApp(self, app):
        tmp = app.split(',')
        for x in tmp :
            x = x.strip()
            if not cmp(common.C_IPW_APP_AAA, x) :
                log._file.debug("Install App: AAA")
                common.g_isInstall_AAA = True
            elif not cmp(common.C_IPW_APP_DNS, x) :
                log._file.debug("Install App: DNS")
                common.g_isInstall_DNS = True
            elif not cmp(common.C_IPW_APP_ENUM, x) :
                log._file.debug("Install App: ENUM")
                common.g_isInstall_DNS = True
                common.g_isInstall_ENUM = True
            elif not cmp(common.C_IPW_APP_DHCP, x) :
                log._file.debug("Install App: DHCP")
                common.g_isInstall_DHCP = True
            elif not cmp(common.C_IPW_APP_CLF, x) :
                log._file.debug("Install App: CLF")
                common.g_isInstall_DHCP = True
                common.g_isInstall_CLF = True
            else :
                raise Exception("Unknown App: " + x)


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


    def commercialCheck(self, tag=True):
        if not cmp(common.C_IPW_MODE_SINGLE, common.g_ipw_mode) :
            if tag :
                if common.g_isInstall_ENUM or common.g_isInstall_AAA or common.g_isInstall_DHCP :
                    raise Exception("IPWorks Only Support DNS on Single Mode")
            if common.g_isInstall_CLF :
                raise Exception("IPWorks Can't Support CLF on Single Mode")
        elif not cmp(common.C_IPW_MODE_ENTRY1, common.g_ipw_mode) :
            if tag :
                if common.g_isInstall_ENUM and common.g_isInstall_DHCP :
                    raise Exception("IPWorks Can't Support DHCP & ENUM co-location on Entry1 Mode")
            if common.g_isInstall_AAA and common.g_isInstall_ENUM :
                raise Exception("IPWorks Can't Support AAA & ENUM co-location on Entry1 Mode")
            if common.g_isInstall_CLF :
                raise Exception("IPWorks Can't Support CLF on Entry1 Mode")
        elif not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode) :
            if tag :
                if common.g_isInstall_ENUM and common.g_isInstall_DHCP :
                    raise Exception("IPWorks Can't Support DHCP & ENUM co-location on Entry2 Mode")
                elif common.g_isInstall_DNS and common.g_isInstall_DHCP :
                    raise Exception("IPWorks Can't Support DHCP & DNS co-location on Entry2 Mode")
            if common.g_isInstall_AAA :
                raise Exception("IPWorks Can't Support AAA on Entry2 Mode")
            if common.g_isInstall_CLF :
                raise Exception("IPWorks Can't Support CLF on Entry2 Mode")
        elif not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) :
            if tag :
                if common.g_isInstall_ENUM and common.g_isInstall_DHCP :
                    raise Exception("IPWorks Can't Support DHCP & ENUM co-location on Medium1 Mode")
            if common.g_isInstall_AAA and common.g_isInstall_ENUM :
                raise Exception("IPWorks Can't Support AAA & ENUM co-location on Medium1 Mode")
            if common.g_isInstall_CLF :
                raise Exception("IPWorks Can't Support CLF on Medium1 Mode")
        elif not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode) :
            if common.g_isInstall_AAA or common.g_isInstall_ENUM or common.g_isInstall_DNS :
                raise Exception("IPWorks Only Support CLF on Medium2 Mode")


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



    def getHaeIsoPath(self) :
        return self._hae_iso

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



    def getInstallPath(self) :
        return self._install_path

    def setInstallPath(self, install_path) :
        if install_path[-1] != '/':
            install_path += '/'
        self._install_path = install_path



    def getMountPoint(self) :
        return self._mount_point

    def setMountPoint(self, mount_point) :
        if mount_point[-1] == '/':
            mount_point = mount_point[0:-1]
        self._mount_point = mount_point



    def getLicensePath(self) :
        return self._license_path

    def setLicensePath(self, license_path) :
        self._license_path = license_path
        tmp = license_path.split('/')
        self.setLicenseName(tmp[-1])

    def getLicenseName(self) :
        return self._license_name

    def setLicenseName(self, license_name) :
        self._license_name = license_name



    def getDataMemSize(self) :
        return self._data_mem

    def getIndexMemSize(self) :
        return self._index_mem


    def getInstallSS7(self) :
        return self._install_ss7

    def setInstallSS7(self, isInstall) :
        if not cmp("yes", isInstall.strip().lower()) :
            self._install_ss7 = True

    def checkfile(self, filepath):
        if not os.path.exists(filepath) :
            raise Exception("%s Doesn't Exist !!!" %(filepath))

    def setCliPassword(self,username = None, password = None):
        if password is not None and username is not None:
            common.g_cli_username = username
            common.g_cli_password = password
            return
            
        print "Please Input Information of ipwcli"
        username = raw_input('  Enter ipwcli user name: ')
        counter = 0;
        success = False
        while (counter < 3) : 
            counter += 1
            p1 = getpass.getpass('  Enter Password: ')
            ret, str = common.checkPassword(p1)
            if ret is False:
                common.print_red(str)
                continue
            p2 = getpass.getpass('  Enter Password (Confirm): ')
            if cmp(p1, p2) :
                common.print_red("Password doesn't Match !!!")
                continue
            success = True
            break
        if not  success:
            log._file.warning("""For security reasons, it is recommended that your password include at least 3 of the following 4 items:
                    o    Lower case characters.
                    o    Upper case characters.
                    o    Numbers.
                    o    Special Characters. (more information is writed in CPI)""")
            raise Exception("Password for ipwcli is invalid !!!")
        common.g_cli_password = p1
        common.g_cli_username = username
        print


class MappingCfg :
    '''
    classdoc
    '''

    def __init__(self) :
        self._oam_mapping = []
        self._traffic_mapping = []
        self._heartbeat_mapping = []
        self._internal_mapping = []




