/*
 * thread.h
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#ifndef VERNAL_SERVER_THREAD_H_
#define VERNAL_SERVER_THREAD_H_

#include <pthread.h>

class thread
{
public:
	thread();
	virtual ~thread();
	int start();
	virtual void run() = 0;
	static void* startThread(void* arg);
private:
	pthread_t _thread;
	pthread_mutex_t _mutexRunning;
	bool _running;
};

#endif /* VERNAL_SERVER_THREAD_H_ */
