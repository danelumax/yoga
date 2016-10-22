/*
 * CDDriver.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "CDDriver.h"
//#include "Mediator.h"

/* CDDriver */
CDDriver::CDDriver(Mediator *mediator)
	:Colleague(mediator)
{
}

CDDriver::~CDDriver()
{
}

std::string CDDriver::getData()
{
	return _data;
}

void CDDriver::readCD()
{
	/*1. Mock store data from CD */
	_data = "Movie";
	/*2. inform mediator for next step*/
	getMediator()->changed(this);
}
