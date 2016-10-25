/*
 * Order.h
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#ifndef ORDER_H_
#define ORDER_H_

#include "OrderApi.h"

class Order : public OrderApi
{
public:
	Order(std::string productName, int orderNum, std::string orderUser);
	virtual ~Order();
	virtual int getOrderNum();
	virtual std::string getOrderUser();
	virtual std::string getProductName();
	virtual void setOrderNum(int orderNum, std::string user);
	virtual void setOrderUser(std::string orderUser, std::string user);
	virtual void setProductName(std::string productName, std::string user);
	virtual void toString(){};

private:
	std::string _productName;
	int _orderNum;
	std::string _orderUser;
};

#endif /* ORDER_H_ */
