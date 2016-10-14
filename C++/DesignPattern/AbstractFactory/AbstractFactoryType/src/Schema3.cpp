/*
 * Scheme3.cpp
 *
 *  Created on: Oct 14, 2016
 *      Author: eliwech
 */

#include "Schema3.h"
#include "IntelCPU.h"
#include "HyMemory.h"
#include "GAMainboard.h"

Schema3::Schema3()
{
}

Schema3::~Schema3()
{
}

void* Schema3::createProduct(int type)
{
	if (1 == type)
	{
		return new IntelCPU(1156);
	}
	else if (2 == type)
	{
		return new GAMainboard(1156);
	}
	else if (3 == type)
	{
		return new HyMemory();
	}

	return NULL;
}
