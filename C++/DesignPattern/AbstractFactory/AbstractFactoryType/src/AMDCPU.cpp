/*
 * AMDCPU.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "AMDCPU.h"

AMDCPU::AMDCPU(int pins)
	: _pins(pins)
{
}

AMDCPU::~AMDCPU()
{
}

void AMDCPU::calculate()
{
	std::cout << "Now in AMD CPU, pins = "<< _pins << std::endl;
}
