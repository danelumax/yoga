/*
 * Factory.h
 *
 *  Created on: Oct 5, 2016
 *      Author: eliwech
 */

#ifndef FACTORY_H_
#define FACTORY_H_

#include "Api.h"

class Factory
{
public:
	Factory();
	virtual ~Factory();
	static Api* createApi(int type);
};

#endif /* FACTORY_H_ */
