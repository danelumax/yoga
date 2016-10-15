/*
 * XmlDAOFactory.h
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#ifndef XMLDAOFACTORY_H_
#define XMLDAOFACTORY_H_

#include "DAOFactory.h"

class XmlDAOFactory : public DAOFactory
{
public:
	XmlDAOFactory();
	virtual ~XmlDAOFactory();
	virtual OrderMainDAO* createOrderMainDAO();
	virtual OrderDetailDAO* createOrderDetailDAO();
};

#endif /* XMLDAOFACTORY_H_ */
