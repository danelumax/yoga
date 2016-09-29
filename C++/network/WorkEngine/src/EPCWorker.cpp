/*
 * EPCWorker.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include <string>
#include "EPCWorker.h"
#include "AbstractProcesser.h"

EPCWorker::EPCWorker(GetMessageCallback getMessageCallback)
	:_getMessageCallback(getMessageCallback)
{
}

EPCWorker::~EPCWorker()
{
}

void EPCWorker::run()
{
	bool isNew = true;
	int count = 0;
	while(1)
	{
		pthread_t threadId = pthread_self();
		if (isNew)
		{
			isNew = false;
			std::cout << "\n[Add]  Thread: " << threadId << " in the Thread Pool." <<std::endl;
		}
		else /* thread has finished the task */
		{
			std::cout << "\n[Recover]  Thread: " << threadId << " is recovered into the Thread Pool." <<std::endl;
		}

		/* block and wait for message coming */
		std::string message = _getMessageCallback();

		std::cout << "\n[Handling]  Thread " << threadId <<" fetch Message: \"" << message << "\", and cost 2 sec to handle it, work time: " << ++count << std::endl;
		AbstractProcesser::getInstance()->processMessage();
	}
}
