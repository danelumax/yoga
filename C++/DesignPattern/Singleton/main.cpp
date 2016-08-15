//============================================================================
// Name        : Singleton.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "AppConfig.h"

int main(void)
{
	AppConfig *configA = AppConfig::getInstance();
	AppConfig *configB = AppConfig::getInstance();

	std::cout << configA << "=" << configB <<std::endl;
	std::cout << configA->getParameterA() << std::endl;
	std::cout << configB->getParameterB() << std::endl;

	return 0;
}
