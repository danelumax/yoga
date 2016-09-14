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
    enum QUERY_PURPOSE
    {
        QUERY_TO_DELETE=1
    };
	NdbDao();
	virtual ~NdbDao();
	int insert(Modification& record);
	int buildChangeParameters(Modification* change, NdbOperationCondition &noc);
};

#endif /* NDBDAO_H_ */
