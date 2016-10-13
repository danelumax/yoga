/*
 * AbstractFactory.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef ABSTRACTFACTORY_H_
#define ABSTRACTFACTORY_H_

#include "CPUApi.h"
#include "MainboardApi.h"

class AbstractFactory
{
public:
	virtual CPUApi* createCPUApi() = 0;
	virtual MainboardApi* createMainboardApi() = 0;
};

#endif /* ABSTRACTFACTORY_H_ */
