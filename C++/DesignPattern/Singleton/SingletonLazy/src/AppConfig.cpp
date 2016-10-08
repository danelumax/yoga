/*
 * AppConfig.cpp
 *
 *  Created on: Aug 3, 2016
 *      Author: eliwech
 */
#include "AppConfig.h"

/* Lazy difference */
AppConfig* AppConfig::_instance = NULL;

AppConfig::AppConfig()
{
	readConfig();
}

AppConfig* AppConfig::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new AppConfig();
	}
	return _instance;
}

std::string AppConfig::getParameterA()
{
	return _parameterA;
}

std::string AppConfig::getParameterB()
{
	return _parameterB;
}

void AppConfig::readConfig()
{
	std::map<std::string, std::string>::iterator iter = Property.find("paramA");
	if (iter != Property.end())
	{
		_parameterA = iter->second;
	}

	iter = Property.find("paramB");
	if (iter != Property.end())
	{
		_parameterB = iter->second;
	}
}
