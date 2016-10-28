/*
 * Observer.h
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#ifndef OBSERVER_H_
#define OBSERVER_H_

class Subject;

class Observer
{
public:
	virtual void update(Subject *subject) = 0;
};

#endif /* OBSERVER_H_ */
