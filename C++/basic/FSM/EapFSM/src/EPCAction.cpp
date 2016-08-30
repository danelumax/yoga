/*
 * EPCAction.cpp
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "EPCAction.h"

EPCAction::EPCAction()
{
}

EPCAction::~EPCAction()
{
}

void EPCActionRequestAuthVector::doAction(DiaSessionContext* context)
{
	std::cout << "do Request Auth Vector" << std::endl;
}

void EPCActionRequestProfile::doAction(DiaSessionContext* context)
{
	std::cout << "do Request Profile" << std::endl;
}
