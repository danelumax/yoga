/*
 * thread.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include "ThreadBase.h"
#include <iostream>

ThreadBase::ThreadBase()
	:_running(false)
{
	_thread = 0;
	pthread_mutex_init(&_mutexRunning, NULL);
}

ThreadBase::~ThreadBase()
{
}

int ThreadBase::start()
{
	int ret = 0;
	pthread_mutex_lock(&_mutexRunning);
	if (_running)
	{
		pthread_mutex_unlock(&_mutexRunning);
		ret = -1;
	}
	ret = pthread_create(&_thread, 0, &ThreadBase::StartThread, this);

	return ret;
}

void* ThreadBase::StartThread(void *arg)
{
	ThreadBase *me = (ThreadBase*)arg;
	me->_running = true;

	pthread_mutex_unlock( &(me->_mutexRunning) );

	me->run();

	me->_running = false;

	pthread_exit(arg);
	return arg;
}
