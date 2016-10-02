/*
 * MessageImplementor.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEIMPLEMENTOR_H_
#define MESSAGEIMPLEMENTOR_H_

#include <string>

class MessageImplementor
{
public:
	virtual void send(std::string message, std::string toUser) = 0;
};

#endif /* MESSAGEIMPLEMENTOR_H_ */
