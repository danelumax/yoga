/*
 * EPCWorker.cpp
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#include "EPCWorker.h"
#include "MessageOperation.h"

EPCWorker::EPCWorker(MessageQ *msgQ)
{
	_msgQ = msgQ;
}

EPCWorker::~EPCWorker()
{
}

void EPCWorker::run()
{
	while(1) //线程之所以能重复使用的关键！！ while
	{
		std::string message;

		std::cout << "\nThread " << pthread_self() << " ： ";
		//如果队列为空。会阻塞
		message = _msgQ->try_get();

		std::cout << "\n< < < < < < < < < < < < < < < \nThread " << pthread_self() << " will do the task" <<std::endl;
		std::cout << "Fetch message : " << message << std::endl;
		std::cout << "After fetching, we find : ";
		_msgQ->showMessage();

		MessageOperation *messopr = new MessageOperation();
		messopr->dothing(message);

	}
}
