/*
 * PersonalOrder.cpp
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#include "PersonalOrder.h"
#include <iostream>

PersonalOrder::PersonalOrder()
	: _orderProductNum(0), _product(NULL)
{
}

PersonalOrder::~PersonalOrder()
{
}

int PersonalOrder::getOrderProductNum()
{
    return _orderProductNum;
}

void PersonalOrder::setOrderProductNum(int orderProductNum)
{
    _orderProductNum = orderProductNum;
}

void PersonalOrder::setProduct(Product* product)
{
	_product = product;
}

Product* PersonalOrder::getProduct()
{
	return _product;
}

void PersonalOrder::toString()
{
	std::cout << "Product: " << _product->getName()
			  << ", ProductNum: " << _orderProductNum << std::endl;
}

OrderApi* PersonalOrder::cloneOrder()
{
	PersonalOrder* order = new PersonalOrder();
	order->setOrderProductNum(_orderProductNum);
	order->setProduct(_product->cloneProduct());

	return order;
}
