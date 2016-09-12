/*
 * NdbDao.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef NDBDAO_H_
#define NDBDAO_H_

#include "Modification.h"
#include "NdbOperationCondition.h"

class NdbDao
{
public:
	NdbDao();
	virtual ~NdbDao();
	int insert(Modification& record);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);
};

#endif /* NDBDAO_H_ */
