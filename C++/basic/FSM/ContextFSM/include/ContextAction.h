/*
 * ContextAction.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef CONTEXTACTION_H_
#define CONTEXTACTION_H_

#include <iostream>
#include <MessageHandler.h>
#include <DiaSessionContext.h>

class ContextAction
{
public:
	ContextAction();
	virtual ~ContextAction();
	void handleAction(DiaSessionContext* context);
protected:
	MessageHandler* _msgHandler;
};

class ContextActionDER : public ContextAction
{
public:
	virtual ~ContextActionDER(){};
	static ContextActionDER* getInstance();
	static void destory();
private:
	ContextActionDER();
	static ContextActionDER* _instance;
};



#endif /* CONTEXTACTION_H_ */
