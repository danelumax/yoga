/*
 * Modification.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "Modification.h"
#include <sstream>

Modification::Modification(std::string table)
	:_table(table)
{
}

Modification::~Modification()
{
}

void Modification::addValue(std::string key, int value)
{
	std::ostringstream oss;
	oss << value;
	_values[key] = oss.str();
}

void Modification::addValue(std::string key, std::string value)
{
	_values[key] = value;
}

std::map<std::string, std::string> Modification::getValues()
{
	return _values;
}

std::string Modification::getTable()
{
	return _table;
}



