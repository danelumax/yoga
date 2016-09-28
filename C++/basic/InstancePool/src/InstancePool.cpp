/*
 * InstancePool.cpp
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#include "InstancePool.h"
#include <stdlib.h>
#include <iostream>
#include "time.h"
#include <sys/time.h>
#include "CriticalSection.h"

InstancePool* InstancePool::_instance = NULL;

const int NdbPoolSize = 10;

InstancePool::InstancePool()
	: _maxNdbPoolSize(NdbPoolSize)
{
    pthread_cond_init(&_ndbPoolCondition, 0);
    pthread_mutex_init(&_ndbPoolMutex, 0);
}

InstancePool::~InstancePool()
{
	CriticalSection cs(&_ndbPoolMutex);
	while(_busyQueue.size() > 0)
	{
		struct timespec timeout;
		struct timeval now;
		gettimeofday(&now, 0);
		timeout.tv_sec = now.tv_sec;
		timeout.tv_nsec = now.tv_usec * 10000;

		pthread_cond_timedwait(&_ndbPoolCondition, &_ndbPoolMutex, &timeout);
	}

    std::map<Ndb*, Ndb*>::iterator iter;
    for(iter = _busyQueue.begin(); iter != _busyQueue.end(); iter++)
    {
        Ndb* ndb = (*iter).first;
        if(ndb)
        {
            delete ndb;
        }
    }

    _busyQueue.clear();

    // destroy free queue
    {
        while(!_freeQueue.empty())
        {
            Ndb* ndb = _freeQueue.front();
            _freeQueue.pop();
            if(ndb)
            {
                delete ndb;
            }
        }
    }

    pthread_cond_destroy(&_ndbPoolCondition);
    pthread_mutex_destroy(&_ndbPoolMutex);
}

InstancePool* InstancePool::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new InstancePool();
	}

	return _instance;
}

void InstancePool::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

Ndb* InstancePool::factoryNdb()
{
	Ndb* ndb = new Ndb(::rand());
	return ndb;
}

void InstancePool::addNdbIntoPool(Ndb *ndb)
{

	if (ndb)
	{
		CriticalSection cs(&_ndbPoolMutex);
		_freeQueue.push(ndb);
	}
}

Ndb* InstancePool::getNdb()
{
	CriticalSection cs(&_ndbPoolMutex);
	if (!_freeQueue.empty())
	{
		Ndb* ndb = _freeQueue.front();
		_freeQueue.pop();

		_busyQueue[ndb] = ndb;
		return ndb;
	}
	else
	{
		int ndbPoolSize = _busyQueue.size();
		if (ndbPoolSize < _maxNdbPoolSize)
		{
			Ndb* ndb = factoryNdb();
			if (ndb)
			{
				_busyQueue[ndb] = ndb;
				return ndb;
			}
			else
			{
				return NULL;
			}
		}
		else
		{
			std::cout << "InstancePool::getNdb exceed max pool size" << std::endl;
			return NULL;
		}
	}
}

void InstancePool::returnNdb(Ndb* ndb)
{
	CriticalSection cs(&_ndbPoolMutex);
	std::map<Ndb*, Ndb*>::iterator iter = _busyQueue.find(ndb);
	if (iter != _busyQueue.end())
	{
		_freeQueue.push(ndb);
		_busyQueue.erase(iter);
	}
}

void InstancePool::checkQueueStatus()
{
	std::cout << "Free queue size : " << _freeQueue.size() << std::endl;
	std::cout << "Busy queue size : " << _busyQueue.size() << std::endl;
}

std::queue<Ndb*> InstancePool::getFreeQueue()
{
	CriticalSection cs(&_ndbPoolMutex);
	return _freeQueue;
}

std::map<Ndb*, Ndb*> InstancePool::getBusyQueue()
{
	CriticalSection cs(&_ndbPoolMutex);
	return _busyQueue;
}
