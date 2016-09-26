/*
 * Dao.h
 *
 *  Created on: Sep 19, 2016
 *      Author: eliwech
 */

#ifndef DAO_H_
#define DAO_H_

#include "ResultSet.h"
#include "Transaction.h"
#include "SearchOption.h"
#include "Modification.h"

static const int RE_DAO_SUC = 0;
static const int RE_DAO_UNAVAILABLE = -1;
static const int RE_DAO_ERROR = -2;
static const int RE_DAO_NO_DATA = -3;
static const int RE_DAO_INVALID_ARGUMENT = -5;

class Dao
{
public:
	Dao(Transaction* trans);
	virtual ~Dao();
	virtual int find(SearchOption& searchOption, std::vector<ResultSet>& records) = 0;
	virtual int insert(Modification& record) = 0;
	virtual int remove(SearchOption& searchOption) = 0;
protected:
	Transaction* _trans;
};

#endif /* DAO_H_ */
