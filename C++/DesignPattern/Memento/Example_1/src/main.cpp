//============================================================================
// Name        : Example_1.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "FlowAMock.h"
#include "FlowAMementoCareTaker.h"

int main()
{
	FlowAMock* mock = new FlowAMock("TestFlow");
	mock->runPhaseOne();

	FlowAMementoCareTaker* careTaker = new FlowAMementoCareTaker();
	FlowAMockMemento* memento = mock->createMemento();
	careTaker->saveMemento(memento);

	mock->schema1();

	mock->setMemento(careTaker->retriveMemento());

	mock->schema2();

	delete memento;
	delete mock;
	return 0;
}
