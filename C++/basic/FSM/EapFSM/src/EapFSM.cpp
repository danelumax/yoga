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
	//StateEntry* pEntry = NULL;
	StateEntry* pEntry = new StateEntry(STATE_IDLE,
							STATE_WAIT_FOR_AUTH_VECTOR,
							EVENT_NO_AUTH_VECTOR,
							new EPCActionRequestAuthVector());
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

	EPCAction* pActionToExecute = pMatchEntry->getAction();
	pActionToExecute->doAction(context);
}

