/*
 * OrderApi.h
 *
 *  Created on: Oct 24, 2016
 *      Author: eliwech
 */

#ifndef ORDERAPI_H_
#define ORDERAPI_H_

#include <string>
#include <iostream>

class OrderApi
{
public:
    virtual int getOrderNum() = 0;
    virtual std::string getOrderUser() = 0;
    virtual std::string getProductName() = 0;
    virtual void setOrderNum(int orderNum, std::string user) = 0;
    virtual void setOrderUser(std::string orderUser, std::string user) = 0;
    virtual void setProductName(std::string productName, std::string user) = 0;
    virtual void toString() = 0;
};

#endif /* ORDERAPI_H_ */
