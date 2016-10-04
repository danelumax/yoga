/*
 * AbstractMessage.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "AbstractMessage.h"
#include "MessageSMS.h"
#include "MessageEmail.h"
#include "MessageMobile.h"
#include <iostream>

AbstractMessage::AbstractMessage()
	: _impl(NULL)
{
}

AbstractMessage::~AbstractMessage()
{
}

MessageImplementor* AbstractMessage::getImpl(std::string message)
{
	MessageImplementor* impl = NULL;
	if (message.length() <= 15)
	{
		impl = new MessageSMS();
	}
	else if (message.length()>15 && message.length()<=17)
	{
		impl = new MessageMobile();
	}
	else if (message.length()>=17)
	{
		impl = new MessageEmail();
	}

	return impl;
}

void AbstractMessage::sendMessage(std::string message, std::string toUser)
{
	_impl = getImpl(message);
	_impl->send(message, toUser);
}
