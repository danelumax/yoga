/*
 * CriticalSection.h
 *
 *  Created on: Aug 9, 2016
 *      Author: eliwech
 */

#ifndef CRITICALSECTION_H_
#define CRITICALSECTION_H_

#include <pthread.h>
#include <iostream>

class CriticalSection {
public:
	CriticalSection(pthread_mutex_t *mutex);
	~CriticalSection();

	static void clean(void *arg);
private:
	pthread_mutex_t *_mutex;
	__pthread_cleanup_class* __clframe;
};

#endif /* CRITICALSECTION_H_ */
