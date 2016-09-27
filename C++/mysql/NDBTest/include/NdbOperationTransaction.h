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
	int startTransaction();
	int commitTransaction();
	NdbTransaction* getNdbTransaction();
	Ndb* getNdb();
	void close();
private:
	Ndb* _ndb;
	NdbTransaction* _ndbTrans;
};

#endif /* NDBOPERATIONTRANSACTION_H_ */
