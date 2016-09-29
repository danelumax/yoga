/*
 * MessageQ.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEQ_H_
#define MESSAGEQ_H_

#include <string>
#include <vector>
#include <pthread.h>
#include <iostream>
#include <stdint.h>
#include "CriticalSection.h"

template<typename QType>
class MessageQ
{
public:
	MessageQ(uint32_t maxSize);
	~MessageQ();
	void try_put(const QType message);
	QType try_get();
private:
	uint32_t _maxSize;
	std::vector<QType> _messageList;
	pthread_mutex_t _mutexMessageList;
	pthread_cond_t _eventEmpty;
	pthread_cond_t _eventFull;
};

/**
 * For Avoid template class function show undefined reference in compiling
 * Put template function definitions in its header file
 */

template<typename QType>
MessageQ<QType>::MessageQ(uint32_t maxSize)
	:_maxSize(maxSize)
{
	pthread_mutex_init(&_mutexMessageList, 0);
	pthread_cond_init(&_eventEmpty, 0);
	pthread_cond_init(&_eventFull, 0);
}

template<typename QType>
MessageQ<QType>::~MessageQ()
{
}

template<typename QType>
void MessageQ<QType>::try_put(const QType message)
{
	CriticalSection cs(&_mutexMessageList);

	while(_messageList.size() >= _maxSize)
	{
		std::cout << "\n[Message Full]  \""<< message << "\" is waiting for entering message queue, please wait ..." << std::endl;
		pthread_cond_wait(&_eventFull, &_mutexMessageList);
	}
	_messageList.push_back(message);

	pthread_cond_signal(&_eventEmpty);
}

template<typename QType>
QType MessageQ<QType>::try_get()
{
	CriticalSection cs(&_mutexMessageList);

	while(_messageList.size() <= 0)
	{
		std::cout << "[Message Empty]  Please wait for new message coming ..." << std::endl;
		pthread_cond_wait(&_eventEmpty, &_mutexMessageList);
	}

	typename std::vector<QType>::iterator iter = _messageList.begin();
	QType message = *iter;
	_messageList.erase(iter);

	if (_messageList.size() < _maxSize)
	{
		pthread_cond_signal(&_eventFull);
	}

	return message;
}


#endif /* MESSAGEQ_H_ */
