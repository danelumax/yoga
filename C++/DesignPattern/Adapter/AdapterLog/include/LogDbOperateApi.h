/*
 * LogDbOperateApi.h
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#ifndef LOGDBOPERATEAPI_H_
#define LOGDBOPERATEAPI_H_

#include "LogModel.h"
#include <vector>

class LogDbOperateApi
{
public:
	virtual void createLog(LogModel* lm) = 0;
	virtual std::vector<LogModel*> getAllLog() = 0;
};

#endif /* LOGDBOPERATEAPI_H_ */
