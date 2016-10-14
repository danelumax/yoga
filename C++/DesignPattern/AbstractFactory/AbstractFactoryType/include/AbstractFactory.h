/*
 * AbstractFactory.h
 *
 *  Created on: Oct 13, 2016
 *      Author: eliwech
 */

#ifndef ABSTRACTFACTORY_H_
#define ABSTRACTFACTORY_H_

class AbstractFactory
{
public:
	virtual void* createProduct(int type) = 0;
};

#endif /* ABSTRACTFACTORY_H_ */
