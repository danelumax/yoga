/*
 * TimeoutMonitor.h
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#ifndef TIMEOUTMONITOR_H_
#define TIMEOUTMONITOR_H_

#include <iostream>
#include <ThreadBase.h>

class TimeoutMonitor : public ThreadBase
{
public:
	static TimeoutMonitor* getInstance();
	static void destroy();
	virtual void run();
	virtual void BreadLoop();
	void TimeoutHandling();
	~TimeoutMonitor();
private:
	TimeoutMonitor();
	static TimeoutMonitor* _instance;

	pthread_mutex_t _sleepMutex;
	pthread_cond_t _sleepCond;
};

#endif /* TIMEOUTMONITOR_H_ */
