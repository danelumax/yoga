/*
 * ConcretePrototype1.cpp
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#include "ConcretePrototype1.h"

ConcretePrototype1::ConcretePrototype1()
	: _name("")
{
}

ConcretePrototype1::~ConcretePrototype1()
{
}

Prototype* ConcretePrototype1::clone()
{
	ConcretePrototype1* prototype = new ConcretePrototype1();
	prototype->setName(_name);
	return prototype;
}

std::string ConcretePrototype1::getName()
{
	return _name;
}

void ConcretePrototype1::setName(std::string name)
{
	_name = name;
}

void ConcretePrototype1::toString()
{
	std::cout << "Now in Prototype1, name=" << _name << std::endl;
}
