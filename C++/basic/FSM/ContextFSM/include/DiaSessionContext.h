/*
 * DiaSessionContext.h
 *
 *  Created on: Sep 2, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONCONTEXT_H_
#define DIASESSIONCONTEXT_H_

#include <string>
#include <Message.h>
#include <DiaSessionContextFsm.h>

class DiaSessionContext
{
public:
	DiaSessionContext();
	virtual ~DiaSessionContext();
	void process(Message* msg);
	void setFSMNextState(std::string nextState);
	std::string getCurrentState();
	std::string getEvent(Message* msg);
private:
	DiaSessionContextFsm* _fsm;
};

#endif /* DIASESSIONCONTEXT_H_ */
