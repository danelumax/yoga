/*
 * ResultSet.cpp
 *
 *  Created on: Sep 16, 2016
 *      Author: eliwech
 */

#include "ResultSet.h"

ResultSet::ResultSet(std::string table)
	:_table(table)
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
