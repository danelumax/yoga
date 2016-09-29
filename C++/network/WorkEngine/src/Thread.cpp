/*
 * thread.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "Thread.h"
#include "CriticalSection.h"

Thread::Thread()
	:_running(false)
{
	_thread = 0;
	pthread_mutex_init(&_mutexRunning, NULL);
}

Thread::~Thread()
{
}

int Thread::start()
{
	{
		CriticalSection cs(&_mutexRunning);
		if (_running)
		{
			return -1;
		}
	}

	int ret = pthread_create(&_thread, 0, &Thread::StartThread, this);

	return ret;
}

void* Thread::StartThread(void *arg)
{
	Thread *me = (Thread*)arg;

	{
		CriticalSection cs( &(me->_mutexRunning) );
		me->_running = true;
	}

	me->run();

	{
		CriticalSection cs( &(me->_mutexRunning) );
		me->_running = false;
	}

	pthread_exit(arg);
	return arg;
}
