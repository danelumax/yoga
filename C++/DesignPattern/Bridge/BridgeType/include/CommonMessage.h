/*
 * CommonMessage.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef COMMONMESSAGE_H_
#define COMMONMESSAGE_H_

#include "AbstractMessage.h"
//#include "MessageImplementor.h"

class CommonMessage : public AbstractMessage
{
public:
	CommonMessage(AbstractMessage::MessageType type);
	virtual ~CommonMessage();
	virtual void sendMessage(std::string message, std::string toUser);
};

#endif /* COMMONMESSAGE_H_ */
