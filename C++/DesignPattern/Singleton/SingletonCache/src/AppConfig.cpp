/*
 * AppConfig.cpp
 *
 *  Created on: Aug 3, 2016
 *      Author: eliwech
 */
#include "AppConfig.h"

const std::string DEFAULT_KEY = "One";
AppConfig* AppConfig::_instance = NULL;

/* initialize _map */
std::map<std::string, AppConfig*> AppConfig::_map;

AppConfig::AppConfig()
{
	readConfig();
}

AppConfig* AppConfig::getInstance()
{
	std::map<std::string, AppConfig*>::iterator iter = _map.find(DEFAULT_KEY);
	if (iter == _map.end())
	{
		std::cout << "First create instance" << std::endl;
		_instance = new AppConfig();
		_map[DEFAULT_KEY] = _instance;
	}
	else
	{
		std::cout << "Get instance from map" << std::endl;
		_instance = _map[DEFAULT_KEY];
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
