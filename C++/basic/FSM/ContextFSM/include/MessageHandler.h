/*
 * MessageHandler.h
 *
 *  Created on: Sep 2, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEHANDLER_H_
#define MESSAGEHANDLER_H_

#include <DiaSessionContext.h>

class MessageHandler
{
public:
	MessageHandler();
	virtual ~MessageHandler();
	virtual void execute(DiaSessionContext* context) = 0;
};


class DERMessageHandler : public MessageHandler
{
public:
	DERMessageHandler(){};
	virtual ~DERMessageHandler(){};
	virtual void execute(DiaSessionContext* context);
};

#endif /* MESSAGEHANDLER_H_ */
