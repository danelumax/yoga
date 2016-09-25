/*
 * FlowAMementoCareTaker.cpp
 *
 *  Created on: Sep 25, 2016
 *      Author: eliwech
 */

#include "FlowAMementoCareTaker.h"

FlowAMementoCareTaker::FlowAMementoCareTaker()
	: _memento(NULL)
{
}

FlowAMementoCareTaker::~FlowAMementoCareTaker()
{
}

void FlowAMementoCareTaker::saveMemento(FlowAMockMemento* memento)
{
	_memento = memento;
}

FlowAMockMemento* FlowAMementoCareTaker::retriveMemento()
{
	return _memento;
}
