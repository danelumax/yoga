/*
 * AbstractProcesser.cpp
 *
 *  Created on: Sep 29, 2016
 *      Author: eliwech
 */

#include "AbstractProcesser.h"

AbstractProcesser* AbstractProcesser::_instance = NULL;

AbstractProcesser::AbstractProcesser()
{
}

AbstractProcesser::~AbstractProcesser()
{
}

AbstractProcesser* AbstractProcesser::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new AbstractProcesser;
	}

	return _instance;
}

void AbstractProcesser::processMessage()
{
	sleep(2);
}
