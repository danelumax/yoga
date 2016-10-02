/*
 * AbstractMessage.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "AbstractMessage.h"

AbstractMessage::AbstractMessage(MessageImplementor* impl)
{
	_impl = impl;
}

AbstractMessage::~AbstractMessage()
{
}

void AbstractMessage::sendMessage(std::string message, std::string toUser)
{
	_impl->send(message, toUser);
}
