/*
 * WorkEngine.cpp
 *
 *  Created on: 2016年2月11日
 *      Author: root
 */

#include "WorkEngine.h"

WorkEngine::WorkEngine(int worker_number):_worker_number(worker_number)
{
}

WorkEngine::~WorkEngine()
{
}

int WorkEngine::initWorkerList()
{
	for(int i=0; i < _worker_number; i++)
	{
		MessageQ *_msg = StringMessageQ::getInstance()->getmsgQ();
		EPCWorker* worker = new EPCWorker(_msg);

		if(NULL == worker)
		{
			return -1;
		}

		//多态，明明是thread list，但是赋值时用EPCWorker
		_worker_list.push_back(worker);
	}

	return 0;
}

void WorkEngine::start()
{
	std::list<thread*>::iterator it = _worker_list.begin();

	while(it != _worker_list.end())
	{
		//多态
		thread* worker = *(it);
		worker->start();
		it++;
	}
}

void WorkEngine::destroyWorkerList()
{
    std::list<thread*>::iterator it = _worker_list.begin();

    while(it != _worker_list.end())
    {
        thread* worker = *(it);
        delete worker;
        it++;
    }
}

void WorkEngine::destroy()
{
	destroyWorkerList();
}
