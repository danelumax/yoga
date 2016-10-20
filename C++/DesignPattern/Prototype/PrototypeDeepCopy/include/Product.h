/*
 * Product.h
 *
 *  Created on: Oct 20, 2016
 *      Author: eliwech
 */

#ifndef PRODUCT_H_
#define PRODUCT_H_

#include <string>
#include <iostream>

class Product
{
public:
	Product();
	virtual ~Product();
    std::string getName();
    std::string getProductId();
    void setName(std::string name);
    void setProductId(std::string productId);
    void toString();
    Product* cloneProduct();

private:
	std::string _productId;
	std::string _name;
};

#endif /* PRODUCT_H_ */
