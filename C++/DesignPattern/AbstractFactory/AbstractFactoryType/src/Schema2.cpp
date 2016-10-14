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

void* Schema2::createProduct(int type)
{
	if (1 == type)
	{
		return new AMDCPU(939);
	}
	else if (2 == type)
	{
		return new MSIMainboard(939);
	}

	return NULL;
}
