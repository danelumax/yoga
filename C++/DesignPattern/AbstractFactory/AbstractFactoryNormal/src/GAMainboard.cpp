/*
 * GAMainboard.cpp
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#include "GAMainboard.h"

GAMainboard::GAMainboard(int cpuHoles)
	: _cpuHoles(cpuHoles)
{
}

GAMainboard::~GAMainboard()
{
}

void GAMainboard::installCPU()
{
	std::cout << "Now in GA Mainboard, cpuHoles = "<< _cpuHoles << std::endl;
}
