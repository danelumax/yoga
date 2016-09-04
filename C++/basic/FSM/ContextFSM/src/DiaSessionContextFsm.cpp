/*
 * DiaSessionContextFsm.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "DiaSessionContextFsm.h"
#include <ContextAction.h>
#include <DiaSessionContext.h>
#include <DiaCommonCode.h>

DiaSessionContextFsm::DiaSessionContextFsm(std::string currentState)
	:_currentState(currentState)
{
}

DiaSessionContextFsm::~DiaSessionContextFsm()
{
}

void DiaSessionContextFsm::reset()
{
	_event = "";
	_currentState = State_INIT;
	_nextState = "";
	_action = NULL;
	_stateContextMap.clear();
}

void DiaSessionContextFsm::addContextAction(std::string event, std::string state, ContextAction *action)
{
	if(NULL != action)
	{
		_stateContextMap.insert(std::make_pair(std::make_pair(event, state), action));
	}
}

bool DiaSessionContextFsm::isInitState()
{
	return (_currentState == State_INIT);
}

ContextAction *DiaSessionContextFsm::getContextAction(std::string event, std::string state)
{
	StateContextActionType::iterator iter = _stateContextMap.find(std::make_pair(event, state));
	if (iter != _stateContextMap.end())
	{
		return iter->second;
	}

	return NULL;
}

void DiaSessionContextFsm::process(std::string event, DiaSessionContext* context)
{
	_event = event;
	_action = getContextAction(event, _currentState);
	if (NULL != _action)
	{
		_action->handleAction(context);
		migrate();
	}
}

void DiaSessionContextFsm::setNextState(std::string nextState)
{
	_nextState = nextState;
}

std::string DiaSessionContextFsm::getCurrentState()
{
	return _currentState;
}

void DiaSessionContextFsm::migrate()
{
	std::cout << "Migrate: " << _currentState;
	_currentState = _nextState;
	std::cout << " ---> " << _currentState << std::endl;
	_nextState = "";
}



