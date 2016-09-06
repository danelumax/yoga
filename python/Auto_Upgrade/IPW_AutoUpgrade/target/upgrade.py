'''
Created on 2015/03/27

@author: eyotang
'''
import re, sys, os, socket, traceback
import glob, cmd
from optparse import OptionParser

import util

import log
log.Init(True)

g_release_list = []
g_num_installed_release = 0


class module(object):
    def __init__(self, name, desc=None, arguments=None, dependants=None, cluster_name=None):
        self.name         = name
        self.desc         = desc
        self.arguments    = arguments
        self.dependants   = dependants
        self.cluster_name = cluster_name

DEPENDENCYS = [
               # (name,desc,arguments,dependant LM)
               #module("All","All","",""),
               module("IPWcommon","IPWcommon","",""),
               module("IPWbackup","IPWbackup","",""),
               module("IPWjre","IPWjre","","IPWcommon IPWbackup"),
               module("IPWmysql","IPWmysql (Innodb Node)","innodbnode","IPWcommon IPWbackup", "INNODB_NODE"),
               module("IPWmysql","IPWmysql (Mgmt Node)","mgmnode","IPWcommon IPWbackup", "MGM_NODE"),
               module("IPWmysql","IPWmysql (Data Node)","datanode","IPWcommon IPWbackup", "DATA_NODE"),
               module("IPWmysql","IPWmysql (SQL Node)","sqlnode","IPWcommon IPWbackup", "SQL_NODE"),
               module("IPWcli","IPWcli","","IPWjre"),
               module("IPWss","IPWss","","IPWmysql IPWcli"),
               module("IPWtomcat","IPWtomcat","","IPWjre"),
               module("IPWwebui","IPWwebui","","IPWtomcat IPWss"),
               module("IPWcnoss","IPWcnoss","","IPWss"),
               module("IPWsm","IPWsm","","IPWjre"),
               module("IPWdns","IPWdns","","IPWsm"),
               module("IPWdhcpv4","IPWdhcpv4","","IPWsm"),
               module("IPWenum","IPWenum","","IPWsm"),
               module("IPWasdnsmon","IPWasdnsmon","","IPWsm"),
               module("IPWerh","IPWerh","","IPWenum IPWsm"),
               module("IPWaaa", "IPWaaa", "", "IPWcommon IPWbackup IPWmysql IPWsm IPWslm"),
               module("IPWslm", "IPWslm", "", "IPWcommon IPWbackup"),
               module("IPWclf", "IPWclf", "", "IPWcommon IPWbackup IPWpmal"),
               module("IPWpmal", "IPWpmal", "", "IPWcommon IPWbackup IPWclf"),
               module("IPWem", "IPWem", "", "IPWtomcat"),
               module("IPWhaagents","IPWhaagents","","IPWcommon")
               ]

def GetArguments(name, cluster_name):
    modules = filter(lambda MD: MD.name == name and MD.cluster_name == cluster_name, DEPENDENCYS)
    if len(modules) > 0:
        return modules[0].arguments
    else:
        return ""

SPACESREQ = {
    "IPWcommon"  : 30,
    "IPWbackup"  : 2,
    "IPWcli"     : 2,
    "IPWcnoss"   : 2,
    "IPWjre"     : 120,
    "IPWasdnsmon": 4,
    "IPWdhcpv4"  : 5,
    "IPWdns"     : 20,
    "IPWenum"    : 8,
    "IPWmysql"   : 300,
    "IPWsm"      : 2,
    "IPWss"      : 2,
    "IPWhaagents": 2,
    "IPWtomcat"  : 30,
    "IPWwebui"   : 2,
    "IPWerh"     : 2,
    "IPWaaa"     : 40,
    "IPWslm"     : 40,
    "IPWclf"     : 20,
    "IPWpmal"    : 20,
    "IPWem"      : 20
}

def GetSpace(name):
    return SPACESREQ[name]

