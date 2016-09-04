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
//#include <ContextAction.h>
class ContextAction;
class DiaSessionContext;
//#include <DiaSessionContext.h>

class DiaSessionContextFsm
{
public:
	DiaSessionContextFsm(std::string currentState);
	virtual ~DiaSessionContextFsm();
	void reset();
	void addContextAction(std::string event, std::string, ContextAction* action);
	void process(std::string event, DiaSessionContext* context);
	bool isInitState();
	ContextAction* getContextAction(std::string event, std::string state);
	void setNextState(std::string nextState);
	std::string getCurrentState();
	void migrate();

private:
	struct stateEventPairCmp
	{
		bool operator()(const std::pair<std::string, std::string> p1, const std::pair<std::string, std::string> p2) const
		{
			return (p1.first < p2.first) || ((p1.first == p2.first) && (p1.second < p2.second));
		}
	};
	typedef std::map<std::pair<std::string, std::string>, ContextAction*, stateEventPairCmp> StateContextActionType;

private:
	StateContextActionType _stateContextMap;
	std::string _event;
	std::string _currentState;
	std::string _nextState;
	ContextAction* _action;
};

#endif /* DIASESSIONCONTEXTFSM_H_ */
