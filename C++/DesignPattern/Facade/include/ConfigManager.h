/*
 * ConfigManager.h
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#ifndef CONFIGMANAGER_H_
#define CONFIGMANAGER_H_

#include <iostream>
#include "ConfigModel.h"

class ConfigManager
{
public:
	virtual ~ConfigManager();
	static ConfigManager* getInstance();
	static void destory();
	ConfigModel* getConfigData();
private:
	ConfigManager();
	static ConfigManager* _instance;
	ConfigModel* _cm;
};

#endif /* CONFIGMANAGER_H_ */
