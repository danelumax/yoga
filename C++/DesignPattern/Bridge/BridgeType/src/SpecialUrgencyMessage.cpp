/*
 * SpecialUrgencyMessage.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "SpecialUrgencyMessage.h"

SpecialUrgencyMessage::SpecialUrgencyMessage(AbstractMessage::MessageType type)
	: AbstractMessage(type)
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
