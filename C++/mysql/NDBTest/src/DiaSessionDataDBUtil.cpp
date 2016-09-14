/*
 * DiaSessionDataDBUtil.cpp
 *
 *  Created on: Sep 13, 2016
 *      Author: eliwech
 */

#include "DiaSessionDataDBUtil.h"

#include "Modification.h"
#include "DBServiceProvider.h"

/**************************************************************************
 * insert 10 tuples in table: (0,0),(1,1),...,(9,9) *
 **************************************************************************/
int DiaSessionDataDBUtil::insertSessionDataToDB()
{
	Modification modify;
	for (int i = 0; i < 10; i++)
	{
		Modification modify;
		modify.addValue("ATTR1", i);
		//modify.addValue("ATTR2", i);
		DBServiceProvider::getInstance()->insert(modify);
	}

	return 0;
}


