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

AbstractMessage::AbstractMessage(MessageType type)
{
	switch(type)
	{
		case AbstractMessage::SMS:
		{
			_impl = new MessageSMS();
			break;
		}
		case AbstractMessage::MOBILE:
		{
			_impl = new MessageMobile();
			break;
		}
		case AbstractMessage::EMAIL:
		{
			_impl = new MessageEmail();
			break;
		}
	}
}

AbstractMessage::~AbstractMessage()
{
}

void AbstractMessage::sendMessage(std::string message, std::string toUser)
{
	_impl->send(message, toUser);
}
