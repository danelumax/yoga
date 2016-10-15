/*
 * XmlDAOFactory.cpp
 *
 *  Created on: Oct 15, 2016
 *      Author: eliwech
 */

#include "XmlDAOFactory.h"
#include "XmlMainDAOImpl.h"
#include "XmlDetailDAOImpl.h"

XmlDAOFactory::XmlDAOFactory()
{
}

XmlDAOFactory::~XmlDAOFactory()
{
}

OrderMainDAO* XmlDAOFactory::createOrderMainDAO()
{
	return new XmlMainDAOImpl();
}

OrderDetailDAO* XmlDAOFactory::createOrderDetailDAO()
{
	return new XmlDetailDAOImpl();
}
