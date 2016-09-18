/*
 * NdbDao.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef NDBDAO_H_
#define NDBDAO_H_

#include <vector>
#include "ResultSet.h"
#include "Transaction.h"
#include "Modification.h"
#include "SearchOption.h"
#include "NdbSearchOption.h"
#include "NdbOperationCondition.h"
#include "NdbOperationTransaction.h"

static const int RE_DAO_SUC = 0;
static const int RE_DAO_UNAVAILABLE = -1;
static const int RE_DAO_ERROR = -2;

class NdbDao
{
public:
    enum QUERY_PURPOSE
    {
        QUERY_TO_DELETE=1
    };
	NdbDao(Transaction* trans);
	virtual ~NdbDao();
	//int find(SearchOption& query, ResultSet& record);
	int find(SearchOption& searchOption, std::vector<ResultSet>& records);
	int insert(Modification& record);
private:
	NdbOperationTransaction* convertTransaction(Transaction* trans);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);
	int mapToNdbSearchOption(SearchOption& searchOption, NdbSearchOption& ndbSearchOption);
private:
	Transaction* _trans;
};

#endif /* NDBDAO_H_ */
