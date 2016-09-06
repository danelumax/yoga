import re, getpass, os
import log, common


class NodeCfg :
    """
    Class NodeCfg
    """

    def __init__(self) :
        self._hostname = ""
        self._username = ""
        self._password = ""
        self._sshport = "22"
        self._oam_ip = ""
        self._oam_prefix = 0
        self._traffic_ip = ""
        self._traffic_prefix = 0
        self._traffic_ipv6 = ""
        self._traffic_ipv6_prefix = 0
        self._internal_ip = ""
        self._internal_prefix = 0
        self._heartbeat_ip1 = ""
        self._heartbeat_ip2 = ""
        self._heartbeat_prefix = 0
        self._role = ''


    def setCommon(self, json_node) :
        # mandatory
        self._hostname = str(json_node["hostname"])
        self._oam_ip, self._oam_prefix = self.parseIp(str(json_node["oam_ip"]), common.C_IPv4_PREFIX_LEN)
        # optional
        #if common.getOptionValue(json_node, "username") :
        #    self._username = json_node["username"]
        #if common.getOptionValue(json_node, "password") :
        #    self._password = json_node["password"]
        need_input = True
        if os.path.exists(common.g_shadow_file) :
            fc = common.getNodeInfo()
            for x in fc :
                if re.search(self._hostname, x) :
                    log._file.info("Find Node info: " + x)
                    tmp = x.split(';')
                    self._username = tmp[2]
                    self._password = common.decrypt(tmp[3].strip())
                    need_input = False
                    break

        if not cmp(common.C_IPW_MODE_MEDIUM1,common.g_ipw_mode) or \
            not cmp(common.C_IPW_MODE_MEDIUM2,common.g_ipw_mode):
            context = common.getEnvInfo()
            if(context):
                self._setEnvInfo(context)

        if need_input :
            self.input_username_password()
        if common.getOptionValue(json_node, "ssh_port") :
            self._sshport = json_node["ssh_port"]
        if common.getOptionValue(json_node, "traffic_ip") :
            self._traffic_ip, self._traffic_prefix = self.parseIp(str(json_node["traffic_ip"]), common.C_IPv4_PREFIX_LEN)
        if not self._username :
            self._username = common.g_username
        if not self._password :
            self._password = common.g_password
        if not self._sshport :
            self._sshport = common.g_sshport
        if not self._internal_ip :
            self._internal_ip = self._oam_ip
        if (self._role == 'PS'):
           for key in json_node["ps_name"].keys():
               self.ps_name[key] = (json_node["ps_name"][key]).strip()
        elif(common.g_ipw_mode == common.C_IPW_MODE_ENTRY2):
           for key in json_node["ps_name"].keys():
               self.ps_name[key] = (json_node["ps_name"][key]).strip()
 
    def _setEnvInfo(self,context):
        log._file.debug(">>> _setEnvInfo")
        for x in context :
            tmp = x.split(';')
            if(tmp[1].strip() == "Active-SS"):
                hostname = tmp[0].strip() 
                if(hostname == self.getHostName()):
                    self._isActiveSs = True
        log._file.debug("<<<")


    def print_red(self, s) :
        print "%s[31;5m%s%s[0m" %(chr(27), s, chr(27))

    def input_username_password(self):
        print "Please Input Informantion of %s" %(self._hostname)
        self._username = raw_input('  Enter User Name: ')
        while 1 :
            p1 = getpass.getpass('  Enter Password: ')
            p2 = getpass.getpass('  Enter Password (Confirm): ')
            if cmp(p1, p2) :
                self.print_red("Password doesn't Match !!!")
                continue
            break
        self._password = p1
        print


    def parseIp(self, ip, prefix) :
        ip = ip.strip()
        if ip :
            if re.search(r'/', ip) :
                t_ip, tmp = ip.split('/')
                prefix = int(tmp)
                #print "ip=%s, prefix=%d" %(t_ip, prefix)
                if re.search(r'\.', t_ip) and (1 > prefix or 31 < prefix) :
                    raise Exception("ipv4 Netmask is error")
                if re.search(r':', t_ip) and (1 > prefix or 127 < prefix) :
                    raise Exception("ipv6 Netmask is error")
            else :
                t_ip = ip
        return t_ip, prefix
        
    

    def validateCfg(self) :
        is_ok = True
        if not self._hostname :
            log._file.error("Host name can't be empty")
            is_ok = False
        if not self._oam_ip :
            log._file.error("OAM IP can't be empty")
            is_ok = False
        if not self._username :
            log._file.error("Username can't be empty")
            is_ok = False
        if not self._password :
            log._file.error("Password can't be empty")
            is_ok = False
        return is_ok



    def getNetAddr(self, ip, prefix) :
        tmp = ip.split(".")
        t1 = prefix / 8
        t2 = prefix % 8
        if 0 == t1 :
            x = int(tmp[t1]) & t2
            netaddr = "%d.0.0.0" %x
        elif 1 == t1 :
            x = int(tmp[t1]) & t2
            netaddr = "%s.%d.0.0" %(tmp[0], x)
        elif 2 == t1 :
            x = int(tmp[t1]) & t2
            netaddr = "%s.%s.%d.0" %(tmp[0], tmp[1], x)
        elif 3 == t1 :
            x = int(tmp[t1]) & t2
            netaddr = "%s.%s.%s.%d" %(tmp[0], tmp[1], tmp[2], x)
        else :
            netaddr = ip
        return netaddr


    def getNetMask(self, prefix) :
        t1 = prefix / 8
        t2 = prefix % 8
        mask = ""
        if 0 == t1 :
            mask = self.getrest(t2) + ".0.0.0"       
        elif 1 == t1 :
            mask = "255." + self.getrest(t2) + ".0.0"
        elif 2 == t1 :
            mask = "255.255." + self.getrest(t2) + ".0"
        elif 3 == t1 :
            mask = "255.255.255." + self.getrest(t2)
        else :
            raise Exception("Netmask is error")
        return mask
            
            
    def getrest(self, rest) :
        if 0 == rest :
            return "0"
        elif 1 == rest :
            return "128"
        elif 2 == rest :
            return "192"
        elif 3 == rest :
            return "224"
        elif 4 == rest :
            return "240"
        elif 5 == rest :
            return "248"
        elif 6 == rest :
            return "252"
        elif 7 == rest :
            return "254"
        else : 
            raise Exception("Netmask is error")

    def getHostName(self) :
        return self._hostname

    def getUserName(self) :
        return self._username

    def getPassword(self) :
        return self._password

    def getOamIp(self) :
        return self._oam_ip
    
    def getOamPrefix(self) :
        return self._oam_prefix
        
    def getOamNetmask(self) :
        return self.getNetmask(self._oam_prefix)

    def getHeartbeatIp1(self) :
        return self._heartbeat_ip1

    def getHeartbeatIp2(self) :
        return self._heartbeat_ip2
    
    def getHeartbeatPrefix(self) :
        return self._heartbeat_prefix
        
    def getHeartbeatNetmask(self) :
        return self.getNetmask(self._heartbeat_prefix)

    def getInternalIp(self) :
        return self._internal_ip
        
    def getInternalPrefix(self) :
        return self._internal_prefix
        
    def getInternalNetmask(self) :
        return self.getNetmask(self._internal_prefix)

    def getTrafficIp(self) :
        return self._traffic_ip
        
    def getTrafficPrefix(self) :
        return self._traffic_prefix
        
    def getTrafficNetmask(self) :
        return self.getNetmask(self._traffic_prefix)

    def getTrafficIpv6(self) :
        return self._traffic_ipv6
        
    def getTrafficIpv6Prefix(self) :
        return self._traffic_ipv6_prefix

    def getSshPort(self) :
        return self._sshport
 
    def getHostRole(self) :
        return self._role

    def getPsName(self) :
        if(self._role == 'PS' or (common.g_ipw_mode == common.C_IPW_MODE_ENTRY2)):
            return self.ps_name
        else:
            return None


