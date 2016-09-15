/*
 * NdbUtils.cpp
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#include "NdbUtils.h"
#include <iostream>



int NdbUtils::executeNdbTransaction(NdbTransaction *& trans,
									NdbTransaction::ExecType execType,
									NdbOperation::AbortOption abortOp)
{
	if (trans->execute(execType, abortOp, 1) < 0)
	{
		std::cout << "NdbUtils::executeNdbTransaction ndb error\n\n" << std::endl;
		return -1;
	}

	return 0;
}

int NdbUtils::setNdbOperationType(NdbOperationCondition* opCondition,
								  const NdbDictionary::Table * &myTable,
                                  NdbTransaction* &myTrans,
                                  NdbOperation * &myOp)
{
	bool singleRowOp = opCondition->isSingleRowOpearation();
	if (singleRowOp)
	{
		myOp = myTrans->getNdbOperation(myTable);
	}
	return 0;
}

int NdbUtils::setNdbOperationActivity(NdbOperation * &oper, NdbOperationCondition& noc)
{
	NdbOperationCondition::Type opType = noc.getType();
	switch(opType)
	{
		case NdbOperationCondition::INSERT:
		{
			if (oper->insertTuple() != 0)
			{
				std::cout << "NdbUtils::setNdbOperationActivity INSERT tuple ndb error" << std::endl;
				return -1;
			}
			break;
		}
	}

	return 0;
}

int NdbUtils::prepareKeyNdbSingleOp(NdbOperation* oper, NdbOperationCondition* opCondition)
{
	std::vector<NdbColumnCondition*> columnVector = opCondition->getChangeColumns();
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
    /*
	 * search condition
	 * insert ATTR2 value in ATTR1 == i
	 * */
	if (myOp->equal(cqf->getColumnName(), cqf->getColumnValue()) != 0)
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
		if (myOp->setValue("ATTR2", cqf->getColumnValue()) != 0)
		{
			std::cout << "NdbUtils::prepareNdbOperationValues setValue failed" << std::endl;
		}
	}

	return 0;
}
