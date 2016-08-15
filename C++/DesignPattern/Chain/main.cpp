//============================================================================
// Name        : Chain.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "Handler.h"

int main()
{
	Handler *h1 = new GeneralManager();
	Handler *h2 = new DepManager();
	Handler *h3 = new ProjectManager();

	h3->setSuccessor(h2);
	h2->setSuccessor(h1);

	std::string ret1 = h3->handleFeeRequest("Lee", 300);
	std::cout << ret1 << std::endl;

	std::string ret2 = h3->handleFeeRequest("Tom", 300);
	std::cout << ret2 << std::endl;

	std::string ret3 = h3->handleFeeRequest("Lee", 600);
	std::cout << ret3 << std::endl;

	std::string ret4 = h3->handleFeeRequest("Tom", 600);
	std::cout << ret4 << std::endl;

	std::string ret5 = h3->handleFeeRequest("Lee", 1200);
	std::cout << ret5 << std::endl;

	std::string ret6 = h3->handleFeeRequest("Tom", 1200);
	std::cout << ret6 << std::endl;

	return 0;
}
