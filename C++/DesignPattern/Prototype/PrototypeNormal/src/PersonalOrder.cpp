/*
 * PersonalOrder.cpp
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#include "PersonalOrder.h"

PersonalOrder::PersonalOrder()
	: _customerName(""), _productId(""), _orderProductNum(0)
{
}

PersonalOrder::~PersonalOrder()
{
}

int PersonalOrder::getOrderProductNum()
{
    return _orderProductNum;
}

void PersonalOrder::setCustomerName(std::string customerName)
{
    _customerName = customerName;
}

void PersonalOrder::setOrderProductNum(int orderProductNum)
{
    _orderProductNum = orderProductNum;
}

void PersonalOrder::setProductId(std::string productId)
{
    _productId = productId;
}

void PersonalOrder::toString()
{
	std::cout << "Customer: " << _customerName
			  << ", Product: " << _productId
			  << ", ProductNum: " << _orderProductNum << std::endl;
}

OrderApi* PersonalOrder::cloneOrder()
{
	PersonalOrder* order = new PersonalOrder();
	order->setCustomerName(_customerName);
	order->setProductId(_productId);
	order->setOrderProductNum(_orderProductNum);

	return order;
}
