//============================================================================
// Name        : EapFSM.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <EapFSM.h>
#include <StateEventDefine.h>
#include <DiaSessionContext.h>

int main()
{
	EapFSM* fsm = EapFSM::getInstance();
	DiaSessionContext *context = new DiaSessionContext();
	context->setState(STATE_IDLE);
	std::cout << context->getState() << std::endl;

	fsm->handleEvent(EVENT_NO_AUTH_VECTOR, context);
	std::cout << context->getState() << std::endl;

	fsm->handleEvent(EVENT_NO_PROFILE, context);
	std::cout << context->getState() << std::endl;

	fsm->handleEvent(EVENT_GENERATE_KEY, context);
	std::cout << context->getState() << std::endl;

	fsm->handleEvent(EVENT_AUTH_SUCCESS, context);
	std::cout << context->getState() << std::endl;

	fsm->handleEvent(EVENT_AUTH_SUCCESS, context);
	std::cout << context->getState() << std::endl;
	return 0;
}
