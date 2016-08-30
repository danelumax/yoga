/*
 * StateEntry.h
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#ifndef STATEENTRY_H_
#define STATEENTRY_H_

#include <StateEventDefine.h>
#include <EPCAction.h>

class StateEntry
{
public:
	StateEntry(EPCState currentState, EPCState nextState, EPCEvent event, EPCAction *action);
	~StateEntry();
	EPCState getCurrentState();
	EPCState getNextState();
	EPCEvent getEvent();
	EPCAction* getAction();

private:
	EPCState _currentState;
	EPCState _nextState;
	EPCEvent _event;
	EPCAction *_acton;
};

#endif /* STATEENTRY_H_ */
