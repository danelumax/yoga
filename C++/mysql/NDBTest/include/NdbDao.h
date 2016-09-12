/*
 * NdbDao.h
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#ifndef NDBDAO_H_
#define NDBDAO_H_

class NdbDao
{
public:
	NdbDao();
	virtual ~NdbDao();
	int insert(int i);
};

#endif /* NDBDAO_H_ */
