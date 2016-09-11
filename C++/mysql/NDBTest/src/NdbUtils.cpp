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
		std::cout << "NdbUtils::executeNdbTransaction ndb error:" << std::endl;
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
			oper->insertTuple();
			break;
		}
	}

	return 0;
}

int NdbUtils::setKeyNdbOperationInfo(NdbOperation * &myOp, NdbColumnCondition* cqf)
{
	myOp->equal(cqf->getColumnName(), cqf->getColumnValue());

	return 0;
}

int NdbUtils::prepareNdbOperationValues(NdbOperation* myOp, NdbColumnCondition* cqf)
{
	myOp->setValue(cqf->getColumnName(), cqf->getColumnValue());

	return 0;
}
