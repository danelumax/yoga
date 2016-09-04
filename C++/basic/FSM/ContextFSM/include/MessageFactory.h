/*
 * MessageFactory.h
 *
 *  Created on: Sep 4, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEFACTORY_H_
#define MESSAGEFACTORY_H_

#include <Message.h>

class MessageFactory
{
public:
	~MessageFactory();
	static MessageFactory* getInstance();
	static void destory();
	Message* getMessage(std::string type);
private:
	MessageFactory();
	static MessageFactory* _instance;
};

#endif /* MESSAGEFACTORY_H_ */
