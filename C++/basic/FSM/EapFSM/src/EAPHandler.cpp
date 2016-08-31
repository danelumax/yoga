/*
 * EAPHandler.cpp
 *
 *  Created on: Aug 31, 2016
 *      Author: eliwech
 */

#include "EAPHandler.h"
#include <StateEventDefine.h>
#include <DiaSessionContext.h>

EAPHandler::EAPHandler(DiaSessionContext* context)
	:_context(context)
{
	_fsm = EapFSM::getInstance();
}

EAPHandler::~EAPHandler()
{
	EapFSM::destory();
}

void EAPHandler::Authentication()
{
	std::cout << "\n***** Start Authentication *****" << std::endl;
	_context->setState(STATE_IDLE);

	std::cout << "\n-----> Receive DER-Identity ----->" << std::endl;
	_fsm->handleEvent(EVENT_NO_AUTH_VECTOR, _context);

	std::cout << "\n-----> Receive MAA-Vector ----->" << std::endl;
	_fsm->handleEvent(EVENT_NO_PROFILE, _context);

	std::cout << "\n-----> Receive SAA-Profile ----->" << std::endl;
	_fsm->handleEvent(EVENT_GENERATE_KEY, _context);

	std::cout << "\n-----> Receive DER-Challenge ----->" << std::endl;
	_fsm->handleEvent(EVENT_AUTH_SUCCESS, _context);

	std::cout << "\n-----> Receive SAA-Registeration ----->" << std::endl;
	_fsm->handleEvent(EVENT_AUTH_SUCCESS, _context);
}

void EAPHandler::Authorization()
{
	std::cout << "\n***** Start Authorization *****" << std::endl;

	std::cout << "\n-----> Receive DER-Identity ----->" << std::endl;
	_fsm->handleEvent(EVENT_LOAD_REAUTH_INFO, _context);

	std::cout << "\n-----> Receive DER-Reauthenticaion ----->" << std::endl;
	_fsm->handleEvent(EVENT_AUTH_SUCCESS, _context);
}




