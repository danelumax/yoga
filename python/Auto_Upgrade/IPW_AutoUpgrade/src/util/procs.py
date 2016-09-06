'''
Created on 2015/04/21

@author: eyotang
'''

import os
import json, uuid, copy

import log

class NoIndent(object):
    def __init__(self, value):
        self.value = value


class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result


def ReadRunningProcs(snapshot=None):
    json_root = None
    if snapshot:
        proc_file = snapshot
    else:
        proc_file = g_running_sevice_proc_file
    if not os.path.exists(proc_file):
        log._file.error("File '" + proc_file + "' doesn't exist!")
        raise Exception("File '" + proc_file + "' doesn't exist!")
    procfd = open(proc_file, 'r')
    content = procfd.read()
    procfd.close()

    RunningProcList = []
    if content:
        json_root = json.loads(content)
        RunningProcList = json_root["Procs"]
    return RunningProcList

def WriteRunningProcs(RunningProcList, snapshot=None):
    msg = "{\n"
    msg += '"Procs" : [\n'
    encodejson = []
    for proc in RunningProcList:
        proc_dict = copy.deepcopy(proc)
        for i in proc_dict:
            if type(proc_dict[i]) is list:
                proc_dict[i] = NoIndent(proc_dict[i])

        # encode process dictionary as NoIndentEncoder in seconder level
        encodejson.append(json.dumps(proc_dict, sort_keys=True, indent=4, cls=NoIndentEncoder))
    msg += ",\n".join(encodejson)

    msg += "\n]\n"
    msg += "}\n"
    if snapshot:
        proc_file = snapshot
    else:
        proc_file = g_running_sevice_proc_file
    procfd = open(proc_file, 'w')
    procfd.write(msg)
    procfd.close()

def GetRunningProcsFileName():
    return g_running_sevice_proc_file

g_running_sevice_proc_file = "running_service_proc.tmp"

IPWSMCTL    = "/opt/ipworks/IPWsm/scripts/ipwsmctl"
IPWSM       = "/opt/ipworks/IPWsm/scripts/ipwsm"
ServerType  = "ServerType="
ShutDown    = "Shutdown=yes"

DAPP        = "DApp="

PSCHECK     = "ps -ef | grep -v grep | grep"
PPSCHECK    = "ps -ef | awk '{ print $8 }' | awk -F/ '{ if ($NF == \"%s\") print $NF }'"

IPWCLI      = "ipwcli"


'''
Item names in process dictionary
'''
name   = "name"
check  = "ncheck"
start  = "start"
stop   = "stop"
status = "vstatus"

SM       = "SM"
ENUM     = "ENUM"
ASDNSMON = "ASDNSMON"
DNS      = "DNS"

AAA_RADIUS   = "AAA Radius"
AAA_PLUGIN   = "AAA Plugin"
AAA_CORE     = "AAA Core"
AAA_DIAMETER = "AAA Diameter"

ASDNSMON_SM = " ".join([ASDNSMON, SM])
DNS_SM      = " ".join([DNS, SM])
ENUM_SM     = " ".join([ENUM, SM])
AAA_SM      = "AAA SM"

DHCP        = "DHCP"
DHCP_SM     = " ".join([DHCP, SM])

SNMPD = "SNMPD"
SNMP_DNS = "SNMP DNS"
SNMP_DHCP = "SNMP DHCP"
SNMP_ENUM = "SNMP ENUM"
SNMP_EM = "SNMP EM"
SNMP_COMMON = "SNMP COMMON"
SNMP_ERH = "SNMP ERH"
SNMP_AAA = "SNMP AAA"
SNMPX = "SNMPX"
SNMPXBOSS = "SNMPXBOSS"
SNMP_HA = "SNMP HA"
SNMP_TRAPD = "SNMP TRAPD"
CNOSS = "CNOSS"
CSV_ENGINE = "CSV ENGINE"


