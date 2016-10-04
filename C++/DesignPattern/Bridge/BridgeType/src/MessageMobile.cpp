/*
 * MessageMobile.cpp
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#include "MessageMobile.h"
#include <iostream>

MessageMobile::MessageMobile() {
	// TODO Auto-generated constructor stub

}

MessageMobile::~MessageMobile() {
	// TODO Auto-generated destructor stub
}

void MessageMobile::send(std::string message, std::string toUser)
{
	std::cout << "Use <Mobile> to send message \"" << message << "\" to " << toUser << std::endl;
}
