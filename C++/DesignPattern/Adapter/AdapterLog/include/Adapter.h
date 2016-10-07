/*
 * Adapter.h
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#ifndef ADAPTER_H_
#define ADAPTER_H_

#include "LogDbOperateApi.h"
#include "LogFileOperateApi.h"

class Adapter : public LogDbOperateApi
{
public:
	Adapter(LogFileOperateApi* adaptee);
	virtual ~Adapter();
	virtual void createLog(LogModel* lm);
	virtual std::vector<LogModel*> getAllLog();
private:
	LogFileOperateApi* _adaptee;
};

#endif /* ADAPTER_H_ */
