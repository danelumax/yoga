/*
 * OrderBusiness.cpp
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#include "OrderBusiness.h"

OrderBusiness::OrderBusiness()
{
}

OrderBusiness::~OrderBusiness()
{
}

void OrderBusiness::saveOrder(OrderApi* order)
{
	while(order->getOrderProductNum() > 1000)
	{
		OrderApi* newOrder = order->cloneOrder();
		newOrder->setOrderProductNum(1000);

		order->setOrderProductNum(order->getOrderProductNum() - 1000);

		std::cout << "Split Order: ";
		newOrder->toString();
	}

	std::cout << "Order: ";
	order->toString();
}
