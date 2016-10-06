/*
 * ConfigManager.cpp
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#include "ConfigManager.h"

ConfigManager* ConfigManager::_instance = NULL;

ConfigManager::ConfigManager()
{
	_cm = new ConfigModel();
}

ConfigManager::~ConfigManager()
{
}

ConfigManager* ConfigManager::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new ConfigManager();
	}

	return _instance;
}

void ConfigManager::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

ConfigModel* ConfigManager::getConfigData()
{
	return _cm;
}

