/*
 * ComputeEngineer.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef COMPUTEENGINEER_H_
#define COMPUTEENGINEER_H_

#include "AbstractFactory.h"

class ComputeEngineer
{
public:
	ComputeEngineer();
	virtual ~ComputeEngineer();
	void makeComputer(AbstractFactory* schema);
private:
	void prepareHardwares(AbstractFactory* schema);
	CPUApi* _cpu;
	MainboardApi* _mainboard;
};

#endif /* COMPUTEENGINEER_H_ */
