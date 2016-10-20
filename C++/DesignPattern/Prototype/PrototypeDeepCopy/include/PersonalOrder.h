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
#include "Product.h"

class PersonalOrder : public OrderApi
{
public:
	PersonalOrder();
	virtual ~PersonalOrder();
    void setProduct(Product* product);
    Product* getProduct();

    virtual int getOrderProductNum();
    virtual void setOrderProductNum(int orderProductNum);
    virtual OrderApi* cloneOrder();
    virtual void toString();
private:
	int _orderProductNum;
	Product* _product;
};

#endif /* PERSONALORDER_H_ */
