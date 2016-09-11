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

int NdbAbstractExecutor::execute(int i)
{
	if (_selfControlTransaction)
	{
		_transaction->startTransaction();
	}

	Ndb* ndb = _transaction->getNdb();
	NdbTransaction* ndbTransaction = _transaction->getNdbTransaction();

	int result = execute(ndb, ndbTransaction, i);

	return result;
}

int NdbAbstractExecutor::execute(Ndb* ndb, NdbTransaction* ndbTransaction,int i)
{
	/* obtain an object for retrieving or manipulating database schema information */
	const NdbDictionary::Dictionary* myDict= ndb->getDictionary();
	/* access the table with a known name */
	const NdbDictionary::Table *myTable= myDict->getTable("api_simple");

	NdbTransaction* myTrans = ndbTransaction;

	NdbOperation *myOperation = NULL;
	NdbUtils::setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	/* an INSERT operation */
	NdbUtils::setNdbOperationActivity(myOperation, *_opCondition);

	/* search condition
	* insert ATTR2 value in ATTR1 == i
	* */
	NdbColumnCondition *cqf = new NdbColumnCondition("ATTR1", i);
	NdbUtils::setKeyNdbOperationInfo(myOperation, cqf);

	cqf = new NdbColumnCondition("ATTR2", i);
	NdbUtils::prepareNdbOperationValues(myOperation, cqf);

	/* Before you want to use any operation within the same transaction, you must initialize them this "getNdbOperation" */
	NdbUtils::setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	/* an INSERT operation */
	NdbUtils::setNdbOperationActivity(myOperation, *_opCondition);
	/* 5~10 */
	cqf = new NdbColumnCondition("ATTR1", i+5);
	NdbUtils::setKeyNdbOperationInfo(myOperation, cqf);

	cqf = new NdbColumnCondition("ATTR2", i+5);
	NdbUtils::prepareNdbOperationValues(myOperation, cqf);

	/* execute a transaction, and execute operation in this trans */
	NdbUtils::executeNdbTransaction(myTrans,
									NdbTransaction::Commit,
									NdbOperation::AbortOnError);

	ndb->closeTransaction(myTrans);

	return 0;
}

