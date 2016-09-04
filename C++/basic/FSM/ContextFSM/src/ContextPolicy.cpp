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

/* Authentication */
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
    /**
     * Authentication FSM transitions: (Event, State) -> Action
     */
	fsm->reset();
	fsm->addContextAction(Event_DER, State_INIT, ContextActionDER::getInstance());
	fsm->addContextAction(Event_DER, State_Wf_DER, ContextActionDER::getInstance());
	fsm->addContextAction(Event_MAA, State_Wf_MAA, ContextActionMAA::getInstance());
	fsm->addContextAction(Event_SAA, State_Wf_SAA_GetProfile, ContextActionSAAGetProfile::getInstance());
	fsm->addContextAction(Event_SAA, State_Wf_SAA_Register, ContextActionSAARegister::getInstance());
}

/* Authorization */
ContextPolicyS6bAuthz* ContextPolicyS6bAuthz::_instance = NULL;
ContextPolicyS6bAuthz* ContextPolicyS6bAuthz::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextPolicyS6bAuthz();
	}

	return _instance;
}

void ContextPolicyS6bAuthz::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void ContextPolicyS6bAuthz::initContextFsm(DiaSessionContextFsm *fsm)
{
	fsm->reset();
	fsm->addContextAction(Event_AAR, State_INIT, ContextActionS6bAAR::getInstance());
	fsm->addContextAction(Event_SAA, State_Wf_SAA_UpdatePdnInfo, ContextActionS6bSAAUpdatePdnInfo::getInstance());
}


