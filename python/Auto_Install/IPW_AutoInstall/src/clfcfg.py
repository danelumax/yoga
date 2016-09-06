import log, common

class ClfCfg :
    """
    Class ClfCfg
    """

    def __init__(self) :
        self.nacf_ip_addressing_zone = ''
        self.clf_sbc_e2_host = ''
        self.clf_sbc_e2_transport = ''
        self.sbc_e2_peer_host = ''
        self.is_install_em = False

    def setCommon(self, json_node) :
        self.nacf_ip_addressing_zone = json_node["nacf_ip_addressing_zone"]
        self.clf_sbc_e2_host = json_node["clf_sbc_e2_host"]
        self.clf_sbc_e2_transport = json_node["clf_sbc_e2_transport"].upper()
        self.sbc_e2_peer_host = json_node["sbc_e2_peer_host"]
        is_install = json_node["install_clf_em"]
        if not cmp("yes", is_install) :
            self.is_install_em = True

    def validateCfg(self) :
        is_ok = True
        if not self.nacf_ip_addressing_zone :
            log._file.error("nacf_ip_addressing_zone can't be empty in Medium2 Mode")
            is_ok = False
        if not self.clf_sbc_e2_host :
            log._file.error("clf_sbc_e2_host can't be empty in Medium2 Mode")
            is_ok = False
        if not self.clf_sbc_e2_transport :
            log._file.error("clf_sbc_e2_transport can't be empty in Medium2 Mode")
            is_ok = False
        else :
            if 'TCP' != self.clf_sbc_e2_transport and 'SCTP' != self.clf_sbc_e2_transport :
                log._file.error("clf_sbc_e2_transport only support TCP and SCTP")
                is_ok = False
        if not self.sbc_e2_peer_host :
            log._file.error("sbc_e2_peer_host can't be empty in Medium2 Mode")
            is_ok = False
        return is_ok


    def getNacfZone(self) :
        return self.nacf_ip_addressing_zone

    def getClfHost(self) :
        return self.clf_sbc_e2_host

    def getClfTransport(self) :
        return self.clf_sbc_e2_transport

    def getSbcHost(self) :
        return self.sbc_e2_peer_host

    def isInstallEM(self) :
        return self.is_install_em


