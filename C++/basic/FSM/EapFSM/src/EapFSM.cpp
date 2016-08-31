/*
 * EapFSM.cpp
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#include "EapFSM.h"
#include "EPCAction.h"

EapFSM* EapFSM::_instance = NULL;

EapFSM::EapFSM()
{
	_stateTable = new StateTable();
	init();
}

EapFSM::~EapFSM()
{
	delete _stateTable;
}

EapFSM *EapFSM::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new EapFSM();
	}

	return _instance;
}

void EapFSM::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void EapFSM::init()
{
	StateEntry* pEntry = NULL;
	/* IDLE --> WAIT_FOR_AUTH_VECTOR :: no authentication vector */
	pEntry = new StateEntry(STATE_IDLE,
							STATE_WAIT_FOR_AUTH_VECTOR,
							EVENT_NO_AUTH_VECTOR,
							new EPCActionRequestAuthVector());
	_stateTable->addStateTableEntry(pEntry);

	/* WAIT_FOR_AUTH_VECTOR --> WAIT_FOR_PROFILE :: fetched authentication vector from HSS but no user profile */
	pEntry = new StateEntry(STATE_WAIT_FOR_AUTH_VECTOR,
							STATE_WAIT_FOR_PROFILE,
							EVENT_NO_PROFILE,
							new EPCActionRequestProfile());
	_stateTable->addStateTableEntry(pEntry);

	/* WAIT_FOR_PROFILE --> AFTER_CHALLENGE_SEND :: fetching user profile from HSS succeed */
	pEntry = new StateEntry(STATE_WAIT_FOR_PROFILE,
							STATE_AFTER_CHALLENGE_SEND,
							EVENT_GENERATE_KEY,
							new EPCActionSendChallenge());
	_stateTable->addStateTableEntry(pEntry);

	/* AFTER_CHALLENGE_SEND --> SUCCESS_END :: Receive the correct CHANLLENGE and Authorization success */
	pEntry = new StateEntry(STATE_AFTER_CHALLENGE_SEND,
							STATE_SUCCESS_END,
							EVENT_AUTH_SUCCESS,
							new EPCActionSendSuccess());
	_stateTable->addStateTableEntry(pEntry);

	/* IDLE --> SUCCESS_END :: Receive the REGISTRATION */
	pEntry = new StateEntry(STATE_IDLE,
	                        STATE_SUCCESS_END,
	                        EVENT_AUTH_SUCCESS,
	                        new EPCActionSendSuccess());
	_stateTable->addStateTableEntry(pEntry);

	/* IDLE --> AFTER_REAUTHENTICATION_SEND :: received correct fast-reauth-id and load related info success. */
	pEntry = new StateEntry(STATE_IDLE,
							STATE_AFTER_REAUTHENTICATION_SEND,
	                        EVENT_LOAD_REAUTH_INFO,
	                        new EPCActionSendReauthentication());
	_stateTable->addStateTableEntry(pEntry);

	/* AFTER_REAUTHENTICATION_SEND --> SUCCESS_END :: Receive the correct reauthentication response and Authorization success */
	pEntry = new StateEntry(STATE_AFTER_REAUTHENTICATION_SEND,
							STATE_SUCCESS_END,
							EVENT_AUTH_SUCCESS,
	                        new EPCActionSendSuccess());
	_stateTable->addStateTableEntry(pEntry);
}

StateEntry *EapFSM::matchState(EPCState state, EPCEvent event)
{
	return _stateTable->findStateTableEntry(state, event);
}

void EapFSM::handleEvent(EPCEvent event, DiaSessionContext *context)
{
	EPCState currentState = context->getState();
	StateEntry* pMatchEntry = matchState(currentState, event);
	EPCState nextState = pMatchEntry->getNextState();
	context->setState(nextState);

	std::cout << "Current State: " << stateMap[pMatchEntry->getCurrentState()] << std::endl;
	std::cout << "Next State: " << stateMap[pMatchEntry->getNextState()] << std::endl;
	std::cout << "Event: " << eventMap[pMatchEntry->getEvent()] << std::endl;

	EPCAction* pActionToExecute = pMatchEntry->getAction();
	pActionToExecute->doAction(context);
}

