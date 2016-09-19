/*
 * NdbSearchOption.cpp
 *
 *  Created on: Sep 18, 2016
 *      Author: eliwech
 */

#include "NdbSearchOption.h"

NdbSearchOption::NdbSearchOption()
	: SearchOption(""), _type(NdbSearchOption::T_UNKNOWN)
{
}

NdbSearchOption::~NdbSearchOption()
{
}

void NdbSearchOption::setTable(std::string table)
{
	_table = table;
}

void NdbSearchOption::setType(NdbSearchOption::Type type)
{
	_type = type;
}

NdbSearchOption::Type NdbSearchOption::getType()
{
	return _type;
}




