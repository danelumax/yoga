/*
 * thread.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef THREAD_H_
#define THREAD_H_

#include <pthread.h>

class ThreadBase {
public:
	ThreadBase();
	virtual ~ThreadBase();
	int start();
	void stop();
	virtual void BreadLoop();
	virtual void run() = 0;
	static void* StartThread(void* arg);
	bool isRunning();
protected:
	bool _running;
private:
	pthread_t _thread;  // not use pointer, coredump will happen
	pthread_mutex_t _mutexRunning;
};

#endif /* THREAD_H_ */
