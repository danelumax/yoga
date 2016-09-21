/*
 * NdbRowData.cpp
 *
 *  Created on: Sep 21, 2016
 *      Author: eliwech
 */

#include "NdbRowData.h"

NdbRowData::NdbRowData()
{
}

NdbRowData::~NdbRowData()
{
}

void NdbRowData::addValue(std::string colName, std::string value)
{
	_values[colName] = value;
}

int NdbRowData::getValue(std::string colName, std::string & value)
{
	std::map<std::string, std::string>::iterator iter = _values.find(colName);
	if (iter == _values.end())
	{
		return -1;
	}

	value = iter->second;

	return 0;
}

std::map<std::string, std::string> NdbRowData::getValues()
{
	return _values;
}

