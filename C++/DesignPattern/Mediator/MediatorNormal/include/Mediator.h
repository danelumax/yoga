/*
 * Mediator.h
 *
 *  Created on: Aug 8, 2016
 *      Author: eliwech
 */

#ifndef MEDIATOR_H_
#define MEDIATOR_H_

/* just for interface restraint */
class Colleague;

class Mediator
{
public:
	virtual void changed(Colleague *colleague) = 0;
};



#endif /* MEDIATOR_H_ */
