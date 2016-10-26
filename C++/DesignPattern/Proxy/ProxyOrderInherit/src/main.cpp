//============================================================================
// Name        : ProxyOrder.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Order.h"
#include "OrderProxy.h"

int main()
{
	Order* order = new OrderProxy("Design Pattern", 100, "John");

	std::cout << "\nNo change after Peter's modification ..." << std::endl;
	order->setOrderNum(123, "Peter");
	order->toString();

	std::cout << "\nAfter John's modification, Order is that ..." << std::endl;
	order->setOrderNum(123, "John");
	order->toString();

	return 0;
}
