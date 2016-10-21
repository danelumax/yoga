/*
 * ConcretePrototype2.h
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#ifndef CONCRETEPROTOTYPE2_H_
#define CONCRETEPROTOTYPE2_H_

#include "Prototype.h"

class ConcretePrototype2 : public Prototype
{
public:
	ConcretePrototype2();
	virtual ~ConcretePrototype2();
	Prototype* clone();
	std::string getName();
	void setName(std::string name);
	void toString();
private:
	std::string _name;
};

#endif /* CONCRETEPROTOTYPE2_H_ */
