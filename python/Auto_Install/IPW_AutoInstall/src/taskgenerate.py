import log, common
from cfg import cfgInstance


class TaskGenerate(object) :
    '''
    classdocs
    '''


    def __init__(self) :
        '''
        Constructor
        '''
        pass
        

    def getPrepareTasks(self) :
        task_root = common.parse_file("src/pretasks.json")
        common.g_exec_tasklist.append(task_root["preparation"])
        #common.g_exec_tasklist.append(task_root["os_cfg"])
    

    def getTasks(self, isUninstall = False) :
        if isUninstall :
            return self.getUninstallTasks()
        else :
            return self.getInstallTasks()


    def getUninstallTasks(self) :
        return None 


    def getInstallTasks(self) :
        task_root = common.parse_file("src/tasks.json")
        
        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
            if not cmp(common.C_EMC_MODE_NFS, cfgInstance().getHaCfg().getEmcMode()):
                common.g_exec_tasklist.append(task_root["nfs_ha_install"])
            else:
                common.g_exec_tasklist.append(task_root["diskarray_ha_install"])
            
        common.g_exec_tasklist.append(task_root["ipw_install"])

        if not cmp(common.C_IPW_MODE_MEDIUM1, common.g_ipw_mode) \
          or not cmp(common.C_IPW_MODE_MEDIUM2, common.g_ipw_mode):
            if not cmp(common.C_EMC_MODE_DISKARRAY, cfgInstance().getHaCfg().getEmcMode()):
                common.g_exec_tasklist.append(task_root["sbd_cfg"])

        common.g_exec_tasklist.append(task_root["ipw_cfg"])
        
        if common.g_isInstall_AAA :
            common.g_exec_tasklist.append(task_root["aaa_cfg"])
        if common.g_isInstall_ENUM :
            common.g_exec_tasklist.append(task_root["enum_cfg"])
        elif common.g_isInstall_DNS :
            common.g_exec_tasklist.append(task_root["dns_cfg"])
        if common.g_isInstall_DHCP :
            common.g_exec_tasklist.append(task_root["dhcp_cfg"])
        if common.g_isInstall_CLF :
            common.g_exec_tasklist.append(task_root["clf_cfg"])
        
        common.g_exec_tasklist.append(task_root["alarm_check"])


        


