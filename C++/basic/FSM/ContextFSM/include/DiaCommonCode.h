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

///////////////////////////////Application ID////////////////////////////////////////////
static const uint32_t DIA_APP_ID_SWM = 16777264;//application id of SWm interface

///////////////////////////////Comand Code////////////////////////////////////////////
static const uint32_t DIA_CMD_CODE_DE = 268;//DER, DEA



//Events
static const std::string Event_DER     = "DER";

// States
static const std::string State_INIT                  = "INIT";
static const std::string State_Wf_DER                = "wf_DER";
#endif /* DIACOMMONCODE_H_ */