# Captures all the states of the LoadModule
FAILED                 = "FAILED"
INSTALLED              = "INSTALLED"
NOTINSTALLED           = "NOTINSTALLED"


class LoadModuleInfo(object):
    def __init__(self, lmName = "IPWeyotang", lmStatus = FAILED,
                 revision = "14.b", lmCXPNumber = "CXP_901_6364_4_R3B02",
                 additional = None, clusterName = None):
        assert lmStatus in [FAILED, INSTALLED, NOTINSTALLED]
        self.lmName       = lmName
        self.clusterName  = clusterName # For IPWmysql innodb, NDB
        self.additional   = additional  # For IPWaaa, core, plugin
        self.lmStatus     = lmStatus
        self.revision     = revision
        self.lmCXPNumber  = lmCXPNumber
        if self.additional is None:
            self.lmActualName = self.lmName + "-" + self.revision + "-" + self.lmCXPNumber
        else:
            self.lmActualName = []
            for suffix in self.additional:
                self.lmActualName.append(self.lmName + "-" + suffix + "-" + self.revision + "-" + self.lmCXPNumber)

    def Print(self):
        log._file.info("Load Module Info{")
        log._file.info("Load Module Name        = " + self.lmName)
        if self.clusterName is not None:
            log._file.info("Mysql Cluster Name      = " + self.clusterName)
        log._file.info("Load Module Status      = " + self.lmStatus)
        log._file.info("Load Module CXP Number  = " + self.lmCXPNumber)

        log._file.info("Load Module Actual Name = " + self.ActualNameString())
        log._file.info("}")

    def ActualNameString(self):
        if type(self.lmActualName) is list:
            return ", ".join(self.lmActualName)
        else:
            return self.lmActualName

    def CheckSetStatus(self):
        if type(self.lmActualName) is list:
            cmd = ["rpm", "-q"] + self.lmActualName
        else:
            cmd = ["rpm", "-q", self.lmActualName]
        result = util.RunShell(cmd)
        match = re.match(r'(.|\n|\r)*is not installed(.|\n|\r)*', result)
        if match:
            self.lmStatus = FAILED
        else:
            self.lmStatus = INSTALLED

    def SetStatus(self, lmStatus):
        self.lmStatus = lmStatus



# Captures all the status of the Release
INACTIVE            = "INACTIVE"
ACTIVE              = "ACTIVE"
PARTIALLY_INSTALLED = "PARTIALLY_INSTALLED"
NOT_INSTALLED       = "NOT_INSTALLED"

class ReleaseInfo(object):
    def __init__(self, revision = None, releaseCSHNumber = None,
                 buildNum = 0, releaseStatus = NOT_INSTALLED, loadModules = []):
        '''
        revision = "15.b"
        releaseCSHNumber = "AVA_901_16_5_R1C"
        '''
        assert releaseStatus in [INACTIVE, ACTIVE, PARTIALLY_INSTALLED, NOT_INSTALLED]

        self.load_module_list    = loadModules
        self.releaseStatus       = releaseStatus
        self.numberOfLoadModules = len(self.load_module_list)
        self.revision            = revision
        self.releaseCSHNumber    = releaseCSHNumber
        self.buildNum            = buildNum

    def Print(self):
        log._file.info("Release Revision      : " + self.revision)
        log._file.info("Release CSH Number    : " + self.releaseCSHNumber)
        log._file.info("Build Number          : " + str(self.buildNum))
        log._file.info("Release Status        : " + self.releaseStatus)
        log._file.info("Number of Load Modules: " + str(self.numberOfLoadModules))
        log._file.info("Load Modules : [")
        for lm in self.load_module_list:
            lm.Print()
        log._file.info("]")




