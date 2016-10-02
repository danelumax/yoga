/*
 * MessageSMS.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef MESSAGESMS_H_
#define MESSAGESMS_H_

#include "MessageImplementor.h"

#include <string>

class MessageSMS : public MessageImplementor
{
public:
	MessageSMS();
	virtual ~MessageSMS();
	virtual void send(std::string message, std::string toUser);
};

#endif /* MESSAGESMS_H_ */
