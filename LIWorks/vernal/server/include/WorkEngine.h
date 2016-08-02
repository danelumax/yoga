/*
 * WorkEngine.h
 *
 *  Created on: 2016年2月11日
 *      Author: root
 */

#ifndef VERNAL_SERVER_WORKENGINE_H_
#define VERNAL_SERVER_WORKENGINE_H_

#include <thread.h>
#include <EPCWorker.h>
#include <list>
#include <MessageQ.h>
#include "StringMessageQ.h"

//完成线程池的功能
class WorkEngine
{
public:
	WorkEngine(int worker_number);
	virtual ~WorkEngine();
	void start();
	int initWorkerList();
	void destroyWorkerList();
	void destroy();
private:
	std::list<thread*> _worker_list;
	int _worker_number;
};

#endif /* VERNAL_SERVER_WORKENGINE_H_ */
