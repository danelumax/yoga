/*
 * Adapter.cpp
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#include "Adapter.h"
#include <iostream>

Adapter::Adapter(LogFileOperateApi* adaptee)
{
	_adaptee = adaptee;
}

Adapter::~Adapter()
{
}

void Adapter::createLog(LogModel* lm)
{
	std::vector<LogModel*> list = _adaptee->readLogFile();
	list.push_back(lm);
	std::cout << "Using File Api to forward..." << std::endl;
	_adaptee->writeLogFile(list);
}

std::vector<LogModel*> Adapter::getAllLog()
{
	return _adaptee->readLogFile();
}
