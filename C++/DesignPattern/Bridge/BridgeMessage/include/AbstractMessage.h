/*
 * AbstractMessage.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef ABSTRACTMESSAGE_H_
#define ABSTRACTMESSAGE_H_

#include <MessageImplementor.h>
#include <string>

class AbstractMessage
{
public:
	AbstractMessage();
	virtual ~AbstractMessage();
	MessageImplementor* getImpl(std::string message);
	virtual void sendMessage(std::string message, std::string toUser);
protected:
	MessageImplementor* _impl;
};

#endif /* ABSTRACTMESSAGE_H_ */
