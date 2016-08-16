/*
 * TimeoutMonitor.cpp
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#include "time.h"
#include "TimeoutMonitor.h"
#include "CriticalSection.h"

TimeoutMonitor* TimeoutMonitor::_instance = NULL;
const int TIMEOUT_INTERVAL = 2;

TimeoutMonitor::TimeoutMonitor()
{
	pthread_mutex_init(&_sleepMutex, 0);
	pthread_cond_init(&_sleepCond, 0);
}

TimeoutMonitor::~TimeoutMonitor()
{
	pthread_mutex_destroy(&_sleepMutex);
	pthread_cond_destroy(&_sleepCond);
}

TimeoutMonitor* TimeoutMonitor::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new TimeoutMonitor();
	}

	return _instance;
}

void TimeoutMonitor::destroy()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void TimeoutMonitor::run()
{
	while(isRunning())
	{
		CriticalSection cs(&_sleepMutex);
		struct timespec tme;
		tme.tv_sec = time(NULL) + TIMEOUT_INTERVAL;
		tme.tv_nsec = 0;

		/* wait for timeout */
		pthread_cond_timedwait(&_sleepCond, &_sleepMutex, &tme);

		TimeoutHandling();
	}
}

void TimeoutMonitor::BreadLoop()
{
	CriticalSection cs(&_sleepMutex);
	_running = false;
	pthread_t tid = pthread_self();
	pthread_cancel(tid);
}

void TimeoutMonitor::TimeoutHandling()
{
	std::cout << " * Timeout * " << std::endl;
}
