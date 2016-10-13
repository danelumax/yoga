/*
 * Schema1.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef SCHEMA1_H_
#define SCHEMA1_H_

#include "AbstractFactory.h"

class Schema1 : public AbstractFactory
{
public:
	Schema1();
	virtual ~Schema1();
	virtual CPUApi* createCPUApi();
	virtual MainboardApi* createMainboardApi();
};

#endif /* SCHEMA1_H_ */
