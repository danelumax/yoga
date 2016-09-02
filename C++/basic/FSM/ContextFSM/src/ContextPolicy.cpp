/*
 * ContextPolicy.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include <DiaCommonCode.h>
#include <ContextPolicy.h>
#include <ContextAction.h>

ContextPolicy::ContextPolicy()
{
}

ContextPolicy::~ContextPolicy()
{
}

ContextPolicyAuth* ContextPolicyAuth::_instance = NULL;
ContextPolicyAuth* ContextPolicyAuth::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextPolicyAuth();
	}

	return _instance;
}

void ContextPolicyAuth::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void ContextPolicyAuth::initContextFsm(DiaSessionContextFsm *fsm)
{
	fsm->reset();
	fsm->addContextAction(Event_DER, State_INIT, ContextActionDER::getInstance());
}


