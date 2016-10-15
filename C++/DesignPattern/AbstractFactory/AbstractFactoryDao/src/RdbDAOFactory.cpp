/*
 * RdbDAOFactory.cpp
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#include "RdbDAOFactory.h"
#include "RdbMainDAOImpl.h"
#include "RdbDetailDAOImpl.h"

RdbDAOFactory::RdbDAOFactory()
{
}

RdbDAOFactory::~RdbDAOFactory()
{
}

OrderMainDAO* RdbDAOFactory::createOrderMainDAO()
{
	return new RdbMainDAOImpl();
}

OrderDetailDAO* RdbDAOFactory::createOrderDetailDAO()
{
	return new RdbDetailDAOImpl();
}
