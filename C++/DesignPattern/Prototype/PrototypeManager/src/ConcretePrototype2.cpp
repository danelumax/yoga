/*
 * ConcretePrototype2.cpp
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#include "ConcretePrototype2.h"

ConcretePrototype2::ConcretePrototype2()
	: _name("")
{
}

ConcretePrototype2::~ConcretePrototype2()
{
}

Prototype* ConcretePrototype2::clone()
{
	ConcretePrototype2* prototype = new ConcretePrototype2();
	prototype->setName(_name);
	return prototype;
}

std::string ConcretePrototype2::getName()
{
	return _name;
}

void ConcretePrototype2::setName(std::string name)
{
	_name = name;
}

void ConcretePrototype2::toString()
{
	std::cout << "Now in Prototype2, name=" << _name << std::endl;
}
