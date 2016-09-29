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
#include <Thread.h>
#include <MessageQ.h>


class WorkEngine {
public:
	WorkEngine(int poolSize, int msgQSize);
	virtual ~WorkEngine();
	int initThreadPool();
	void start();
	std::string getFromMsgQueue();
	void putIntoMsgQueue(std::string);

private:
	int _poolSize;
	int _msgQSize;
	std::vector<Thread*> _workerList;
	MessageQ<std::string> *_msgQ;

};

#endif /* THREADPOOL_H_ */
