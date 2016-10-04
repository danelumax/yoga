/*
 * MessageMobile.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "MessageMobile.h"
#include <iostream>

MessageMobile::MessageMobile()
{
}

MessageMobile::~MessageMobile()
{
}

void MessageMobile::send(std::string message, std::string toUser)
{
	std::cout << "Use <Mobile> to send message \"" << message << "\" to " << toUser << std::endl;
}
