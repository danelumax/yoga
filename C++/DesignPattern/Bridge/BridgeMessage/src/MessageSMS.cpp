/*
 * MessageSMS.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "MessageSMS.h"
#include <iostream>

MessageSMS::MessageSMS()
{
}

MessageSMS::~MessageSMS()
{
}

void MessageSMS::send(std::string message, std::string toUser)
{
	std::cout << "Use <SMS> to send message \"" << message << "\" to " << toUser << std::endl;
}


