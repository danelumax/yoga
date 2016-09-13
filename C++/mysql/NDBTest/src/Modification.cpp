/*
 * Modification.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "Modification.h"

Modification::Modification()
{
}

Modification::~Modification()
{
}

void Modification::addValue(std::string key, int value)
{
	_values[key] = value;
}

std::map<std::string,int> Modification::getValues()
{
	return _values;
}



