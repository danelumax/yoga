/*
 * NdbDao.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "NdbDao.h"
#include <map>
#include <string>
#include <iostream>
#include "NdbOperationCondition.h"
#include "NdbAbstractExecutor.h"

NdbDao::NdbDao() {
	// TODO Auto-generated constructor stub

}

NdbDao::~NdbDao() {
	// TODO Auto-generated destructor stub
}

int NdbDao::insert(Modification& record)
{
	NdbOperationCondition noc(NdbOperationCondition::INSERT);
	buildChangeParameters(&record, noc);
	NdbAbstractExecutor executor(noc, NULL);
	executor.execute();
}

int NdbDao::buildChangeParameters(Modification *change, NdbOperationCondition & noc)
{
	std::map<std::string, int> values = change->getValues();
	std::map<std::string, int>::iterator iter = values.begin();
	for(; iter!=values.end(); ++iter)
	{
		std::string colName = iter->first;
		int colValue = iter->second;
		NdbColumnCondition *column = new NdbColumnCondition(colName, colValue);
		noc.addChangeColumn(column);
	}
}




