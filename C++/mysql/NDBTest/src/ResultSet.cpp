/*
 * ResultSet.cpp
 *
 *  Created on: Sep 16, 2016
 *      Author: eliwech
 */

#include "ResultSet.h"

ResultSet::ResultSet()
{
}

ResultSet::~ResultSet()
{
}

std::string ResultSet::getTable()
{
	return _table;
}

void ResultSet::addValue(std::string key, std::string value)
{
	_values[key] = value;
}

std::map<std::string, std::string> ResultSet::getValues()
{
	return _values;
}
