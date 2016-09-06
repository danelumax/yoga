#!/usr/sbin/env python

import os, subprocess, re, time

import sys
import ConfigParser
import StringIO

import log
#log.Init(True)


# mode: start or stop
def check_process(command, mode, max_retry=3) :
    log._cons.debug('>>> Check process "%s" is %s, try %d times' %(command, mode, max_retry))	
    if max_retry < 1 :
        raise Exception("invalid parameter max_retry mush great than 0")
    cmd = 'ps -ef |grep -v grep |grep "%s"' %(command)
    for i in xrange(0, max_retry) :
        log._cons.debug('Try %d: %s' %(i, cmd))
        proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        ret = proc.wait()
        info = proc.stdout.read()
        log._cons.debug('Recv info:\n%s' %(info))
        if re.search(command, info) :
            if not cmp("start", mode) :
                log._cons.info("<<< Process \"%s\" Successfully %s !" %(command, mode))
                return True
            else :		
                time.sleep(3)
        else :
            if not cmp("start", mode) :
                time.sleep(3)
            else :
                log._cons.info("<<< Process \"%s\" Successfully %s !" %(command, mode))
                return True
    log._cons.error("<<< Process \"%s\" Failed %s !" %(command, mode))
    return False


def replace_context(file_path, replace_pair_list) :
    fd = open(file_path, "r+w")
    context = fd.read()
    for replace_pair in replace_pair_list :
        context = re.sub(replace_pair[0], replace_pair[1], context)
    fd.seek(os.SEEK_SET)
    fd.write(context)
    fd.close()


def readfile(filename) :
    log._cons.debug('Read file %s' %(filename))
    fd = open(filename, 'r')
    context = fd.read()
    fd.close()
    return context


def readfilelines(filename) :
    log._cons.debug('Read file lines %s' %(filename))
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()
    return lines


def writefile(filename, context) :
    log._cons.debug('Write file %s' %(filename))
    fd = open(filename, 'w')
    fd.write(context)
    fd.close()


def Error(msg):
    """Print an error message to stderr and exit."""
    print >>sys.stderr, msg
    log._file.debug(msg)
    #sys.exit(1)

def RunShellWithReturnCode(command, print_output=False,
                            universal_newlines=True, use_shell=False):
    """Executes a command and returns the output from stdout and the return code.

    Args:
        command: Command to execute.
        print_output: If True, the output is printed to stdout.
                      If False, both stdout and stderr are ignored.
        universal_newlines: Use universal_newlines flag (default: True).

      Returns:
        Tuple (output, return code)
    """
    if use_shell:
        log._file.debug("Running %s", command)
    else:
        log._file.debug("Running %s", ' '.join(command))

    env = os.environ
    env['TERM'] = 'xterm'
    if not use_shell:
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
             print_output=False, use_shell=False):
    data, retcode = RunShellWithReturnCode(command, print_output,
                                           universal_newlines, use_shell)
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

def obfuscate(password):
    length = len(password)
    if length < 2:
        return password+'*'
    else:
        return password[0]+'*'*(length-1)
