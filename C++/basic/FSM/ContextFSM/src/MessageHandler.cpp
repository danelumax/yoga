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

void DERMessageHandler::execute(DiaSessionContext* context)
{
	std::cout << "DER message handle finish" << std::endl;
	context->setFSMNextState(State_Wf_MAA);
}


