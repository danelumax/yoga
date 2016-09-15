/*
 * Modification.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "Modification.h"

Modification::Modification(std::string table)
	:_table(table)
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

std::string Modification::getTable()
{
	return _table;
}



