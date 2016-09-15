/*
 * VernalNdbTransaction.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef VERNALNDBTRANSACTION_H_
#define VERNALNDBTRANSACTION_H_

#include "Transaction.h"
#include "NdbOperationTransaction.h"

class VernalNdbTransaction : public Transaction
{
public:
	VernalNdbTransaction();
	virtual ~VernalNdbTransaction();
	virtual int start();
	virtual int commit();
	NdbOperationTransaction* getNdbTransaction();
private:
	NdbOperationTransaction* _ndbTrans;
};

#endif /* VERNALNDBTRANSACTION_H_ */
