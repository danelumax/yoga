/*
 * NdbAbstractExecutor.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBABSTRACTEXECUTOR_H_
#define NDBABSTRACTEXECUTOR_H_

#include <iostream>
#include <NdbApi.hpp>
#include <NdbOperationTransaction.h>
#include <NdbOperationCondition.h>

class NdbAbstractExecutor {
public:
	NdbAbstractExecutor(NdbOperationCondition& opCondition, NdbOperationTransaction* transaction = NULL);
	virtual ~NdbAbstractExecutor();
	int execute();
private:
	int execute(Ndb* ndb, NdbTransaction* ndbTransaction);
	int setNdbOperationActivity(NdbOperation* &oper);
private:
	NdbOperationCondition* _opCondition;
    NdbOperationTransaction* _transaction;
    bool _selfControlTransaction;
};

#endif /* NDBABSTRACTEXECUTOR_H_ */
