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
        self._use_csv = False
        self._emc_mode = common.C_EMC_MODE_NFS   #  'nfs' or 'diskarray'


    def setCommon(self, json_node) :
        if common.getOptionValue(json_node, "emc_mode") :
            self._emc_mode = json_node["emc_mode"].strip().lower()
            if not cmp(common.C_EMC_MODE_NFS, self._emc_mode): 
                common.C_EMC_MOUNT_MODE_DOUBLE = False
            elif not cmp(common.C_EMC_MODE_DISKARRAY,self._emc_mode):
                common.C_EMC_MOUNT_MODE_DOUBLE = True 
            else:
                raise Exception("Unknown EMC Mode: " + self._emc_mode)
        # common
        self._ss_vip = json_node["ipwss_vip"]
        if((json_node["use_csv_engine_grp"].lower().strip()) == "yes"):
            self._use_csv = True
        if common.g_isInstall_AAA :
            self._mgm_vip = json_node["dbcluster_vip"]
            self._sql_vip = json_node["ipwsql_vip"]
            self._csv_vip = json_node["csvengine_vip"]

    def validateCfg(self) :
        is_ok = True
        # common validate
        if not self._ss_vip :
            log._file.error("ss_vip can't be empty in Medium Mode")
            is_ok = False
        if common.g_isInstall_AAA :
            if not self._mgm_vip or not self._sql_vip or not self._csv_vip :
                log._file.error("mgm_vip, sql_vip, csv_vip can't be empty in Medium AAA")
                is_ok = False
        if common.g_isInstall_CLF :
            if not self._a2_vip or not self._e2_vip or not self._pmal_vip :
                log._file.error("clf_cmi_nacf_pmi_racfe4_umi_vip, ipw_clf_sbccops_sbce2_vip, ipw_pmal_cmipmi_soap_vip can't be empty in Medium CLF")
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
        
    def getEmcMode(self) :
        return self._emc_mode

    def useCsvGrp(self) :
        return self._use_csv

