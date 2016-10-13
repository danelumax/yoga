/*
 * Schema1.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "Schema1.h"
#include "IntelCPU.h"
#include "GAMainboard.h"


Schema1::Schema1()
{
}

Schema1::~Schema1()
{
}

CPUApi* Schema1::createCPUApi()
{
	return new IntelCPU(1156);
}

MainboardApi* Schema1::createMainboardApi()
{
	return new GAMainboard(1156);
}
