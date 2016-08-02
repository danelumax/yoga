/*
 * thread.cpp
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#include "thread.h"

thread::thread():_running(false)
{
	_thread = 0;
	pthread_mutex_init(&_mutexRunning, NULL);
}

thread::~thread()
{
	// TODO Auto-generated destructor stub
}

int thread::start()
{
	int ret;
	//防止统一对象的两个进程同时抢_running=false，保护资源
    pthread_mutex_lock(&_mutexRunning);
    //确保一个对象只有running一个线程
    if (_running)
    {
        pthread_mutex_unlock(&_mutexRunning);
        return -1;
    }

    ret = pthread_create(&_thread, 0, thread::startThread, this);

    return ret;
}

void* thread::startThread(void* arg)
{
	thread *me = (thread *) arg;

	//告知，有线程正在running
	me->_running = true;
	//_running已经等于true，不怕其他进程抢了
	pthread_mutex_unlock(&(me->_mutexRunning));

	me->run();

	me->_running = false;

	pthread_exit(arg);
	return arg;
}
