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
		std::cout << "_transaction is null" << std::endl;
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

	std::string table = _opCondition->getTableName();
	/* access the table with a known name */
	const NdbDictionary::Table *myTable= myDict->getTable(table.c_str());

	NdbTransaction* myTrans = ndbTransaction;

	NdbOperation *myOperation = NULL;
	setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	/* an INSERT operation */
	setNdbOperationActivity(myOperation);

	/* equal */
	prepareKeyNdbOperation(myOperation, _opCondition);

	/* setValue */
	prepareNdbOperation(myOperation, _opCondition);

//	/* Before you want to use any operation within the same transaction, you must initialize them this "getNdbOperation" */
//	NdbUtils::setNdbOperationType(_opCondition, myTable, myTrans, myOperation);

	if (_selfControlTransaction)
	{
		/* execute a transaction, and execute operation in this trans */
		executeNdbTransaction(myTrans);
	}

	return 0;
}

int NdbAbstractExecutor::setNdbOperationType(NdbOperationCondition* opCondition,
											 const NdbDictionary::Table * &myTable,
											 NdbTransaction* &myTrans,
											 NdbOperation * &myOp)
{
	NdbUtils::setNdbOperationType(opCondition, myTable, myTrans, myOp);

	return 0;
}

int NdbAbstractExecutor::setNdbOperationActivity(NdbOperation *& oper)
{
	return NdbUtils::setNdbOperationActivity(oper, *_opCondition);
}

int NdbAbstractExecutor::prepareKeyNdbOperation(NdbOperation * &myOp, NdbOperationCondition* opCondition)
{
	if (opCondition->isSingleRowOpearation())
	{
		NdbUtils::prepareKeyNdbSingleOp(myOp, opCondition);
	}

	return 0;
}

int NdbAbstractExecutor::prepareNdbOperation(NdbOperation * &myOp, NdbOperationCondition* opCondition)
{
	NdbOperationCondition::Type opType = opCondition->getType();

	switch(opType)
	{
		case NdbOperationCondition::INSERT:
		{
			NdbUtils::prepareNdbOperationValues(myOp, opCondition);
		}
		default:
		{
			return -1;
		}
	}

	return 0;
}

int NdbAbstractExecutor::executeNdbTransaction(NdbTransaction* &trans)
{
	NdbOperationCondition::Type opType = _opCondition->getType();

	switch(opType)
	{
		case NdbOperationCondition::INSERT:
		{
			NdbUtils::executeNdbTransaction(trans,
											NdbTransaction::Commit,
											NdbOperation::AbortOnError);
		}
		default:
		{
			return -1;
		}
	}

	return 0;
}


