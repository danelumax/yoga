/*
 * DiaSessionContext.cpp
 *
 *  Created on: Sep 2, 2016
 *      Author: eliwech
 */

#include "DiaSessionContext.h"
#include "ContextPolicyFactory.h"
#include "ContextPolicy.h"
#include "DiaCommonCode.h"

DiaSessionContext::DiaSessionContext()
{
	_fsm = new DiaSessionContextFsm(State_INIT);
}

DiaSessionContext::~DiaSessionContext()
{
}

std::string DiaSessionContext::getEvent(Message* msg)
{
	std::string event;
	uint32_t code = msg->getCode();
	if (code == DIA_CMD_CODE_DE)
	{
		event = Event_DER;
	}
	else if (code == DIA_CMD_CODE_MA)
	{
		event = Event_MAA;
	}
	else if (code == DIA_CMD_CODE_SA)
	{
		event = Event_SAA;
	}
	else if (code == DIA_CMD_CODE_AA)
	{
		event = Event_AAR;
	}

	return event;
}
void DiaSessionContext::process(Message* msg)
{
	std::string event = getEvent(msg);

	if (_fsm->isInitState())
	{
		ContextPolicy* ctxPolicy = ContextPolicyFactory::getInstance()->getContextPolicy(msg->getAppId(), msg->getCode());
		if (NULL != ctxPolicy)
		{
			ctxPolicy->initContextFsm(_fsm);
		}
	}
	_fsm->process(event, this);
}

void DiaSessionContext::setFSMNextState(std::string nextState)
{
	_fsm->setNextState(nextState);
}

std::string DiaSessionContext::getCurrentState()
{
	return _fsm->getCurrentState();
}




