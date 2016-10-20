/*
 * Product.cpp
 *
 *  Created on: Oct 20, 2016
 *      Author: eliwech
 */

#include "Product.h"

Product::Product()
{
}

Product::~Product()
{
}

std::string Product::getName()
{
    return _name;
}

std::string Product::getProductId()
{
    return _productId;
}

void Product::setName(std::string name)
{
    _name = name;
}

void Product::setProductId(std::string productId)
{
    _productId = productId;
}

Product* Product::cloneProduct()
{
	Product* product = new Product();
	product->setProductId(_productId);
	product->setName(_name);
	return product;
}

void Product::toString()
{
	std::cout << "ProductId: " << _productId
			  << ", ProductName: " << _name << std::endl;
}
