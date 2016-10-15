//============================================================================
// Name        : AbstractFactoryDao.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "RdbDAOFactory.h"
#include "XmlDAOFactory.h"

int main()
{
	std::cout << "\nTest Rdb DAO ..." << std::endl;
	DAOFactory* df = new RdbDAOFactory();

	OrderMainDAO* mainDAO = df->createOrderMainDAO();
	OrderDetailDAO* detailDAO = df->createOrderDetailDAO();

	mainDAO->saveOrderMain();
	detailDAO->saveOrderDetail();

	std::cout << "\nTest Xml DAO ..." << std::endl;
	df = new XmlDAOFactory();

	mainDAO = df->createOrderMainDAO();
	detailDAO = df->createOrderDetailDAO();

	mainDAO->saveOrderMain();
	detailDAO->saveOrderDetail();

	delete detailDAO;
	delete mainDAO;
	delete df;

	return 0;
}
