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

void* Schema1::createProduct(int type)
{
	if (1 == type)
	{
		return new IntelCPU(1156);
	}
	else if (2 == type)
	{
		return new GAMainboard(1156);
	}

	return NULL;
}
