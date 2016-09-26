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
#include "NdbRowData.h"
#include "Transaction.h"
#include "Modification.h"
#include "SearchOption.h"
#include "NdbSearchOption.h"
#include "NdbAbstractExecutor.h"
#include "NdbOperationCondition.h"
#include "NdbOperationTransaction.h"

class NdbDao : public Dao
{
public:
    enum QUERY_PURPOSE
    {
        PURE_QUERY = 1,
    	QUERY_TO_DELETE
    };
	NdbDao(Transaction* trans);
	virtual ~NdbDao();
	//int find(SearchOption& query, ResultSet& record);
	virtual int find(SearchOption& searchOption, std::vector<ResultSet>& records);
	virtual int insert(Modification& record);
	virtual int remove(SearchOption& searchOption);
private:
	NdbOperationTransaction* convertTransaction(Transaction* trans);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);

	int buildQueryFilterType(NdbSearchOption &query,
							 NdbDao::QUERY_PURPOSE queryPurpose,
							 NdbOperationCondition::Type &ndbOpType);

	int buildQueryFilterCond(SearchOption::CRITERIA_TYPE &ct,
							 NdbColumnCondition::Condition &cond);

	int buildQueryFilterContent(NdbSearchOption& query, NdbOperationCondition& queryFilter);

	int buildQueryResult(NdbAbstractExecutor* queryExecutor, std::vector<ResultSet>& records);

	int mapToNdbSearchOption(SearchOption& searchOption, NdbSearchOption& ndbSearchOption);

	void mapNdbRowDataToResultSet(NdbRowData& rowData, ResultSet& resultSet);

	int convertReturnCode(int ndbReturnCode);

};

#endif /* NDBDAO_H_ */
