/*
 * PersonalOrder.h
 *
 *  Created on: Oct 18, 2016
 *      Author: eliwech
 */

#ifndef PERSONALORDER_H_
#define PERSONALORDER_H_

#include <string>
#include "OrderApi.h"

class PersonalOrder : public OrderApi
{
public:
	PersonalOrder();
	virtual ~PersonalOrder();

    void setCustomerName(std::string customerName);
    void setProductId(std::string productId);

    virtual int getOrderProductNum();
    virtual void setOrderProductNum(int orderProductNum);
    virtual OrderApi* cloneOrder();
    virtual void toString();
private:
	std::string _customerName;
	std::string _productId;
	int _orderProductNum;
};

#endif /* PERSONALORDER_H_ */
