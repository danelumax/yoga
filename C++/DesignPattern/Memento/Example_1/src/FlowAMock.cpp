/*
 * FlowAMock.cpp
 *
 *  Created on: Sep 25, 2016
 *      Author: eliwech
 */

#include "FlowAMock.h"
#include <iostream>

FlowAMock::FlowAMock(std::string flowName)
	:_tempState(""), _tempResult(0)
{
	_flowName = flowName;
}

FlowAMock::~FlowAMock()
{
}

void FlowAMock::runPhaseOne()
{
	_tempResult = 3;
	_tempState = "PhaseOne";
}

void FlowAMock::schema1()
{
	_tempState += ",Schema1";
	std::cout << _tempState << " : now run " << _tempResult << std::endl;
	_tempResult += 11;
}

void FlowAMock::schema2()
{
	_tempState += ",Schema2";
	std::cout << _tempState << " : now run " << _tempResult << std::endl;
	_tempResult += 22;
}

FlowAMockMemento* FlowAMock::createMemento()
{
	return new MementoImpl(_tempResult, _tempState);
}

void FlowAMock::setMemento(FlowAMockMemento* memento)
{
	MementoImpl* mementoImpl = static_cast<MementoImpl*>(memento);
	_tempResult = mementoImpl->getImplTempResult();
	_tempState = mementoImpl->getImplTempState();
	std::cout << "Get info from memo" << std::endl;
}
