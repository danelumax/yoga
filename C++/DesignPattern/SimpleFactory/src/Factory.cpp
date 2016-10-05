/*
 * Factory.cpp
 *
 *  Created on: Oct 5, 2016
 *      Author: eliwech
 */

#include "Factory.h"
#include "Impl.h"
#include "Impl2.h"

Factory::Factory()
{
}

Factory::~Factory()
{
}

Api* Factory::createApi(int type)
{
	Api* api = NULL;
	if (1 == type)
	{
		api = new Impl();
	}
	else if (2 == type)
	{
		api = new Impl2();
	}

	return api;
}
