/*
 * StateTable.h
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#ifndef STATETABLE_H_
#define STATETABLE_H_

#include <map>
#include <iostream>
#include <StateEntry.h>
#include <StateEventDefine.h>

struct stateEventPairCmp
{
	bool operator()( const std::pair<EPCState, EPCEvent>p1, const std::pair<EPCState, EPCEvent>p2) const
	{
		return (p1.first<p2.first) || ((p1.first==p2.first)&&(p1.second<p2.second));
	}
};

class StateTable {
public:
	StateTable();
	virtual ~StateTable();

	void addStateTableEntry(StateEntry *stateEntry);
	StateEntry* findStateTableEntry(EPCState currentState, EPCEvent event);
private:
	std::map<std::pair<EPCState, EPCEvent>, StateEntry*, stateEventPairCmp> _entryMap;
	//std::map<int, StateEntry*> _entryMap;
};

#endif /* STATETABLE_H_ */
