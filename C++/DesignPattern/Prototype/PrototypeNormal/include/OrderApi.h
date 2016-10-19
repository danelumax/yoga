/*
 * OrderApi.h
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#ifndef ORDERAPI_H_
#define ORDERAPI_H_

#include <iostream>

class OrderApi
{
public:
	virtual int getOrderProductNum() = 0;
	virtual void setOrderProductNum(int num) = 0;
	virtual OrderApi* cloneOrder() = 0;
	virtual void toString() = 0;
};

#endif /* ORDERAPI_H_ */
