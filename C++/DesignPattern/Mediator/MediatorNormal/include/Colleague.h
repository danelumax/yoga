/*
 * Colleague.h
 *
 *  Created on: Aug 8, 2016
 *      Author: eliwech
 */

#ifndef COLLEAGUE_H_
#define COLLEAGUE_H_

#include <string>
#include <iostream>
#include "Mediator.h"

/***** Declaration *****/
class Colleague
{
public:
	//wait derived class to call, tell colleague, you need to inform who
	Colleague(Mediator *mediator);
	virtual ~Colleague();
	Mediator* getMediator();

private:
	Mediator *_mediator;
};





#endif /* COLLEAGUE_H_ */
