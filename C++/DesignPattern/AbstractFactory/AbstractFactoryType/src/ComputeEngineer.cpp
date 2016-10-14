/*
 * ComputeEngineer.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "ComputeEngineer.h"

ComputeEngineer::ComputeEngineer()
	: _cpu(NULL), _mainboard(NULL), _memory(NULL)
{
}

ComputeEngineer::~ComputeEngineer()
{
}

void ComputeEngineer::makeComputer(AbstractFactory* schema)
{
	prepareHardwares(schema);
}

void ComputeEngineer::prepareHardwares(AbstractFactory* schema)
{
	_cpu = (CPUApi*)schema->createProduct(1);
	_mainboard = (MainboardApi*)schema->createProduct(2);
	_memory = (MemoryApi*)schema->createProduct(3);

	_cpu->calculate();
	_mainboard->installCPU();
	if (_memory != NULL)
	{
		_memory->cacheData();
	}
}
