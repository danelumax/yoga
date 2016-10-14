/*
 * Scheme3.h
 *
 *  Created on: Oct 14, 2016
 *      Author: eliwech
 */

#ifndef SCHEMA3_H_
#define SCHEMA3_H_

#include "AbstractFactory.h"

class Schema3 : public AbstractFactory
{
public:
	Schema3();
	virtual ~Schema3();
	virtual void* createProduct(int type);
};

#endif /* SCHEMA3_H_ */
