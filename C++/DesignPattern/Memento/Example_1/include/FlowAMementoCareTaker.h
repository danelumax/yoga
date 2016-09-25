/*
 * FlowAMementoCareTaker.h
 *
 *  Created on: Sep 25, 2016
 *      Author: eliwech
 */

#ifndef FLOWAMEMENTOCARETAKER_H_
#define FLOWAMEMENTOCARETAKER_H_

#include "FlowAMock.h"

class FlowAMementoCareTaker
{
public:
	FlowAMementoCareTaker();
	virtual ~FlowAMementoCareTaker();
	void saveMemento(FlowAMockMemento* memento);
	FlowAMockMemento* retriveMemento();
private:
	FlowAMockMemento* _memento;
};

#endif /* FLOWAMEMENTOCARETAKER_H_ */
