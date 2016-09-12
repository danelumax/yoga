/*
 * Modification.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "Modification.h"

Modification::Modification() {
	// TODO Auto-generated constructor stub

}

Modification::~Modification() {
	// TODO Auto-generated destructor stub
}

void Modification::addValue(std::string key, int value)
{
	_values[key] = value;
}

std::map<std::string,int> Modification::getValues()
{
	return _values;
}



