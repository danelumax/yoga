/*
 * IntelCPU.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "IntelCPU.h"

IntelCPU::IntelCPU(int pins)
	: _pins(pins)
{

}

IntelCPU::~IntelCPU()
{

}

void IntelCPU::calculate()
{
	std::cout << "Now in Intel CPU, pins = "<< _pins << std::endl;
}
