/*
 * NdbColumnCondition.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbColumnCondition.h"

NdbColumnCondition::NdbColumnCondition(std::string columnName,
									   std::string columnValue,
									   NdbColumnCondition::Condition op)
	:_columnName(columnName),
	 _columnValue(columnValue),
	 _op(op)
{
}

NdbColumnCondition::~NdbColumnCondition()
{
}

const char* NdbColumnCondition::getColumnName()
{
	return _columnName.c_str();
}

std::string NdbColumnCondition::getColumnValue()
{
	return _columnValue;
}


