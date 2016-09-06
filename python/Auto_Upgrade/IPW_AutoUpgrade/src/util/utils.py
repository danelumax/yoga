'''
Created on 2015/03/27

@author: eyotang
'''
import log
import os
import subprocess
import sys
import time
import re

import ConfigParser
import StringIO

from sshmanager import sshManagerInstance
from sshutil import SshUtil

def Error(msg):
    """Print an error message to stderr and exit."""
    print >>sys.stderr, msg
    log._file.debug(msg)
    #sys.exit(1)

def RunShellWithReturnCode(command, print_output=False,
                            universal_newlines=True):
    """Executes a command and returns the output from stdout and the return code.

    Args:
        command: Command to execute.
        print_output: If True, the output is printed to stdout.
                      If False, both stdout and stderr are ignored.
        universal_newlines: Use universal_newlines flag (default: True).

      Returns:
        Tuple (output, return code)
    """
    log._file.debug("Running %s", ' '.join(command))
    env = os.environ
    env['TERM'] = 'xterm'
    # Use a shell for subcommands on Windows to get a PATH search.
    use_shell = sys.platform.startswith("win")
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=use_shell, universal_newlines=universal_newlines,
                         env=env)
    if print_output:
        output_array = []
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print line.strip("\n")
            output_array.append(line)
        output = "".join(output_array)
    else:
        output = p.stdout.read()
    p.wait()
    errout = p.stderr.read()
    if print_output and errout:
        print >>sys.stderr, errout
    p.stdout.close()
    p.stderr.close()
    return output, p.returncode



def RunShell(command, silent_ok=False, universal_newlines=True,
             print_output=False):
    data, retcode = RunShellWithReturnCode(command, print_output,
                                           universal_newlines)
    if retcode:
        Error("Got error status from %s:\n%s\n %s" \
                  % (command, data, retcode))
    if not silent_ok and not data:
        Error("No output from %s" % command)
    return data


def ReadNoSectionConf(path, FAKE_SECTION = "eyotang"):
    ini_cfg = '['+ FAKE_SECTION +']\n' + open(path, 'r').read()
    ini_fp = StringIO.StringIO(ini_cfg)
    config = ConfigParser.RawConfigParser()
    config.readfp(ini_fp)
    return config

def check_process(ssh_conn, process, mode, max_retry=30) :
    if max_retry < 1 :
        raise Exception("invalid parameter max_retry mush great than 0")
    ssh_util = SshUtil(ssh_conn)
    cmd = 'ps -ef |grep -v grep |grep "%s"' %(process)
    for i in xrange(0, max_retry) :
        res,r_code = ssh_util.remote_exec(cmd, p_err=False, throw=False)
	if re.search(process, res) :
	    if not cmp("start", mode) :
		log._file.debug("<<< Process \"%s\" Successfully %s !" %(process, mode))
	        return True
	    else :
	        time.sleep(3)
	else :
	    if not cmp("start", mode) :
	        time.sleep(3)
	    else :
		log._file.debug("<<< Process \"%s\" Successfully %s !" %(process, mode))
	        return True
    log._file.error("<<< Process \"%s\" Failed %s !" %(process, mode))
    return False

