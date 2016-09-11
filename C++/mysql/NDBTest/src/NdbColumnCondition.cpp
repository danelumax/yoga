/*
 * NdbColumnCondition.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbColumnCondition.h"

NdbColumnCondition::NdbColumnCondition(std::string columnName, int columnValue)
	:_columnName(columnName), _columnValue(columnValue)
{
}

NdbColumnCondition::~NdbColumnCondition()
{
}

const char* NdbColumnCondition::getColumnName()
{
	return _columnName.c_str();
}

int NdbColumnCondition::getColumnValue()
{
	return _columnValue;
}


