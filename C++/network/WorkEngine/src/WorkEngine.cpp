/*
 * WorkEngine.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include <boost/bind.hpp>
#include "WorkEngine.h"
#include "Thread.h"
#include "EPCWorker.h"

WorkEngine::WorkEngine(int poolSize, int msgQSize)
	:_poolSize(poolSize), _msgQSize(msgQSize)
{
	_msgQ = new MessageQ<std::string>(_msgQSize);
}

WorkEngine::~WorkEngine()
{
}

int WorkEngine::initThreadPool()
{
	int ret = 0;
	for(int i=0; i<_poolSize; i++)
	{
		EPCWorker *worker = new EPCWorker(boost::bind(&WorkEngine::getFromMsgQueue, this));
		if (NULL == worker)
		{
			ret = -1;
		}

		_workerList.push_back(worker);
	}

	return ret;
}

void WorkEngine::start()
{
	std::vector<Thread*>::iterator iter = _workerList.begin();
	for(; iter!=_workerList.end(); ++iter)
	{
		Thread *thread = *(iter);
		thread->start();
	}
}

std::string WorkEngine::getFromMsgQueue()
{
	return _msgQ->try_get();
}

void WorkEngine::putIntoMsgQueue(std::string message)
{
	_msgQ->try_put(message);
}


