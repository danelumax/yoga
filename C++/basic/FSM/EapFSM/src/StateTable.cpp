/*
 * StateTable.cpp
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#include "StateTable.h"

StateTable::StateTable()
{
}

StateTable::~StateTable()
{
}

void StateTable::addStateTableEntry(StateEntry *stateEntry)
{
	if (stateEntry != NULL)
	{
		_entryMap[std::make_pair(stateEntry->getCurrentState(), stateEntry->getEvent())] = stateEntry;
	}
}

StateEntry *StateTable::findStateTableEntry(EPCState currentState, EPCEvent event)
{
	return _entryMap[std::make_pair(currentState, event)];
}


