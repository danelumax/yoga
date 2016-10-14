/*
 * IntelCPU.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef INTELCPU_H_
#define INTELCPU_H_

#include "CPUApi.h"

class IntelCPU : public CPUApi
{
public:
	IntelCPU(int pins = 0);
	virtual ~IntelCPU();
	virtual void calculate();
private:
	int _pins;
};

#endif /* INTELCPU_H_ */
