//============================================================================
// Name        : PrototypeNormal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "PersonalOrder.h"
#include "OrderBusiness.h"
#include "EnterpriseOrder.h"

int main()
{
	std::cout << "\nTest Personal Order ..." << std::endl;
	PersonalOrder* op = new PersonalOrder();
	op->setOrderProductNum(2925);
	op->setCustomerName("John");
	op->setProductId("P0001");

	OrderBusiness* ob = new OrderBusiness();
	ob->saveOrder(op);

	std::cout << "\nTest Enterprise Order ..." << std::endl;
	EnterpriseOrder* ep = new EnterpriseOrder();
	ep->setOrderProductNum(3855);
	ep->setEnterpriseName("Apple Company");
	ep->setProductId("A001");

	ob->saveOrder(ep);

	delete ob;
	delete ep;
	delete op;
	return 0;
}
