/*
 * AppConfig.cpp
 *
 *  Created on: Aug 3, 2016
 *      Author: eliwech
 */
#include "AppConfig.h"

static int num = 1;
static const int NUM_MAX = 3;
AppConfig* AppConfig::_instance = NULL;

/* initialize _map */
std::map<int, AppConfig*> AppConfig::_map;

AppConfig::AppConfig()
{
}

AppConfig* AppConfig::getInstance()
{
	std::cout << "The " << num << "-th instance" << std::endl;
	std::map<int, AppConfig*>::iterator iter = _map.find(num);
	if (iter == _map.end())
	{
		_instance = new AppConfig();
		_map[num] = _instance;
	}
	else
	{
		_instance = _map[num];
	}

	num++;
	if (num > NUM_MAX)
	{
		num = 1;
	}

	return _instance;
}
