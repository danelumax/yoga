/*
 * LogFileOperate.h
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#ifndef LOGFILEOPERATE_H_
#define LOGFILEOPERATE_H_

#include "LogFileOperateApi.h"

class LogFileOperate : public LogFileOperateApi
{
public:
	LogFileOperate();
	virtual ~LogFileOperate();
	virtual std::vector<LogModel*> readLogFile();
	virtual void writeLogFile(std::vector<LogModel*> list);

private:
	std::string _logFilePathName;
};

#endif /* LOGFILEOPERATE_H_ */
