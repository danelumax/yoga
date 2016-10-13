/*
 * AMDCPU.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef AMDCPU_H_
#define AMDCPU_H_

#include "CPUApi.h"

class AMDCPU : public CPUApi
{
public:
	AMDCPU(int pins = 0);
	virtual ~AMDCPU();
	virtual void calculate();
private:
	int _pins;
};

#endif /* AMDCPU_H_ */
