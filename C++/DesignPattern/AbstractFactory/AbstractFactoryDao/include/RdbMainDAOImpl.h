/*
 * RdbMainDAOImpl.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef RDBMAINDAOIMPL_H_
#define RDBMAINDAOIMPL_H_

#include "OrderMainDAO.h"

class RdbMainDAOImpl : public OrderMainDAO
{
public:
	RdbMainDAOImpl();
	virtual ~RdbMainDAOImpl();
	virtual void saveOrderMain();
};

#endif /* RDBMAINDAOIMPL_H_ */
