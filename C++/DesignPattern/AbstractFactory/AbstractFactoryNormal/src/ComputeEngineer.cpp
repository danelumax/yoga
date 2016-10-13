/*
 * ComputeEngineer.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "ComputeEngineer.h"

ComputeEngineer::ComputeEngineer()
	: _cpu(NULL), _mainboard(NULL)
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
	_cpu = schema->createCPUApi();
	_mainboard = schema->createMainboardApi();

	_cpu->calculate();
	_mainboard->installCPU();
}
