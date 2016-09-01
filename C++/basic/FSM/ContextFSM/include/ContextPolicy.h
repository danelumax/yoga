/*
 * ContextPolicy.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef CONTEXTPOLICY_H_
#define CONTEXTPOLICY_H_

#include <DiaSessionContextFsm.h>

/* builder */
class ContextPolicy
{
public:
	ContextPolicy();
	virtual ~ContextPolicy();
	virtual void initContextFsm(DiaSessionContextFsm* fsm) = 0;
};

class ContextPolicyAuth : public ContextPolicy
{
public:
	virtual ~ContextPolicyAuth(){};
	static ContextPolicyAuth* getInstance();
	static void destory();
private:
	ContextPolicyAuth(){};
	virtual void initContextFsm(DiaSessionContextFsm* fsm);
	static ContextPolicyAuth* _instance;
};



#endif /* CONTEXTPOLICY_H_ */
