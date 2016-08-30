/*
 * StateEntry.cpp
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#include <StateEntry.h>

StateEntry::StateEntry(EPCState currentState, EPCState nextState, EPCEvent event, EPCAction *action)
		:_currentState(currentState), _nextState(nextState), _event(event), _acton(action)
{
}

StateEntry::~StateEntry()
{
}

EPCState StateEntry::getCurrentState()
{
	return _currentState;
}

EPCState StateEntry::getNextState()
{
	return _nextState;
}

EPCEvent StateEntry::getEvent()
{
	return _event;
}

EPCAction* StateEntry::getAction()
{
	return _acton;
}
