/*
 * NdbAbstractExecutor.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBABSTRACTEXECUTOR_H_
#define NDBABSTRACTEXECUTOR_H_

#include <iostream>
#include <Dao.h>
#include <NdbApi.hpp>
#include <NdbOperationTransaction.h>
#include <NdbOperationCondition.h>

class NdbAbstractExecutor
{
public:
	NdbAbstractExecutor(NdbOperationCondition& opCondition, NdbOperationTransaction* transaction = NULL);
	virtual ~NdbAbstractExecutor();
	int execute();
	NdbRecAttr** getQuerySpace();
	void setQuerySpace(NdbRecAttr* attr);
private:
	int execute(Ndb* ndb, NdbTransaction* ndbTransaction);
	int setNdbOperationType(NdbOperationCondition* opCondition,
							const NdbDictionary::Table * &myTable,
							NdbTransaction* &myTrans,
							NdbOperation * &myOp);
	int setNdbOperationActivity(NdbOperation* &oper);
	int prepareKeyNdbOperation(NdbOperation * &myOp, NdbOperationCondition* opCondition);
	int prepareNdbOperation(NdbOperation * &myOp, NdbOperationCondition* opCondition);
	int executeNdbTransaction(NdbTransaction* &trans);
private:
	NdbOperationCondition* _opCondition;
    NdbOperationTransaction* _transaction;
    bool _selfControlTransaction;
    NdbRecAttr** _ptr_attrs;
};

#endif /* NDBABSTRACTEXECUTOR_H_ */
