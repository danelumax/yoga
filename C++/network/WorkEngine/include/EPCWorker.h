/*
 * ExecuteThread.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef EXECUTETHREAD_H_
#define EXECUTETHREAD_H_

#include <boost/function.hpp>
#include <Thread.h>

class EPCWorker : public Thread
{
private:
	typedef boost::function<std::string()> GetMessageCallback;
	GetMessageCallback _getMessageCallback;
public:
	EPCWorker(GetMessageCallback getMessageCallback);
	virtual ~EPCWorker();
	virtual void run();
};

#endif /* EXECUTETHREAD_H_ */
