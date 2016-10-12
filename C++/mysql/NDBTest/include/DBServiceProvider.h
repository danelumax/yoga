/*
 * DBServiceProvider.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef DBSERVICEPROVIDER_H_
#define DBSERVICEPROVIDER_H_

#include <vector>
#include "Dao.h"
#include "ResultSet.h"
#include "Modification.h"
#include "Transaction.h"
#include "SearchOption.h"

class DBServiceProvider
{
public:
	virtual ~DBServiceProvider();
	static DBServiceProvider* getInstance();
	static void destory();
	int find(SearchOption& searchOption, ResultSet& record);
	int find(SearchOption& searchOption, std::vector<ResultSet>& records);
	int insert(Modification& record);
	Dao* getDao(const std::string& key, Transaction* transaction = NULL);
	Transaction* startTransaction();
	void closeTransaction(Transaction* transaction);
private:
	DBServiceProvider();
	static DBServiceProvider* _instance;
};

#endif /* DBSERVICEPROVIDER_H_ */
