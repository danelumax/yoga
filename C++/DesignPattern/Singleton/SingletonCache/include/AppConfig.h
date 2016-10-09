/*
 * AppConfig.h
 *
 *  Created on: Aug 3, 2016
 *      Author: eliwech
 */

#ifndef APPCONFIG_H_
#define APPCONFIG_H_

#include <string>
#include <map>
#include "boost/assign.hpp"

static std::map<std::string, std::string> Property = boost::assign::map_list_of
		("paramA", "value1")
		("paramB", "value2");

class AppConfig
{
public:
	static AppConfig* getInstance();
	std::string getParameterA();
	std::string getParameterB();
private:
	AppConfig();
	void readConfig();

	static AppConfig* _instance;
	static std::map<std::string, AppConfig*> _map;
	std::string _parameterA;
	std::string _parameterB;
};

#endif /* APPCONFIG_H_ */
