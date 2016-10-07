/*
 * LogFileOperateApi.h
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#ifndef LOGFILEOPERATEAPI_H_
#define LOGFILEOPERATEAPI_H_

#include <vector>
#include "LogModel.h"

class LogFileOperateApi
{
public:
	virtual std::vector<LogModel*> readLogFile() = 0;
	virtual void writeLogFile(std::vector<LogModel*> list) = 0;
};

#endif /* LOGFILEOPERATEAPI_H_ */
