/*
 * NdbAbstractExecutor.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "NdbAbstractExecutor.h"
#include <iostream>
#include "NdbUtils.h"

NdbAbstractExecutor::NdbAbstractExecutor(NdbOperationCondition& opCondition, NdbOperationTransaction* transaction)
	:_opCondition(&opCondition),
	 _transaction(transaction),
	 _selfControlTransaction(false)
{
	if (_transaction == NULL)
	{
		_transaction = new NdbOperationTransaction();
		_selfControlTransaction = true;
	}
}

NdbAbstractExecutor::~NdbAbstractExecutor()
{
	if (_selfControlTransaction && _transaction)
	{
		delete _transaction;
		_transaction = NULL;
	}
}

int NdbAbstractExecutor::execute()
{
	if (_selfControlTransaction)
	{
		_transaction->startTransaction();
	}

	Ndb* ndb = _transaction->getNdb();
	NdbTransaction* ndbTransaction = _transaction->getNdbTransaction();

	int result = execute(ndb, ndbTransaction);

	return result;
}

int NdbAbstractExecutor::execute(Ndb* ndb, NdbTransaction* ndbTransaction)
{
	/* obtain an object for retrieving or manipulating database schema information */
	const NdbDictionary::Dictionary* myDict= ndb->getDictionary();
	/* access the table with a known name */
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	NdbTransaction* myTrans = ndbTransaction;

	NdbOperation *myOperation = NULL;
	NdbUtils::setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	/* an INSERT operation */
	setNdbOperationActivity(myOperation);

	/* search condition
	* insert ATTR2 value in ATTR1 == i
	* */
	std::vector<NdbColumnCondition*> columnVector = _opCondition->getChangeColumns();
	std::vector<NdbColumnCondition*>::iterator iter = columnVector.begin();
	for(; iter!=columnVector.end(); ++iter)
	{
		NdbColumnCondition *cqf = *iter;
		NdbUtils::setKeyNdbOperationInfo(myOperation, cqf);
	}

	NdbUtils::prepareNdbOperationValues(myOperation, _opCondition);

//	/* Before you want to use any operation within the same transaction, you must initialize them this "getNdbOperation" */
//	NdbUtils::setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	/* execute a transaction, and execute operation in this trans */
	NdbUtils::executeNdbTransaction(myTrans,
									NdbTransaction::Commit,
									NdbOperation::AbortOnError);

	ndb->closeTransaction(myTrans);

	return 0;
}

int NdbAbstractExecutor::setNdbOperationActivity(NdbOperation *& oper)
{
	return NdbUtils::setNdbOperationActivity(oper, *_opCondition);
}



