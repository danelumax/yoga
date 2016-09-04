/*
 * MessageHandler.cpp
 *
 *  Created on: Sep 2, 2016
 *      Author: eliwech
 */

#include "MessageHandler.h"
#include <DiaCommonCode.h>

MessageHandler::MessageHandler() {
	// TODO Auto-generated constructor stub

}

MessageHandler::~MessageHandler() {
	// TODO Auto-generated destructor stub
}

/* DER */
void DERMessageHandler::execute(DiaSessionContext* context)
{
	if (context->getCurrentState() == State_INIT)
	{
		std::cout << "* DER message handle finish *" << std::endl;
		context->setFSMNextState(State_Wf_MAA);
	}
	else if (context->getCurrentState() == State_Wf_DER)
	{
		std::cout << "* DER Challenge message handle finish *" << std::endl;
		context->setFSMNextState(State_Wf_SAA_Register);
	}
}

/* MAA */
void SWxMAAMessageHandler::execute(DiaSessionContext* context)
{
	std::cout << "* MAA message handle finish *" << std::endl;
	context->setFSMNextState(State_Wf_SAA_GetProfile);
}

/* SAA */
void SWxSAAMessageHandler::execute(DiaSessionContext* context)
{
	if (context->getCurrentState() == State_Wf_SAA_GetProfile)
	{
		std::cout << "* SAA Get Profile message handle finish *" << std::endl;
		context->setFSMNextState(State_Wf_DER);
	}
	else if (context->getCurrentState() == State_Wf_SAA_Register)
	{
		std::cout << "* SAA Register message handle finish *" << std::endl;
		context->setFSMNextState(State_FINAL);
	}
	else if (context->getCurrentState() == State_Wf_SAA_UpdatePdnInfo)
	{
		std::cout << "* SAA Update Pdn Info message handle finish *" << std::endl;
		context->setFSMNextState(State_FINAL);
	}
}

/* AAR */
void S6bAARMessageHandler::execute(DiaSessionContext* context)
{
	std::cout << "* AAR message handle finish *" << std::endl;
	context->setFSMNextState(State_Wf_SAA_UpdatePdnInfo);
}


