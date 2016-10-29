/*
 * Observer.h
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#ifndef OBSERVER_H_
#define OBSERVER_H_

#include <string>

class Observer
{
public:
	virtual void update(std::string content) = 0;
};

#endif /* OBSERVER_H_ */
