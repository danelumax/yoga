#!/usr/bin/env python

import os, re, sys, subprocess, time, traceback, subprocess
import pexpect
import logging, logging.config
from optparse import OptionParser
from ipwcli import IpworksCli
import util


logging.config.fileConfig("logging.conf")    
logger = logging.getLogger("install")


class ConfigClf() :

    def __init__(self,cli_username,cli_pwd dhcp1_ip='', dhcp2_ip='', address_zone='', clf_sbc_e2_host='', clf_sbc_e2_transport='', sbc_e2_peer_host='', clf_a2_ip='', ipwss_vip='') :
        self.dhcp1_ip = dhcp1_ip
        self.dhcp2_ip = dhcp2_ip
        self.address_zone = address_zone
        self.clf_sbc_e2_host = clf_sbc_e2_host
        self.clf_sbc_e2_transport = clf_sbc_e2_transport
        self.sbc_e2_peer_host = sbc_e2_peer_host
        self.clf_a2_ip = clf_a2_ip
        self.dhcp_conf = '/etc/ipworks/ipworks_dhcpv4.conf'
        self.clf_conf = '/etc/ipworks/clf/clfd.conf'
        self._cli = IpworksCli(cli_username,cli_pwd, logger, server_ip=ipwss_vip)


    def enable_clf_interface(self) :
        logger.debug(">>> Enable CLF Interface")
        tmp = util.readfilelines(self.dhcp_conf)
        fcontext = ""
        for s in tmp:
            if re.search("DHCPV4_CLF_INTERFACE_ENABLE=", s):
                fcontext += "DHCPV4_CLF_INTERFACE_ENABLE=1\n"
            else :
                fcontext += s
        util.writefile(self.dhcp_conf, fcontext)
        logger.debug("<<<")

    def config_clf(self) :
        logger.debug(">>> Config file clfd.conf")
        fc = util.readfile(self.clf_conf)
        tmp1 = ''
        tmp2 = ''
        try :
            # config NACFs
            tag1 = fc.find('<!-- <NACFs')
            logger.debug("NACFs index: %d" %(tag1))
            if -1 != tag1 :
                tag2 = fc.find('</NACFs> -->', tag1)
                tmp1 = fc[0:tag1]
                tag2 += len('</NACFs> -->')
                tmp2 = fc[tag2:]
                nacf_str = self._get_nacf_str()
                fc = tmp1 + nacf_str + tmp2
            # config clf.sbc.e2.transport
            tag1 = fc.find('<clf.sbc.e2.transport')
            logger.debug("clf.sbc.e2.transport index: %d" %(tag1))
            if -1 != tag1 :
                tag2 = fc.find('</clf.sbc.e2.transport>', tag1)
                tmp1 = fc[0:tag1]
                tag2 += len('</clf.sbc.e2.transport>')
                tmp2 = fc[tag2:]
                trans_str = self._get_transport_str()
                fc = tmp1 + trans_str + tmp2
            # config clf.sbc.e2.host
            tag1 = fc.find('<clf.sbc.e2.host')
            logger.debug("clf.sbc.e2.host index: %d" %(tag1))
            if -1 != tag1 :
                tag2 = fc.find('</clf.sbc.e2.host>', tag1)
                tmp1 = fc[0:tag1]
                tag2 += len('</clf.sbc.e2.host>')
                tmp2 = fc[tag2:]
                trans_str = self._get_host_str()
                fc = tmp1 + trans_str + tmp2
            # config clf.sbc.e2.SBCs
            tag1 = fc.find('<clf.sbc.e2>')
            logger.debug("clf.sbc.e2.SBCs index: %d" %(tag1))
            if -1 != tag1 :
                tmp1 = fc[0:tag1]
                tmp2 = fc[tag1:]
                tmp2 = tmp2.replace('<!-- <SBCs type="list">', '<SBCs type="list">')
                tmp2 = tmp2.replace('</SBCs> -->', '</SBCs>')
                tmp2 = tmp2.replace('@sbc.name@', 'sbc1')
                tmp2 = tmp2.replace('@sbc.e2.peer.host@', self.sbc_e2_peer_host)
                fc = tmp1 + tmp2
        except Exception, e :
            logger.error(e)
            traceback.print_exc(file = sys.stderr)
            raise Exception("Error when config CLF")
        if fc :
            util.writefile(self.clf_conf, fc)
        logger.debug("<<<")

    def _get_nacf_str(self) :
        ss  = '<NACFs type="list">\n'
        ss += '            <NACF type="list-item" name="dhcp1">\n'
        ss += '                <nacf.client.ip.address type="ipaddress">' + self.dhcp1_ip + '</nacf.client.ip.address>\n'
        ss += '                <nacf.ip.addressing.zone description="DNS name(max 255 characters)" type="string">' + self.address_zone + '</nacf.ip.addressing.zone>\n'
        ss += '            </NACF>\n'
        ss += '            <NACF type="list-item" name="dhcp2">\n'
        ss += '                <nacf.client.ip.address type="ipaddress">' + self.dhcp2_ip + '</nacf.client.ip.address>\n'
        ss += '                <nacf.ip.addressing.zone description="DNS name(max 255 characters)" type="string">' + self.address_zone + '</nacf.ip.addressing.zone>\n'
        ss += '            </NACF>\n'
        ss += '        </NACFs>'
        return ss

    def _get_transport_str(self) :
        ss = '<clf.sbc.e2.transport description="Diameter transport layer for all E2 peers (SCTP or TCP). Note: this tag is not dynamically configurable." type="string">' + self.clf_sbc_e2_transport + '</clf.sbc.e2.transport>'
        return ss

    def _get_host_str(self) :
        ss = '<clf.sbc.e2.host description = "E2 host identity" type = "string">' + self.clf_sbc_e2_host + '</clf.sbc.e2.host>'
        return ss

    def config_dhcp(self) :
        logger.debug(">>> create dhcpv4 server in failover mode")
        self._cli.login()
        cmd = 'create dhcpv4server dhcp1 -set address=%s -set V4Option="clf-address %s"' %(self.dhcp1_ip, self.clf_a2_ip)
        self._cli.execute(cmd)
        cmd = 'create dhcpv4server dhcp2 -set address=%s;primary=dhcp1' %(self.dhcp2_ip)
        self._cli.execute(cmd)
        cmd = 'create subnet subnet1 -set address=80.0.0.0 -set Masklength=8 -set server=dhcp1 -set V4Option="network-type "atm""'
        self._cli.execute(cmd)
        cmd = 'create pool pool1 -set addressrange=80.0.0.1-80.0.0.10 -set server=dhcp1 -set subnet=subnet1 -set v4option="clf-address-zone %s"' %(self.address_zone)
        self._cli.execute(cmd)
        cmd = 'create dhcpv4option82format juniper_erx -set category=0 -set suboptionid=1 -set informat="^(.*): ATM ([0-9]{1,2})/([0-9]{1,2}).?[0-9]*:([0-9]{1,3}).([0-9]{1,5})$" -set outformat="$1#$2#$3#$4#$5"'
        self._cli.execute(cmd)
        cmd = 'create dhcpv4option82iprange iprange1 -set address=80.0.0.0 -set masklength=8 -set server=dhcp1 -set option82format=juniper_erx'
        self._cli.execute(cmd)
        self._cli.logout()
        logger.debug("<<<")

    def clean_dhcp(self) :
        logger.debug(">>> clean dhcpv4 server in failover mode")
        self._cli.login()
        cmd = 'delete dhcpv4option82iprange'
        self._cli.execute(cmd)
        cmd = 'delete dhcpv4option82format'
        self._cli.execute(cmd)
        cmd = 'delete pool'
        self._cli.execute(cmd)
        cmd = 'delete subnet'
        self._cli.execute(cmd)
        cmd = 'delete dhcpv4server'
        self._cli.execute(cmd)
        self._cli.logout()
        logger.debug("<<<")




