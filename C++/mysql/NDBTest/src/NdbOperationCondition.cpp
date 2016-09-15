/*
 * NdbOperationCondition.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbOperationCondition.h"

NdbOperationCondition::NdbOperationCondition(std::string tableName, Type type)
	:_tableName(tableName), _type(type)
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

	return 0;
}

std::vector<NdbColumnCondition*> NdbOperationCondition::getChangeColumns()
{
	return _changeColumns;
}

std::string NdbOperationCondition::getTableName()
{
	return _tableName;
}




