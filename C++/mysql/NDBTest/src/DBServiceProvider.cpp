/*
 * DBServiceProvider.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "DBServiceProvider.h"
#include <iostream>

DBServiceProvider* DBServiceProvider::_instance = NULL;

DBServiceProvider::DBServiceProvider()
{
}

DBServiceProvider::~DBServiceProvider()
{
}

DBServiceProvider* DBServiceProvider::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new DBServiceProvider();
	}

	return _instance;
}

void DBServiceProvider::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}
