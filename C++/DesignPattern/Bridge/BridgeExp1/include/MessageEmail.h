/*
 * MessageEmail.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEEMAIL_H_
#define MESSAGEEMAIL_H_

#include "MessageImplementor.h"

class MessageEmail : public MessageImplementor
{
public:
	MessageEmail();
	virtual ~MessageEmail();
	virtual void send(std::string message, std::string toUser);
};

#endif /* MESSAGEEMAIL_H_ */
