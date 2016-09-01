/*
 * DiaSessionContextFsm.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONCONTEXTFSM_H_
#define DIASESSIONCONTEXTFSM_H_

#include <map>
#include <string>
#include <ContextAction.h>

class DiaSessionContextFsm
{
public:
	DiaSessionContextFsm();
	virtual ~DiaSessionContextFsm();
	void addContextAction(std::string event, std::string, ContextAction* action);

private:
	struct stateEventPairCmp
	{
		bool operator()(const std::pair<std::string, std::string> p1, const std::pair<std::string, std::string> p2) const
		{
			return (p1.first < p2.first) || ((p1.first == p2.first) && (p1.second < p2.second));
		}
	};
	typedef std::map<std::pair<std::string, std::string>, ContextAction*, stateEventPairCmp> StateContextActionType;
	StateContextActionType _stateContextMap;
};

#endif /* DIASESSIONCONTEXTFSM_H_ */
