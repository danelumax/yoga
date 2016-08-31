/*
 * EPCAction.h
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#ifndef EPCACTION_H_
#define EPCACTION_H_

#include <DiaSessionContext.h>

class EPCAction {
public:
	EPCAction();
	virtual ~EPCAction();

	virtual void doAction(DiaSessionContext* context) = 0;
};

class EPCActionRequestAuthVector : public EPCAction
{
public:
	EPCActionRequestAuthVector(){};
	virtual ~EPCActionRequestAuthVector(){};

	virtual void doAction(DiaSessionContext*context);
};

class EPCActionRequestProfile : public EPCAction
{
public:
	EPCActionRequestProfile(){};
	virtual ~EPCActionRequestProfile(){};

	virtual void doAction(DiaSessionContext* context);
};

class EPCActionSendChallenge : public EPCAction
{
public:
	EPCActionSendChallenge(){};
	virtual ~EPCActionSendChallenge(){};

	virtual void doAction(DiaSessionContext* context);
};

class EPCActionSendSuccess : public EPCAction
{
public:
	EPCActionSendSuccess(){};
	virtual ~EPCActionSendSuccess(){};

	virtual void doAction(DiaSessionContext* context);
};

class EPCActionSendReauthentication : public EPCAction
{
public:
	EPCActionSendReauthentication(){};
	virtual ~EPCActionSendReauthentication(){};

	virtual void doAction(DiaSessionContext* context);
};


#endif /* EPCACTION_H_ */
