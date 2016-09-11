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
