#!/usr/sbin/env python

import os, subprocess, re, time
import logging, logging.config
import base64

import re

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


# mode: start or stop
def check_process(command, mode, max_retry=3) :
    logger.debug('>>> Check process "%s" is %s, try %d times' %(command, mode, max_retry))	
    if max_retry < 1 :
        raise Exception("invalid parameter max_retry mush great than 0")
    cmd = 'ps -ef |grep -v grep |grep "%s"' %(command)
    for i in xrange(0, max_retry) :
        logger.debug('Try %d: %s' %(i, cmd))
        proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
        ret = proc.wait()
        info = proc.stdout.read()
        logger.debug('Recv info:\n%s' %(info))
        if re.search(command, info) :
            if not cmp("start", mode) :
                logger.info("<<< Process \"%s\" Successfully %s !" %(command, mode))
                return True
            else :		
                time.sleep(3)
        else :
            if not cmp("start", mode) :
                time.sleep(3)
            else :
                logger.info("<<< Process \"%s\" Successfully %s !" %(command, mode))
                return True
    logger.error("<<< Process \"%s\" Failed %s !" %(command, mode))
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
    logger.debug('Read file %s' %(filename))
    fd = open(filename, 'r')
    context = fd.read()
    fd.close()
    return context


def readfilelines(filename) :
    logger.debug('Read file lines %s' %(filename))
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()
    return lines


def writefile(filename, context) :
    logger.debug('Write file %s' %(filename))
    fd = open(filename, 'w')
    fd.write(context)
    fd.close()

def obfuscate_passwd(command):
    def obfuscate(password):
        length = len(password)
        if length < 2:
            return password+'*'
        else:
            return password[0]+'*'*(length-1)

    def repl(m):
        if m.group(2):
            return "%s=%s" % (m.group(1), obfuscate(m.group(2)))
        return m.group(1)

    keywords = ['password', 'passwd'] # extend it in future, if neccessary.
    return re.sub(r"(%s)=(\S+)" % '|'.join(keywords), repl, command)


def rot13(s,offSet=13):
    rot_dictionary = {}
    for c in (65, 97):
        for i in range(26):
            rot_dictionary[chr(i+c)] = chr((i+offSet) % 26 + c)
    return ''.join([rot_dictionary.get(c, c) for c in s])
def ipworksEncryptPassword(input):
    encoded = base64.b64encode(input)
    return rot13(encoded)
