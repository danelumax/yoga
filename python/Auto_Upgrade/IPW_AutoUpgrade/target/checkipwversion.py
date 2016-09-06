#!/usr/bin/env python
import subprocess, sys, re, os

from optparse import OptionParser

import util

import log
log.Init(True)

class CheckIPWVersion:
    def __init__(self) :
        pass

    def execute(self, base_version_list) :
        command = '/opt/ipworks/IPWcommon/scripts/ipwversion'
        result = util.RunShell(command, use_shell=True)
        log._file.debug(result)
        '''
        # ipwversion

        Installed IPWorks 15.b (AVA_901_16_5_R1C) load modules:

        IPWcommon                -> CXP_901_6363_5_R1C
        IPWbackup                -> CXP_901_6365_5_R1C
        IPWjre                   -> 36_CAX_105_3951_5_R1C
        IPWmysql                 -> 17_CAX_105_3867_1_R1C
        IPWss                    -> CXP_901_6361_5_R1C
        IPWcli                   -> CXP_901_6362_5_R1C
        IPWtomcat                -> CXS_102_712_R1C
        IPWwebui                 -> CXP_901_6235_5_R1C
        IPWcnoss                 -> CXP_901_6364_5_R1C
        IPWsm                    -> CXP_901_6366_5_R1C
        IPWaaa                   -> CXP_901_6719_5_R1C
        IPWslm                   -> 10_CAX_105_3268_1_R1C
        '''

        for line in result.split('\n'):
            if re.search("Installed IPWorks", line):
                major_version = line.split()[2]
                minor_version = line.split()[3].strip('()')
                break

        log._file.debug("Current major:%s, minor:%s" %(major_version, minor_version))

        version = "%s (%s)" % (major_version, minor_version)
        if version in base_version_list:
            log._file.debug("Find the valid base version!")
            print version
        else:
            log._file.error("IPWorks Version is Incorrect !")
            raise Exception("IPWorks Version is Incorrect !")

        return 0

def main() :
    log._file.info(">> Remote Call Start")

    parser = OptionParser()
    parser.add_option("--base_versions",
                      help="List of base versions.",
                      action="store",
                      dest="base_version_list",
                      default=None)

    (options, _args) = parser.parse_args(args=sys.argv)
    log._file.debug("options.base_version_list : %s" %options.base_version_list)

    task = CheckIPWVersion()
    task.execute(eval(options.base_version_list))
    log._file.info("<< Remote Call End")
    return 0

if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        log._cons.error(e)
        sys.exit(2)