class SsCfg(NodeCfg) :
    """
    Class SsCfg
    """

    def __init__(self) :
        NodeCfg.__init__(self)
        self._role = 'SS'
        self._isActiveSs = False
        self.ps_name = {} # for entry2

    def validateCfg(self) :
        is_ok = NodeCfg.validateCfg(self)
        if (not cmp(common.C_IPW_MODE_ENTRY2, common.g_ipw_mode)) \
          and (not self._traffic_ip and not self._traffic_ipv6) :
            log._file.error("Traffic IP can't be empty in Entry2 with SS node")
            is_ok = False
        return is_ok



class PsCfg(NodeCfg) :
    """
    Class PsCfg
    """

    def __init__(self) :
        NodeCfg.__init__(self)
        self._role = 'PS'
        self.ps_name = {} 

    def validateCfg(self) :
        is_ok = NodeCfg.validateCfg(self)
        if not self._traffic_ip :
            log._file.error("Traffic IP can't be empty with PS node")
            is_ok = False
        return is_ok



class ClientCfg(NodeCfg) :
    """
    Class ClientCfg
    """

    def __init__(self) :
        NodeCfg.__init__(self)

    def validateCfg(self) :
        is_ok = NodeCfg.validateCfg(self)
        if not self._traffic_ip and not self._traffic_ipv6:
            log._file.error("Traffic IP can't be empty with Client node")
            is_ok = False
        return is_ok



