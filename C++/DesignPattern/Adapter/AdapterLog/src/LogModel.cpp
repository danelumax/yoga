/*
 * LogModel.cpp
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#include "LogModel.h"
#include <iostream>

LogModel::LogModel()
	: _logId(""),
	  _operateUser(""),
	  _OperateTime(""),
	  _logContent("")
{
}

LogModel::~LogModel()
{
}

std::string LogModel::getLogContent() const
{
    return _logContent;
}

std::string LogModel::getLogId() const
{
    return _logId;
}

std::string LogModel::getOperateTime() const
{
    return _OperateTime;
}

std::string LogModel::getOperateUser() const
{
    return _operateUser;
}

void LogModel::setLogContent(std::string logContent)
{
    _logContent = logContent;
}

void LogModel::setLogId(std::string logId)
{
    _logId = logId;
}

void LogModel::setOperateTime(std::string OperateTime)
{
    _OperateTime = OperateTime;
}

void LogModel::setOperateUser(std::string operateUser)
{
    _operateUser = operateUser;
}
