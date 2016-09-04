/*
 * DiaCommonCode.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef DIACOMMONCODE_H_
#define DIACOMMONCODE_H_

#include <string>
#include <stdint.h>
#include <iostream>

///////////////////////////////Application ID////////////////////////////////////////////
static const uint32_t DIA_APP_ID_STA = 16777250;//application id of STa interface
static const uint32_t DIA_APP_ID_SWX = 16777265;//application id of SWx interface
static const uint32_t DIA_APP_ID_S6B = 16777272;//application id of S6b interface
static const uint32_t DIA_APP_ID_SWM = 16777264;//application id of SWm interface

///////////////////////////////Comand Code////////////////////////////////////////////
//<!-- ************************* [RFC4072] *************************************** -->
static const uint32_t DIA_CMD_CODE_DE = 268;//DER, DEA
//<!-- ************************* [RFC4005] *************************************** -->
static const uint32_t DIA_CMD_CODE_AA = 265;//AAR, AAA
//<!-- ************************* [3GPP 29273] ************************************ -->
static const uint32_t DIA_CMD_CODE_SA = 301;//SAR, SAA
static const uint32_t DIA_CMD_CODE_MA = 303;//MAR, MAA



//Events
static const std::string Event_DER     = "DER";
static const std::string Event_MAA     = "MAA";
static const std::string Event_SAA     = "SAA";
static const std::string Event_AAR     = "AAR";
static const std::string Event_STR     = "STR";

// States
static const std::string State_INIT                  = "INIT";
static const std::string State_Wf_DER                = "wf_DER";
static const std::string State_Wf_MAA                = "wf_MAA";
static const std::string State_Wf_SAA_GetProfile     = "wf_SAA_GetProfile";
static const std::string State_Wf_SAA_Register       = "wf_SAA_Register";
static const std::string State_Wf_SAA_UpdatePdnInfo  = "wf_SAA_UpdatePdnInfo";
static const std::string State_FINAL                 = "FINAL";
#endif /* DIACOMMONCODE_H_ */
