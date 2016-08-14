/*
 * ThreadPool.cpp
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#include <iostream>
#include <boost/bind.hpp>
#include "ThreadPool.h"
#include "ExecuteThread.h"

ThreadPool::ThreadPool(int poolSize, int msgQSize)
	:_poolSize(poolSize), _msgQSize(msgQSize)
{
	_msgQ = new MessageQ<std::string>(_msgQSize);
}

ThreadPool::~ThreadPool()
{
}

int ThreadPool::initThreadPool()
{
	int ret = 0;
	for(int i=0; i<_poolSize; i++)
	{
		ThreadBase *thread = new ExecuteThread(boost::bind(&ThreadPool::getMessage, this));
		if (thread == NULL)
		{
			ret = -1;
		}

		_theadList.push_back(thread);
	}

	return ret;
}

void ThreadPool::StartAllThread()
{
	std::vector<ThreadBase*>::iterator iter = _theadList.begin();
	for(; iter!=_theadList.end(); ++iter)
	{
		ThreadBase *thread = *(iter);
		thread->start();
	}
}

std::string ThreadPool::getMessage()
{
	return _msgQ->try_get();
}

void ThreadPool::putMessage(std::string message)
{
	_msgQ->try_put(message);
}


