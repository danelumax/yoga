/*
 * MSIMainboard.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "MSIMainboard.h"

MSIMainboard::MSIMainboard(int cpuHoles)
	: _cpuHoles(cpuHoles)
{
}

MSIMainboard::~MSIMainboard()
{
}

void MSIMainboard::installCPU()
{
	std::cout << "Now in MSI Mainboard, cpuHoles = "<< _cpuHoles << std::endl;
}
