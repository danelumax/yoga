/*
 * SpecialUrgencyMessage.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "SpecialUrgencyMessage.h"

SpecialUrgencyMessage::SpecialUrgencyMessage(MessageImplementor* impl)
	: AbstractMessage(impl)
{
}

SpecialUrgencyMessage::~SpecialUrgencyMessage()
{
}

void SpecialUrgencyMessage::sendMessage(std::string message, std::string toUser)
{
	message = "Sepcial: " + message;
	AbstractMessage::sendMessage(message, toUser);
}
