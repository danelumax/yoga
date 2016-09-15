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
#include "VernalNdbTransaction.h"

NdbDao::NdbDao(Transaction* trans)
	:_trans(trans)
{
}

NdbDao::~NdbDao()
{
}

int NdbDao::insert(Modification& record)
{
	std::string tableName = record.getTable();
	NdbOperationCondition noc(tableName, NdbOperationCondition::INSERT);
	buildChangeParameters(&record, noc);

	NdbOperationTransaction* ndbOpTransaction = convertTransaction(_trans);
	NdbAbstractExecutor executor(noc, ndbOpTransaction);
	executor.execute();

	return 0;
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

	return 0;
}

NdbOperationTransaction* NdbDao::convertTransaction(Transaction* trans)
{
    NdbOperationTransaction* ndbOpTransaction = NULL;

    if(trans != NULL)
    {
        ndbOpTransaction = (dynamic_cast<VernalNdbTransaction*>(trans))->getNdbTransaction();
    }

    return ndbOpTransaction;
}




