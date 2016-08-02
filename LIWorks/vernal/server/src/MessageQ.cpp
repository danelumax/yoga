/*
 * MessageQ.cpp
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#include "MessageQ.h"

MessageQ::MessageQ()
{
    // Initializes mutex
    pthread_mutex_init(&_gate, 0);

    // Initializes event object
    pthread_cond_init(&_event, 0);
}

MessageQ::~MessageQ() {
	// TODO Auto-generated destructor stub
}

void MessageQ::try_put(std::string message)
{
	pthread_mutex_lock(&_gate);

	while(_message_list.size() >= N)
	{
		std::cout << "message is full, please wait..." << std::endl;
		pthread_cond_wait(&_event,&_gate);
	}
	_message_list.push_back(message);
	//告知，队列非空,让卡住的线程，跑起来
	pthread_cond_signal(&_event);

	pthread_mutex_unlock(&_gate);
}

void MessageQ::showMessage()
{
	int listLength = _message_list.size();

	if(listLength > 0)
	{
		std::list<std::string>::iterator it = _message_list.begin();
		std::cout << listLength << " messages need to be handled : ";
		while(it != _message_list.end())
		{
			std::cout << *(it) << "  ";
			it++;
		}
		std::cout << std::endl;
	}
	else
	{
		std::cout << "This message queue is empty!" << std::endl;
	}
}

std::string MessageQ::try_get()
{
	pthread_mutex_lock(&_gate);

	//如果queue为空，线程卡住
	while(_message_list.size() <= 0)
	{
		std::cout << "～ ～ ～ ～ e m p t y , b l o c k i n g ～ ～ ～ ～" << std::endl;
		pthread_cond_wait(&_event,&_gate);
	}

	std::string message = _message_list.front();
	_message_list.pop_front();

	pthread_mutex_unlock(&_gate);

	return message;
}

int MessageQ::getQueueLen()
{
	return _message_list.size();
}
