/*
 * NdbOperationTransaction.h
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#ifndef NDBOPERATIONTRANSACTION_H_
#define NDBOPERATIONTRANSACTION_H_

#include <NdbApi.hpp>

class NdbOperationTransaction
{
public:
	NdbOperationTransaction();
	virtual ~NdbOperationTransaction();
	void startTransaction();
	NdbTransaction* getNdbTransaction();
private:
	Ndb* _ndb;
	NdbTransaction* _ndbTrans;
};

#endif /* NDBOPERATIONTRANSACTION_H_ */
