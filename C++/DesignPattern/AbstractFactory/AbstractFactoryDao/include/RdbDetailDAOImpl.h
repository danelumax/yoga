/*
 * RdbDetailDAOImpl.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef RDBDETAILDAOIMPL_H_
#define RDBDETAILDAOIMPL_H_

#include "OrderDetailDAO.h"

class RdbDetailDAOImpl : public OrderDetailDAO
{
public:
	RdbDetailDAOImpl();
	virtual ~RdbDetailDAOImpl();
	virtual void saveOrderDetail();
};

#endif /* RDBDETAILDAOIMPL_H_ */
