/*
 * ExecuteThread.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include <string>
#include "ExecuteThread.h"

ExecuteThread::ExecuteThread(GetMessageCallback getMessageCallback)
	:_getMessageCallback(getMessageCallback)
{
}

ExecuteThread::~ExecuteThread()
{
}

void ExecuteThread::run()
{
	bool isNew = true;
	int count = 0;
	while(1)
	{
		pthread_t thread_id = pthread_self();
		if (isNew)
		{
			isNew = false;
			std::cout << "\n[Add]  Thread: " << thread_id << " in the Thread Pool." <<std::endl;
		}
		else
		{
			std::cout << "\n[Recover]  Thread: " << thread_id << " is recovered into the Thread Pool." <<std::endl;
		}

		/* block and wait for message coming */
		std::string message = _getMessageCallback();

		std::cout << "\n[Handling]  Thread " << thread_id <<" fetch Message: \"" << message << "\", and cost 2 sec to handle it, work time: " << ++count << std::endl;
		sleep(2);
	}
}