class initialize(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.IPWorksPath = "/opt/IPWorks/"
        self.ipworksSoftLink = "/opt/ipworks"
        self.usrConfPath = "/usr/ipworks_configs/"

    def GetInstalledReleases(self):
        global g_release_list, g_num_installed_release
        g_release_list = []
        g_num_installed_release = 0

        if os.path.exists(self.IPWorksPath):
            cmd = ["find", self.IPWorksPath, "-name", "version.txt"]
            versions = util.RunShell(cmd)
            log._file.debug("Version files:" + versions)
            for line in versions.splitlines():
                FAKE_SECTION = "eyotang"
                config = util.ReadNoSectionConf(line, FAKE_SECTION)
                value = config.get(FAKE_SECTION, "BUILD_NUMBER")
                buildNum = value.split(";")[0]

                words = line.split("/")
                revision = words[3]
                releaseCSHNumber = words[4]
                g_release_list.append(ReleaseInfo(revision, releaseCSHNumber, buildNum, INACTIVE))
                g_num_installed_release = g_num_installed_release + 1
        else:
            util.Error("find: '%s': No such file or directory", self.IPWorksPath)


    def SetActiveRelease(self):
        global g_release_list, g_num_installed_release
        if os.path.islink(self.ipworksSoftLink):
            realpath = os.path.realpath(self.ipworksSoftLink)
            words = realpath.split("/")
            revision = words[3]
            releaseCSHNumber = words[4]
            for release in g_release_list:
                if revision == release.revision and releaseCSHNumber == release.releaseCSHNumber:
                    release.releaseStatus = ACTIVE
        else:
            util.Error("dir: '%s': is not a soft link dir", self.ipworksSoftLink)


    def SetLoadModules(self):
        for release in g_release_list:
            VersionPath = release.revision + "/" + release.releaseCSHNumber + "/"
            path = self.IPWorksPath + VersionPath
            match_rule = path + "IPW*"
            result = glob.glob(match_rule)
            module_dirs = [component.split("/")[-1] for component in result]

            version_txt = path + "version.txt"
            FAKE_SECTION = "eyotang"
            config = util.ReadNoSectionConf(version_txt, FAKE_SECTION)

            log._file.debug("Get load module names for revision:" + release.revision + " " + release.releaseCSHNumber)

            loadModules = []
            for load_module in DEPENDENCYS:
                component = load_module.name
                if component not in module_dirs:
                    continue
                value = config.get(FAKE_SECTION, component)
                lmCXPNumber = value.split(";")[0]
                if component == "IPWmysql":
                    loadModule = LoadModuleInfo(component, NOTINSTALLED, release.revision, lmCXPNumber, None, load_module.cluster_name)
                elif component == "IPWaaa":
                    if release.revision < "15.b":
                        additional = ["radius", "core", "plugins", "server"]
                    else:
                        additional = ["radius", "core", "server"]
                    loadModule = LoadModuleInfo(component, NOTINSTALLED, release.revision, lmCXPNumber, additional)
                else:
                    loadModule = LoadModuleInfo(component, NOTINSTALLED, release.revision, lmCXPNumber)

                loadModules.append(loadModule)

            '''
            Check and set each load module status and mysql cluster status
            '''
            log._file.debug("Set load module status for revision:" + release.revision + " " + release.releaseCSHNumber)
            usrConf = self.usrConfPath + VersionPath + "ipworks.conf"
            config = util.ReadNoSectionConf(usrConf, FAKE_SECTION)
            for loadModule in loadModules:
                loadModule.CheckSetStatus()
                if loadModule.lmName == "IPWmysql":
                    value = config.get(FAKE_SECTION, loadModule.clusterName)
                    if value == "0":
                        loadModule.SetStatus(NOTINSTALLED)
                if loadModule.lmName == "IPWtomcat" and loadModule.lmStatus == FAILED: # chroot tomcat has a bug, ignore this failure
                    loadModule.SetStatus(NOTINSTALLED)
                if loadModule.lmStatus == FAILED:
                    release.releaseStatus = PARTIALLY_INSTALLED

            release.load_module_list = loadModules
            release.numberOfLoadModules = len(loadModules)

    def execute(self):
        self.GetInstalledReleases()
        self.SetActiveRelease()
        self.SetLoadModules()


NOT_ENOUGH_SPACE  = "Not enough space"
VERSION_GT_ACTIVE = "Current version is greater than active"
VERSION_LT_ACTIVE = "Current version is less than active"
VERSION_EQ_ACTIVE = "Current version is equal to active"

class iso(object):
    def __init__(self, mount_path = "/mnt"):
        self.x86_util   = mount_path + "/x86-linux/utils/"
        self.version_txt = self.x86_util + "version.txt"
        self.cwd         = os.getcwd()
        self.loadModules = None
        self.releaseInfo = None

        hostname = util.RunShell("hostname", use_shell=True)
        hostname = hostname.strip()
        log._file.debug("hostname of upgrade target is [%s]" %hostname)
        self.logfile = "/var/ipworks/logs/ipworks_ipwsetup_" + hostname + ".log"


    def GetCDInfo(self):
        global g_release_list, g_num_installed_release
        # 1. Get release info from CD
        if not os.path.exists(self.version_txt):
            log._file.error("Version file '" + self.version_txt + "' in ISO doesn't exist!")
            raise Exception("Version file '" + self.version_txt + "' in ISO doesn't exist!")
        FAKE_SECTION = "eyotang"
        config = util.ReadNoSectionConf(self.version_txt, FAKE_SECTION)

        value = config.get(FAKE_SECTION, "REVISION_MAJOR")
        major = value.split(";")[0]
        value = config.get(FAKE_SECTION, "REVISION_MINOR")
        minor = value.split(";")[0]
        revision = major + "." + minor

        value = config.get(FAKE_SECTION, "IPWorks")
        releaseCSHNumber = value.split(";")[0]

        value = config.get(FAKE_SECTION, "BUILD_NUMBER")
        buildNum = value.split(";")[0]

        self.releaseInfo = ReleaseInfo(revision, releaseCSHNumber, buildNum, NOT_INSTALLED)

        # 2. Get load modules from CD
        active_release = filter(lambda release: release.releaseStatus == ACTIVE, g_release_list)[0]

        loadModules = []
        for load_module in active_release.load_module_list:
            if load_module.lmStatus != INSTALLED:
                continue
            component = load_module.lmName
            value = config.get(FAKE_SECTION, component)
            lmCXPNumber = value.split(";")[0]
            if component == "IPWmysql":
                loadModule = LoadModuleInfo(component, NOTINSTALLED, revision, lmCXPNumber, None, load_module.clusterName)
            elif component == "IPWaaa":
                if revision < "15.b":
                    additional = ["radius", "core", "plugins", "server"]
                else:
                    additional = ["radius", "core", "server"]
                loadModule = LoadModuleInfo(component, NOTINSTALLED, revision, lmCXPNumber, additional)
            else:
                loadModule = LoadModuleInfo(component, NOTINSTALLED, revision, lmCXPNumber)

            loadModules.append(loadModule)

        self.loadModules = loadModules
        self.releaseInfo.load_module_list = self.loadModules
        self.releaseInfo.numberOfLoadModules = len(self.loadModules)

    def Check(self):
        # 1. Check space required
        required_space = 0
        for loadmodule in self.loadModules:
            required_space = required_space + GetSpace(loadmodule.lmName)
        vfs = os.statvfs("/opt")
        space_available = vfs.f_bavail * vfs.f_frsize / (1024 * 1024)
        if required_space > space_available:
            util.Error("Update:Not enough disk space, %dM space is needed", required_space)
            return False, NOT_ENOUGH_SPACE

        # 2. Check release version
        global g_release_list, g_num_installed_release
        active_release = filter(lambda release: release.releaseStatus == ACTIVE, g_release_list)[0]
        active_version = active_release.revision + " " + active_release.releaseCSHNumber
        current_version = self.releaseInfo.revision + " " + self.releaseInfo.releaseCSHNumber
        if self.releaseInfo.revision > active_release.revision:
            log._file.info("OK, active release: " + active_version + ", current release: " + current_version)
            return True, VERSION_GT_ACTIVE
        elif self.releaseInfo.revision == active_release.revision:
            if self.releaseInfo.releaseCSHNumber > active_release.releaseCSHNumber:
                log._file.info("OK, active release: " + active_version + ", current release: " + current_version)
                return True, VERSION_GT_ACTIVE
            elif self.releaseInfo.releaseCSHNumber == active_release.releaseCSHNumber:
                log._file.info("OK, active release: " + active_version + ", current release: " + current_version)
                return True, VERSION_EQ_ACTIVE
            else:
                log._file.info("NOK, active release: " + active_version + ", current release: " + current_version)
                return False, VERSION_LT_ACTIVE
        else:
            log._file.info("NOK, active release: " + active_version + ", current release: " + current_version)
            return False, VERSION_LT_ACTIVE


    def Upgrade(self):
        os.chdir(self.x86_util)
        log._file.debug("Change path to [" + self.x86_util + "] to install the modules")

        global g_release_list, g_num_installed_release
        installed_release = filter(lambda release: release.revision == self.releaseInfo.revision and release.releaseCSHNumber == self.releaseInfo.releaseCSHNumber, g_release_list)
        for loadmodule in self.loadModules:
            if len(installed_release) > 0:
                installed = filter(lambda lm: lm.lmName == loadmodule.lmName and lm.lmStatus == INSTALLED, installed_release[0].load_module_list)
                if len(installed) > 0:
                    log._file.debug("Module already installed, ignore: " + loadmodule.ActualNameString())
                    continue

            # Install the upgrade version
            check_install = self.x86_util + "check_install"
            arguments = GetArguments(loadmodule.lmName, loadmodule.clusterName)
            cmd = [check_install, self.releaseInfo.releaseCSHNumber, loadmodule.lmCXPNumber, loadmodule.lmName, self.logfile, arguments]
            result, retcode = util.RunShellWithReturnCode(cmd, False, True)
            if retcode:
                util.Error("Got error status from %s:\n%s\n %s" \
                            % (cmd, result, retcode))
                loadmodule.lmStatus = FAILED

        os.chdir(self.cwd)
        log._file.debug("Change path back to [" + self.cwd + "] after install the modules")


    def Activate(self):
        os.chdir(self.x86_util)
        log._file.debug("Change path to [" + self.x86_util + "] to activate the version")

        activate_ipworks = self.x86_util + "activate_ipworks"
        cmd = [activate_ipworks, self.releaseInfo.releaseCSHNumber, self.logfile]
        result, retcode = util.RunShellWithReturnCode(cmd, False, True)
        logfd = open(self.logfile, 'a')
        print >> logfd, result
        logfd.close()

        os.chdir(self.cwd)
        log._file.debug("Change path back to [" + self.cwd + "] after activate the version")
        if retcode != 0:
            raise Exception("Activate IPWorks failed!")

    def execute(self):
        self.GetCDInfo()
        rcode, desc = self.Check()
        log._file.debug(desc)
        if rcode:
            self.Upgrade()
            if desc == VERSION_GT_ACTIVE:
                self.Activate()




class Upgrade:
    def __init__(self) :
        pass

    def execute(self, mount_point):
        initial = initialize()
        initial.execute()

        global g_release_list, g_num_installed_release
        for release in g_release_list:
            release.Print()

        newiso = iso(mount_point)
        newiso.execute()

        initial.execute()
        for release in g_release_list:
            release.Print()
        return 0


def main() :
    parser = OptionParser()
    parser.add_option("--mount_point",
        help="the path to the mount point.",
        action="store",
        dest="mount_point",
        default=None)

    (options, _args) = parser.parse_args(args=sys.argv)
    log._file.info("options.mount_point: " + str(options.mount_point))

    log._file.debug(">> Remote Call Start Upgrade")
    task = Upgrade()
    task.execute(options.mount_point)
    log._file.debug(">> Remote Call End Upgrade")
    return 0



if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception as e :
        traceback.print_exc(file = sys.stderr)
        sys.exit(2)
