/*
 * NdbOperationCondition.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbOperationCondition.h"

NdbOperationCondition::NdbOperationCondition(Type type)
	:_type(type)
{
}

NdbOperationCondition::~NdbOperationCondition()
{
}

NdbOperationCondition::Type NdbOperationCondition::getType()
{
	return _type;
}

bool NdbOperationCondition::isSingleRowOpearation()
{
	bool singleRowOperation = false;

	if (_type == NdbOperationCondition::INSERT)
	{
		singleRowOperation = true;
	}

	return singleRowOperation;
}

int NdbOperationCondition::addChangeColumn(NdbColumnCondition *column)
{
	_changeColumns.push_back(column);
}

std::vector<NdbColumnCondition*> NdbOperationCondition::getChangeColumns()
{
	return _changeColumns;
}




