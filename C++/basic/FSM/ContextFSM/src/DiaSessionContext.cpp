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

void DiaSessionContext::process()
{
	ContextPolicy* ctxPolicy = ContextPolicyFactory::getInstance()->getContextPolicy(DIA_APP_ID_SWM, DIA_CMD_CODE_DE);
	ctxPolicy->initContextFsm(_fsm);
	_fsm->process(Event_DER, this);
}

void DiaSessionContext::setFSMNextState(std::string nextState)
{
	_fsm->setNextState(nextState);
}




