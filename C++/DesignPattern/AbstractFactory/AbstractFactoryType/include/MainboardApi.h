/*
 * MainboardApi.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef MAINBOARDAPI_H_
#define MAINBOARDAPI_H_

#include <iostream>

class MainboardApi
{
public:
	virtual void installCPU() = 0;
};

#endif /* MAINBOARDAPI_H_ */
