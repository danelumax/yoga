/*
 * GAMainboard.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef GAMAINBOARD_H_
#define GAMAINBOARD_H_

#include "MainboardApi.h"

class GAMainboard : public MainboardApi
{
public:
	GAMainboard(int cpuHoles = 0);
	virtual ~GAMainboard();
	virtual void installCPU();
private:
	int _cpuHoles;
};

#endif /* GAMAINBOARD_H_ */
