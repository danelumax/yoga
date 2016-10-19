/*
 * EnterpriseOrder.cpp
 *
 *  Created on: Oct 19, 2016
 *      Author: eliwech
 */

#include "EnterpriseOrder.h"

EnterpriseOrder::EnterpriseOrder()
	: _enterpriseName(""), _productId(""), _orderProductNum(0)
{
}

EnterpriseOrder::~EnterpriseOrder()
{
}

void EnterpriseOrder::setEnterpriseName(std::string enterpriseName)
{
    _enterpriseName = enterpriseName;
}

void EnterpriseOrder::setProductId(std::string productId)
{
    _productId = productId;
}

int EnterpriseOrder::getOrderProductNum()
{
    return _orderProductNum;
}

void EnterpriseOrder::setOrderProductNum(int orderProductNum)
{
    _orderProductNum = orderProductNum;
}

void EnterpriseOrder::toString()
{
	std::cout << "Enterprise: " << _enterpriseName
			  << ", Product: " << _productId
			  << ", ProductNum: " << _orderProductNum << std::endl;
}

OrderApi* EnterpriseOrder::cloneOrder()
{
	EnterpriseOrder* order = new EnterpriseOrder();
	order->setEnterpriseName(_enterpriseName);
	order->setProductId(_productId);
	order->setOrderProductNum(_orderProductNum);

	return order;
}
