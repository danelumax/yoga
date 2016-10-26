/*
 * OrderProxy.cpp
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#include "OrderProxy.h"

OrderProxy::OrderProxy(std::string productName, int orderNum, std::string orderUser)
	: Order::Order(productName, orderNum, orderUser)
{
}

OrderProxy::~OrderProxy()
{
}

int OrderProxy::getOrderNum()
{
    return Order::getOrderNum();
}

std::string OrderProxy::getOrderUser()
{
    return Order::getOrderUser();
}

std::string OrderProxy::getProductName()
{
    return Order::getProductName();
}

void OrderProxy::setOrderNum(int orderNum, std::string user)
{
	if (user!="" && user == getOrderUser())
	{
		Order::setOrderNum(orderNum, user);
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
		Order::setOrderUser(orderUser, user);
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
		Order::setProductName(productName, user);
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
