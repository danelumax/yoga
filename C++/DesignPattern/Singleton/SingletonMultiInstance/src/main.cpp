//============================================================================
// Name        : Singleton.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "AppConfig.h"

int main(void)
{
	AppConfig *t1 = AppConfig::getInstance();
	AppConfig *t2 = AppConfig::getInstance();
	AppConfig *t3 = AppConfig::getInstance();
	AppConfig *t4 = AppConfig::getInstance();
	AppConfig *t5 = AppConfig::getInstance();
	AppConfig *t6 = AppConfig::getInstance();

	std::cout << t1 <<std::endl;
	std::cout << t2 <<std::endl;
	std::cout << t3 <<std::endl;
	std::cout << t4 <<std::endl;
	std::cout << t5 <<std::endl;
	std::cout << t6 <<std::endl;

	return 0;
}
