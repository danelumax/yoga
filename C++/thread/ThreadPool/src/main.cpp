//============================================================================
// Name        : ThreadPool.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Thread Pool
//============================================================================

#include <iostream>
#include <sstream>
#include "ThreadPool.h"

const int POOL_SIZE = 5;
const int MSGQ_SIZE = 8;
const int MSG_COMING = 11;

int main(void)
{
    std::cout << "\n[Configuration] "
			  << POOL_SIZE << " thread, "
    		  << MSGQ_SIZE << " Message Queue, "
    		  << MSG_COMING << " Message Coming" << std::endl;
	ThreadPool *pool = new ThreadPool(POOL_SIZE, MSGQ_SIZE);
	if(pool->initThreadPool() != 0)
	{
		std::cout << "Init thread pool failed" << std::endl;
	}
	pool->StartAllThread();
	sleep(2);
	std::cout << "\n\n*** [Result]  All Threads have been initialization.***\n\n" << std::endl;

	for(int i=0; i<MSG_COMING; i++)
	{
		std::ostringstream oss;
		oss << "ABC + " << i;
		pool->putMessage(oss.str());
	}

	sleep(100);
	return 0;
}
