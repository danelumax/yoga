/*
 * LogModel.h
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#ifndef LOGMODEL_H_
#define LOGMODEL_H_

#include <string>

class LogModel
{
public:
	LogModel();
	virtual ~LogModel();
	std::string getLogContent() const;
	std::string getLogId() const;
	std::string getOperateTime() const;
	std::string getOperateUser() const;
	void setLogContent(std::string logContent);
	void setLogId(std::string logId);
	void setOperateTime(std::string OperateTime);
	void setOperateUser(std::string operateUser);
private:
	std::string _logId;
	std::string _operateUser;
	std::string _OperateTime;
	std::string _logContent;
};

#endif /* LOGMODEL_H_ */
