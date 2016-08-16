/*
 * thread.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "ThreadBase.h"
#include "CriticalSection.h"

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
	{
		CriticalSection cs(&_mutexRunning);
		if (_running)
		{
			return -1;
		}
	}

	int ret = pthread_create(&_thread, 0, &ThreadBase::StartThread, this);

	return ret;
}

void ThreadBase::stop()
{
	BreadLoop();
}

void ThreadBase::BreadLoop()
{
	return;
}

void* ThreadBase::StartThread(void *arg)
{
	ThreadBase *me = (ThreadBase*)arg;

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

bool ThreadBase::isRunning()
{
	CriticalSection cs(&_mutexRunning);
	return _running;
}
