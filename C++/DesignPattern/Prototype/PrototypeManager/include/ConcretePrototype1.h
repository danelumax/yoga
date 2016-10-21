/*
 * ConcretePrototype1.h
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#ifndef CONCRETEPROTOTYPE1_H_
#define CONCRETEPROTOTYPE1_H_

#include "Prototype.h"

class ConcretePrototype1 : public Prototype
{
public:
	ConcretePrototype1();
	virtual ~ConcretePrototype1();
	Prototype* clone();
	std::string getName();
	void setName(std::string name);
	void toString();
private:
	std::string _name;
};

#endif /* CONCRETEPROTOTYPE1_H_ */
