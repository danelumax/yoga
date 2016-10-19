/*
 * EnterpriseOrder.h
 *
 *  Created on: Oct 19, 2016
 *      Author: eliwech
 */

#ifndef ENTERPRISEORDER_H_
#define ENTERPRISEORDER_H_

#include "OrderApi.h"
#include <string>

class EnterpriseOrder : public OrderApi
{
public:
	EnterpriseOrder();
	virtual ~EnterpriseOrder();
    void setEnterpriseName(std::string enterpriseName);
    void setProductId(std::string productId);

    virtual int getOrderProductNum();
    virtual void setOrderProductNum(int orderProductNum);
	virtual OrderApi* cloneOrder();
    virtual void toString();
private:
	std::string _enterpriseName;
	std::string _productId;
	int _orderProductNum;

};

#endif /* ENTERPRISEORDER_H_ */
