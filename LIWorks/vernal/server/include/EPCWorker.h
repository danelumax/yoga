/*
 * EPCWorker.h
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#ifndef VERNAL_SERVER_EPCWorker_H_
#define VERNAL_SERVER_EPCWorker_H_

#include "thread.h"
#include "MessageOperation.h"
#include "MessageQ.h"

class EPCWorker : public thread
{
public:
	EPCWorker();
	EPCWorker(MessageQ *msgQ);
	virtual ~EPCWorker();
	virtual void run();
private:
	MessageQ *_msgQ;
};

#endif /* VERNAL_SERVER_EPCWorker_H_ */
