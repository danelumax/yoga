/*
 * ThreadPool.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef THREADPOOL_H_
#define THREADPOOL_H_

#include <vector>
#include <string>
#include <ThreadBase.h>
#include <MessageQ.h>


class ThreadPool {
public:
	ThreadPool(int poolSize, int msgQSize);
	virtual ~ThreadPool();
	int initThreadPool();
	void StartAllThread();
	std::string getMessage();
	void putMessage(std::string);

private:
	int _poolSize;
	int _msgQSize;
	std::vector<ThreadBase*> _theadList;
	MessageQ<std::string> *_msgQ;

};

#endif /* THREADPOOL_H_ */
