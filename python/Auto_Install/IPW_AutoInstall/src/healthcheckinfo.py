import log, common


def healthcheckInstance() :
    try :
        inst = HealthCheckInfo()
    except HealthCheckInfo as x:
        inst = x
    return inst


class HealthCheckInfo :
    '''
    class doc
    '''

    __instance = None


    def __init__(self) :
        if HealthCheckInfo.__instance :
            raise HealthCheckInfo.__instance
        HealthCheckInfo.__instance = self
        self._cfgfile = 'healthcheck.json'
        self._os_version = ''
        self._os_patchlevel = ''
        self._kernal_version = ''
        self._ipworks_version = ''
        self._license_md5 = ''


    def parse(self):
        log._file.debug(">> enter parse cfg file: " + self._cfgfile)
        json_root = common.parse_file(self._cfgfile)
        self._os_version = json_root['os_version_check']['version'].strip()
        self._os_patchlevel = json_root['os_version_check']['patchlevel'].strip()
        self._kernal_version = json_root['kernal_version_check']['version'].strip()
        self._ipworks_version = json_root['ipworks_version_check']['version'].strip()
        self._license_md5 = json_root['license_md5_check']['md5_checksum'].strip()
        log._file.debug("<< outer parse cfg file")


    def getOsVersion(self):
        return self._os_version

    def getOsPatchLevel(self):
        return self._os_patchlevel

    def getKernalVersion(self):
        return self._kernal_version

    def getIpwVersion(self):
        return self._ipworks_version

    def getLicenseMd5(self):
        return self._license_md5








