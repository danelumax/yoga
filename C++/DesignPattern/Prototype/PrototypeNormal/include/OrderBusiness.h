/*
 * OrderBusiness.h
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#ifndef ORDERBUSINESS_H_
#define ORDERBUSINESS_H_

#include "OrderApi.h"

class OrderBusiness
{
public:
	OrderBusiness();
	virtual ~OrderBusiness();
	void saveOrder(OrderApi* order);
};

#endif /* ORDERBUSINESS_H_ */