def main() :
    parser = OptionParser()
    parser.add_option("--command",
        help="config_clf, enable_clf_int, config_dhcp",
        action="store",
        dest="command",
        default=None)
    parser.add_option("--dhcp1_ip",
        help="dhcp1 traffic ip",
        action="store",
        dest="dhcp1_ip",
        default=None)
    parser.add_option("--dhcp2_ip",
        help="dhcp2 traffic ip",
        action="store",
        dest="dhcp2_ip",
        default=None)
    parser.add_option("--address_zone",
        help="nacf ip addressing zone",
        action="store",
        dest="address_zone",
        default=None)
    parser.add_option("--clf_sbc_e2_host",
        help="clf sbc e2 host",
        action="store",
        dest="clf_sbc_e2_host",
        default=None)
    parser.add_option("--clf_sbc_e2_transport",
        help="clf sbc e2 transport",
        action="store",
        dest="clf_sbc_e2_transport",
        default=None)
    parser.add_option("--sbc_e2_peer_host",
        help="sbc e2 peer host",
        action="store",
        dest="sbc_e2_peer_host",
        default=None)
    parser.add_option("--clf_a2_ip",
        help="clf a2 traffic ip",
        action="store",
        dest="clf_a2_ip",
        default=None)
    parser.add_option("--ipwss_vip",
        help="Storage Server vip",
        action="store",
        dest="ipwss_vip",
        default=None)
    parser.add_option("--password",
        help="ipwcli password",
        action="store",
        dest="password",
        default=None)
    parser.add_option("--username",
        help="ipwcli username",
        action="store",
        dest="username",
        default=None)


    (options, args) = parser.parse_args(args=sys.argv)
    logger.info("options.command: " + str(options.command))
    logger.info("options.dhcp1_ip: " + str(options.dhcp1_ip))
    logger.info("options.dhcp2_ip: " + str(options.dhcp2_ip))
    logger.info("options.address_zone: " + str(options.address_zone))
    logger.info("options.clf_sbc_e2_host: " + str(options.clf_sbc_e2_host))
    logger.info("options.clf_sbc_e2_transport: " + str(options.clf_sbc_e2_transport))
    logger.info("options.sbc_e2_peer_host: " + str(options.sbc_e2_peer_host))
    logger.info("options.clf_a2_ip: " + str(options.clf_a2_ip))
    logger.info("options.ipwss_vip: " + str(options.ipwss_vip))
    
    logger.debug(">> Remote Call Start")
    task = ConfigClf(options.username, options.password, options.dhcp1_ip, options.dhcp2_ip, options.address_zone, options.clf_sbc_e2_host, options.clf_sbc_e2_transport, options.sbc_e2_peer_host, options.clf_a2_ip, options.ipwss_vip)
    if options.command == "enable_clf_int" :
        task.enable_clf_interface()
    elif options.command == "config_clf" :
        task.config_clf()
    elif options.command == "config_dhcp" :
        task.config_dhcp()
    elif options.command == "clean_dhcp" :
        task.clean_dhcp()
    else :
        raise Exception("Unknown command: " + options.command)
    logger.debug("<< Remote Call End")
    return 0
 


if __name__ == '__main__' :
    try :
        sys.exit(main())
    except Exception, e :
        logger.error(e)
        traceback.print_exc(file = sys.stderr)
        print str(e)
        sys.exit(2)






