#!/usr/bin/env python
import sys
import pexpect

from optparse import OptionParser

import util

import log
log.Init(True)


C_CHROOT_TYPE_INNDB='innodb'
C_CHROOT_TYPE_TOMCAT='tomcat'
C_CHROOT_TYPE_SQLNODE='sqlnode'

class ConfigHAChrootEnv:
    
    def __init__(self) :
        pass
   
    def execute(self,chroot_type,chroot_action,slave_password) :
        cmd = ""
        if not cmp(C_CHROOT_TYPE_INNDB,chroot_type):
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_innodb_env"
        elif not cmp(C_CHROOT_TYPE_TOMCAT,chroot_type):
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_tomcat_env"
        elif not cmp(C_CHROOT_TYPE_SQLNODE,chroot_type):
            cmd = "/opt/ipworks/IPWcommon/usr/bin/chroot_sqlnode_env"
        else:
            return -1            

        self.configChrootEnv(cmd, chroot_action, slave_password);
        return 0
    
    def configChrootEnv(self, cmd, chroot_action, slave_password) :
        log._cons.debug("Ececute chroot cmd: \n" + cmd)
        #TR HT92258 
        # change default from 20 mins to 60 mins
        self._child = pexpect.spawn(cmd, [chroot_action], timeout=3600)
        self._child.logfile = sys.stdout
         
        i = self._child.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password:)"])
        if i==0:
            # New certificate -- always accept it.
            # This is what you get if SSH does not have the remote host's
            # public key stored in the 'known_hosts' cache.
            self._child.sendline("yes")
            i = self._child.expect(["(?i)are you sure you want to continue connecting", "(?i)(?:password:)"])
        if i==1:
            # password or passphrase
            self._child.sendline(slave_password)
         
        self._child.expect(pexpect.EOF)    

 

def main() :
    parser = OptionParser()
    
    parser.add_option("--chroot_type",
        help="the chroot type which should be configured, could be innodb, tomcat or sqlnode",
        action="store",
        dest="chroot_type",
        choices=[C_CHROOT_TYPE_INNDB,C_CHROOT_TYPE_TOMCAT,C_CHROOT_TYPE_SQLNODE],
        default=None)
    
    parser.add_option("--chroot_action",
        help="the chroot action which should be executed, could be start or stop",
        action="store",
        dest="chroot_action",
        choices=["start","stop"],
        default=None)
    
    parser.add_option("--slave_password",
        help="the slave host password",
        action="store",
        dest="slave_password",
        default=None)
 
    (options, args) = parser.parse_args(args=sys.argv)
    log._cons.info("options.chroot_type: " + str(options.chroot_type))
    log._cons.info("options.chroot_action: " + str(options.chroot_action))
    log._cons.info("options.slave_password: " + util.obfuscate(options.slave_password))

    log._cons.debug(">> Call Start")
    task = ConfigHAChrootEnv()
    result = task.execute(options.chroot_type,options.chroot_action,options.slave_password)
    log._cons.debug("<< Call End")
    return result
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        log._cons.error(e)
        print str(e)
        sys.exit(2)

