//============================================================================
// Name        : PrototypeNormal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Product.h"
#include "PersonalOrder.h"

int main()
{
	PersonalOrder* oa1 = new PersonalOrder();
	Product* product = new Product();
	product->setName("Product #1");
	oa1->setProduct(product);
	oa1->setOrderProductNum(100);
	std::cout << "\nThis is the first time to get instance: ";
	oa1->toString();

	PersonalOrder* oa2 = (PersonalOrder*)oa1->cloneOrder();
	oa2->getProduct()->setName("Product #2");
	oa2->setOrderProductNum(80);
	std::cout << "\nThis is the second time to get instance: ";
	oa2->toString();

	std::cout << "\nGet Prototype instance again: ";
	oa1->toString();

	delete oa2;
	delete product;
	delete oa1;

	return 0;
}