'''
The sequence in PROCS has the relationship, please consider it carefully!!!
'''
PROCS = [
    {
        name   : ENUM,
        check  : [PPSCHECK, "ipwenum"],
        start  : [IPWCLI, "start enumserver"],
        stop   : "/etc/init.d/ipworks.enum stop",
        status : []
    },
    {
        name   : ENUM_SM,
        check  : [PSCHECK, DAPP+"ipwenumserversm"],
        start  : " ".join([IPWSM, ServerType+"ENUMSERVER", "&"]),
        stop   : " ".join([IPWSMCTL, ServerType+"ENUMSERVER", ShutDown]),
        status : []
    },
    {
        name   : ASDNSMON,
        check  : [PPSCHECK, "asdnsmon"],
        start  : [IPWCLI, "update monitor"],
        stop   : "/etc/init.d/ipworks.asdnsmon stop",
        status : []
    },
    {
        name   : ASDNSMON_SM,
        check  : [PSCHECK, DAPP+"ipwasdnsmonsm"],
        start  : " ".join([IPWSM, ServerType+"ASDNSMON", "&"]),
        stop   : " ".join([IPWSMCTL, ServerType+"ASDNSMON", ShutDown]),
        status : []
    },
    {
        name   : DNS,
        check  : [PPSCHECK, "named"],
        start  : [IPWCLI, "update dnsserver"],
        stop   : "/etc/init.d/ipworks.dns stop",
        status : []
    },
    {
        name   : DNS_SM,
        check  : [PSCHECK, DAPP+"ipwdnssm"],
        start  : " ".join([IPWSM, ServerType+"DNS", "&"]),
        stop   : " ".join([IPWSMCTL, ServerType+"DNS", ShutDown]),
        status : []
    },
    {
        name   : AAA_RADIUS,
        check  : [PPSCHECK, "a3radiusd"],
        start  : "/etc/init.d/ipworks.aaa_radius_stack start",
        stop   : "/etc/init.d/ipworks.aaa_radius_stack stop",
        status : []
    },
    {
        name   : AAA_PLUGIN,
        check  : [PPSCHECK, "a3backend"],
        start  : "/etc/init.d/ipworks.aaa_plugins start",
        stop   : "/etc/init.d/ipworks.aaa_plugins stop",
        status : []
    },
    {
        name   : AAA_DIAMETER,
        check  : [PPSCHECK, "ipwa3d"],
        start  : "/etc/init.d/ipworks.aaa start",
        stop   : "/etc/init.d/ipworks.aaa stop",
        status : []
    },
    {
        name   : AAA_CORE,
        check  : [PPSCHECK, "a3cored"],
        start  : [IPWCLI, "update aaaserver"],
        stop   : "/etc/init.d/ipworks.aaa_core_server stop",
        status : []
    },
    {
        name   : AAA_SM,
        check  : [PSCHECK, DAPP+"ipwaaasm"],
        start  : " ".join([IPWSM, ServerType+"AAA", "&"]),
        stop   : " ".join([IPWSMCTL, ServerType+"AAA", ShutDown]),
        status : []
    },
    {
        name   : DHCP,
        check  : [PPSCHECK, "dhcpd"],
        start  : "/etc/init.d/ipworks.dhcpv4 start",
        stop   : "/etc/init.d/ipworks.dhcpv4 stop",
        status : []
    },
    {
        name   : DHCP_SM,
        check  : [PSCHECK, DAPP+"ipwdhcpv4sm"],
        start  : " ".join([IPWSM, ServerType+"DHCPV4", "&"]),
        stop   : " ".join([IPWSMCTL, ServerType+"DHCPV4", ShutDown]),
        status : []
    }
]

ASSISTANTPROCS = [
    {
        name   : SNMPD,
        check  : [PSCHECK, "/usr/bin/snmpd"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_DNS,
        check  : [PSCHECK, "/usr/bin/ipwdns-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_DHCP,
        check  : [PSCHECK, "/usr/bin/ipwdhcpv4-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_ENUM,
        check  : [PSCHECK, "/usr/bin/ipwenum-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_EM,
        check  : [PSCHECK, "/usr/bin/ipwem-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_COMMON,
        check  : [PSCHECK, "/usr/bin/ipwcommon-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_ERH,
        check  : [PSCHECK, "/usr/bin/ipwerh-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_AAA,
        check  : [PSCHECK, "/usr/bin/ipwaaa-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMPX,
        check  : [PSCHECK, "/usr/bin/ipwxsnmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMPXBOSS,
        check  : [PSCHECK, "/usr/bin/ipwxboss-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_HA,
        check  : [PSCHECK, "/usr/bin/ipwha-snmp"],
        start  : "/etc/init.d/ipworks.snmpd_noreset start",
        stop   : "/etc/init.d/ipworks.snmpd stop",
        status : []
    },
    {
        name   : SNMP_TRAPD,
        check  : [PSCHECK, "/usr/bin/snmptrapd"],
        start  : "/etc/init.d/ipworks.snmptrapd start",
        stop   : "/etc/init.d/ipworks.snmptrapd stop",
        status : []
    },
    {
        name   : CNOSS,
        check  : [PSCHECK, DAPP+"ipwcnoss"],
        start  : "/etc/init.d/ipworks.cnoss start",
        stop   : "/etc/init.d/ipworks.cnoss stop",
        status : []
    },
    {
        name   : CSV_ENGINE,
        check  : [PSCHECK, "/usr/bin/a3csvdemon"],
        start  : "/etc/init.d/ipworks.aaa_csv_engine start",
        stop   : "/etc/init.d/ipworks.aaa_csv_engine stop",
        status : []
    }
]


def GetServiceDict(service_type):
    assert service_type in ['ENUM', 'DNS', 'AAA', 'DHCP', 'CLF']

    ServiceDict = {
        'ENUM' : [ENUM, ENUM_SM, ASDNSMON, ASDNSMON_SM, DNS, DNS_SM],
        'DNS'  : [ASDNSMON, ASDNSMON_SM, DNS, DNS_SM],
        'AAA'  : [AAA_RADIUS, AAA_PLUGIN, AAA_CORE, AAA_DIAMETER, AAA_SM],
        'DHCP' : [DHCP, DHCP_SM],
        'CLF'  : [DHCP, DHCP_SM]
    }

    return ServiceDict[service_type]

def GetService(service_list):
    proc_name_list = []
    for service in service_list:
        proc_name_list += GetServiceDict(service)

    return proc_name_list


def IsServerManager(proc_name):
    SM_List = [ENUM_SM, ASDNSMON_SM, DNS_SM, AAA_SM, DHCP_SM]
    if proc_name in SM_List:
        return True
    else:
        return False


def SMProcsMap(proc_name):
    if not IsServerManager(proc_name):
        return []
    else:
        SMProcsDict = {
            ENUM_SM     : [ENUM],
            ASDNSMON_SM : [ASDNSMON],
            DNS_SM      : [DNS],
            AAA_SM      : [AAA_RADIUS, AAA_PLUGIN, AAA_CORE, AAA_DIAMETER],
            DHCP_SM     : [DHCP]
        }
        return SMProcsDict[proc_name]


def GetChecker(check):
    assert type(check) is list

    method = check[0]
    name   = check[1]
    if method == PPSCHECK:
        return method %(name)
    else:
        return ' '.join(check)
