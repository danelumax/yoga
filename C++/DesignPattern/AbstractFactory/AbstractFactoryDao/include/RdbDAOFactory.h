/*
 * RdbDAOFactory.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef RDBDAOFACTORY_H_
#define RDBDAOFACTORY_H_

#include "DAOFactory.h"

class RdbDAOFactory : public DAOFactory
{
public:
	RdbDAOFactory();
	virtual ~RdbDAOFactory();
	virtual OrderMainDAO* createOrderMainDAO();
	virtual OrderDetailDAO* createOrderDetailDAO();
};

#endif /* RDBDAOFACTORY_H_ */
