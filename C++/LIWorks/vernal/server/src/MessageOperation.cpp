/*
 * MessageOperation.cpp
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#include "MessageOperation.h"

MessageOperation::MessageOperation()
{
}

MessageOperation::~MessageOperation() {
	// TODO Auto-generated destructor stub
}

void MessageOperation::dothing(std::string message)
{
		message = StringUtil::toUpperCase(message);
		sleep(5);
		std::cout << "\n* * * * * * * * * * * * * * * * * *" << std::endl;
		std::cout << "After do something, the message has been transformed to " << message << std::endl;
}
