/*
 * Order.cpp
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#include "Order.h"

Order::Order(std::string productName, int orderNum, std::string orderUser)
	:_productName(productName), _orderNum(orderNum), _orderUser(orderUser)
{
}

Order::~Order()
{
}

int Order::getOrderNum()
{
    return _orderNum;
}

std::string Order::getOrderUser()
{
    return _orderUser;
}

std::string Order::getProductName()
{
    return _productName;
}

void Order::setOrderNum(int orderNum, std::string user)
{
    _orderNum = orderNum;
}

void Order::setOrderUser(std::string orderUser, std::string user)
{
    _orderUser = orderUser;
}

void Order::setProductName(std::string productName, std::string user)
{
    _productName = productName;
}
