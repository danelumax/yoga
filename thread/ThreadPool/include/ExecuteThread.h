/*
 * ExecuteThread.h
 *
 *  Created on: Aug 14, 2016
 *      Author: eliwech
 */

#ifndef EXECUTETHREAD_H_
#define EXECUTETHREAD_H_

#include <boost/function.hpp>
#include <ThreadBase.h>

class ExecuteThread : public ThreadBase
{
private:
	typedef boost::function<std::string()> GetMessageCallback;
	GetMessageCallback _getMessageCallback;
public:
	ExecuteThread(GetMessageCallback getMessageCallback);
	virtual ~ExecuteThread();
	virtual void run();
};

#endif /* EXECUTETHREAD_H_ */
