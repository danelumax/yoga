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

void ResultSet::addValue(std::string key, std::string value)
{
	_value[key] = value;
}
