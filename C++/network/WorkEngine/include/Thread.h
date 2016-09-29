/*
 * thread.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef THREAD_H_
#define THREAD_H_

#include <pthread.h>

class Thread {
public:
	Thread();
	virtual ~Thread();
	int start();
	virtual void run() = 0;
	static void* StartThread(void* arg);
private:
	pthread_t _thread;  // not use pointer, coredump will happen
	pthread_mutex_t _mutexRunning;
	bool _running;
};

#endif /* THREAD_H_ */
