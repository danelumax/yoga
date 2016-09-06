import threading, traceback, sys, time, logging
from cfg import cfgInstance
from sshmanager import sshManagerInstance
from sshutil import SshUtil



class InstallThread(threading.Thread) :

    def __init__(self, cfg, rpmList, jsonRoot, installSS7=False) :
        threadname = "install_%s" %cfg.getHostName()
        threading.Thread.__init__(self, name=threadname)
        self.cfg = cfg
        self.rpm_list = rpmList
        self.json_root = jsonRoot
        self.install_ss7 = installSS7
        self.running = True
        # create own logger
        formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s | %(message)s')
        file_handler = logging.FileHandler("log/"+threadname)
        file_handler.setFormatter(formatter)
        self.log = logging.getLogger(threadname)
        self.log.addHandler(file_handler)
        self.log.setLevel(logging.DEBUG)


    def run(self) :
        self.log.debug("##### Install thread Start on %s #####" % self.cfg.getHostName())
        try :
            if self.running and self.install_ss7 :
                self._installSS7()
            for module in self.rpm_list :
                if self.running :
                    self._install_module(self.json_root, module)
            if self.running :
                self._remote_setup_env()
        except Exception as e :
            self.log.error("Exception info: " + str(e))
            traceback.print_exc(file = sys.stderr)
            raise Exception("Running Install Thread Failed on " + self.cfg.getHostName())
        self.log.debug("##### Install thread Finish on %s #####" % self.cfg.getHostName())

    def stop(self) :
        self.running = False

    def _install_module(self, root, module) :
        for item in root[module] :
            if item["isShell"] == "True" :
                isShell = True
            else :
                isShell = False
            if self.running :
                if 'erh' == item["moudle"] :
                    if self.install_ss7 :
                        self._remote_install_package(item["moudle"], is_shell=isShell, sub_module=item["subModule"])
                else :
                    self._remote_install_package(item["moudle"], is_shell=isShell, sub_module=item["subModule"])

    def _remote_install_package(self, package_name, is_shell, sub_module=None):
        self.log.debug(">>> Install %s %s on %s" %(package_name, sub_module, self.cfg.getHostName()))
        ssh = sshManagerInstance().getSsh(self.cfg.getHostName())
        ssh_util = SshUtil(ssh, logger=self.log)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "python installpackage.py --mount_point=" + cfgInstance().getMountPoint() + " --name=" + package_name 
        if is_shell :
            command += " --shell"
        if sub_module :
            command += " --sub_module=" + sub_module
        # need to wait other 3 seconds to receive compeletly return infomation
        ssh_util.remote_exec(command, wait=3)
        self.log.debug("<<<")

    def _remote_setup_env(self) :
        self.log.debug(">>> Setup Env on %s" %(self.cfg.getHostName()))
        ssh = sshManagerInstance().getSsh(self.cfg.getHostName())
        ssh_util = SshUtil(ssh, logger=self.log)
        ssh_util.remote_exec("cd " + cfgInstance().getInstallPath())
        command = "python setenv.py --command=write_bashrc"
        ssh_util.remote_exec(command)
        ssh_util.remote_exec("umount " + cfgInstance().getMountPoint(), p_err=False, throw=False) 
        self.log.debug("<<<")

    def _installSS7(self) :
        self.log.debug(">>> Install SS7 on " + self.cfg.getHostName())
        ssh = sshManagerInstance().getSsh(self.cfg.getHostName())
        ssh_util = SshUtil(ssh, logger=self.log)
        ssh_util.remote_exec("cd " + cfgInstance().getMountPoint() + "/x86-linux/ss7")
        res,code = ssh_util.remote_exec("/opt/sign/EABss7023/bin/showver /opt/sign/EABss7035/bin/be", p_err=False, throw=False)
        if code == 0 :
            self.log.debug("SS7 has already installed on this machine, will uninstall it automatically")
            ssh_util.remote_exec("/etc/init.d/ss7ec stop", p_err=False, throw=False)
            check_cnt = 0
            while check_cnt < 5 :
                time.sleep(10)
                res,code = ssh_util.remote_exec("ps -ef |grep EAB |grep -v grep", p_err=False, throw=False)
                if 0 != code :
                    self.log.debug("SS7 Process has already stopped")
                    break
                check_cnt += 1
            if check_cnt == 5 :
                raise Exception("Can't stop SS7 Process !!!")
            ssh_util.remote_exec("./uninstall")
        ssh_util.remote_exec("./install")
        self.log.debug("<<< Install SS7 End")


