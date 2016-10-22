/*
 * Colleague.cpp
 *
 *  Created on: Aug 10, 2016
 *      Author: eliwech
 */

#include "Colleague.h"

/***** Definition*****/
/* Colleague */
Colleague::Colleague(Mediator *mediator)
{
	_mediator = mediator;
}

Colleague::~Colleague()
{
}

Mediator* Colleague::getMediator()
{
	return _mediator;
}
