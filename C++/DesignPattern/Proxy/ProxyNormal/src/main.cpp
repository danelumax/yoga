//============================================================================
// Name        : ProxyNormal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "UserManager.h"
#include "UserModelApi.h"

int main()
{
	UserManager* manager = new UserManager();
	std::vector<UserModelApi*> vec = manager->getUserByDepId("010101");

	std::cout << "\nJust Check Brief Info of DepId: 010101 ..." << std::endl;
	std::vector<UserModelApi*>::iterator iter = vec.begin();
	for(; iter!=vec.end(); ++iter)
	{
		std::cout << "UserId: " << (*iter)->getUserId()
				  << ", UserName: " << (*iter)->getName() << std::endl;
	}

	std::cout << "\nList All Detailed Info of DepId: 010101 ..." << std::endl;
	for(iter = vec.begin(); iter!=vec.end(); ++iter)
	{
		std::cout << "UserId: " << (*iter)->getUserId()
				  << ", UserName: " << (*iter)->getName()
				  << ", DepId: " << (*iter)->getDepId() << std::endl;
	}

	return 0;
}
