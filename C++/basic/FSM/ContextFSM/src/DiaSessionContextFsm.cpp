/*
 * DiaSessionContextFsm.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "DiaSessionContextFsm.h"

DiaSessionContextFsm::DiaSessionContextFsm()
{
}

DiaSessionContextFsm::~DiaSessionContextFsm()
{
}

void DiaSessionContextFsm::addContextAction(std::string event, std::string state, ContextAction *action)
{
	if(NULL != action)
	{
		_stateContextMap.insert(std::make_pair(std::make_pair(event, state), action));
	}
}


