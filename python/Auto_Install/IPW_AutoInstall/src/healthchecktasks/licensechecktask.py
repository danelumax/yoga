import re, subprocess
import log, common
from cfg import cfgInstance
from healthcheckinfo import healthcheckInstance


class LicenseCheckTask(object):
    '''
    Check License MD5 Checksum
    '''

    def __init__(self):
        pass

    def precheck(self):
        pass


    def verify(self):
        pass
    
    
    def cleanup(self):
        pass
    
    
    def updateProgress(self):
        pass


    def execute(self):
        log._file.debug(">> License Checksum Begin") 
        if not healthcheckInstance().getLicenseMd5() :
            log._file.info("No need to Check License checksum, Because checksum doesn't Configured.")
            return
        cmd = 'md5sum %s' %(cfgInstance().getLicensePath())
        log._file.info("Exec cmd: " + cmd)
        proc = subprocess.Popen(['md5sum', cfgInstance().getLicensePath()], stdout=subprocess.PIPE)
        code = proc.wait()
        info = proc.stdout.read()
        log._file.info("Return code: %d, Return info:\n%s" %(code, info))
        if re.search(healthcheckInstance().getLicenseMd5(), info):
            expValue = healthcheckInstance().getLicenseMd5()
            common.save_healthcheck_info("License Checksum", expValue, expValue, "OK")
        else:
            log._file.error("License Checksum is incorrect ! Exp value: %s, Real value: %s" %(healthcheckInstance().getLicenseMd5(), info))
            raise Exception("License Checksum is incorrect !")
        log._file.debug("<< License Checksum End") 




