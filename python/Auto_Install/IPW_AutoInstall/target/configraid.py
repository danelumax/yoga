#!/usr/bin/env python
import subprocess, sys, re, os, time
import logging, logging.config
import util
from optparse import OptionParser

logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")



class ConfigRaid:

    def __init__(self) :
        pass


    def createPartition(self, device_path, md0_size, sbd_size) :
        logger.debug(">> device_path = " + device_path)
        device = self._parseDeviceList(device_path)[0]
        size_kb = self._getDiskSize(device)
        size_gb = size_kb / 1024 / 1024
        logger.info("EMC disk " + device + " size: " + str(size_gb) + "G")
        logger.info("md0 size: " + str(md0_size) + "G, stonish size: " + str(sbd_size) + "M")
        if size_gb < (md0_size+1) :
            raise Exception("The size of EMC Raid is too small: %d G, it must be larger than md0 + stonish" % size_gb)
        
        # 1 sector = 512 bytes = 0.5 KB
        size_sector = md0_size * 1024 * 1024 * 2
        s1 = 2048 + size_sector
        logger.debug("size_sector = " + str(size_sector))
        context = util.readfile("disk.sectors.tmp")
        context = context.replace("###DEVICE_PATH###", device)
        context = context.replace("###SIZE0###", str(size_sector))
        context = context.replace("###SIZE1###", str(s1))
        logger.debug("\n%s" %context)
        
        logger.info("sfdisk --force " + device)
        proc = subprocess.Popen(["sfdisk", "--force", device], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(context)
        proc.stdin.flush()
        proc.communicate()
        proc.wait()
        time.sleep(3)
        # wait until the disk file is created
        proc = subprocess.Popen(["ls", device + "2"])
        ret = proc.wait()
        logger.info("return code %d" %ret)
        while ret != 0 :
            time.sleep(1)
            proc = subprocess.Popen(["ls", device + "2"])
            ret = proc.wait()
            logger.info("return code %d" %ret)
        
        logger.info("partprobe")
        # make kernal to reload disk patition
        proc = subprocess.Popen(["partprobe"])
        proc.wait()
        
        #TODO: check the result
#        proc = subprocess.Popen(["sfdisk", "-l", device_path])
#        proc.wait()
        logger.debug("<<")



    def removePartition(self, disk) :
        logger.debug(">> remove partition on " + disk)
        content = util.readfile("disk.sectors.empty")
        content = content.replace("###DEVICE_PATH###", disk)
        logger.debug("\n%s" %content)
        proc = subprocess.Popen(["sfdisk", "--force", disk], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(content)
        proc.stdin.flush()
        proc.communicate()
        proc.wait()
        time.sleep(3)
        proc = subprocess.Popen(["fdisk", "-l", disk])
        proc.wait()
        logger.info("partprobe")
        # make kernal to reload disk patition
        proc = subprocess.Popen(["partprobe"])
        proc.wait()
        logger.debug("<<")



    def createRaid(self, device_path_list) :
        logger.debug(">> device_path_list = " + device_path_list)
        disk_list = self._parseDeviceList(device_path_list)
        command = "mdadm" +  " --create" + " /dev/md0" + " --run" + " --chunk=4"  + " --level=1" + " --raid-devices=2 "  + disk_list[0] + "1 " + disk_list[1] + "1"
        logger.debug(command)    
        #proc = subprocess.Popen(["ls", "/dev/"])
        #proc.wait()
        proc = subprocess.Popen(["mdadm", "--create", "/dev/md0", "--run", "--chunk=4", "--level=1", "--raid-devices=2", disk_list[0] + "1", disk_list[1] + "1"])
        proc.wait()
        #mdadm --readwrite /dev/md0
        proc = subprocess.Popen(["mdadm", "--manage", "/dev/md0", "--readwrite"])
        proc.wait()
        #proc = subprocess.Popen(["rcmdadmd", "start"])
        #proc.wait()
        #proc = subprocess.Popen(["chkconfig", "-s", "mdadmd", "on"])
        #proc.wait()
        #proc = subprocess.Popen(["/etc/init.d/boot.md", "start"])
        #proc.wait()
        proc = subprocess.Popen(["chkconfig", "-s", "boot.md", "on"])
        proc.wait()
        logger.debug("<<")
        #TODO: check the result
        return 0



    def waitPeerReboot(self, peer_ip) :
        ret = 0
        while ret == 0 :
            logger.debug("check if %s is down" %peer_ip)
            proc = subprocess.Popen(["ping", "-c", "1", peer_ip], stdout=subprocess.PIPE)
            ret = proc.wait()
            time.sleep(5)
        while ret != 0 :
            logger.debug("remote %s can't reachable" %peer_ip)
            proc = subprocess.Popen(["ping", "-c", "1", peer_ip], stdout=subprocess.PIPE)
            ret = proc.wait()
            time.sleep(10)
        time.sleep(10)
        logger.debug("remote %s is up" %peer_ip)

 


    def _getDiskSize(self, device_path) :
        proc = subprocess.Popen(["sfdisk", "-s", device_path], stdout=subprocess.PIPE)
        proc.wait()
        size = proc.stdout.readline()
        return int(size)


    def _parseDeviceList(self, string_device_path) :
        return string_device_path.split(',')



def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="create_partition.",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--device_path",
        help="the path to the disk device.",
        action="store",
        dest="device_path",
        default=None)
    parser.add_option("--peer_ip",
        help="the IP address of the HA peer.",
        action="store",
        dest="peer_ip",
        default=None)
    parser.add_option("--md0_size",
        help="the /dev/md0 size Gbytes.",
        action="store",
        dest="md0_size",
        default=None)
    parser.add_option("--sbd_size",
        help="the stonish block device size Mbytes.",
        action="store",
        dest="sbd_size",
        default=None)


    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.device_path: " + str(options.device_path))
    logger.info("options.peer_ip: " + str(options.peer_ip))
    logger.info("options.md0_size: " + str(options.md0_size))
    logger.info("options.sbd_size: " + str(options.sbd_size))
    
    logger.debug(">> Remote Call Start")
    task = ConfigRaid()
    if options.command == "create_partition" :
        task.createPartition(options.device_path, int(options.md0_size), int(options.sbd_size))
    elif options.command == 'remove_partition' :
        task.removePartition(options.device_path)
    elif options.command == 'create_raid' :
        task.createRaid(options.device_path)
    elif options.command == 'wait_peer_reboot' :
        task.waitPeerReboot(options.peer_ip)
    logger.debug("<< Remote Call End")
    return 0
 
 

if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        print str(e)
        sys.exit(2)

