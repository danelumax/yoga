/*
 * MessageMobile.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEMOBILE_H_
#define MESSAGEMOBILE_H_

#include "MessageImplementor.h"

class MessageMobile : public MessageImplementor
{
public:
	MessageMobile();
	virtual ~MessageMobile();
	virtual void send(std::string message, std::string toUser);
};

#endif /* MESSAGEMOBILE_H_ */
