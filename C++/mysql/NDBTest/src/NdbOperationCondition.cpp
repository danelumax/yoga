/*
 * NdbOperationCondition.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbOperationCondition.h"
#include <iostream>

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

	if (_type == NdbOperationCondition::QUERY_SINGLE
			|| _type == NdbOperationCondition::INSERT
			|| _type == NdbOperationCondition::DELETE_SINGLE)
	{
		singleRowOperation = true;
	}

	return singleRowOperation;
}

int NdbOperationCondition::addQueryColumn(NdbColumnCondition *column)
{
	if (_type == NdbOperationCondition::INSERT)
	{
		std::cout << "NdbOperationCondition::addQueryColumn Can not apply to INSERT operation." << std::endl;
		return -1;
	}

	_queryColumns.push_back(column);

	return 0;
}

int NdbOperationCondition::addChangeColumn(NdbColumnCondition *column)
{
	if (_type == NdbOperationCondition::QUERY_SINGLE)
	{
		std::cout << "NdbOperationCondition::addChangeColumn can only apply to query/delete operation." << std::endl;
		return -1;
	}

	_changeColumns.push_back(column);

	return 0;
}

bool NdbOperationCondition::hasQueryColumn()
{
	return _queryColumns.empty() ? false : true;
}

bool NdbOperationCondition::hasChangeColumn()
{
	return _changeColumns.empty() ? false: true;
}

std::vector<NdbColumnCondition*> NdbOperationCondition::getQueryColumns()
{
	return _queryColumns;
}

std::vector<NdbColumnCondition*> NdbOperationCondition::getChangeColumns()
{
	return _changeColumns;
}

std::string NdbOperationCondition::getTableName()
{
	return _tableName;
}




