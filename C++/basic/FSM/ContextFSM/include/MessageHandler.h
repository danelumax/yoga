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

/* DER */
class DERMessageHandler : public MessageHandler
{
public:
	DERMessageHandler(){};
	virtual ~DERMessageHandler(){};
	virtual void execute(DiaSessionContext* context);
};

/* MAA */
class SWxMAAMessageHandler : public MessageHandler
{
public:
	SWxMAAMessageHandler(){};
	virtual ~SWxMAAMessageHandler(){};
	virtual void execute(DiaSessionContext* context);
};

/* SAA */
class SWxSAAMessageHandler : public MessageHandler
{
public:
	SWxSAAMessageHandler(){};
	virtual ~SWxSAAMessageHandler(){};
	virtual void execute(DiaSessionContext* context);
};

/* AAR */
class S6bAARMessageHandler : public MessageHandler
{
public:
	S6bAARMessageHandler(){};
	virtual ~S6bAARMessageHandler(){};
	virtual void execute(DiaSessionContext* context);
};



#endif /* MESSAGEHANDLER_H_ */
