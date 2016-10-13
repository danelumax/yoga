/*
 * Schema2.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "Schema2.h"
#include "AMDCPU.h"
#include "MSIMainboard.h"

Schema2::Schema2()
{
}

Schema2::~Schema2()
{
}

CPUApi* Schema2::createCPUApi()
{
	return new AMDCPU(939);
}

MainboardApi* Schema2::createMainboardApi()
{
	return new MSIMainboard(939);
}
