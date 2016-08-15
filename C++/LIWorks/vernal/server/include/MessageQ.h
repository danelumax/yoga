/*
 * MessageQ.h
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#ifndef VERNAL_SERVER_MESSAGEQ_H_
#define VERNAL_SERVER_MESSAGEQ_H_

#include "MessageQ.h"
#include <string>
#include <list>
#include <iostream>
#include <pthread.h>

#define N 5

class MessageQ
{
public:
	MessageQ();
	virtual ~MessageQ();
	void try_put(std::string message);
	std::string try_get();
	void showMessage();
	int getQueueLen();
private:
	std::list<std::string> _message_list;
    pthread_mutex_t _gate; // mutex
    pthread_cond_t _event; // event
};

#endif /* VERNAL_SERVER_MESSAGEQ_H_ */
