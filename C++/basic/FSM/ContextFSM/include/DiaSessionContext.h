/*
 * DiaSessionContext.h
 *
 *  Created on: Sep 2, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONCONTEXT_H_
#define DIASESSIONCONTEXT_H_

#include <string>
#include <DiaSessionContextFsm.h>

class DiaSessionContext
{
public:
	DiaSessionContext();
	virtual ~DiaSessionContext();
	void process();
	void setFSMNextState(std::string nextState);
private:
	DiaSessionContextFsm* _fsm;
};

#endif /* DIASESSIONCONTEXT_H_ */
