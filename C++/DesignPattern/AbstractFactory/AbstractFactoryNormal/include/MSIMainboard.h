/*
 * MSIMainboard.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef MSIMAINBOARD_H_
#define MSIMAINBOARD_H_

#include "MainboardApi.h"

class MSIMainboard : public MainboardApi
{
public:
	MSIMainboard(int cpuHoles = 0);
	virtual ~MSIMainboard();
	virtual void installCPU();
private:
	int _cpuHoles;
};

#endif /* MSIMAINBOARD_H_ */
