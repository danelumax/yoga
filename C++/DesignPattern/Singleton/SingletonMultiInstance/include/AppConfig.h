/*
 * AppConfig.h
 *
 *  Created on: Aug 3, 2016
 *      Author: eliwech
 */

#ifndef APPCONFIG_H_
#define APPCONFIG_H_

#include <map>
#include <iostream>

class AppConfig
{
public:
	static AppConfig* getInstance();
private:
	AppConfig();

	static AppConfig* _instance;
	static std::map<int, AppConfig*> _map;
};

#endif /* APPCONFIG_H_ */
