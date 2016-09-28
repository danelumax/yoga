/*
 * CriticalSection.cpp
 *
 *  Created on: Aug 9, 2016
 *      Author: eliwech
 */

#include "CriticalSection.h"

void CriticalSection::clean(void *arg)
{
	pthread_mutex_unlock((pthread_mutex_t *)arg);
}

CriticalSection::CriticalSection(pthread_mutex_t *mutex)
	:_mutex(mutex)
{
	pthread_mutex_lock(_mutex);
	//pthread_cleanup_push(clean, (void*)_mutex)
	//push cleanup function
	__clframe = new __pthread_cleanup_class(clean, (void*)_mutex);
}

CriticalSection::~CriticalSection()
{
	//pthread_cleanup_pop(1)
	//pop cleanup function
	//1: call clean function   0: not call
	__clframe->__setdoit(1);
	delete __clframe;
	__clframe = NULL;
}
