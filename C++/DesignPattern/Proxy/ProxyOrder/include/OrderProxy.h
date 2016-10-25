/*
 * OrderProxy.h
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#ifndef ORDERPROXY_H_
#define ORDERPROXY_H_

#include "Order.h"

class OrderProxy : public OrderApi
{
public:
	OrderProxy(OrderApi* realSubject);
	virtual ~OrderProxy();
	virtual int getOrderNum();
	virtual std::string getOrderUser();
	virtual std::string getProductName();
	virtual void setOrderNum(int orderNum, std::string user);
	virtual void setOrderUser(std::string orderUser, std::string user);
	virtual void setProductName(std::string productName, std::string user);
	virtual void toString();
private:
	OrderApi* _order;
};

#endif /* ORDERPROXY_H_ */
