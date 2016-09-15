/*
 * NdbDao.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef NDBDAO_H_
#define NDBDAO_H_

#include "Transaction.h"
#include "Modification.h"
#include "NdbOperationCondition.h"
#include "NdbOperationTransaction.h"

class NdbDao
{
public:
    enum QUERY_PURPOSE
    {
        QUERY_TO_DELETE=1
    };
	NdbDao(Transaction* trans);
	virtual ~NdbDao();
	int insert(Modification& record);
private:
	NdbOperationTransaction* convertTransaction(Transaction* trans);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);
private:
	Transaction* _trans;
};

#endif /* NDBDAO_H_ */
