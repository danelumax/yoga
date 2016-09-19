/*
 * NdbDao.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef NDBDAO_H_
#define NDBDAO_H_

#include <vector>
#include "Dao.h"
#include "ResultSet.h"
#include "Transaction.h"
#include "Modification.h"
#include "SearchOption.h"
#include "NdbSearchOption.h"
#include "NdbOperationCondition.h"
#include "NdbOperationTransaction.h"

class NdbDao : public Dao
{
public:
    enum QUERY_PURPOSE
    {
        QUERY_TO_DELETE=1
    };
	NdbDao(Transaction* trans);
	virtual ~NdbDao();
	//int find(SearchOption& query, ResultSet& record);
	virtual int find(SearchOption& searchOption, std::vector<ResultSet>& records);
	virtual int insert(Modification& record);
private:
	NdbOperationTransaction* convertTransaction(Transaction* trans);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);
	int mapToNdbSearchOption(SearchOption& searchOption, NdbSearchOption& ndbSearchOption);
};

#endif /* NDBDAO_H_ */
