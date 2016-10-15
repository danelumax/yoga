/*
 * DAOFactory.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef DAOFACTORY_H_
#define DAOFACTORY_H_

#include "OrderMainDAO.h"
#include "OrderDetailDAO.h"

class DAOFactory
{
public:
	virtual OrderMainDAO* createOrderMainDAO() = 0;
	virtual OrderDetailDAO* createOrderDetailDAO() = 0;
};

#endif /* DAOFACTORY_H_ */
