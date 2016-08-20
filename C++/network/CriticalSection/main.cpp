//============================================================================
// Name        : CriticalSection.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <pthread.h>
#include "CriticalSection.h"

static pthread_mutex_t _Mutex = PTHREAD_MUTEX_INITIALIZER;

int main()
{
	CriticalSection cs(&_Mutex);
	return 0;
}
