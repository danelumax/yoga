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
	:Dao(trans)
{
}

NdbDao::~NdbDao()
{
}


int NdbDao::find(SearchOption & searchOption, std::vector<ResultSet> & records)
{
	/* convert search option to NDB special search option */
	NdbSearchOption query;
	if (mapToNdbSearchOption(searchOption, query) != 0)
	{
		return RE_DAO_ERROR;
	}

	std::string tableName = query.getTable();
	NdbOperationCondition::Type ndbOpType = NdbOperationCondition::UNKNOWN_OP;
	buildQueryFilterType(query, NdbDao::PURE_QUERY, ndbOpType);

	/* just for test */
	std::cout << query.getType() << std::endl;
	std::vector<SearchOption::SearchCriteria*> criteriaVec = query.getCriteriaVector();
	std::vector<SearchOption::SearchCriteria*>::iterator iter = criteriaVec.begin();
	for(; iter!=criteriaVec.end(); ++iter)
	{
		SearchOption::SearchCriteria* searchCriteria = *iter;
		{
			if (searchCriteria)
			{
				std::cout << searchCriteria->key << " " << searchCriteria->type << " " << searchCriteria->value << std::endl;
			}
		}
	}
	std::cout << "ndbOpType :" << ndbOpType << std::endl;
	/* test finished */

	std::vector<NdbColumnCondition*> tempVector;
	NdbOperationTransaction* ndbOpTransaction = convertTransaction(_trans);

	NdbOperationCondition noc(tableName, ndbOpType);
	NdbAbstractExecutor executor(noc, ndbOpTransaction);

	return 0;
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

int NdbDao::mapToNdbSearchOption(SearchOption & searchOption, NdbSearchOption & ndbSearchOption)
{
	ndbSearchOption.setTable(searchOption.getTable());

	std::string queryType;
	NdbSearchOption::Type ndbQueryType = NdbSearchOption::T_UNKNOWN;
	if (searchOption.getCriteria(SEARCH_OPTION_QUERY_TYPE, queryType) != 0)
	{
		return -1;
	}

	if (queryType.compare(SEARCH_OPTION_QUERY_TYPE_SINGLE_PK) == 0)
	{
		ndbQueryType = NdbSearchOption::T_SINGLE_PK;
	}

	ndbSearchOption.setType(ndbQueryType);

	std::vector<SearchOption::SearchCriteria*> criteriaVec = searchOption.getCriteriaVector();
	std::vector<SearchOption::SearchCriteria*>::iterator iter = criteriaVec.begin();
	for(; iter!=criteriaVec.end(); ++iter)
	{
		SearchOption::SearchCriteria* searchCriteria = *iter;
		{
			if (searchCriteria)
			{
				ndbSearchOption.addCriteria(searchCriteria->key, searchCriteria->type, searchCriteria->value);
			}
		}
	}

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

int NdbDao::buildQueryFilterType(NdbSearchOption & query,
								 NdbDao::QUERY_PURPOSE queryPurpose,
								 NdbOperationCondition::Type &ndbOpType)
{
	NdbSearchOption::Type queryType = query.getType();
	switch(queryType)
	{
		case NdbSearchOption::T_SINGLE_PK:
		{
			if (queryPurpose == NdbDao::PURE_QUERY)
			{
				ndbOpType = NdbOperationCondition::QUERY_SINGLE;
			}
		}
		default:
		{
			return RE_DAO_ERROR;
		}
	}
	return RE_DAO_SUC;
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

