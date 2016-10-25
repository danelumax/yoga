/*
 * OrderProxy.cpp
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#include "OrderProxy.h"

OrderProxy::OrderProxy(OrderApi* realSubject)
	: _order(realSubject)
{
}

OrderProxy::~OrderProxy()
{
}

int OrderProxy::getOrderNum()
{
    return _order->getOrderNum();
}

std::string OrderProxy::getOrderUser()
{
    return _order->getOrderUser();
}

std::string OrderProxy::getProductName()
{
    return _order->getProductName();
}

void OrderProxy::setOrderNum(int orderNum, std::string user)
{
	if (user!="" && user == getOrderUser())
	{
		_order->setOrderNum(orderNum, user);
	}
	else
	{
		std::cout << "Sorry <" << user <<">, you have no permission to change <Order Number> ..." << std::endl;
	}
}

void OrderProxy::setOrderUser(std::string orderUser, std::string user)
{
	if (user!="" && user == getOrderUser())
	{
		_order->setOrderUser(orderUser, user);
	}
	else
	{
		std::cout << "Sorry <" << user <<">, you have no permission to change <Order User> ..." << std::endl;
	}
}

void OrderProxy::setProductName(std::string productName, std::string user)
{
	if (user!="" && user == getOrderUser())
	{
		_order->setProductName(productName, user);
	}
	else
	{
		std::cout << "Sorry <" << user <<">, you have no permission to change <Product Name> ..." << std::endl;
	}
}

void OrderProxy::toString()
{
	std::cout << "ProductName: " << getProductName()
			  << ", OrderNum: " << getOrderNum()
			  << ", OrderUser: " << getOrderUser() << std::endl;
}
