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

class ContextPolicyS6bAuthz : public ContextPolicy
{
public:
	virtual ~ContextPolicyS6bAuthz(){};
	static ContextPolicyS6bAuthz* getInstance();
	static void destory();
private:
	ContextPolicyS6bAuthz(){};
	virtual void initContextFsm(DiaSessionContextFsm* fsm);
	static ContextPolicyS6bAuthz* _instance;
};



#endif /* CONTEXTPOLICY_H_ */
