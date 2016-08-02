/*
 * StringMessageQ.h
 *
 *  Created on: 2016年2月12日
 *      Author: root
 */

#ifndef VERNAL_SERVER_STRINGMESSAGEQ_H_
#define VERNAL_SERVER_STRINGMESSAGEQ_H_

#include <iostream>
#include "MessageQ.h"

class StringMessageQ {
public:
	virtual ~StringMessageQ();
	static StringMessageQ* getInstance();
	MessageQ* getmsgQ();
	int initMessageQueue();
protected:
	StringMessageQ();
private:
	static StringMessageQ* _instance;
	MessageQ* _msgQ;

};

#endif /* VERNAL_SERVER_STRINGMESSAGEQ_H_ */
