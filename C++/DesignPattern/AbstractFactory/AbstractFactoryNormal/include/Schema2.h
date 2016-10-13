/*
 * Schema2.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef SCHEMA2_H_
#define SCHEMA2_H_

#include "AbstractFactory.h"

class Schema2 : public AbstractFactory
{
public:
	Schema2();
	virtual ~Schema2();
	virtual CPUApi* createCPUApi();
	virtual MainboardApi* createMainboardApi();
};

#endif /* SCHEMA2_H_ */
