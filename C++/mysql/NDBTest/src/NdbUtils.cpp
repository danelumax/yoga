/*
 * NdbUtils.cpp
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#include "NdbUtils.h"
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <NdbWrapperCode.h>


int NdbUtils::executeNdbTransaction(NdbTransaction *& trans,
									NdbTransaction::ExecType execType,
									NdbOperation::AbortOption abortOp)
{
	if (trans->execute(execType, abortOp, 1) != 0)
	{
		std::cout << "NdbUtils::executeNdbTransaction ndb error\n\n" << std::endl;
		if (trans->getNdbError().code == NDB_ERR_NO_DATA)
		{
			std::cout << "NdbUtils::executeNdbTransaction result: no data found" << std::endl;
			return RE_DAO_NO_DATA;
		}
	}

	if (trans->getNdbError().classification == NdbError::NoDataFound)
	{
		std::cout << "### Detected that deleted tuple doesn't exist! ###" << std::endl;
	}

	return RE_NDB_SUC;
}

int NdbUtils::setNdbOperationType(NdbOperationCondition* opCondition,
								  const NdbDictionary::Table * &myTable,
                                  NdbTransaction* &myTrans,
                                  NdbOperation * &myOp)
{
	if (NULL == opCondition)
	{
		std::cout << "NdbUtils::setNdbOperationType invalid operation condition NULL argument." << std::endl;
		return -1;
	}
	bool singleRowOp = opCondition->isSingleRowOpearation();
	if (singleRowOp)
	{
		myOp = myTrans->getNdbOperation(myTable);
	}

	if (NULL == myOp)
	{
		std::cout << "NdbUtils::setNdbOperationType ndb error" << std::endl;
		return -1;
	}
	return 0;
}

int NdbUtils::setNdbOperationActivity(NdbOperation * &oper, NdbOperationCondition& noc)
{
	NdbOperationCondition::Type opType = noc.getType();
	switch(opType)
	{
		case NdbOperationCondition::QUERY_SINGLE:
		{
			if (oper->readTuple(NdbOperation::LM_CommittedRead) != 0)
			{
				std::cout << "NdbUtils::setNdbOperationActivity QUERY_SINGLE tuple ndb error" << std::endl;
				return -1;
			}
			break;
		}
		case NdbOperationCondition::INSERT:
		{
			if (oper->insertTuple() != 0)
			{
				std::cout << "NdbUtils::setNdbOperationActivity INSERT tuple ndb error" << std::endl;
				return -1;
			}
			break;
		}
		case NdbOperationCondition::DELETE_SINGLE:
		{
			if (oper->deleteTuple() != 0)
			{
				std::cout << "NdbUtils::setNdbOperationActivity DELETE_SINGLE tuple ndb error" << std::endl;
				return -1;
			}
			break;
		}
		default:
		{
			return -1;
		}
	}

	return 0;
}

int NdbUtils::prepareKeyNdbSingleOp(NdbOperation* oper, NdbOperationCondition* opCondition)
{
	std::vector<NdbColumnCondition*> columnVector;

	if (opCondition->getType() == NdbOperationCondition::INSERT)
	{
		if (!opCondition->hasChangeColumn())
		{
			std::cout << "NdbUtils::prepareKeyNdbSingleOp to insert action, no available column found." << std::endl;
			return -1;
		}
		columnVector = opCondition->getChangeColumns();
	}
	else
	{
		if (!opCondition->hasQueryColumn())
		{
			std::cout << "NdbUtils::prepareKeyNdbSingleOp the condition has no available query column." << std::endl;
			return -1;
		}
		columnVector = opCondition->getQueryColumns();
	}

	std::vector<NdbColumnCondition*>::iterator iter = columnVector.begin();
	for(; iter!=columnVector.end(); ++iter)
	{
		NdbColumnCondition *cqf = *iter;
		NdbUtils::setKeyNdbOperationInfo(oper, cqf);
	}

	return 0;
}

int NdbUtils::setKeyNdbOperationInfo(NdbOperation * &myOp, NdbColumnCondition* cqf)
{
	int tempValue = atoi((cqf->getColumnValue()).c_str());

//	std::cout << "NdbUtils::setKeyNdbOperationInfo tostring:"
//			  << "\tkey:" << cqf->getColumnName()
//			  << "\tvalue:" << tempValue << std::endl;

	/*
	 * search condition
	 * insert ATTR2 value in ATTR1 == i
	 * */
	if (myOp->equal(cqf->getColumnName(), tempValue) != 0)
	{
		std::cout << "NdbUtils::setKeyNdbOperationInfo equal failed" << std::endl;
		return -1;
	}

	return 0;
}

int NdbUtils::prepareNdbOperationValues(NdbOperation* myOp, NdbOperationCondition* opCondition)
{
	std::vector<NdbColumnCondition*> columnVector = opCondition->getChangeColumns();
	std::vector<NdbColumnCondition*>::iterator iter = columnVector.begin();
	for(; iter!=columnVector.end(); ++iter)
	{
		NdbColumnCondition *cqf = *iter;

		int tempValue = atoi((cqf->getColumnValue()).c_str());
		if (myOp->setValue("ATTR2", tempValue) != 0)
		{
			std::cout << "NdbUtils::prepareNdbOperationValues setValue failed" << std::endl;
		}
	}

	return 0;
}

int NdbUtils::prepareNdbOperationQuerySpace(NdbOperation* oper,
											NdbOperationCondition* opCondition,
											NdbAbstractExecutor* queryExecutor)
{
	std::string tableName = opCondition->getTableName();
	NdbRecAttr** querySpace = queryExecutor->getQuerySpace();
	querySpace[0] = oper->getValue("ATTR2", NULL);
	//queryExecutor->setQuerySpace(querySpace);
	if (NULL == queryExecutor->getQuerySpace())
	{
		std::cout << "NdbUtils::prepareNdbOperationQuerySpace error" << std::endl;
		return -1;
	}

	return 0;
}

bool NdbUtils::isValidColumnName(const std::string& columnName)
{
	bool ret = false;
	if (columnName.compare(SEARCH_OPTION_QUERY_TYPE)!= 0)
	{
		ret = true;
	}

	return ret;
}

int NdbUtils::getValue(NdbRecAttr* ndbRecAttr, std::string& sink)
{
	if (NULL == ndbRecAttr)
	{
		std::cout << "NdbUtils::getValue invalid NULL argument." << std::endl;
		return -1;
	}

	std::ostringstream oss;
	if (0 == ndbRecAttr->isNULL())
	{
		oss << ndbRecAttr->u_32_value();
	}

	sink = oss.str();

	return 0;
}

NdbRecAttr* NdbUtils::findNdbRecAttr(NdbRecAttr** querySpace)
{
	NdbRecAttr* ndbRecAttr = NULL;

	ndbRecAttr = querySpace[0];

	if (NULL == ndbRecAttr)
	{
		std::cout << "NdbUtils::findNdbRecAttr No NdbRecAttr found" << std::endl;
	}

	return ndbRecAttr;
}

int NdbUtils::sinkValues(NdbAbstractExecutor* queryExecutor, NdbRowData& sink)
{
	std::string valueSink("");
	NdbRecAttr** querySpace = queryExecutor->getQuerySpace();

	NdbRecAttr* ndbRecAttr = findNdbRecAttr(querySpace);

	getValue(ndbRecAttr, valueSink);

	sink.addValue("ATTR2", valueSink);

	return RE_NDB_SUC;
}
