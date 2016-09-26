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
#include "NdbUtils.h"
#include "NdbWrapperCode.h"
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

	std::vector<NdbColumnCondition*> tempVector;
	NdbOperationTransaction* ndbOpTransaction = convertTransaction(_trans);

	NdbOperationCondition noc(tableName, ndbOpType);
	NdbAbstractExecutor executor(noc, ndbOpTransaction);

	buildQueryFilterContent(query, noc);

	int rt = executor.execute();
	rt = convertReturnCode(rt);

	buildQueryResult(&executor, records);

	return rt;
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

int NdbDao::remove(SearchOption& searchOption)
{
	/* convert search option to NDB special search option */
	NdbSearchOption query;
	if (mapToNdbSearchOption(searchOption, query) != 0)
	{
		return RE_DAO_ERROR;
	}

	std::string tableName = query.getTable();
	NdbOperationCondition::Type ndbOpType = NdbOperationCondition::UNKNOWN_OP;
	buildQueryFilterType(query, NdbDao::QUERY_TO_DELETE, ndbOpType);

	std::vector<NdbColumnCondition*> tempVector;
	NdbOperationTransaction* ndbOpTransaction = convertTransaction(_trans);

	NdbOperationCondition noc(tableName, ndbOpType);
	NdbAbstractExecutor executor(noc, ndbOpTransaction);

	buildQueryFilterContent(query, noc);

	int rt = executor.execute();
	rt = convertReturnCode(rt);

	return rt;
}

int NdbDao::buildQueryFilterContent(NdbSearchOption & query, NdbOperationCondition & queryFilter)
{
	std::vector<SearchOption::SearchCriteria*> conditions = query.getCriteriaVector();
	std::vector<SearchOption::SearchCriteria*>::iterator iter = conditions.begin();
	for(; iter!=conditions.end(); ++iter)
	{
		SearchOption::SearchCriteria* vqc = *iter;
		if (vqc)
		{
			SearchOption::CRITERIA_TYPE ct = vqc->type;
			NdbColumnCondition::Condition cond;
			buildQueryFilterCond(ct, cond);

//			std::cout << "NdbDao::buildQueryFilterContent tostring:"
//					  << "\tkey:" << vqc->key
//					  << "\tvalue:" << vqc->value
//					  << "\tcond:" << cond << std::endl;

			NdbColumnCondition* ncc = new NdbColumnCondition(vqc->key, vqc->value, cond);
			if (queryFilter.addQueryColumn(ncc) != 0)
			{
				std::cout << "NdbDao::buildQueryFilterContent invalid argument" << std::endl;
				delete ncc;
				return RE_DAO_INVALID_ARGUMENT;
			}
		}
	}

	return RE_DAO_SUC;
}

/*
 * map searchOption to ndbSearchOption
 * skip SEARCH_OPTION_QUERY_TYPE query
 * */
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
				/* skip SEARCH_OPTION_QUERY_TYPE */
				if (NdbUtils::isValidColumnName(searchCriteria->key))
				{
					ndbSearchOption.addCriteria(searchCriteria->key, searchCriteria->type, searchCriteria->value);
				}
				else if (!searchOption.isHelpSearchKey(searchCriteria->key))
				{
					std::cout << "NdbDao::mapToNdbSearchOption invalid search argument" << std::endl;
					return -1;
				}
			}
		}
	}

	return 0;
}

int NdbDao::buildChangeParameters(Modification *change, NdbOperationCondition & noc)
{
	std::map<std::string, std::string> values = change->getValues();
	std::map<std::string, std::string>::iterator iter = values.begin();
	for(; iter!=values.end(); ++iter)
	{
		std::string colName = iter->first;
		std::string colValue = iter->second;
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
			else if (queryPurpose == NdbDao::QUERY_TO_DELETE)
			{
				ndbOpType = NdbOperationCondition::DELETE_SINGLE;
			}
			else
			{
				return RE_DAO_INVALID_ARGUMENT;
			}
			break;
		}
		default:
		{
			return RE_DAO_ERROR;
		}
	}
	return RE_DAO_SUC;
}

int NdbDao::buildQueryFilterCond(SearchOption::CRITERIA_TYPE & ct, NdbColumnCondition::Condition & cond)
{
	switch(ct)
	{
		case NdbSearchOption::CT_EQ:
		{
			cond = NdbColumnCondition::COND_EQ;
			break;
		}
	}

	return RE_DAO_SUC;
}

int NdbDao::buildQueryResult(NdbAbstractExecutor* queryExecutor, std::vector<ResultSet>& records)
{
	ResultSet sink;
	NdbRowData rowData;
	NdbUtils::sinkValues(queryExecutor, rowData);

	mapNdbRowDataToResultSet(rowData, sink);

	records.push_back(sink);

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

void NdbDao::mapNdbRowDataToResultSet(NdbRowData& rowData, ResultSet& resultSet)
{
	std::map<std::string, std::string> values = rowData.getValues();
	std::map<std::string, std::string>::iterator iter = values.begin();
	for(; iter!=values.end(); ++iter)
	{
		resultSet.addValue(iter->first, iter->second);
	}
}

int NdbDao::convertReturnCode(int ndbReturnCode)
{
	int rt = RE_DAO_SUC;

	if ( NDB_ERR_NO_DATA == ndbReturnCode)
	{
		std::cout << "NdbDao::convertReturnCode no data found." << std::endl;
		rt = RE_DAO_NO_DATA;
	}

	return rt;
}
